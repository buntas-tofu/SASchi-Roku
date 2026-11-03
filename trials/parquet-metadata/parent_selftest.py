"""Exercise the parent oracle, file comparator and bridge before dispatch."""
import json,platform,struct,tempfile
from datetime import date
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
from bridge import export,sha
from verify import check_bundle,expect_reject
ROOT=Path(__file__).resolve().parent
oracle=json.loads((ROOT/'oracle.json').read_text())
with tempfile.TemporaryDirectory() as temp:
    work=Path(temp)
    for case,e in oracle.items():
        source=ROOT/'packet/cases'/f'{case}.json';s=json.loads(source.read_text())
        arrays=[]
        for name,typ in e['schema']:
            values=[]
            for row,col,kind,value,tag in e['cells']:
                if col!=name:continue
                values.append(None if tag else bytes.fromhex(value).decode('utf-8') if kind=='text_hex' else struct.unpack('<d',bytes.fromhex(value))[0] if kind=='float64_hex' else date.fromisoformat(value))
            arrays.append(pa.array(values,type={'string':pa.string(),'double':pa.float64(),'date32[day]':pa.date32()}[typ]))
        table=pa.Table.from_arrays(arrays,names=[c[0] for c in e['schema']])
        bundle=work/case;bundle.mkdir();pq.write_table(table,bundle/'data.parquet')
        meta=dict(version=1,policy='preserve-v1',source_format=s['source_format'],encoding=s['encoding'],columns=s['columns'],row_count=e['rows'],source_sha256=sha(source),parquet_sha256=sha(bundle/'data.parquet'),missing_tags=e['missing_tags'],versions={'python':platform.python_version(),'pyarrow':pa.__version__})
        (bundle/'metadata.json').write_text(json.dumps(meta))
        check_bundle(bundle,source,e)
        cells,metadata,labels=export(bundle,work/f'{case}-bridge',sha(source))
        assert (cells,metadata,labels)==(e['cells'],e['metadata'],e['labels'])
        if case=='main':
            values=table['value'].to_pylist();values[2]=0.0
            table=table.set_column(2,pa.field('value',pa.float64()),pa.array(values,type=pa.float64()))
            pq.write_table(table,bundle/'data.parquet');meta['parquet_sha256']=sha(bundle/'data.parquet')
            (bundle/'metadata.json').write_text(json.dumps(meta))
            expect_reject(lambda:check_bundle(bundle,source,e))
print('PASS: six parent Parquet/bridge witnesses and one repaired-hash signed-zero control')
