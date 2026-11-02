#!/usr/bin/env python3
"""Independent replay of the three bounded skill evaluations."""
import argparse
import copy
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=20)

def compare(path, columns, expected, text_columns):
    # Decode bytes without universal-newline conversion: CRLF inside a cell matters.
    rows = list(csv.reader(io.StringIO(path.read_bytes().decode('utf-8'), newline='')))
    assert rows and rows[0] == columns, 'column schema differs'
    assert len(rows) - 1 == len(expected), 'row count differs'
    for actual, target in zip(rows[1:], expected):
        assert len(actual) == len(target), 'row width differs'
        for index, (value, wanted) in enumerate(zip(actual, target)):
            if columns[index] in text_columns:
                assert value == wanted, 'text bytes or row order differ'
            elif wanted is None:
                assert value == '', 'missing position differs'
            else:
                try:
                    number = Decimal(value)
                except InvalidOperation as exc:
                    raise AssertionError('invalid numeric output') from exc
                assert number.is_finite() and number == Decimal(str(wanted)), 'numeric value differs'

def write_csv(path, columns, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)

def check_bundle(source, directory, oracle, empty=False):
    data = directory / 'data.csv'
    metadata = json.loads((directory / 'metadata.json').read_text())
    original = json.loads(source.read_text())
    compare(data, oracle['columns'], [] if empty else oracle['rows'], {'id', 'text'})
    assert metadata['source_sha256'] == sha(source), 'source hash differs'
    assert metadata['data_sha256'] == sha(data), 'data hash differs'
    assert metadata['descriptor'] == original['descriptor'], 'descriptor differs'
    assert metadata['rows'] == ([] if empty else oracle['metadata_rows']), 'cell metadata differs'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if not shutil.which('Rscript'):
        raise SystemExit('Native Rscript required; no implicit skip')
    for manifest in ('freeze.json', 'delivery.json'):
        for name, digest in json.loads((ROOT / manifest).read_text())['hashes'].items():
            if sha(ROOT / name) != digest:
                raise SystemExit('artifact drift: ' + name)
    review = json.loads((ROOT / 'review.json').read_text())
    for name, digest in review['reviewed_hashes'].items():
        assert sha(ROOT / name) == digest, 'reviewed artifact drift'
    oracle = json.loads((ROOT / 'oracle.json').read_text())
    checks = []
    def record(name, operation):
        try:
            operation()
            checks.append({'name': name, 'verdict': 'PASS'})
        except (AssertionError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
            checks.append({'name': name, 'verdict': 'FAIL', 'detail': str(exc)})
    def successful(command, directory):
        result = run(command, directory)
        assert result.returncode == 0, result.stderr[-1800:]
    with tempfile.TemporaryDirectory(prefix='roku-proposals-replay-') as temp:
        directory = Path(temp)
        candidate = ROOT / 'candidates/interchange/bundle.py'
        source = ROOT / 'packets/interchange/main.json'
        input_hashes = {p: sha(p) for p in (ROOT / 'packets').rglob('*') if p.is_file()}
        for case in ('main', 'empty'):
            src = source.with_name(case + '.json')
            dest = directory / ('bundle-' + case)
            def build_check(src=src, dest=dest, case=case):
                successful([sys.executable, '-I', str(candidate), 'build', str(src), str(dest)], directory)
                check_bundle(src, dest, oracle['interchange'], case == 'empty')
                successful([sys.executable, '-I', str(candidate), 'check', str(src), str(dest)], directory)
            record('interchange/' + case + '/build-reopen-check', build_check)
        # Invalid inputs must fail before creating any output directory.
        original = json.loads(source.read_text())
        for name in ('encoding', 'width', 'duplicate-row'):
            mutated = copy.deepcopy(original)
            if name == 'encoding': mutated['descriptor']['encoding'] = 'not-a-codec'
            if name == 'width': mutated['rows'][0]['text_hex'] += '41'
            if name == 'duplicate-row': mutated['rows'][1]['row_no'] = 1
            invalid = directory / (name + '.json')
            invalid.write_text(json.dumps(mutated))
            dest = directory / ('invalid-' + name)
            def refuse(invalid=invalid, dest=dest):
                result = run([sys.executable, '-I', str(candidate), 'build', str(invalid), str(dest)], directory)
                assert result.returncode != 0 and not dest.exists(), 'invalid input accepted or partial output created'
            record('interchange/refuse-' + name, refuse)
        def existing_refusal():
            dest = directory / 'existing'
            dest.mkdir()
            marker = dest / 'keep.txt';marker.write_text('keep')
            result = run([sys.executable, '-I', str(candidate), 'build', str(source), str(dest)], directory)
            assert result.returncode != 0 and sorted(p.name for p in dest.iterdir()) == ['keep.txt'] and marker.read_text() == 'keep'
        record('interchange/refuse-existing', existing_refusal)
        # Rehash semantic mutants so content comparison, not merely a stale hash,
        # is required to detect them. Both the parent and candidate must refuse.
        for name in ('text', 'tag', 'raw-bytes', 'row-association', 'source-hash', 'data-hash'):
            def reject_mutant(name=name):
                dest = directory / ('mutant-' + name)
                shutil.copytree(directory / 'bundle-main', dest)
                metadata = json.loads((dest / 'metadata.json').read_text())
                if name == 'text':
                    rows = copy.deepcopy(oracle['interchange']['rows']);rows[0][2] = 'A\nB  '
                    write_csv(dest / 'data.csv', oracle['interchange']['columns'], rows)
                    metadata['data_sha256'] = sha(dest / 'data.csv')
                if name == 'tag': metadata['rows'][1]['amount_missing'] = '.'
                if name == 'raw-bytes': metadata['rows'][1]['text_raw_hex'] = '412042202020'
                if name == 'row-association': metadata['rows'][1]['row_no'] = 1
                if name == 'source-hash': metadata['source_sha256'] = '0' * 64
                if name == 'data-hash': metadata['data_sha256'] = '0' * 64
                (dest / 'metadata.json').write_text(json.dumps(metadata))
                rejected = False
                try:check_bundle(source, dest, oracle['interchange'])
                except AssertionError:rejected = True
                assert rejected, 'parent accepted mutant'
                result = run([sys.executable, '-I', str(candidate), 'check', str(source), str(dest)], directory)
                assert result.returncode != 0, 'candidate check accepted mutant'
            record('interchange/reject-' + name, reject_mutant)
        for language in ('python', 'r'):
            extension = '.py' if language == 'python' else '.R'
            candidate = ROOT / 'candidates/state' / ('converted' + extension)
            runtime = [sys.executable, '-I'] if language == 'python' else ['Rscript', '--vanilla']
            for case in ('main', 'single', 'silent', 'empty'):
                src = ROOT / 'packets/state' / (case + '.csv')
                for interface in ('cli', 'memory'):
                    dest = directory / ('state-' + language + '-' + case + '-' + interface)
                    command = runtime + [str(candidate), str(src), str(dest)]
                    if interface == 'memory':
                        driver = ROOT / 'drivers' / ('python_state.py' if language == 'python' else 'r_state.R')
                        command = runtime + [str(driver), str(candidate), str(src), str(dest)]
                    def state_check(command=command, dest=dest, case=case):
                        successful(command, directory)
                        for table in ('stage', 'want'):
                            columns = ['row_id', 'value', 'prev', 'total'] + (['delta'] if table == 'want' else [])
                            compare(dest / (table + '.csv'), columns, oracle['state'][table][case], {'row_id'})
                    record('state/' + language + '/' + case + '/' + interface, state_check)
        # Run the supplied original failing implementation in a separate process.
        def original_failure():
            driver = ROOT / 'drivers/python_state.py'
            dest = directory / 'original-bug'
            successful([sys.executable, '-I', str(driver), str(ROOT / 'packets/state/buggy.py'), str(ROOT / 'packets/state/main.csv'), str(dest)], directory)
            rejected = False
            try:compare(dest / 'stage.csv', ['row_id','value','prev','total'], oracle['state']['stage']['main'], {'row_id'})
            except AssertionError:rejected = True
            assert rejected, 'original bug was accepted'
        record('state/reproduce-original-failure', original_failure)
        mutants = [('unconditional-queue', 'stage', 1, 2, 100),
                   ('retained-prev', 'stage', 2, 2, 5),
                   ('wrong-initial', 'stage', 0, 3, 5),
                   ('missing-poison', 'stage', 1, 3, None),
                   ('discard-nonemitted-state', 'stage', 1, 3, 15),
                   ('downstream-delta', 'want', 3, 4, 2)]
        for name, table, row, col, value in mutants:
            def reject_state(name=name, table=table, row=row, col=col, value=value):
                expected = oracle['state'][table]['main']
                rows = copy.deepcopy(expected);rows[row][col] = value
                path = directory / (name + '.csv')
                columns = ['row_id','value','prev','total'] + (['delta'] if table == 'want' else [])
                write_csv(path, columns, rows)
                rejected = False
                try:compare(path, columns, expected, {'row_id'})
                except AssertionError:rejected = True
                assert rejected, 'wrong state output accepted'
            record('state/reject-' + name, reject_state)
        assert all(sha(p) == digest for p, digest in input_hashes.items()), 'packet modified by execution'
    receipt = {'status':'bounded replay and archived parent review; no live-SAS, SAS-binary or Parquet claim',
               'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
               'environment':{'python':platform.python_version(),'r':run(['Rscript','--version'],ROOT).stdout.strip(),'platform':platform.platform()},
               'model_revision':None,'sampling_parameters':None,'model_details':'not exposed; replay is saved-code execution',
               'manual_review':review['verdict'],'checks':checks,
               'hashes':{str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'receipt.json'}}
    receipt['verdict'] = 'PASS' if review['verdict'] == 'PASS' and all(c['verdict']=='PASS' for c in checks) else 'FAIL'
    if args.receipt:
        with args.receipt.open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
    print(json.dumps(receipt,indent=2))
    return int(receipt['verdict'] != 'PASS')

if __name__ == '__main__':
    raise SystemExit(main())
