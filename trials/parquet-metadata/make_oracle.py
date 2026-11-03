"""Freeze expected values from original source envelopes before evaluation."""
import json,struct
from datetime import date,timedelta
from pathlib import Path
from bridge import metadata_rows
ROOT=Path(__file__).resolve().parent
oracle={}
for path in sorted((ROOT/'packet/cases').glob('*.json')):
    source=json.loads(path.read_text())
    cells=[];tags=[]
    for i,row in enumerate(source['rows']):
        for c,value in zip(source['columns'],row):
            kind={'char':'text_hex','numeric':'float64_hex','date':'date_iso'}[c['source_type']]
            tag=value.get('missing','') if isinstance(value,dict) else ''
            if tag:
                encoded='';tags.append({'row':i,'column':c['name'],'tag':tag})
            elif kind=='text_hex':
                encoded=bytes.fromhex(value['hex']).decode(source['encoding']).encode('utf-8').hex()
            elif kind=='float64_hex':
                encoded=struct.pack('<d',float(value)).hex()
            else:
                encoded=(date(1960,1,1)+timedelta(days=value)).isoformat()
            cells.append([str(i),c['name'],kind,encoded,tag])
    metadata,labels=metadata_rows(source)
    oracle[path.stem]={'schema':[[c['name'],{'char':'string','numeric':'double','date':'date32[day]'}[c['source_type']]] for c in source['columns']], 'cells':cells,'metadata':metadata,'labels':labels,'missing_tags':tags,'rows':len(source['rows'])}
(ROOT/'oracle.json').write_text(json.dumps(oracle,ensure_ascii=True,indent=2)+'\n')
