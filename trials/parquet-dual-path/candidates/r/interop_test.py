import json, hashlib, datetime, pathlib
import pyarrow as pa
import pyarrow.parquet as pq
import pyreadstat
root=pathlib.Path('.')
for name in ['main','empty','all-missing','utf8','reordered']:
    env=json.loads((root/f'packet/synthetic/{name}.json').read_text())
    out=root/f'scratch/{name}'
    archive=pq.read_table(out/'archive.parquet'); analysis=pq.read_table(out/'analysis.parquet')
    meta=json.loads((out/'metadata.json').read_text())
    expected_archive={'__row_index':list(range(len(env['rows'])))}
    expected_analysis={'__row_index':list(range(len(env['rows'])))}
    events=[]
    for col in env['columns']:
        nm=col['name']; vals=[]; tags=[]; avals=[]
        for ri,row in enumerate(env['rows']):
            cell=row[nm];action=None
            if col['kind']=='character':
                vals.append(cell['hex']); raw=bytes.fromhex(cell['hex'])
                if b'\0' in raw: v=None; action='embedded-nul'
                else:
                    try: text=raw.decode(env['encoding'],errors='strict')
                    except UnicodeError: v=None;action='decode-error'
                    else:
                        v=text.rstrip(' ')
                        if not v:v=None;action='blank-to-null'
                        elif v!=text:action='right-trim'
                avals.append(v)
            else:
                v=cell.get('value'); tag=cell.get('missing','');vals.append(v);tags.append(tag)
                if tag:avals.append(None);action='missing-to-null'
                elif col['logical']=='date':avals.append(datetime.date(1960,1,1)+datetime.timedelta(days=v));action='date-to-date32'
                elif col['logical']=='datetime':avals.append(datetime.datetime(1960,1,1)+datetime.timedelta(seconds=v));action='datetime-to-timestamp-us'
                else:avals.append(float(v))
            if action:
                event={'row':ri,'column':nm,'action':action}
                if action=='missing-to-null':event['tag']=tag
                events.append(event)
        expected_archive[nm]=vals
        if col['kind']=='numeric':expected_archive[nm+'__sas_missing']=tags
        expected_analysis[nm]=avals
        atype=analysis.schema.field(nm).type
        typ=pa.string() if col['kind']=='character' else {'date':pa.date32(),'datetime':pa.timestamp('us')}.get(col['logical'],pa.float64())
        assert atype==typ,(name,nm,atype,typ)
        assert archive.schema.field(nm).type==(pa.string() if col['kind']=='character' else pa.float64())
    order={col['name']:i for i,col in enumerate(env['columns'])}
    events.sort(key=lambda e:(e['row'],order[e['column']]))
    assert meta['events']==events,(name,'events')
    assert archive.to_pydict()==expected_archive,(name,'archive')
    assert analysis.to_pydict()==expected_analysis,(name,'analysis')
    for mode,table in [('archive',archive),('analysis',analysis)]:
        assert table.schema.field('__row_index').type==pa.int64()
        assert table.schema.metadata[b'saschi.mode']==mode.encode()
        assert table.schema.metadata[b'saschi.source_sha256'].decode()==hashlib.sha256((root/f'packet/synthetic/{name}.json').read_bytes()).hexdigest()
        assert meta['files'][mode+'.parquet']==hashlib.sha256((out/(mode+'.parquet')).read_bytes()).hexdigest()
    print('PYTHON FULL ENVELOPE PASS',name)
for name,source,catalog in [('sample','sample.sas7bdat',None),('missing-no-catalog','missing.sas7bdat',None),('missing-catalog','missing.sas7bdat','missing.sas7bcat')]:
    input=root/'packet/fixtures'/source;out=root/'scratch'/name
    data,md=pyreadstat.read_sas7bdat(str(input),catalog_file=None,user_missing=True,disable_datetime_conversion=True)
    archive=pq.read_table(out/'archive.parquet').to_pydict()
    for nm in md.column_names:
        for i,v in enumerate(data[nm]):
            if md.readstat_variable_types[nm]=='string':
                assert archive[nm][i]==v.encode('utf-8').hex(),(name,nm,i)
            elif isinstance(v,str):
                assert archive[nm][i] is None and archive[nm+'__sas_missing'][i]=='.'+v.upper(),(name,nm,i)
            elif v!=v:
                assert archive[nm][i] is None and archive[nm+'__sas_missing'][i]=='.',(name,nm,i)
            else:assert archive[nm][i]==v and archive[nm+'__sas_missing'][i]=='',(name,nm,i)
    if catalog:
        _, labeled=pyreadstat.read_sas7bdat(str(input),catalog_file=str(root/'packet/fixtures'/catalog),user_missing=True,disable_datetime_conversion=True)
        side=json.loads((out/'metadata.json').read_text())
        cols={c['name']:c for c in side['columns']}
        for nm,mapping in labeled.variable_value_labels.items():
            normalized={'.'+k.upper() if isinstance(k,str) and k.upper() in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ_') else str(k):v for k,v in mapping.items()}
            assert cols[nm]['value_labels']==normalized,(name,nm,'labels')
    print('PYTHON SAS RAW PROJECTION PASS',name)
print('INTEROPERABILITY PASSED')
