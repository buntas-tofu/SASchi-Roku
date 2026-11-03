#!/usr/bin/env python3
"""Replay three first deliveries against literal parent expectations."""
import argparse
import copy
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from python_driver import schemas

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(path):
    return {str(p.relative_to(path)): sha(p) for p in sorted(path.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def execute(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)


def compare(path, columns, expected):
    with path.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.reader(stream))
    assert rows and rows[0] == [c for c, _ in columns], 'column schema differs'
    assert len(rows) - 1 == len(expected), 'row count differs'
    for position, (actual, target) in enumerate(zip(rows[1:], expected), 1):
        assert len(actual) == len(columns), 'row width differs'
        for (column, kind), value, wanted in zip(columns, actual, target):
            context = f'{path.stem} row {position} {column}'
            if kind == 'text':
                assert value == wanted, context + f': expected {wanted!r}, got {value!r}'
            elif wanted is None:
                assert value == '', context + ': expected missing'
            else:
                try:
                    number = Decimal(value)
                except InvalidOperation as error:
                    raise AssertionError(context + ': invalid number') from error
                assert number.is_finite() and number == Decimal(str(wanted)), context + f': expected {wanted}, got {value}'


def write_csv(path, columns, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow([c for c, _ in columns])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if not shutil.which('Rscript'):
        raise SystemExit('Native Rscript required; no implicit skip')
    for name in ('freeze.json', 'delivery.json'):
        for path, digest in json.loads((ROOT / name).read_text())['hashes'].items():
            assert sha(ROOT / path) == digest, 'artifact drift: ' + path
    review = json.loads((ROOT / 'review.json').read_text())
    for path, digest in review['reviewed_hashes'].items():
        assert sha(ROOT / path) == digest, 'reviewed artifact drift: ' + path
    oracle = json.loads((ROOT / 'oracle.json').read_text())
    before = snapshot(ROOT / 'packets')
    checks = []
    original = {}

    def record(name, operation):
        try:
            operation()
            checks.append({'name': name, 'verdict': 'PASS'})
        except (AssertionError, ValueError, OSError, KeyError, subprocess.TimeoutExpired) as error:
            checks.append({'name': name, 'verdict': 'FAIL', 'detail': str(error)})

    def success(command, cwd):
        result = execute(command, cwd)
        assert result.returncode == 0, result.stderr[-2400:]

    with tempfile.TemporaryDirectory(prefix='roku-boundaries-replay-') as temp:
        work = Path(temp)
        for task, cases in oracle.items():
            packet = ROOT / 'packets' / task
            schema = schemas(packet / 'schema.csv')
            for language in ('python', 'r'):
                runtime = [sys.executable, '-I', '-B'] if language == 'python' else ['Rscript', '--vanilla']
                candidate = ROOT / 'candidates' / task / ('converted.py' if language == 'python' else 'converted.R')
                driver = ROOT / ('python_driver.py' if language == 'python' else 'r_driver.R')
                for case, expected in cases.items():
                    source = packet / 'cases' / case
                    for interface in ('cli', 'memory'):
                        dest = work / f'{task}-{language}-{case}-{interface}'
                        command = runtime + ([str(candidate), str(source), str(dest)] if interface == 'cli' else
                          [str(driver), str(candidate), str(packet / 'schema.csv'), str(source), str(dest)])

                        def check(command=command, dest=dest, expected=expected, schema=schema, interface=interface):
                            success(command, work)
                            for table, rows in expected.items():
                                compare(dest / (table + '.csv'), schema['output'][table], rows)
                            if interface == 'cli':
                                saved = snapshot(dest)
                                result = execute(command, work)
                                assert result.returncode != 0 and snapshot(dest) == saved, 'existing destination modified'
                        record(f'{task}/{language}/{case}/{interface}', check)
                if task in ('groups', 'merge'):
                    for table in schema['input']:
                        source = work / f'unsorted-{task}-{language}-{table}'
                        shutil.copytree(packet / 'cases/main', source)
                        with (source / (table + '.csv')).open(newline='') as stream:
                            rows = list(csv.reader(stream))
                        rows[1:] = list(reversed(rows[1:]))
                        with (source / (table + '.csv')).open('w', newline='') as stream:
                            csv.writer(stream).writerows(rows)
                        for interface in ('cli', 'memory'):
                            dest = work / f'rejected-{task}-{language}-{table}-{interface}'
                            command = runtime + ([str(candidate), str(source), str(dest)] if interface == 'cli' else
                              [str(driver), str(candidate), str(packet / 'schema.csv'), str(source), str(dest), '--reject'])

                            def reject_unsorted(command=command, dest=dest, interface=interface, source=source):
                                saved = snapshot(source)
                                result = execute(command, work)
                                assert (result.returncode != 0 if interface == 'cli' else result.returncode == 0), result.stderr[-1800:]
                                assert not dest.exists() and snapshot(source) == saved, 'rejection left effects'
                            record(f'{task}/{language}/reject-unsorted-{table}/{interface}', reject_unsorted)

        def reproduce():
            packet = ROOT / 'packets/groups'
            dest = work / 'original'
            success([sys.executable, '-I', '-B', str(ROOT / 'python_driver.py'), str(packet / 'buggy.py'),
                     str(packet / 'schema.csv'), str(packet / 'cases/main'), str(dest)], work)
            try:
                compare(dest / 'want.csv', schemas(packet / 'schema.csv')['output']['want'], oracle['groups']['main']['want'])
            except AssertionError as error:
                original['first_difference'] = str(error)
                assert str(error) == 'want row 3 last_account: expected 1, got 0', str(error)
            else:
                raise AssertionError('original bug accepted')
        record('groups/reproduce-original', reproduce)

        mutations = [
          ('groups', 'reset-queue', 'want', 3, 4, None),
          ('groups', 'flat-last-flag', 'want', 2, 10, 0),
          ('groups', 'unmasked-receiver', 'want', 3, 5, 20),
          ('groups', 'reset-sum-at-account', 'want', 2, 6, 120),
          ('merge', 'cartesian-row', 'want', None, None, None),
          ('merge', 'reuse-right-shared', 'want', 1, 5, 101),
          ('merge', 'coalesce-missing', 'want', 7, 5, 7),
          ('merge', 'carry-across-key', 'want', 6, 1, 6),
          ('widths', 'runtime-tag-width', 'stage', 0, 3, 'LONG'),
          ('widths', 'restore-lost-characters', 'want', 0, 1, 'ABCDE'),
          ('widths', 'trim-transport', 'stage', 0, 2, 'ABCZ'),
          ('widths', 'blank-length-zero', 'want', 2, 6, 0),
        ]
        for task, name, table, row, column, value in mutations:
            def reject(task=task, name=name, table=table, row=row, column=column, value=value):
                rows = copy.deepcopy(oracle[task]['main'][table])
                if row is None:
                    rows.insert(3, copy.deepcopy(rows[2]))
                else:
                    rows[row][column] = value
                path = work / (name + '.csv')
                columns = schemas(ROOT / 'packets' / task / 'schema.csv')['output'][table]
                write_csv(path, columns, rows)
                try:
                    compare(path, columns, oracle[task]['main'][table])
                except AssertionError:
                    return
                raise AssertionError('wrong output accepted')
            record(task + '/reject-output/' + name, reject)
    assert before == snapshot(ROOT / 'packets'), 'packet changed'
    receipt = {
      'status': 'Bounded target-runtime evidence for maintainer review; no live SAS comparison',
      'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
      'environment': {'python': platform.python_version(), 'r': execute(['Rscript', '--version'], ROOT).stdout.strip()},
      'model_revision': None, 'sampling_parameters': None,
      'model_details': 'Not exposed. Three fresh evaluators, each supplied both language targets.',
      'manual_review': review['verdict'], 'checks': checks, 'original_failure': original,
      'hashes': {path: digest for path, digest in snapshot(ROOT).items() if path != 'receipt.json'}
    }
    receipt['verdict'] = 'PASS' if review['verdict'] == 'PASS' and all(c['verdict'] == 'PASS' for c in checks) else 'FAIL'
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'verdict': receipt['verdict'], 'checks': len(checks),
                      'failures': [c for c in checks if c['verdict'] != 'PASS']}, indent=2))
    return 0 if receipt['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
