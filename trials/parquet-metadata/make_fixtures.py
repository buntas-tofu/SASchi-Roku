"""Generate original synthetic decoded envelopes, before any candidate exists."""
import copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def col(name,typ,**kw):
    d=dict(name=name,source_type=typ,byte_width=None,label=None,format=None,informat=None,units=None,origin=None,timezone=None,value_labels=None)
    d.update(kw)
    return d

columns=[col('id','char',byte_width=4,label='Record identifier',format='$CHAR4.',informat='$CHAR4.'),
 col('text','char',byte_width=8,label='Exact text bytes',format='$CHAR8.'),
 col('value','numeric',label='Measured value',format='BEST12.'),
 col('date','date',label='Observation date',format='DATE9.',units='days',origin='1960-01-01'),
 col('stamp','numeric',label='Unzoned timestamp',format='DATETIME20.',units='seconds',origin='1960-01-01'),
 col('all_missing','numeric',label='',format=None),
 col('status','numeric',label='Response',format='RESP.',value_labels={'1':'Yes','2':'No'})]

def missing(tag='.'):
    return {'missing':tag}

def text(value,width,encoding='utf-8'):
    b=value.encode(encoding) if isinstance(value,str) else value
    assert len(b)<=width
    return {'hex':b.ljust(width,b' ').hex()}

def row(i='0001',s='text',v=1.5,d=0,stamp=0.0,tag='.',status=1,encoding='utf-8'):
    return [text(i,4,encoding),text(s,8,encoding),v,d,stamp,missing(tag),status]

main=[row(s='café'),row(s=b'A\x00B',v=missing('.A'),d=-1,stamp=.5,tag='._',status=2),
      row(i='NA',s='NA',v=-0.0,d=3653,stamp=-0.0,tag='.Z'),
      row(i='',s='e\u0301',v=missing(),d=missing('.Z'),stamp=missing('.A'),tag='.A',status=missing())]
cases={
 'main':('utf-8',main),
 'empty':('utf-8',[]),
 'all-missing':('utf-8',[row(i='0000',s='',v=missing(),d=missing(),stamp=missing(),status=missing()),row(i='0000',s=' ',v=missing('.A'),d=missing('._'),stamp=missing('.Z'),status=missing('.A'))]),
 'all-tags':('utf-8',[row(i='dup',s='tags',v=missing(t),d=missing(t),stamp=missing(t),tag=t,status=missing(t)) for t in ['.','._']+['.'+chr(x) for x in range(65,91)]]),
 'controls':('utf-8',[row(i='0001',s=s,v=float(j),d=[-1,0,3653,21915][j%4]) for j,s in enumerate(['a,b','"q"','A\rB','A\nB','A\tB','\x00','🚗','é'])]),
 'latin1':('latin-1',[row(s='café',encoding='latin-1'),row(s=b'\xff',i='0012',d=21915,encoding='latin-1')])}
for name,(encoding,rows) in cases.items():
    d=dict(source_format='decoded-synthetic-v1',encoding=encoding,columns=copy.deepcopy(columns),rows=rows)
    (ROOT/'packet/cases'/f'{name}.json').write_text(json.dumps(d,ensure_ascii=True,indent=2)+'\n')
base=json.loads((ROOT/'packet/cases/main.json').read_text())
invalid={}
d=copy.deepcopy(base); d['rows'][0][1]={'hex':(b'\xff'+b' '*7).hex()};invalid['invalid-utf8']=d
d=copy.deepcopy(base); d['rows'][0][0]={'hex':b'12345'.hex()};invalid['over-width']=d
d=copy.deepcopy(base); d['rows'][0][2]={'missing':'..'};invalid['bad-tag']=d
d=copy.deepcopy(base); d['rows'][0][3]=.5;invalid['fractional-date']=d
d=copy.deepcopy(base); d['columns'][1]['name']='id';invalid['duplicate-column']=d
d=copy.deepcopy(base); d['encoding']='unknown-codec';invalid['unknown-encoding']=d
d=copy.deepcopy(base); d['rows'][0][2]=True;invalid['boolean-number']=d
(ROOT/'packet/invalid').mkdir()
for name,d in invalid.items():
    (ROOT/'packet/invalid'/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n')
