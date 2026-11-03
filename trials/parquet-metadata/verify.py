#!/usr/bin/env python3
"""Independent replay of frozen Parquet values, metadata and an R bridge."""
import copy,csv,hashlib,importlib.util,json,math,platform,shutil,struct,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
from bridge import export,sha
ROOT=Path(__file__).resolve().parent


def snapshot(root):
    return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def read_csv(path):
    with path.open(newline='',encoding='utf-8') as f:
        return list(csv.reader(f))


def load_candidate():
    spec=importlib.util.spec_from_file_location('parquet_candidate',ROOT/'candidate/converted.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run(cmd):
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
    assert result.returncode==0,result.stderr[-3000:]
    return result


def canonical(value):
    if isinstance(value,dict):return {k:canonical(v) for k,v in value.items()}
    if isinstance(value,list):return [canonical(v) for v in value]
    if isinstance(value,(int,float)) and not isinstance(value,bool):return {'binary64':struct.pack('<d',float(value)).hex()}
    return value


def check_bundle(bundle,source,expected):
    meta=json.loads((bundle/'metadata.json').read_text())
    raw=(bundle/'data.parquet').read_bytes()
    assert raw[:4]==raw[-4:]==b'PAR1','not an actual Parquet file'
    assert meta['version']==1 and meta['policy']=='preserve-v1'
    assert meta['source_sha256']==sha(source),'source association'
    assert meta['parquet_sha256']==sha(bundle/'data.parquet'),'Parquet association'
    original=json.loads(source.read_text())
    assert meta['source_format']==original['source_format'] and meta['encoding']==original['encoding']
    assert meta['columns']==original['columns'],'descriptor fields'
    assert meta['missing_tags']==expected['missing_tags'],'tag positions or tags'
    assert meta['row_count']==expected['rows']
    assert meta['versions']['pyarrow']==pa.__version__
    assert meta['versions']['python']==platform.python_version()
    table=pq.read_table(bundle/'data.parquet')
    assert [[f.name,str(f.type)] for f in table.schema]==expected['schema'],'ordered typed schema'
    assert table.num_rows==expected['rows'],'row count'
    tags={(x['row'],x['column']):x['tag'] for x in meta['missing_tags']}
    actual=[]
    for i,row in enumerate(table.to_pylist()):
        for name,typ in expected['schema']:
            value=row[name]
            kind='text_hex' if typ=='string' else 'float64_hex' if typ=='double' else 'date_iso'
            text='' if value is None else value.encode('utf-8').hex() if kind=='text_hex' else struct.pack('<d',value).hex() if kind=='float64_hex' else value.isoformat()
            actual.append([str(i),name,kind,text,tags.get((i,name),'')])
    assert actual==expected['cells'],'typed values, bits, bytes or order'


def expect_reject(operation):
    try:operation()
    except Exception:return
    raise AssertionError('incorrect artifact accepted')


def main():
    for name,digest in json.loads((ROOT/'freeze.json').read_text())['hashes'].items():
        assert sha(ROOT/name)==digest,'frozen artifact drift: '+name
    for name,digest in json.loads((ROOT/'delivery.json').read_text())['hashes'].items():
        assert sha(ROOT/name)==digest,'first-delivery drift: '+name
    candidate=load_candidate()
    before=snapshot(ROOT/'packet')
    oracle=json.loads((ROOT/'oracle.json').read_text())
    checks=[]
    def record(name,operation):
        try:operation();checks.append({'name':name,'verdict':'PASS'})
        except Exception as error:checks.append({'name':name,'verdict':'FAIL','detail':str(error)})
    with tempfile.TemporaryDirectory(prefix='roku-parquet-replay-') as temp:
        work=Path(temp); bundles={}
        for case,expected in oracle.items():
            source=ROOT/'packet/cases'/f'{case}.json'
            for interface in ('cli','api'):
                dest=work/f'{case}-{interface}'
                def convert(dest=dest,source=source,expected=expected,interface=interface):
                    if interface=='cli':run([sys.executable,'-B',str(ROOT/'candidate/converted.py'),str(source),str(dest)])
                    else:candidate.convert(source,dest)
                    check_bundle(dest,source,expected)
                record(f'{case}/{interface}/Parquet-and-companion',convert)
                if dest.exists():
                    original=snapshot(dest)
                    def refuse(dest=dest,source=source,original=original,interface=interface):
                        if interface=='cli':
                            result=subprocess.run([sys.executable,'-B',str(ROOT/'candidate/converted.py'),str(source),str(dest)],capture_output=True,timeout=45)
                            assert result.returncode!=0,'existing destination accepted'
                        else:expect_reject(lambda:candidate.convert(source,dest))
                        assert snapshot(dest)==original,'existing destination changed'
                    record(f'{case}/{interface}/existing-destination-refusal',refuse)
            bundle=work/f'{case}-api'
            bundles[case]=bundle
            def restore(bundle=bundle,source=source):
                restored=candidate.restore(bundle,sha(source))
                assert canonical(restored)==canonical(json.loads(source.read_text())),'restored source differs'
            record(f'{case}/restore-from-Parquet',restore)
            def r_consume(bundle=bundle,source=source,expected=expected,case=case):
                bridge=work/f'{case}-bridge';out=work/f'{case}-r'
                export(bundle,bridge,sha(source))
                run(['Rscript','--vanilla',str(ROOT/'r_driver.R'),str(ROOT/'candidate/consume.R'),str(bridge),str(out)])
                for file,key,header in [('cells.csv','cells',['row','column','kind','value','tag']),('columns.csv','metadata',['column','property','type','value']),('labels.csv','labels',['column','value_hex','label_hex'])]:
                    assert read_csv(out/file)==[header]+expected[key],f'R {file} differs'
            record(f'{case}/R-typed-values-raw-bytes-tags-metadata',r_consume)
        for source in sorted((ROOT/'packet/invalid').glob('*.json')):
            for interface in ('cli','api'):
                dest=work/f'reject-{source.stem}-{interface}'
                def invalid(source=source,dest=dest,interface=interface):
                    if interface=='cli':
                        result=subprocess.run([sys.executable,'-B',str(ROOT/'candidate/converted.py'),str(source),str(dest)],capture_output=True,timeout=45)
                        assert result.returncode!=0,'invalid input accepted'
                    else:expect_reject(lambda:candidate.convert(source,dest))
                    assert not dest.exists(),'invalid input created destination'
                record(f'{source.stem}/{interface}/invalid-input-refusal',invalid)
        source=ROOT/'packet/cases/main.json';expected=oracle['main'];base=bundles['main']
        def alter_table(dest,change):
            table=pq.read_table(dest/'data.parquet');table=change(table)
            pq.write_table(table,dest/'data.parquet')
            m=json.loads((dest/'metadata.json').read_text());m['parquet_sha256']=sha(dest/'data.parquet')
            (dest/'metadata.json').write_text(json.dumps(m))
        def alter_meta(dest,change):
            m=json.loads((dest/'metadata.json').read_text());change(m)
            (dest/'metadata.json').write_text(json.dumps(m))
        def change_column(table,name,values,typ):
            i=table.schema.get_field_index(name)
            return table.set_column(i,pa.field(name,typ),pa.array(values,type=typ))
        mutations={
            'swapped-companion':lambda d:shutil.copyfile(bundles['latin1']/'metadata.json',d/'metadata.json'),
            'wrong-source-hash':lambda d:alter_meta(d,lambda m:m.update(source_sha256='0'*64)),
            'wrong-Parquet-hash':lambda d:alter_meta(d,lambda m:m.update(parquet_sha256='0'*64)),
            'lost-tag':lambda d:alter_meta(d,lambda m:m['missing_tags'].pop()),
            'tag-on-value':lambda d:alter_meta(d,lambda m:m['missing_tags'].append({'row':0,'column':'value','tag':'.A'})),
            'missing-column-metadata':lambda d:alter_meta(d,lambda m:m['columns'][0].pop('label')),
            'wrong-all-null-type':lambda d:alter_table(d,lambda t:change_column(t,'all_missing',[None]*4,pa.null())),
            'trimmed-ID':lambda d:alter_table(d,lambda t:change_column(t,'id',[x.lstrip('0').rstrip() for x in t['id'].to_pylist()],pa.string())),
            'date-origin-offset':lambda d:alter_table(d,lambda t:change_column(t,'date',[None if x is None else x.replace(year=x.year+10) for x in t['date'].to_pylist()],pa.date32())),
            'signed-zero-lost':lambda d:alter_table(d,lambda t:change_column(t,'value',[0.0 if x==0 else x for x in t['value'].to_pylist()],pa.float64())),
            'label-changed':lambda d:alter_meta(d,lambda m:m['columns'][-1]['value_labels'].update({'1':'Changed'})),
            'Unicode-normalized':lambda d:alter_table(d,lambda t:change_column(t,'text',[unicodedata.normalize('NFC',x) for x in t['text'].to_pylist()],pa.string())),
        }
        enforce={'swapped-companion','wrong-source-hash','wrong-Parquet-hash','lost-tag','tag-on-value','wrong-all-null-type'}
        for name,mutation in mutations.items():
            dest=work/f'corrupt-{name}'
            if not base.exists():
                record(f'control/{name}',lambda:(_ for _ in ()).throw(AssertionError('base delivery absent')))
                continue
            shutil.copytree(base,dest)
            mutation(dest)
            record(f'control/{name}/independent-comparator',lambda d=dest:expect_reject(lambda:check_bundle(d,source,expected)))
            if name in enforce:
                record(f'control/{name}/candidate-validation',lambda d=dest:expect_reject(lambda:candidate.validate(d,sha(source))))
    assert snapshot(ROOT/'packet')==before,'evaluation packet changed'
    result={'status':'bounded engineering replay, not live SAS or direct R Parquet','python':platform.python_version(),'pyarrow':pa.__version__,'R':subprocess.check_output(['Rscript','--version'],text=True).strip(),'checks':checks,'total':len(checks),'passed':sum(x['verdict']=='PASS' for x in checks),'failures':[x for x in checks if x['verdict']=='FAIL']}
    if '--receipt' in sys.argv:
        path=Path(sys.argv[sys.argv.index('--receipt')+1]);path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'total':result['total'],'passed':result['passed'],'failures':result['failures']},indent=2))
    return bool(result['failures'])


if __name__=='__main__':sys.exit(main())
