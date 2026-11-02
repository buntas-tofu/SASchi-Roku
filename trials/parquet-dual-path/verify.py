#!/usr/bin/env python3
"""Independent complete-file replay of the frozen dual-path trial."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def run(command, cwd):
    return subprocess.run([str(x) for x in command], cwd=cwd, text=True,
                          capture_output=True, timeout=90)


def success(command, cwd):
    result = run(command, cwd)
    assert result.returncode == 0, result.stderr[-3000:] + result.stdout[-1000:]
    return result


def source_case(name, fixtures):
    if name == 'sas-sample':
        return fixtures / 'sample.sas7bdat', None
    if name.startswith('sas-missing'):
        return fixtures / 'missing.sas7bdat', fixtures / 'missing.sas7bcat' if name.endswith('-catalog') and not name.endswith('no-catalog') else None
    return ROOT / 'packet/synthetic' / (name + '.json'), None


def footer(source, catalog, mode):
    return {'saschi.source_sha256': sha(source), 'saschi.catalog_sha256': sha(catalog) if catalog else '',
            'saschi.mode': mode, 'saschi.schema_version': '1'}


def python_observation(directory):
    result = {}
    for mode in ('archive', 'analysis'):
        table = pq.read_table(directory / (mode + '.parquet'))
        columns = []
        for field, column in zip(table.schema, table.columns):
            if pa.types.is_date32(field.type):
                column = column.cast(pa.int32())
            elif pa.types.is_timestamp(field.type):
                column = column.cast(pa.int64())
            columns.append(column.to_pylist())
        result[mode] = {'schema': [[f.name, str(f.type)] for f in table.schema],
                        'rows': [list(row) for row in zip(*columns)],
                        'metadata': {k.decode(): v.decode() for k, v in (table.schema.metadata or {}).items()}}
    return result


def compare_observation(observed, expected, source, catalog):
    for mode in ('archive', 'analysis'):
        assert observed[mode]['schema'] == expected[mode + '_schema'], mode + ': physical/logical schema differs'
        actual, wanted = observed[mode]['rows'], expected[mode + '_rows']
        assert len(actual) == len(wanted), mode + ': row count differs'
        for i, (row, truth) in enumerate(zip(actual, wanted)):
            assert len(row) == len(truth), mode + ': row width differs'
            for j, (value, target) in enumerate(zip(row, truth)):
                context = f'{mode} row {i} column {expected[mode + "_schema"][j][0]}'
                if target is None:
                    assert value is None, context + ': missing differs'
                elif isinstance(target, str):
                    assert isinstance(value, str) and value == target, context + ': exact text/tag differs'
                else:
                    assert type(value) in (int, float) and math.isfinite(value) and value == target, context + f': expected {target!r}, got {value!r}'
        for key, value in footer(source, catalog, mode).items():
            assert observed[mode]['metadata'].get(key) == value, mode + ': source/mode association differs'


def compare_metadata(directory, expected, source, catalog, writer=None):
    meta = json.loads((directory / 'metadata.json').read_text())
    assert meta['schema_version'] == 1 and meta['source_format'] == expected['source_kind']
    assert meta['row_count'] == len(expected['archive_rows'])
    assert meta['character_fidelity'] == expected['character_fidelity']
    assert meta['catalog_status'] == expected['catalog_status'] and meta['timezone'] is None
    if expected['source_kind'] == 'envelope':
        assert meta['source_encoding'].lower() == expected['encoding'].lower()
    else:
        assert meta['source_encoding'] is None or meta['source_encoding'].lower().replace('-', '') == 'utf8'
    sources = [('data', source)] + ([('catalog', catalog)] if catalog else [])
    if (source.parent / 'LICENSE').exists():
        sources.append(('license', source.parent / 'LICENSE'))
    source_rows = [{'role': role, 'path': 'source/' + p.name, 'sha256': sha(p)} for role, p in sources]
    assert meta['source_files'] == source_rows, 'retained source identity differs'
    for row in source_rows:
        assert sha(directory / row['path']) == row['sha256'], 'retained source bytes differ'
    assert len(meta['columns']) == len(expected['columns'])
    for actual, wanted in zip(meta['columns'], expected['columns']):
        for key, value in wanted.items():
            if expected['source_kind'] == 'sas7bdat' and key == 'width_bytes' and actual[key] is None:
                continue  # haven does not expose original storage width.
            if expected['source_kind'] == 'sas7bdat' and key == 'informat':
                # The pre-dispatch oracle mistakenly marked all informats null.
                # Require known pyreadstat values; haven's unavailable fields stay null.
                correction = json.loads((ROOT / 'reader-metadata-correction.json').read_text())
                if writer == 'python' and sha(source) == correction['source_sha256']:
                    value = correction['sample_informats'][wanted['name']]
            assert actual[key] == value, wanted['name'] + ': descriptor differs at ' + key
    assert meta['events'] == expected['events'], 'per-cell transformation log differs'
    assert meta['files'] == {mode + '.parquet': sha(directory / (mode + '.parquet')) for mode in ('archive', 'analysis')}
    assert isinstance(meta['libraries'], dict) and meta['libraries'], 'library versions missing'
    return meta


def update_output_hash(directory, mode):
    path = directory / 'metadata.json'
    meta = json.loads(path.read_text())
    meta['files'][mode + '.parquet'] = sha(directory / (mode + '.parquet'))
    path.write_text(json.dumps(meta, indent=2) + '\n')


def replace_cell(directory, mode, name, row, value):
    path = directory / (mode + '.parquet')
    table = pq.read_table(path)
    index = table.schema.get_field_index(name)
    values = table.column(index).to_pylist()
    values[row] = value
    table = table.set_column(index, table.schema.field(index), pa.array(values, type=table.schema.field(index).type))
    pq.write_table(table, path)
    update_output_hash(directory, mode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--rscript', default='Rscript')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    assert shutil.which(args.rscript) or Path(args.rscript).exists(), 'native R required'
    for name in ('freeze.json', 'delivery.json'):
        for path, digest in json.loads((ROOT / name).read_text())['hashes'].items():
            original = ROOT / 'parent-original/verify.py' if name == 'freeze.json' and path == 'verify.py' else ROOT / path
            assert sha(original) == digest, 'artifact drift: ' + path
    for path, digest in json.loads((ROOT / 'harness-correction.json').read_text())['hashes'].items():
        assert sha(ROOT / path) == digest, 'corrected harness drift: ' + path
    # Cached inputs are checked without any network call during replay.
    from fetch_fixtures import SELECTED
    for record in json.loads((ROOT / 'upstream.json').read_text())['files']:
        if record['path'] in SELECTED:
            assert sha(args.fixtures / SELECTED[record['path']]) == record['sha256'], 'upstream identity differs'
    review = json.loads((ROOT / 'review.json').read_text())
    for path, digest in review['reviewed_hashes'].items():
        assert sha(ROOT / path) == digest, 'reviewed artifact drift'
    oracle = json.loads((ROOT / 'oracle.json').read_text())
    before = snapshot(ROOT / 'packet')
    fixture_before = snapshot(args.fixtures)
    checks = []

    def record(name, operation):
        try:
            operation()
            checks.append({'name': name, 'verdict': 'PASS'})
        except (AssertionError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as error:
            checks.append({'name': name, 'verdict': 'FAIL', 'detail': str(error)})

    with tempfile.TemporaryDirectory(prefix='roku-parquet-replay-') as temp:
        work = Path(temp)
        for language in ('python', 'r'):
            candidate = ROOT / 'candidates' / language / ('convert.py' if language == 'python' else 'convert.R')
            runtime = [sys.executable, '-I', '-B'] if language == 'python' else [args.rscript, '--vanilla']
            outputs = {}
            for case, expected in oracle.items():
                source, catalog = source_case(case, args.fixtures)
                dest = work / (language + '-' + case)
                outputs[case] = dest
                suffix = ['--catalog', catalog] if catalog else []
                command = runtime + [candidate, 'convert', source, dest] + suffix

                def convert_check(command=command, dest=dest, expected=expected, source=source, catalog=catalog):
                    success(command, work)
                    compare_metadata(dest, expected, source, catalog, writer=language)
                    compare_observation(python_observation(dest), expected, source, catalog)
                    observer = dest / 'r-observation.json'
                    success([args.rscript, '--vanilla', ROOT / 'r_observer.R', dest, observer], work)
                    observed = json.loads(observer.read_text())
                    observer.unlink()
                    compare_observation(observed, expected, source, catalog)
                    saved = snapshot(dest)
                    result = run(command, work)
                    assert result.returncode != 0 and snapshot(dest) == saved, 'existing destination modified'
                record(language + '/' + case + '/convert-two-consumers', convert_check)

                def validate_check(source=source, dest=dest, suffix=suffix):
                    saved = snapshot(dest)
                    success(runtime + [candidate, 'validate', source, dest] + suffix, work)
                    assert snapshot(dest) == saved, 'validation modified output'
                record(language + '/' + case + '/validate', validate_check)

            mutations = ('corrupt-parquet', 'swapped-metadata', 'changed-analysis', 'collapsed-tag',
                         'reordered-analysis', 'wrong-date', 'modified-source', 'wrong-external-source')
            for name in mutations:
                def reject(name=name):
                    dest = work / (language + '-wrong-' + name)
                    shutil.copytree(outputs['main'], dest)
                    source, catalog = source_case('main', args.fixtures)
                    if name == 'corrupt-parquet':
                        path = dest / 'archive.parquet'; data = bytearray(path.read_bytes()); data[0] ^= 255; path.write_bytes(data)
                    elif name == 'swapped-metadata':
                        shutil.copy2(outputs['utf8'] / 'metadata.json', dest / 'metadata.json')
                    elif name == 'changed-analysis':
                        replace_cell(dest, 'analysis', 'amount', 0, 2.5)
                    elif name == 'collapsed-tag':
                        replace_cell(dest, 'archive', 'amount__sas_missing', 1, '.')
                    elif name == 'reordered-analysis':
                        table = pq.read_table(dest / 'analysis.parquet')
                        pq.write_table(table.take(pa.array(list(reversed(range(table.num_rows))))), dest / 'analysis.parquet')
                        update_output_hash(dest, 'analysis')
                    elif name == 'wrong-date':
                        replace_cell(dest, 'analysis', 'day', 0, datetime(1970, 1, 1).date())
                    elif name == 'modified-source':
                        path = dest / 'source' / source.name; path.write_bytes(path.read_bytes() + b' ')
                    else:
                        source, catalog = source_case('utf8', args.fixtures)
                    saved = snapshot(dest)
                    result = run(runtime + [candidate, 'validate', source, dest], work)
                    assert result.returncode != 0, 'corrupted/stale output accepted'
                    assert snapshot(dest) == saved, 'failed validation modified output'
                    # Independent parent checks must also reject the same corruption.
                    try:
                        compare_metadata(dest, oracle['main'], source, catalog, writer=language)
                        compare_observation(python_observation(dest), oracle['main'], source, catalog)
                    except (AssertionError, ValueError, OSError):
                        return
                    raise AssertionError('parent accepted corrupted output')
                record(language + '/reject/' + name, reject)

            for name in ('wrong-width', 'ambiguous-number', 'invalid-tag', 'reserved-name'):
                def reject_domain(name=name):
                    document = json.loads((ROOT / 'packet/synthetic/main.json').read_text())
                    if name == 'wrong-width': document['rows'][0]['note']['hex'] = '61'
                    elif name == 'ambiguous-number': document['rows'][0]['amount']['missing'] = '.'
                    elif name == 'invalid-tag': document['rows'][0]['amount'] = {'missing': '.AA'}
                    else: document['columns'][0]['name'] = '__row_index'
                    source = work / (language + '-' + name + '.json')
                    source.write_text(json.dumps(document))
                    dest = work / (language + '-rejected-' + name)
                    saved = sha(source)
                    result = run(runtime + [candidate, 'convert', source, dest], work)
                    assert result.returncode != 0 and not dest.exists(), 'invalid input accepted or destination created'
                    assert sha(source) == saved, 'source mutated'
                record(language + '/domain/' + name, reject_domain)
    assert before == snapshot(ROOT / 'packet') and fixture_before == snapshot(args.fixtures), 'input changed'
    receipt = {
      'status': 'Bounded actual-file interchange evidence for maintainer review; no live SAS execution',
      'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
      'environment': {'python': platform.python_version(), 'pyarrow': pa.__version__,
                      'r': success([args.rscript, '--version'], ROOT).stdout.strip()},
      'model_revision': None, 'sampling_parameters': None,
      'model_details': 'Not exposed. Two fresh evaluators, one per writer language; both readers share ReadStat.',
      'manual_review': review['verdict'], 'checks': checks,
      'hashes': {p: d for p, d in snapshot(ROOT).items() if p != 'receipt.json'},
      'fixture_hashes': fixture_before,
    }
    receipt['verdict'] = 'PASS' if review['verdict'] == 'PASS' and all(c['verdict'] == 'PASS' for c in checks) else 'FAIL'
    if args.receipt: args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'verdict': receipt['verdict'], 'checks': len(checks),
                      'failures': [c for c in checks if c['verdict'] != 'PASS']}, indent=2))
    return 0 if receipt['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
