import copy
import csv
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
candidate, source, destination = map(Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location('candidate', candidate)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
with source.open(newline='', encoding='utf-8') as stream:
    rows = list(csv.DictReader(stream))
for row in rows:
    row['value'] = None if row['value'] == '' else float(row['value'])
    row['take'] = int(row['take'])
    row['emit'] = int(row['emit'])
before = copy.deepcopy(rows)
first = module.translate(rows)
snapshot = copy.deepcopy(first)
second = module.translate(rows)
def logical(value):
    if isinstance(value, float) and value != value:
        return None
    if isinstance(value, list):
        return [logical(x) for x in value]
    if isinstance(value, dict):
        return {k: logical(v) for k, v in value.items()}
    return value
assert rows == before, 'caller mutation'
assert logical(first) == logical(snapshot) == logical(second), 'fresh-call state differs'
assert isinstance(first, dict) and list(first) == ['stage', 'want']
destination.mkdir()
for table in ('stage', 'want'):
    columns = ['row_id', 'value', 'prev', 'total'] + (['delta'] if table == 'want' else [])
    assert isinstance(first[table], list)
    for row in first[table]:
        assert list(row) == columns and isinstance(row['row_id'], str)
        assert all(v is None or isinstance(v, (int, float)) and not isinstance(v, bool) for k, v in row.items() if k != 'row_id')
    with (destination / (table + '.csv')).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(logical(first[table]))
