"""Invoke a candidate in a child process; check caller preservation and fresh calls."""
import copy
import csv
import importlib.util
import sys

sys.dont_write_bytecode = True
candidate, input_path, output_path, mechanism = sys.argv[1:]
spec = importlib.util.spec_from_file_location('candidate', candidate)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
with open(input_path, newline='', encoding='utf-8') as stream:
    rows = list(csv.DictReader(stream))
if mechanism == 'lag':
    for row in rows:
        row['value'] = None if row['value'] == '' else float(row['value'])
def logical(value):
    if isinstance(value, float) and value != value:
        return None
    if isinstance(value, list):
        return [logical(item) for item in value]
    if isinstance(value, dict):
        return {key: logical(item) for key, item in value.items()}
    return value

before = copy.deepcopy(rows)
first = module.translate(rows)
if rows != before:
    raise AssertionError('caller input changed')
snapshot = copy.deepcopy(first)
second = module.translate(rows)
if rows != before:
    raise AssertionError('caller input changed')
if logical(first) != logical(snapshot) or logical(second) != logical(snapshot):
    raise AssertionError('fresh-call results differ')
if not isinstance(first, list) or first is rows:
    raise AssertionError('expected a new list')
columns = ['row_id', 'text', 'len'] if mechanism == 'length' else ['row_id', 'value', 'prev', 'prev2', 'change']
for row in first:
    if not isinstance(row, dict) or list(row) != columns:
        raise AssertionError('column order or row type differs')
    if not isinstance(row['row_id'], str):
        raise AssertionError('row_id must be character')
    if mechanism == 'length' and not isinstance(row['text'], str):
        raise AssertionError('text must be character')
    for key in columns[2:] if mechanism == 'length' else columns[1:]:
        value = row[key]
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
            raise AssertionError('numeric field has wrong in-memory type')
with open(output_path, 'w', newline='', encoding='utf-8') as stream:
    writer = csv.DictWriter(stream, fieldnames=columns)
    writer.writeheader()
    for row in first:
        # Ordinary numeric missing may be None or NaN in a Python target.
        writer.writerow({k: '' if isinstance(v, float) and v != v else v for k, v in row.items()})
