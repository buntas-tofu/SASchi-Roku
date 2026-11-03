"""Parent adapter over reopened files; imports no candidate implementation."""
import csv, hashlib, json, struct
from pathlib import Path
import pyarrow.parquet as pq


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, header, rows):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)


def metadata_rows(source):
    rows=[];labels=[]
    for column in source['columns']:
        name=column['name']
        for key,value in list(column.items())+[('encoding',source['encoding'])]:
            if key in ('name','value_labels'):
                continue
            typ='null' if value is None else 'number' if isinstance(value,(int,float)) else 'string'
            val='' if value is None else str(value) if typ=='number' else value.encode('utf-8').hex()
            rows.append([name,key,typ,val])
        for value,label in (column['value_labels'] or {}).items():
            labels.append([name,struct.pack('<d',float(value)).hex(),label.encode('utf-8').hex()])
    return rows,labels


def export(bundle,dest,expected_source_hash):
    bundle=Path(bundle);dest=Path(dest)
    meta=json.loads((bundle/'metadata.json').read_text())
    assert meta['source_sha256']==expected_source_hash
    assert meta['parquet_sha256']==sha(bundle/'data.parquet')
    table=pq.read_table(bundle/'data.parquet')
    tags={(x['row'],x['column']):x['tag'] for x in meta['missing_tags']}
    cells=[]
    for i,row in enumerate(table.to_pylist()):
        for c in meta['columns']:
            name=c['name'];value=row[name]
            kind={'char':'text_hex','numeric':'float64_hex','date':'date_iso'}[c['source_type']]
            encoded='' if value is None else value.encode('utf-8').hex() if kind=='text_hex' else struct.pack('<d',value).hex() if kind=='float64_hex' else value.isoformat()
            cells.append([str(i),name,kind,encoded,tags.get((i,name),'')])
    dest.mkdir()
    write_csv(dest/'cells.csv',['row','column','kind','value','tag'],cells)
    rows,labels=metadata_rows(meta)
    write_csv(dest/'columns.csv',['column','property','type','value'],rows)
    write_csv(dest/'labels.csv',['column','value_hex','label_hex'],labels)
    return cells,rows,labels
