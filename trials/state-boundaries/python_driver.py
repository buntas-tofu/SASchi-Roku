"""Parent adapter for the frozen Python interface, not candidate logic."""
import copy
import csv
import importlib.util
import math
from pathlib import Path
import sys


def schemas(path):
    result = {'input': {}, 'output': {}}
    with open(path, newline='', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            result[row['side']].setdefault(row['table'], []).append((row['column'], row['type']))
    return result


def read_tables(directory, schema):
    tables = {}
    for table, columns in schema.items():
        with (Path(directory) / (table + '.csv')).open(newline='', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            assert reader.fieldnames == [c for c, _ in columns]
            tables[table] = [{c: value[c] if kind == 'text' else
                              (None if value[c] == '' else float(value[c]))
                              for c, kind in columns} for value in reader]
    return tables


def validate(tables, schema):
    assert type(tables) is dict and list(tables) == list(schema), 'table schema differs'
    for table, columns in schema.items():
        assert type(tables[table]) is list
        for row in tables[table]:
            assert type(row) is dict and list(row) == [c for c, _ in columns]
            for column, kind in columns:
                value = row[column]
                if kind == 'text':
                    assert type(value) is str, column + ': expected text'
                else:
                    assert value is None or (type(value) in (int, float) and math.isfinite(value)), column + ': expected numeric'


def main():
    candidate, schema_path, source, destination, *flags = sys.argv[1:]
    spec = importlib.util.spec_from_file_location('candidate', candidate)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    schema = schemas(schema_path)
    tables = read_tables(source, schema['input'])
    before = copy.deepcopy(tables)
    if flags == ['--reject']:
        try:
            module.translate(tables)
        except (ValueError, TypeError, RuntimeError):
            assert tables == before, 'rejection mutated input'
            return
        raise AssertionError('unsorted input accepted')
    result = module.translate(tables)
    validate(result, schema['output'])
    saved = copy.deepcopy(result)
    empty = {table: [] for table in schema['input']}
    validate(module.translate(empty), schema['output'])
    assert module.translate(tables) == saved and result == saved, 'state leaked between calls'
    assert tables == before, 'input mutated'
    Path(destination).mkdir()
    for table, columns in schema['output'].items():
        with (Path(destination) / (table + '.csv')).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=[c for c, _ in columns])
            writer.writeheader()
            writer.writerows(saved[table])


if __name__ == '__main__':
    main()
