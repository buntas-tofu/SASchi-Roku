"""Independent hand fixtures and transport checks for this bounded source slice."""
import copy
import csv
import hashlib
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'output'
INPUT = ('row_id', 'region', 'account', 'value')
COLUMNS = INPUT + ('raw_prev', 'prev', 'total', 'first_region', 'last_region', 'first_account', 'last_account')
# Independently traced rows in schema order, not captured SAS results.
HAND = {
    'main': [
        ('0007', 1, 7, 5, None, None, 105, 1, 0, 1, 0),
        ('NA', 1, 7, None, 5, 5, 105, 0, 0, 0, 1),
        ('g3', 1, 8, 20, None, None, 125, 0, 1, 1, 1),
        ('g4', 2, 8, 100, 20, None, 200, 1, 0, 1, 0),
        ('g5', 2, 8, -2, 100, 100, 198, 0, 0, 0, 1),
        ('g6', 2, 9, 0, -2, None, 198, 0, 1, 1, 1),
        ('g7', 3, 9, None, 0, None, 100, 1, 1, 1, 1),
    ],
    'hierarchy': [
        ('h1', 1, 9, 4, None, None, 104, 1, 1, 1, 1),
        ('h2', 2, 9, 8, 4, None, 108, 1, 1, 1, 1),
    ],
    'missing-keys': [
        ('m1', None, None, 2, None, None, 102, 1, 0, 1, 1),
        ('m2', None, 1, 3, 2, None, 105, 0, 1, 1, 1),
        ('m3', 1, 1, 4, 3, None, 104, 1, 1, 1, 1),
    ],
    'single': [('only', 1, 1, None, None, None, 100, 1, 1, 1, 1)],
    'empty': [],
}


def load(path):
    with path.open(newline='') as stream:
        reader = csv.DictReader(stream)
        columns = tuple(reader.fieldnames)
        rows = [{key: (value if key == 'row_id' else None if value == '' else float(value))
                 for key, value in row.items()} for row in reader]
    return columns, rows


def module(path):
    namespace = {'__name__': 'selftest_loaded', '__file__': str(path)}
    exec(compile(path.read_text(), str(path), 'exec'), namespace)
    return namespace


def first_diff(actual, expected):
    if len(actual) != len(expected):
        return f'row count actual={len(actual)} expected={len(expected)}'
    for i, (got, want) in enumerate(zip(actual, expected), 1):
        if tuple(got) != COLUMNS:
            return f'row={i} column order mismatch'
        for key in COLUMNS:
            if got[key] != want[key]:
                return f'row={i} column={key} actual={got[key]!r} expected={want[key]!r}'
    return None


def fixtures():
    for name, raw in HAND.items():
        _, rows = load(BASE / 'packet' / 'cases' / name / 'have.csv')
        yield name, rows, [dict(zip(COLUMNS, values)) for values in raw]


def baseline():
    buggy = module(BASE / 'packet' / 'buggy.py')['translate']
    for name, rows, expected in fixtures():
        print(f'BASELINE {name}: {first_diff(buggy({"have": rows})["want"], expected) or "MATCH"}')
    for path in [BASE / 'packet' / 'source.sas', BASE / 'packet' / 'buggy.py', BASE / 'packet' / 'schema.csv'] + sorted((BASE / 'packet' / 'cases').glob('*/have.csv')):
        print(f'SHA256 {path.relative_to(BASE)} {hashlib.sha256(path.read_bytes()).hexdigest()}')


def independent(rows):
    """Group-run oracle, independent of the target's adjacent-row loop."""
    n = len(rows)
    result = [{**row, 'raw_prev': None if i == 0 else rows[i - 1]['value'],
               'prev': None, 'total': None, 'first_region': 0,
               'last_region': 0, 'first_account': 0, 'last_account': 0}
              for i, row in enumerate(rows)]
    start = 0
    while start < n:
        end = start + 1
        while end < n and rows[end]['region'] == rows[start]['region']:
            end += 1
        result[start]['first_region'] = 1
        result[end - 1]['last_region'] = 1
        balance = 100.0
        for i in range(start, end):
            balance += 0 if rows[i]['value'] is None else rows[i]['value']
            result[i]['total'] = balance
        account_start = start
        while account_start < end:
            account_end = account_start + 1
            while account_end < end and rows[account_end]['account'] == rows[account_start]['account']:
                account_end += 1
            result[account_start]['first_account'] = 1
            result[account_end - 1]['last_account'] = 1
            for i in range(account_start + 1, account_end):
                result[i]['prev'] = rows[i - 1]['value']
            account_start = account_end
        start = end
    return result


def write_input(directory, rows):
    directory.mkdir()
    with (directory / 'have.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=INPUT)
        writer.writeheader()
        writer.writerows(rows)


def run(command, success=True):
    completed = subprocess.run([str(x) for x in command], cwd=BASE, capture_output=True, text=True)
    assert (completed.returncode == 0) == success, (command, completed.returncode, completed.stdout, completed.stderr)
    return completed


def validated_tests():
    target = module(OUT / 'converted.py')['translate']
    case_list = list(fixtures())
    for name, rows, expected in case_list:
        assert first_diff(independent(rows), expected) is None, name
    rng = random.Random(83197)
    keys = [(None, None), (None, -2), (None, 0), (-3, None), (-3, -2),
            (-3, 0), (0, None), (0, 0), (4, None), (4, 0), (4, 20)]
    for number in range(40):
        rows = []
        for region, account in keys:
            for _ in range(rng.randrange(5)):
                row_id = rng.choice(['0007', 'NA', '  exact  ', 'a,"b"', '#comment', 'A\\B', '0'])
                rows.append(dict(zip(INPUT, [row_id, region, account, rng.choice([None, -9.5, 0.0, 3.25, 17.0]) ])))
        case_list.append((f'generated-{number}', rows, independent(rows)))
    precision = [dict(zip(INPUT, ['precise', -5, None, 0.12345678901234566])),
                 dict(zip(INPUT, ['small', -5, None, 1e-100])),
                 dict(zip(INPUT, ['large', 2, -9, -1e200]))]
    case_list.append(('precision', precision, independent(precision)))
    overflow = [dict(zip(INPUT, [f'overflow-{i}', 1, 1, value]))
                for i, value in enumerate([1e308, 1e308, None, 2, -3])]
    overflow_expected = [dict(zip(COLUMNS, row)) for row in [
        ('overflow-0', 1, 1, 1e308, None, None, 1e308, 1, 0, 1, 0),
        ('overflow-1', 1, 1, 1e308, 1e308, 1e308, None, 0, 0, 0, 0),
        ('overflow-2', 1, 1, None, 1e308, 1e308, None, 0, 0, 0, 0),
        ('overflow-3', 1, 1, 2, None, None, 2, 0, 0, 0, 0),
        ('overflow-4', 1, 1, -3, 2, 2, -1, 0, 1, 0, 1),
    ]]
    case_list.append(('overflow', overflow, overflow_expected))
    for name, rows, expected in case_list:
        before = copy.deepcopy(rows)
        actual = target({'have': rows})
        assert list(actual) == ['want'], name
        assert first_diff(actual['want'], expected) is None, (name, first_diff(actual['want'], expected))
        assert rows == before, name
        assert target({'have': []}) == {'want': []}
        assert target({'have': rows}) == actual, name
        if actual['want']:
            actual['want'][0]['row_id'] = 'mutated output'
            assert rows == before, name
    print(f'PASS Python API: {len(case_list)} datasets, independent expectations, fresh calls, input preservation')
    launchers = [('python', ['python3', '-B', OUT / 'converted.py']),
                 ('R', ['Rscript', '--vanilla', OUT / 'converted.R'])]
    cli_count = 0
    invalid_count = 0
    with tempfile.TemporaryDirectory(prefix='selftest-', dir=BASE) as tmp:
        scratch = Path(tmp)
        for number, (name, rows, expected) in enumerate(case_list):
            source = scratch / f'input-{number}'
            write_input(source, rows)
            for label, command in launchers:
                destination = scratch / f'{label}-{number}'
                run(command + [source, destination])
                columns, got = load(destination / 'want.csv')
                assert columns == COLUMNS, (label, name, columns)
                assert first_diff(got, expected) is None, (label, name, first_diff(got, expected))
                cli_count += 1
        source = scratch / 'input-0'
        for label, command in launchers:
            destination = scratch / f'{label}-0'
            saved = (destination / 'want.csv').read_bytes()
            sentinel = destination / 'keep.txt'
            sentinel.write_text('unchanged')
            run(command + [source, destination], success=False)
            assert saved == (destination / 'want.csv').read_bytes()
            assert sentinel.read_text() == 'unchanged'
            occupied = scratch / f'occupied-{label}'
            occupied.write_text('keep existing file')
            run(command + [source, occupied], success=False)
            assert occupied.read_text() == 'keep existing file'
        sorted_rows = [dict(zip(INPUT, ['a', 1, 0, 2])), dict(zip(INPUT, ['b', 1, 1, 3]))]
        invalids = [list(reversed(sorted_rows)),
                    [dict(zip(INPUT, ['a', 1, 0, 2])), dict(zip(INPUT, ['b', None, 0, 3]))],
                    [dict(zip(INPUT, ['a', 1, 0, 2])), dict(zip(INPUT, ['b', 1, None, 3]))],
                    [dict(zip(INPUT, ['a', 1.5, 0, 2]))],
                    [dict(zip(INPUT, ['a', 1, 0, float('inf')]))],
                    [dict(zip(INPUT, ['', 1, 0, 2]))]]
        for number, rows in enumerate(invalids):
            try:
                target({'have': rows})
            except (ValueError, OverflowError):
                pass
            else:
                raise AssertionError(('invalid Python API accepted', number))
            source = scratch / f'invalid-{number}'
            write_input(source, rows)
            for label, command in launchers:
                destination = scratch / f'rejected-{label}-{number}'
                run(command + [source, destination], success=False)
                assert not destination.exists()
                invalid_count += 1
        rcheck = run(['Rscript', '--vanilla', OUT / 'selftest.R'])
        print(rcheck.stdout.strip())
    print(f'PASS CSV: {cli_count} executions, headers, order, exact text, blanks, binary64-safe serialization')
    print(f'PASS rejection: {invalid_count} invalid-input CLI executions, 6 Python API cases, 4 existing destinations unchanged')


if __name__ == '__main__':
    baseline()
    if '--baseline' not in sys.argv:
        validated_tests()
