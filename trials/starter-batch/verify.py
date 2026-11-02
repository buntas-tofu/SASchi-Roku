#!/usr/bin/env python3
"""Replay archived starter candidates against frozen independent expectations.

Assessment verdicts remain attributed human-style parent review, not executable
semantic checks. Artifact hashes bind those reviews to the inspected reports.
"""
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

ROOT = Path(__file__).resolve().parent
TASKS = ['A1', 'A2', 'A3', 'A4', 'length-python', 'length-r', 'lag-python', 'lag-r']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(text, mechanism, expected):
    """Compare logical CSV exactly, allowing equivalent finite numeric spelling."""
    parsed = list(csv.reader(text.splitlines(keepends=True)))
    if not parsed or parsed[0] != mechanism['output_columns']:
        raise AssertionError('column schema differs')
    rows = parsed[1:]
    if len(rows) != len(expected):
        raise AssertionError('row count differs')
    for actual, wanted in zip(rows, expected):
        if len(actual) != len(wanted):
            raise AssertionError('row width differs')
        for index, (value, target) in enumerate(zip(actual, wanted)):
            if index == 0 or mechanism['output_columns'][index] == 'text':
                if value != target:
                    raise AssertionError('character value/order differs')
            elif target is None:
                if value != '':
                    raise AssertionError('missing position differs')
            else:
                try:
                    number = Decimal(value)
                except InvalidOperation as exc:
                    raise AssertionError('invalid numeric output') from exc
                if not number.is_finite() or number != Decimal(str(target)):
                    raise AssertionError('numeric value differs')


def csv_text(columns, rows):
    import io
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    return output.getvalue()


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                          timeout=15, check=False)


def harness_command(language, candidate, inputs, output, mechanism):
    prefix = [sys.executable, '-I', str(ROOT / 'python_harness.py')] if language == 'python' else ['Rscript', '--vanilla', str(ROOT / 'r_harness.R')]
    return prefix + [str(candidate), str(inputs), str(output), mechanism]


def negative_controls(oracle, directory):
    rejected = []
    mutations = [
        ('blank-length-zero', 'length', 'edge', 2, 2, 0),
        ('trim-leading-space', 'length', 'edge', 0, 2, 2),
        ('trim-tab', 'length', 'edge', 1, 2, 2),
        ('wrong-storage-width', 'length', 'main', 0, 1, 'KITE'),
        ('zero-lag-initialization', 'lag', 'main', 0, 2, 0),
        ('skip-missing-queue-input', 'lag', 'edge', 2, 2, 5),
        ('wrong-lag-direction', 'lag', 'main', 0, 2, 18),
    ]
    for name, mechanism, case, row, col, bad in mutations:
        spec = oracle[mechanism]
        rows = copy.deepcopy(spec['expected'][case])
        rows[row][col] = bad
        try:
            compare(csv_text(spec['output_columns'], rows), spec, spec['expected'][case])
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('negative control accepted: ' + name)
    spec = oracle['length']
    try:
        compare(csv_text(spec['output_columns'], list(reversed(spec['expected']['main']))), spec, spec['expected']['main'])
    except AssertionError:
        rejected.append('row-reordering')
    else:
        raise AssertionError('reordering accepted')
    # Real programs exercise input-mutation and repeatability detection in the
    # same subprocess harness used for candidates, rather than mocking checks.
    programs = {
        'caller-mutation': ("def translate(rows):\n    rows[0]['text'] = 'changed'\n    return []\n", 'length', 'caller input changed'),
        'queue-state-leak': ("history = [None, None]\ndef translate(rows):\n    result = []\n    for row in rows:\n        value = row['value']\n        prev, prev2 = history[-1], history[-2]\n        result.append(dict(row_id=row['row_id'], value=value, prev=prev, prev2=prev2, change=None if value is None or prev is None else value-prev))\n        history.append(value)\n    return result\n", 'lag', 'fresh-call results differ'),
    }
    for name, (source, mechanism, message) in programs.items():
        candidate = directory / (name + '.py')
        candidate.write_text(source)
        inputs = ROOT / 'packets' / (mechanism + '-python') / 'main.csv'
        result = run(harness_command('python', candidate, inputs, directory / (name + '.csv'), mechanism), directory)
        if result.returncode == 0 or message not in result.stderr:
            raise AssertionError('harness negative control failed: ' + name)
        rejected.append(name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if not shutil.which('Rscript'):
        raise SystemExit('Rscript is required; no partial PASS or implicit skip')
    frozen = json.loads((ROOT / 'freeze.json').read_text())
    for name, digest in frozen['hashes'].items():
        if sha(ROOT / name) != digest:
            raise SystemExit('frozen input drift: ' + name)
    delivery = json.loads((ROOT / 'delivery.json').read_text())
    for name, digest in delivery['hashes'].items():
        if sha(ROOT / name) != digest:
            raise SystemExit('first-delivery drift: ' + name)
    oracle = json.loads((ROOT / 'oracle.json').read_text())
    review = json.loads((ROOT / 'assessment-review.json').read_text())
    results = []
    for task in TASKS[:4]:
        entry = review['cases'][task]
        if sha(ROOT / 'candidates' / task / 'report.md') != entry['report_sha256']:
            raise SystemExit('assessment report drift: ' + task)
        results.append({'task': task, 'kind': 'archived-parent-review', 'verdict': entry['verdict'], 'criteria': len(entry['criteria'])})
    with tempfile.TemporaryDirectory(prefix='roku-starter-replay-') as temporary:
        directory = Path(temporary)
        for task in TASKS[4:]:
            mechanism, language = task.split('-')
            spec = oracle[mechanism]
            candidate = ROOT / 'candidates' / task / ('converted.py' if language == 'python' else 'converted.R')
            checks = []
            for case, expected in spec['expected'].items():
                inputs = ROOT / 'packets' / task / (case + '.csv')
                input_digest = sha(inputs)
                # Execute against a temporary copy, and verify source bytes too.
                input_copy = directory / (task + '-' + case + '-input.csv')
                shutil.copyfile(inputs, input_copy)
                for interface in ('cli', 'memory'):
                    output = directory / (task + '-' + case + '-' + interface + '.csv')
                    command = ([sys.executable, '-I', str(candidate)] if language == 'python' else ['Rscript', '--vanilla', str(candidate)]) + [str(input_copy), str(output)]
                    if interface == 'memory':
                        command = harness_command(language, candidate, input_copy, output, mechanism)
                    try:
                        result = run(command, directory)
                        if result.returncode != 0:
                            raise AssertionError('execution failed: ' + result.stderr[-2000:])
                        if sha(input_copy) != input_digest:
                            raise AssertionError('input file changed')
                        compare(output.read_text(encoding='utf-8'), spec, expected)
                        checks.append({'case': case, 'interface': interface, 'verdict': 'PASS'})
                    except (AssertionError, OSError, subprocess.TimeoutExpired) as exc:
                        checks.append({'case': case, 'interface': interface, 'verdict': 'FAIL', 'detail': str(exc)})
            results.append({'task': task, 'kind': 'runtime-comparison', 'verdict': 'PASS' if all(c['verdict'] == 'PASS' for c in checks) else 'FAIL', 'checks': checks})
        negatives = negative_controls(oracle, directory)
    receipt = {
        'status': 'bounded starter observations; no live-SAS or general reliability claim',
        'acceptance_scope': 'frozen witnesses and archived assessment rubric only',
        'full_domain_signoff': False,
        'remaining_findings': 'findings.json',
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'r': run(['Rscript', '--version'], ROOT).stdout.strip(),
        'platform': platform.platform(), 'model_revision': None, 'sampling_parameters': None,
        'model_details_note': 'not exposed to parent; replay executes saved code, not model generation',
        'results': results, 'negative_controls_rejected': negatives,
        'hashes': {str(path.relative_to(ROOT)): sha(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and '__pycache__' not in path.parts and ('candidates' in path.parts or path.name in ['verify.py', 'python_harness.py', 'r_harness.R', 'freeze.json', 'delivery.json', 'oracle.json', 'assessment-review.json'])},
    }
    receipt['verdict'] = 'PASS' if all(r['verdict'] == 'PASS' for r in results) else 'FAIL'
    if args.receipt:
        with args.receipt.open('x') as stream:
            json.dump(receipt, stream, indent=2)
            stream.write('\n')
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
