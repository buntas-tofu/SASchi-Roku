"""Exercise the declared typed API without candidate CLI helpers."""
import copy
import csv
import importlib.util
import math
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
    row['eligible'] = int(row['eligible'])
before = copy.deepcopy(rows)
first = module.translate(rows)
snapshot = copy.deepcopy(first)
second = module.translate(rows)
empty = module.translate([])
third = module.translate(rows)
assert rows == before, 'caller mutation'
assert first == snapshot == second == third, 'state leaked between invocations'
assert isinstance(first, dict) and list(first) == ['where_path', 'if_path']
assert empty == {'where_path': [], 'if_path': []}, 'empty-call state differs'
columns = ['row_id', 'value', 'prev', 'total']
destination.mkdir()
for table in ('where_path', 'if_path'):
    assert isinstance(first[table], list)
    for row in first[table]:
        assert isinstance(row, dict) and list(row) == columns
        assert isinstance(row['row_id'], str)
        for key in columns[1:]:
            value = row[key]
            assert value is None or (type(value) in (int, float) and math.isfinite(value)), 'wrong typed numeric field'
    with (destination / (table + '.csv')).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(first[table])
