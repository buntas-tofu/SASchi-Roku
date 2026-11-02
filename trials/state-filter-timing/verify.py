#!/usr/bin/env python3
"""Replay archived WHERE/IF translations against frozen independent truth."""
import argparse
import copy
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TABLES = ('where_path', 'if_path')
CASES = ('main', 'leading', 'single', 'all-missing', 'silent', 'empty')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=20)


def read_csv(path):
    return list(csv.reader(io.StringIO(path.read_bytes().decode('utf-8'), newline='')))


def compare(path, columns, expected):
    rows = read_csv(path)
    assert rows and rows[0] == columns, 'column schema differs'
    assert len(rows) - 1 == len(expected), 'row count differs'
    for position, (actual, target) in enumerate(zip(rows[1:], expected), 1):
        assert len(actual) == len(columns), 'row width differs'
        for index, (value, wanted) in enumerate(zip(actual, target)):
            context = f'{path.stem} row {position}, {columns[index]}'
            if index == 0:
                assert value == wanted, context + ': identifier or order differs'
            elif wanted is None:
                assert value == '', context + ': expected missing, got ' + repr(value)
            else:
                try:
                    number = Decimal(value)
                except InvalidOperation as exc:
                    raise AssertionError(context + ': invalid numeric value') from exc
                assert number.is_finite() and number == Decimal(str(wanted)), context + f': expected {wanted}, got {value}'


def write_csv(path, columns, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if not shutil.which('Rscript'):
        raise SystemExit('Native Rscript is required; no implicit skip')
    for manifest in ('freeze.json', 'harness-freeze.json', 'delivery.json'):
        for path, digest in json.loads((ROOT / manifest).read_text())['hashes'].items():
            if sha(ROOT / path) != digest:
                raise SystemExit('artifact drift: ' + path)
    review = json.loads((ROOT / 'review.json').read_text())
    for path, digest in review['reviewed_hashes'].items():
        assert sha(ROOT / path) == digest, 'reviewed artifact drift'
    oracle = json.loads((ROOT / 'oracle.json').read_text())
    checks = []
    original_evidence = {}

    def record(name, operation):
        try:
            operation()
            checks.append({'name': name, 'verdict': 'PASS'})
        except (AssertionError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as error:
            checks.append({'name': name, 'verdict': 'FAIL', 'detail': str(error)})

    def success(command, cwd):
        result = execute(command, cwd)
        assert result.returncode == 0, result.stderr[-1800:]

    packet_hashes = {str(p.relative_to(ROOT)): sha(p) for p in (ROOT / 'packet').rglob('*') if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='roku-filter-replay-') as temp:
        directory = Path(temp)
        for language in ('python', 'r'):
            runtime = [sys.executable, '-I'] if language == 'python' else ['Rscript', '--vanilla']
            candidate = ROOT / 'candidate' / ('converted.py' if language == 'python' else 'converted.R')
            driver = ROOT / ('python_driver.py' if language == 'python' else 'r_driver.R')
            for case in CASES:
                source = ROOT / 'packet' / (case + '.csv')
                for interface in ('cli', 'memory'):
                    dest = directory / (language + '-' + case + '-' + interface)
                    command = runtime + ([str(candidate), str(source), str(dest)] if interface == 'cli'
                                         else [str(driver), str(candidate), str(source), str(dest)])

                    def check(command=command, dest=dest, case=case, interface=interface):
                        success(command, directory)
                        for table in TABLES:
                            compare(dest / (table + '.csv'), oracle['columns'], oracle[table][case])
                        if interface == 'cli':
                            before = {str(p.relative_to(dest)): sha(p) if p.is_file() else 'directory' for p in dest.rglob('*')}
                            result = execute(command, directory)
                            after = {str(p.relative_to(dest)): sha(p) if p.is_file() else 'directory' for p in dest.rglob('*')}
                            assert result.returncode != 0 and before == after, 'existing output was overwritten'
                    record(language + '/' + case + '/' + interface, check)

        def reproduce():
            dest = directory / 'original'
            success([sys.executable, '-I', str(ROOT / 'python_driver.py'), str(ROOT / 'packet/buggy.py'),
                     str(ROOT / 'packet/main.csv'), str(dest)], directory)
            original_evidence['outputs'] = {table: read_csv(dest / (table + '.csv')) for table in TABLES}
            mismatch = None
            for table in TABLES:
                try:
                    compare(dest / (table + '.csv'), oracle['columns'], oracle[table]['main'])
                except AssertionError as error:
                    mismatch = str(error)
                    break
            assert mismatch is not None, 'original buggy implementation was accepted'
            original_evidence['first_difference'] = mismatch
        record('reproduce-original-failure', reproduce)

        mutations = ('where-as-late-if', 'if-filter-before-queue', 'if-filter-before-sum',
                     'missing-poison', 'wrong-initial', 'sorted-order')
        for name in mutations:
            def reject(name=name):
                table = 'if_path' if name.startswith('if-') else 'where_path'
                rows = copy.deepcopy(oracle[table]['main'])
                if name == 'where-as-late-if': rows = copy.deepcopy(oracle['if_path']['main'])
                if name == 'if-filter-before-queue': rows[1][2] = 5
                if name == 'if-filter-before-sum': rows[1][3] = 15
                if name == 'missing-poison': rows[1][3] = None
                if name == 'wrong-initial': rows[0][3] = 5
                if name == 'sorted-order': rows.sort(key=lambda row: row[0])
                path = directory / (name + '.csv')
                write_csv(path, oracle['columns'], rows)
                rejected = False
                try:
                    compare(path, oracle['columns'], oracle[table]['main'])
                except AssertionError:
                    rejected = True
                assert rejected, 'incorrect output accepted'
            record('reject/' + name, reject)
    assert packet_hashes == {str(p.relative_to(ROOT)): sha(p) for p in (ROOT / 'packet').rglob('*') if p.is_file()}, 'packet changed'
    receipt = {
        'status': 'Bounded saved-code replay and archived manual review; no live SAS execution',
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'environment': {'python': platform.python_version(), 'r': execute(['Rscript', '--version'], ROOT).stdout.strip(),
                        'platform': platform.platform()},
        'model_revision': None, 'sampling_parameters': None,
        'model_details': 'not exposed; one evaluator produced both targets',
        'manual_review': review['verdict'], 'checks': checks, 'original_failure': original_evidence,
        'hashes': {str(p.relative_to(ROOT)): sha(p) for p in sorted(ROOT.rglob('*'))
                   if p.is_file() and '__pycache__' not in p.parts and p.name != 'receipt.json'}
    }
    receipt['verdict'] = 'PASS' if review['verdict'] == 'PASS' and all(c['verdict'] == 'PASS' for c in checks) else 'FAIL'
    if args.receipt:
        with args.receipt.open('x') as stream:
            json.dump(receipt, stream, indent=2)
            stream.write('\n')
    print(json.dumps(receipt, indent=2))
    return int(receipt['verdict'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
