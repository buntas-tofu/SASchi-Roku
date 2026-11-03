"""Isolated contract self-tests. Run from the frozen packet workspace."""
import copy
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import pyarrow as pa
import pyarrow.parquet as pq
import pyreadstat

ROOT = Path.cwd()
CONVERTER = Path(__file__).resolve().with_name('convert.py')
RUNTIME = '/tmp/roku-interchange-runtime/bin/Rscript'
passed = 0


def run(action, source, dest, catalog=None, ok=True):
    global passed
    command = [sys.executable, str(CONVERTER), action, str(source), str(dest)]
    if catalog:
        command += ['--catalog', str(catalog)]
    p = subprocess.run(command, capture_output=True, text=True)
    if (p.returncode == 0) != ok:
        raise AssertionError((command, p.returncode, p.stdout, p.stderr))
    passed += 1
    print(('PASS ' if ok else 'REJECT ') + ' '.join(command) + ' => ' + str(p.returncode) + ' ' + (p.stdout or p.stderr).strip())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(path):
    return {str(p.relative_to(path)): digest(p) for p in path.rglob('*') if p.is_file()}


def update_hash(path, file):
    m = json.loads((path / 'metadata.json').read_text())
    m['files'][file] = digest(path / file)
    (path / 'metadata.json').write_text(json.dumps(m))


with tempfile.TemporaryDirectory(prefix='selftest-', dir=ROOT) as scratch:
    tmp = Path(scratch)
    inputs = sorted((ROOT / 'packet/synthetic').glob('*.json'))
    outputs = []
    for i, source in enumerate(inputs):
        dest = tmp / ('case' + str(i))
        run('convert', source, dest)
        before = snapshot(dest)
        run('validate', source, dest)
        assert before == snapshot(dest)
        run('convert', source, dest, ok=False)
        assert before == snapshot(dest)
        e = json.loads(source.read_text())
        arc, ana = pq.read_table(dest / 'archive.parquet'), pq.read_table(dest / 'analysis.parquet')
        assert arc['__row_index'].to_pylist() == list(range(len(e['rows'])))
        assert ana['__row_index'].to_pylist() == list(range(len(e['rows'])))
        for c in e['columns']:
            name = c['name']
            if c['kind'] == 'character':
                assert arc[name].to_pylist() == [r[name]['hex'] for r in e['rows']]
                wanted = []
                for r in e['rows']:
                    b = bytes.fromhex(r[name]['hex'])
                    try:
                        text = b.decode(e['encoding'], errors='strict')
                        text = None if '\x00' in text else (text.rstrip(' ') or None)
                    except UnicodeDecodeError:
                        text = None
                    wanted.append(text)
                assert ana[name].to_pylist() == wanted
            else:
                assert arc[name + '__sas_missing'].to_pylist() == [r[name].get('missing', '') for r in e['rows']]
                assert arc[name].to_pylist() == [r[name].get('value') for r in e['rows']]
                wanted = []
                for r in e['rows']:
                    v = r[name].get('value')
                    if v is not None and c['logical'] == 'date':
                        v = date(1960, 1, 1) + timedelta(days=v)
                    elif v is not None and c['logical'] == 'datetime':
                        v = datetime(1960, 1, 1) + timedelta(seconds=v)
                    wanted.append(v)
                assert ana[name].to_pylist() == wanted
        outputs.append((source, dest, None))
    for source, cat in [(ROOT / 'packet/fixtures/sample.sas7bdat', None),
                        (ROOT / 'packet/fixtures/missing.sas7bdat', None),
                        (ROOT / 'packet/fixtures/missing.sas7bdat', ROOT / 'packet/fixtures/missing.sas7bcat')]:
        dest = tmp / ('sas' + str(len(outputs)))
        run('convert', source, dest, cat)
        run('validate', source, dest, cat)
        d, m = pyreadstat.read_sas7bdat(str(source), user_missing=True, disable_datetime_conversion=True, output_format='dict')
        arc = pq.read_table(dest / 'archive.parquet')
        meta = json.loads((dest / 'metadata.json').read_text())
        assert meta['character_fidelity'] == 'reader-utf8-reencoding'
        assert meta['source_encoding'] == m.file_encoding
        catalog_maps = {}
        if cat is not None:
            _, cm = pyreadstat.read_sas7bcat(str(cat))
            catalog_maps = cm.value_labels
        for c in meta['columns']:
            raw_labels = catalog_maps.get(m.variable_to_label.get(c['name']))
            wanted_labels = None if raw_labels is None else {('.' + k if isinstance(k, str) and k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_' else str(k)): v for k, v in raw_labels.items()}
            assert c['value_labels'] == wanted_labels
            assert c['format'] == m.original_variable_types[c['name']]
            assert c['width_bytes'] == m.variable_storage_width[c['name']]
            assert c['informat'] == m.original_variable_informats[c['name']]
            for i, v in enumerate(d[c['name']]):
                if c['kind'] == 'character':
                    assert arc[c['name']][i].as_py() == v.encode('utf-8').hex()
                else:
                    tag = '.' + v if isinstance(v, str) else '.' if v is None else ''
                    assert arc[c['name'] + '__sas_missing'][i].as_py() == tag
        for item in meta['source_files']:
            assert digest(dest / item['path']) == item['sha256']
        outputs.append((source, dest, cat))
    # Every single-byte CP1252 input and all canonical SAS missing tags.
    e = json.loads(inputs[2].read_text())
    char = copy.deepcopy(next(c for c in e['columns'] if c['kind'] == 'character'))
    num = copy.deepcopy(next(c for c in e['columns'] if c['logical'] == 'number'))
    char['width_bytes'] = 1
    e['columns'] = [char, num]
    tagset = ['.', '._'] + ['.' + chr(v) for v in range(65, 91)]
    e['rows'] = [{char['name']: {'hex': bytes([v]).hex()}, num['name']: {'missing': tagset[v % len(tagset)]}} for v in range(256)]
    matrix = tmp / 'byte-matrix.json'; matrix.write_text(json.dumps(e))
    matrix_out = tmp / 'byte-matrix-out'
    run('convert', matrix, matrix_out)
    run('validate', matrix, matrix_out)
    a = pq.read_table(matrix_out / 'archive.parquet')
    b = pq.read_table(matrix_out / 'analysis.parquet')
    assert a[char['name']].to_pylist() == [bytes([v]).hex() for v in range(256)]
    assert a[num['name'] + '__sas_missing'].to_pylist() == [tagset[v % len(tagset)] for v in range(256)]
    for v, value in enumerate(b[char['name']].to_pylist()):
        try:
            text = bytes([v]).decode('windows-1252', errors='strict')
            want = None if v == 0 else text.rstrip(' ') or None
        except UnicodeDecodeError:
            want = None
        assert value == want
    print('BYTE MATRIX PASS: 256 CP1252 byte cells; all 28 canonical missing tags')
    # Both JSON and binary sources remain supported after arbitrary renaming.
    for index in (2, 5):
        src, _, cat = outputs[index]
        renamed = tmp / ('renamed' + str(index) + '.opaque')
        shutil.copyfile(src, renamed)
        run('convert', renamed, tmp / ('renamed-out' + str(index)), cat)
    # R is a separate Parquet consumer; ReadStat is still a shared SAS reader.
    r_source = tmp / 'consumer.R'
    r_source.write_text('''args <- commandArgs(trailingOnly=TRUE)
library(arrow)
library(jsonlite)
for (d in args) {
 m <- fromJSON(file.path(d,"metadata.json"), simplifyVector=FALSE)
 a <- read_parquet(file.path(d,"archive.parquet"), as_data_frame=FALSE)
 b <- read_parquet(file.path(d,"analysis.parquet"), as_data_frame=FALSE)
 stopifnot(a$num_rows == m$row_count, b$num_rows == m$row_count)
 stopifnot(a$schema$GetFieldByName("__row_index")$type$ToString() == "int64")
 stopifnot(identical(a$schema$metadata[["saschi.mode"]], "archive"))
 stopifnot(identical(b$schema$metadata[["saschi.mode"]], "analysis"))
 for(c in m$columns) {
  stopifnot(a$schema$GetFieldByName(c$name)$type$ToString() == if(c$kind=="character") "string" else "double")
  want <- if(c$kind=="character") "string" else if(c$logical=="date") "date32[day]" else if(c$logical=="datetime") "timestamp[us]" else "double"
  stopifnot(b$schema$GetFieldByName(c$name)$type$ToString() == want)
 }
 cat("R consumer PASS", basename(d), "rows", a$num_rows, "\\n")
}
''')
    p = subprocess.run([RUNTIME, str(r_source)] + [str(d) for _, d, _ in outputs], capture_output=True, text=True)
    print('R COMMAND', RUNTIME, str(r_source), '[eight output directories] =>', p.returncode)
    print(p.stdout, p.stderr)
    assert p.returncode == 0
    source, baseline, cat = outputs[2]
    def attack(label, mutate, external=source, expected_catalog=cat):
        dest = tmp / ('attack-' + label)
        shutil.copytree(baseline, dest)
        mutate(dest)
        before = snapshot(dest)
        run('validate', external, dest, expected_catalog, ok=False)
        assert before == snapshot(dest)
    def edit_column(d, file, column, values):
        t = pq.read_table(d / file)
        idx = t.schema.get_field_index(column)
        t = t.set_column(idx, t.schema[idx], pa.array(values, type=t.schema[idx].type))
        pq.write_table(t, d / file)
        update_hash(d, file)
    analysis = pq.read_table(baseline / 'analysis.parquet')
    archive = pq.read_table(baseline / 'archive.parquet')
    number = next(c['name'] for c in json.loads(source.read_text())['columns'] if c['logical'] == 'number')
    numeric = analysis[number].to_pylist(); numeric[0] += 1
    attack('changed-rehashed', lambda d: edit_column(d, 'analysis.parquet', number, numeric))
    tagname = number + '__sas_missing'; tags = archive[tagname].to_pylist(); tags = ['.' if t else '' for t in tags]
    attack('tags-rehashed', lambda d: edit_column(d, 'archive.parquet', tagname, tags))
    datecol = next(c['name'] for c in json.loads(source.read_text())['columns'] if c['logical'] == 'date')
    dates = analysis[datecol].to_pylist(); dates[0] += timedelta(days=3653)
    attack('date-rehashed', lambda d: edit_column(d, 'analysis.parquet', datecol, dates))
    def reverse(d):
        t = pq.read_table(d / 'analysis.parquet').take(list(reversed(range(analysis.num_rows))))
        pq.write_table(t, d / 'analysis.parquet'); update_hash(d, 'analysis.parquet')
    attack('reordered-rehashed', reverse)
    attack('corrupt', lambda d: (d / 'archive.parquet').write_bytes(b'corrupt'))
    attack('source-copy', lambda d: (d / 'source' / source.name).write_bytes(b'changed'))
    attack('wrong-external', lambda d: None, external=outputs[3][0])
    attack('swapped-sidecar', lambda d: shutil.copyfile(outputs[0][1] / 'metadata.json', d / 'metadata.json'))
    def edit_metadata(d):
        path = d / 'metadata.json'; m = json.loads(path.read_text()); m['columns'][0]['label'] = 'stale'; path.write_text(json.dumps(m))
    attack('stale-descriptor', edit_metadata)
    def edit_events(d):
        path = d / 'metadata.json'; m = json.loads(path.read_text()); m['events'] = []; path.write_text(json.dumps(m))
    attack('missing-events', edit_events)
    def edit_binding(d):
        path = d / 'analysis.parquet'; t = pq.read_table(path); meta = t.schema.metadata.copy(); meta[b'saschi.source_sha256'] = b'0' * 64
        pq.write_table(t.replace_schema_metadata(meta), path); update_hash(d, 'analysis.parquet')
    attack('schema-binding', edit_binding)
    # Catalog omission or substitution changes the associated contract.
    src, dest, supplied_cat = outputs[-1]
    run('validate', src, dest, ok=False)
    wrong_catalog = tmp / 'wrong-catalog'; wrong_catalog.write_bytes(b'not a catalog')
    run('validate', src, dest, wrong_catalog, ok=False)
    # Invalid admitted envelopes must fail before creating a destination.
    envelope = json.loads(source.read_text())
    invalids = {}
    e = copy.deepcopy(envelope); e['columns'][0]['name'] = '__row_index'; invalids['reserved'] = e
    e = copy.deepcopy(envelope); e['columns'][0]['name'] += '__sas_missing'; invalids['suffix'] = e
    e = copy.deepcopy(envelope); e['columns'][1]['name'] = e['columns'][0]['name']; invalids['duplicate'] = e
    e = copy.deepcopy(envelope); e['rows'][0][e['columns'][0]['name']]['hex'] = 'FF'; invalids['uppercase-hex'] = e
    e = copy.deepcopy(envelope); e['rows'][0][e['columns'][0]['name']]['hex'] = '0'; invalids['odd-hex'] = e
    e = copy.deepcopy(envelope); e['rows'][0][e['columns'][0]['name']]['hex'] = '00'; invalids['width'] = e
    e = copy.deepcopy(envelope); e['rows'][0][number] = {'missing': '.a'}; invalids['bad-tag'] = e
    e = copy.deepcopy(envelope); e['rows'][0][number] = {'value': True}; invalids['boolean'] = e
    e = copy.deepcopy(envelope); e['rows'][0][number] = {'value': 1, 'missing': '.'}; invalids['ambiguous'] = e
    e = copy.deepcopy(envelope); e['rows'][0][datecol] = {'value': 0.5}; invalids['fractional-date'] = e
    e = copy.deepcopy(envelope); e['encoding'] = 'nonexistent-codec'; invalids['codec'] = e
    for label, e in invalids.items():
        path = tmp / ('bad-' + label + '.json'); path.write_text(json.dumps(e)); dest = tmp / ('bad-out-' + label)
        run('convert', path, dest, ok=False)
        assert not dest.exists()
print('SELFTEST COMPLETE:', passed, 'CLI assertions; 8 R-consumed projections pairs; temporary artifacts removed')
