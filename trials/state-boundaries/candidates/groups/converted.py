"""Bounded translation of the supplied BY-group DATA step."""
import csv
import math
from pathlib import Path
import sys

INPUT_COLUMNS = ('row_id', 'region', 'account', 'value')
OUTPUT_COLUMNS = INPUT_COLUMNS + (
    'raw_prev', 'prev', 'total', 'first_region', 'last_region',
    'first_account', 'last_account',
)


def _number(value, name, integer=False):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be numeric or None')
    value = float(value)
    if not math.isfinite(value) or (integer and not value.is_integer()):
        raise ValueError(f'{name} must be a finite {"integer" if integer else "number"}')
    return value


def _key(value):
    return (0, 0) if value is None else (1, value)


def translate(tables):
    """Return fresh output rows; reject inputs outside the stated contract."""
    if not isinstance(tables, dict) or 'have' not in tables or not isinstance(tables['have'], list):
        raise ValueError('tables must contain have as a list')
    rows = []
    prior_key = None
    for i, row in enumerate(tables['have'], 1):
        if not isinstance(row, dict) or set(row) != set(INPUT_COLUMNS):
            raise ValueError(f'row {i}: incorrect input schema')
        row_id = row['row_id']
        if not isinstance(row_id, str) or not row_id or any(ord(ch) < 32 or ord(ch) > 126 for ch in row_id):
            raise ValueError(f'row {i}: row_id must be nonempty printable ASCII')
        item = {'row_id': row_id}
        for column in INPUT_COLUMNS[1:]:
            item[column] = _number(row[column], column, integer=column != 'value')
        key = (_key(item['region']), _key(item['account']))
        if prior_key is not None and key < prior_key:
            raise ValueError(f'row {i}: input is not sorted by region, account')
        prior_key = key
        rows.append(item)

    out = []
    queue = None
    total = 0.0
    for i, row in enumerate(rows):
        previous = rows[i - 1] if i else None
        following = rows[i + 1] if i + 1 < len(rows) else None
        fr = int(previous is None or previous['region'] != row['region'])
        lr = int(following is None or following['region'] != row['region'])
        fa = int(fr or previous['account'] != row['account'])
        la = int(lr or following['account'] != row['account'])
        raw_prev = queue
        queue = row['value']
        prev = None if fa else raw_prev
        if fr:
            total = 100.0
        if total is not None or row['value'] is not None:
            total = (0.0 if total is None else total) + (0.0 if row['value'] is None else row['value'])
            if not math.isfinite(total):
                total = None
        values = [row[c] for c in INPUT_COLUMNS] + [raw_prev, prev, total, fr, lr, fa, la]
        out.append(dict(zip(OUTPUT_COLUMNS, values)))
    return {'want': out}


def _read_input(directory):
    with (Path(directory) / 'have.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream, strict=True)
        if tuple(reader.fieldnames or ()) != INPUT_COLUMNS:
            raise ValueError('have.csv has incorrect headers')
        rows = []
        for row in reader:
            if set(row) != set(INPUT_COLUMNS) or any(v is None for v in row.values()):
                raise ValueError('have.csv has an incorrect field count')
            for key in INPUT_COLUMNS[1:]:
                row[key] = None if row[key] == '' else float(row[key])
            rows.append(row)
    return {'have': rows}


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        raise ValueError('usage: converted.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY')
    source, target = args
    destination = Path(target)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('destination already exists')
    result = translate(_read_input(source))
    destination.mkdir()
    with (destination / 'want.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(result['want'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, csv.Error, OverflowError) as error:
        raise SystemExit(str(error))
