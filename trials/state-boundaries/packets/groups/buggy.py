def translate(tables):
    rows=tables['have']; out=[]; queue=None; total=0
    columns=('row_id','region','account','value','raw_prev','prev','total','first_region','last_region','first_account','last_account')
    for i,row in enumerate(rows):
        previous=rows[i-1] if i else None
        following=rows[i+1] if i+1<len(rows) else None
        fr=int(previous is None or row['region']!=previous['region'])
        lr=int(following is None or row['region']!=following['region'])
        fa=int(previous is None or row['account']!=previous['account'])
        la=int(following is None or row['account']!=following['account'])
        if fr or fa: queue=None
        raw_prev=queue; queue=row['value']
        prev=None if fa else raw_prev
        if fr: total=100
        total+=row['value'] if row['value'] is not None else 0
        values=[row['row_id'],row['region'],row['account'],row['value'],raw_prev,prev,total,fr,lr,fa,la]
        out.append(dict(zip(columns,values)))
    return {'want':out}
