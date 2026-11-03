#!/usr/bin/env python3
"""Bounded SAS/envelope interchange; retained source is the raw-byte boundary."""
import argparse
import codecs
import copy
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import shutil
import sys
from decimal import Decimal, ROUND_HALF_EVEN

import pyarrow as pa
import pyarrow.parquet as pq
import pyreadstat

FIELDS = ('name', 'kind', 'logical', 'width_bytes', 'label', 'format', 'informat',
          'origin', 'units', 'timezone', 'value_labels')
TAGS = {'.', '._'} | {'.' + chr(n) for n in range(65, 91)}
DAY_OFFSET = -3653
SECOND_OFFSET = -315619200


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def read_json(path):
    with Path(path).open(encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=unique_object,
                         parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON: ' + x)))


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_columns(columns):
    require(isinstance(columns, list), 'columns must be an ordered array')
    names = []
    for c in columns:
        require(isinstance(c, dict) and set(FIELDS) <= set(c), 'incomplete descriptor')
        n = c['name']
        require(isinstance(n, str) and n and '\x00' not in n, 'invalid column name')
        require(n != '__row_index' and not n.endswith('__sas_missing'), 'reserved column name: ' + n)
        require(n not in names, 'duplicate column name: ' + n)
        names.append(n)
        require(c['kind'] in ('character', 'numeric'), 'unknown storage kind')
        require(c['logical'] in (('text',) if c['kind'] == 'character' else ('number', 'date', 'datetime', 'time')), 'unsupported logical kind')
        require(c['width_bytes'] is None or (type(c['width_bytes']) is int and c['width_bytes'] > 0), 'invalid source width')
        for key in ('label', 'format', 'informat', 'origin', 'units'):
            require(c[key] is None or isinstance(c[key], str), 'invalid descriptor ' + key)
        require(c['timezone'] is None, 'only timezone-unknown inputs are admitted')
        require(c['value_labels'] is None or (isinstance(c['value_labels'], dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in c['value_labels'].items())), 'invalid value labels')
        if c['logical'] == 'date':
            require(c['origin'] == '1960-01-01' and c['units'] == 'days', 'date origin/units mismatch')
        if c['logical'] == 'datetime':
            require(c['origin'] == '1960-01-01T00:00:00' and c['units'] == 'seconds', 'datetime origin/units mismatch')
        if c['logical'] == 'time':
            require(c['units'] == 'seconds', 'time units mismatch')
    return names


def read_envelope(path, catalog):
    require(catalog is None, 'catalog option requires SAS input')
    e = read_json(path)
    require(isinstance(e, dict) and type(e.get('version')) is int and e['version'] == 1, 'unsupported envelope version')
    require(isinstance(e.get('encoding'), str), 'missing declared encoding')
    codecs.lookup(e['encoding'])
    require(e.get('timezone') is None and e.get('catalog') is None, 'unsupported envelope timezone/catalog')
    cols = copy.deepcopy(e['columns'])
    names = validate_columns(cols)
    require(all(c['width_bytes'] is not None for c in cols), 'envelope requires declared widths')
    rows = e.get('rows')
    require(isinstance(rows, list), 'rows must be an array')
    for row in rows:
        require(isinstance(row, dict) and set(row) == set(names), 'row does not match descriptor')
        for c in cols:
            cell = row[c['name']]
            require(isinstance(cell, dict), 'cell must be an object')
            if c['kind'] == 'character':
                require(set(cell) == {'hex'} and isinstance(cell['hex'], str), 'character requires hex')
                require(re.fullmatch(r'(?:[0-9a-f]{2})*', cell['hex']) is not None, 'hex must be lowercase byte pairs')
                require(len(cell['hex']) == c['width_bytes'] * 2, 'physical byte width mismatch')
            elif set(cell) == {'missing'}:
                require(isinstance(cell['missing'], str) and cell['missing'] in TAGS, 'invalid SAS missing marker')
            else:
                require(set(cell) == {'value'} and finite(cell.get('value')), 'numeric requires finite value or canonical missing')
    return cols, rows, e['encoding'], e.get('dataset_label'), []


def logical_format(fmt):
    """Explicit bounded SAS display-format profile; custom formats remain numeric."""
    name = (fmt or '').upper().rstrip('.')
    if re.fullmatch(r'(?:DATE|YYMMDD)(?:\d+)?', name):
        return 'date'
    if re.fullmatch(r'DATETIME(?:\d+(?:\.\d+)?)?', name):
        return 'datetime'
    if re.fullmatch(r'TIME(?:\d+(?:\.\d+)?)?', name):
        return 'time'
    return 'number'


def label_key(value):
    if isinstance(value, str) and value in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_':
        return '.' + value
    if isinstance(value, str) and value in TAGS:
        return value
    if isinstance(value, (float, int)):
        return str(int(value)) if float(value).is_integer() else str(value)
    return str(value)


def read_sas(path, catalog):
    # A catalog passed to read_sas7bdat replaces codes with labels. Read separately.
    data, m = pyreadstat.read_sas7bdat(str(path), user_missing=True,
        disable_datetime_conversion=True, output_format='dict')
    catalog_labels = {}
    if catalog is not None:
        _, cm = pyreadstat.read_sas7bcat(str(catalog), output_format='dict')
        catalog_labels = cm.value_labels
    columns = []
    for name in m.column_names:
        kind = 'character' if m.readstat_variable_types[name] == 'string' else 'numeric'
        fmt = m.original_variable_types.get(name)
        logical = 'text' if kind == 'character' else logical_format(fmt)
        labels = catalog_labels.get(m.variable_to_label.get(name))
        c = dict(name=name, kind=kind, logical=logical,
            width_bytes=m.variable_storage_width.get(name),
            label=m.column_names_to_labels.get(name), format=fmt,
            informat=getattr(m, 'original_variable_informats', {}).get(name),
            origin={'date': '1960-01-01', 'datetime': '1960-01-01T00:00:00'}.get(logical),
            units={'date': 'days', 'datetime': 'seconds', 'time': 'seconds'}.get(logical),
            timezone=None,
            value_labels=None if labels is None else {label_key(k): v for k, v in labels.items()})
        columns.append(c)
    validate_columns(columns)
    n = len(data[m.column_names[0]]) if m.column_names else int(m.number_rows or 0)
    rows = []
    for i in range(n):
        row = {}
        for c in columns:
            name = c['name']
            value = data[name][i]
            if c['kind'] == 'character':
                require(isinstance(value, str), 'reader returned non-text character cell')
                row[name] = {'hex': value.encode('utf-8', errors='strict').hex()}
            elif isinstance(value, str):
                require(value in m.missing_user_values.get(name, []) and '.' + value in TAGS, 'unrecognized reader missing tag')
                row[name] = {'missing': '.' + value}
            elif value is None or math.isnan(float(value)):
                row[name] = {'missing': '.'}
            else:
                require(math.isfinite(float(value)), 'nonfinite reader numeric value')
                row[name] = {'value': float(value)}
        rows.append(row)
    gaps = ['Original SAS character bytes and padding are not exposed by this reader; retained source supplies them.',
            'Timezone is unavailable and is not inferred from display formats.',
            'Formats outside DATE, YYMMDD, DATETIME and TIME stay numeric.',
            'Descriptor fields absent from reader metadata stay null; no original-SAS rewrite is claimed.']
    return columns, rows, m.file_encoding, m.file_label, gaps


def normalize(raw, encoding):
    if b'\x00' in raw:
        return None, 'embedded-nul'
    try:
        value = raw.decode(encoding, errors='strict')
    except UnicodeDecodeError:
        return None, 'decode-error'
    if '\x00' in value:
        return None, 'embedded-nul'
    trimmed = value.rstrip(' ')
    if not trimmed:
        return None, 'blank-to-null'
    return trimmed, 'right-trim' if trimmed != value else None


def projection(columns, rows, codec, binding, mode):
    arrays = [pa.array(range(len(rows)), type=pa.int64())]
    names = ['__row_index']
    events = []
    for c in columns:
        name = c['name']
        values, tags = [], []
        logical = c['logical']
        typ = pa.string() if c['kind'] == 'character' else pa.float64()
        if mode == 'analysis' and logical == 'date':
            typ = pa.date32()
        if mode == 'analysis' and logical == 'datetime':
            typ = pa.timestamp('us')
        for i, row in enumerate(rows):
            cell = row[name]
            action = None
            tag = None
            if c['kind'] == 'character':
                if mode == 'archive':
                    value = cell['hex']
                else:
                    value, action = normalize(bytes.fromhex(cell['hex']), codec)
            elif 'missing' in cell:
                value = None
                tag = cell['missing']
                tags.append(tag)
                if mode == 'analysis':
                    action = 'missing-to-null'
            else:
                value = float(cell['value'])
                tags.append('')
                if mode == 'analysis' and logical == 'date':
                    require(value.is_integer(), 'fractional SAS date cannot be represented exactly as date32')
                    value = int(value) + DAY_OFFSET
                    require(-(2**31) <= value < 2**31, 'date32 overflow')
                    action = 'date-to-date32'
                elif mode == 'analysis' and logical == 'datetime':
                    # Round once to microseconds, then add the exact epoch offset.
                    value = int((Decimal(str(value)) * 1000000).to_integral_value(rounding=ROUND_HALF_EVEN)) + SECOND_OFFSET * 1000000
                    require(-(2**63) <= value < 2**63, 'timestamp overflow')
                    action = 'datetime-to-timestamp-us'
            values.append(value)
            if action is not None:
                event = {'row': i, 'column': name, 'action': action}
                if tag is not None:
                    event['tag'] = tag
                events.append(event)
        arrays.append(pa.array(values, type=typ))
        names.append(name)
        if mode == 'archive' and c['kind'] == 'numeric':
            arrays.append(pa.array(tags, type=pa.string()))
            names.append(name + '__sas_missing')
    order = {c['name']: i for i, c in enumerate(columns)}
    events.sort(key=lambda e: (e['row'], order[e['column']]))
    meta = {('saschi.' + k).encode(): str(v).encode() for k, v in dict(binding, mode=mode, schema_version='1').items()}
    return pa.Table.from_arrays(arrays, names=names).replace_schema_metadata(meta), events


def prepare(input_path, catalog):
    input_path = Path(input_path)
    catalog = Path(catalog) if catalog else None
    require(input_path.is_file(), 'input is not a file')
    require(catalog is None or catalog.is_file(), 'catalog is not a file')
    with input_path.open('rb') as stream:
        prefix = stream.read(4096).lstrip()
    sas = not prefix.startswith((b'{', b'['))
    if sas:
        columns, rows, encoding, label, gaps = read_sas(input_path, catalog)
    else:
        columns, rows, encoding, label, gaps = read_envelope(input_path, catalog)
    retained = [('data', input_path)]
    if catalog is not None:
        retained.append(('catalog', catalog))
    license_path = input_path.parent / 'LICENSE'
    if license_path.is_file() and license_path != input_path:
        retained.append(('license', license_path))
    require(len({p.name for _, p in retained}) == len(retained), 'retained source basename collision')
    sources = [{'role': role, 'path': 'source/' + p.name, 'sha256': sha(p)} for role, p in retained]
    binding = {'source_sha256': sources[0]['sha256'], 'catalog_sha256': '' if catalog is None else sha(catalog)}
    codec = 'utf-8' if sas else encoding
    archive, _ = projection(columns, rows, codec, binding, 'archive')
    analysis, events = projection(columns, rows, codec, binding, 'analysis')
    meta = dict(schema_version=1, source_format='sas7bdat' if sas else 'envelope',
        row_count=len(rows), source_files=sources, source_encoding=encoding,
        character_fidelity='reader-utf8-reencoding' if sas else 'exact-envelope-bytes',
        catalog_status='provided' if catalog else 'absent', timezone=None,
        columns=columns, events=events, files={},
        libraries={'python': platform.python_version(), 'pyarrow': pa.__version__, 'pyreadstat': pyreadstat.__version__},
        dataset_label=label, metadata_gaps=gaps,
        datetime_precision='nearest microsecond, decimal rendering of reader float, half-even ties',
        logical_format_profile='DATE/YYMMDD with optional width; DATETIME/TIME with optional width and decimal precision; case-insensitive')
    return archive, analysis, meta, retained


def validate(input_path, destination, catalog=None):
    archive, analysis, expected, retained = prepare(input_path, catalog)
    dest = Path(destination)
    require(dest.is_dir() and not dest.is_symlink(), 'output is not a real directory')
    actual = read_json(dest / 'metadata.json')
    for name, table in [('archive.parquet', archive), ('analysis.parquet', analysis)]:
        path = dest / name
        require(path.is_file() and not path.is_symlink(), 'missing or linked projection: ' + name)
        expected['files'][name] = sha(path)
        reopened = pq.read_table(path)
        require(reopened.schema.equals(table.schema, check_metadata=True), 'schema or binding mismatch: ' + name)
        require(reopened.equals(table, check_metadata=True), 'complete typed value mismatch: ' + name)
        # Arrow equality treats signed zero as equal. Compare finite float payloads too.
        for field in table.schema:
            if pa.types.is_float64(field.type):
                import struct
                for a, b in zip(table[field.name].to_pylist(), reopened[field.name].to_pylist()):
                    require(a is None and b is None or a is not None and b is not None and struct.pack('>d', a) == struct.pack('>d', b), 'float64 payload mismatch')
    require(json.dumps(actual, sort_keys=True, ensure_ascii=True) == json.dumps(expected, sort_keys=True, ensure_ascii=True),
            'metadata disagrees with source-derived contract or output identity')
    for item, (_, source) in zip(expected['source_files'], retained):
        path = dest / item['path']
        require(path.is_file() and not path.is_symlink(), 'retained source absent or linked')
        require(sha(path) == item['sha256'], 'retained source bytes changed')
    return expected['row_count']


def convert(input_path, destination, catalog=None):
    dest = Path(destination)
    require(not dest.exists() and not dest.is_symlink(), 'destination already exists')
    archive, analysis, meta, retained = prepare(input_path, catalog)
    dest.mkdir(parents=False, exist_ok=False)
    try:
        (dest / 'source').mkdir()
        for item, (_, source) in zip(meta['source_files'], retained):
            target = dest / item['path']
            shutil.copyfile(source, target)
            require(sha(target) == item['sha256'], 'source changed during conversion')
        for name, table in [('archive.parquet', archive), ('analysis.parquet', analysis)]:
            pq.write_table(table, dest / name, version='2.6', compression='snappy')
            meta['files'][name] = sha(dest / name)
        (dest / 'metadata.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        validate(input_path, dest, catalog)
    except BaseException:
        shutil.rmtree(dest)
        raise
    return meta['row_count']


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['convert', 'validate'])
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--catalog')
    args = p.parse_args()
    try:
        count = (convert if args.action == 'convert' else validate)(args.input, args.output, args.catalog)
    except Exception as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1
    print(f'{args.action}: complete source-derived check, {count} rows')
    return 0


if __name__ == '__main__':
    sys.exit(main())
