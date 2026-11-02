def translate(rows):
    total = 10
    prev = None
    prior = None
    stage = []
    for row in rows:
        if not row['emit']:
            continue
        if row['take']:
            prev = prior
        value = row['value']
        total = None if value is None or total is None else total + value
        stage.append(dict(row_id=row['row_id'], value=value, prev=prev, total=total))
        prior = value
    want = [dict(row, delta=None if row['value'] is None or row['prev'] is None else row['value']-row['prev']) for row in stage]
    return dict(stage=stage, want=want)
