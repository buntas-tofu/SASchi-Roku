"""Translate the supplied two DATA steps using Python's standard library."""

from collections import OrderedDict
import csv
import math
import os
from pathlib import Path
import sys

INPUT_COLUMNS = ["row_id", "value", "eligible"]
OUTPUT_COLUMNS = ["row_id", "value", "prev", "total"]


def _validate_rows(rows):
    if not isinstance(rows, list):
        raise TypeError("rows must be a list of typed dictionaries")
    normalized = []
    for position, row in enumerate(rows, 1):
        if not isinstance(row, dict) or set(row) != set(INPUT_COLUMNS):
            raise ValueError(f"row {position}: expected row_id, value and eligible")
        identifier = row["row_id"]
        if (not isinstance(identifier, str) or not identifier
                or any(ord(char) < 32 or ord(char) > 126 for char in identifier)):
            raise ValueError(f"row {position}: row_id must be nonempty printable ASCII")
        value = row["value"]
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"row {position}: value must be numeric or None")
            value = float(value)
            if not math.isfinite(value):
                raise ValueError(f"row {position}: value must be finite or None")
        eligible = row["eligible"]
        if type(eligible) is not int or eligible not in (0, 1):
            raise ValueError(f"row {position}: eligible must be integer 0 or 1")
        normalized.append({"row_id": identifier, "value": value, "eligible": eligible})
    return normalized


def _add_to_total(total, value):
    # A SAS sum statement ignores a missing operand; both missing remain missing.
    if value is None:
        return total
    if total is None:
        return value
    result = total + value
    return result if math.isfinite(result) else None


def _step(rows, filter_before):
    queue = None
    total = 10.0
    output = []
    for row in rows:
        if filter_before and row["eligible"] != 1:
            continue
        value = row["value"]
        prev = queue
        queue = value
        total = _add_to_total(total, value)
        if row["eligible"] == 1:
            output.append({"row_id": row["row_id"], "value": value,
                           "prev": prev, "total": total})
    return output


def translate(rows):
    """Return where_path and if_path in order, with fresh independent state."""
    normalized = _validate_rows(rows)
    return OrderedDict([
        ("where_path", _step(normalized, filter_before=True)),
        ("if_path", _step(normalized, filter_before=False)),
    ])


def _read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != INPUT_COLUMNS:
            raise ValueError("CSV header must be row_id,value,eligible in that order")
        rows = []
        for position, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"CSV record {position}: expected exactly three fields")
            if row["eligible"] not in ("0", "1"):
                raise ValueError(f"CSV record {position}: eligible must be 0 or 1")
            rows.append({"row_id": row["row_id"],
                         "value": None if row["value"] == "" else float(row["value"]),
                         "eligible": int(row["eligible"])})
        return rows


def _write_csv(path, rows):
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("Usage: python3 converted.py INPUT_CSV NEW_OUTPUT_DIRECTORY", file=sys.stderr)
        return 2
    source, destination = args
    try:
        if os.path.lexists(destination):
            raise FileExistsError("output destination already exists")
        outputs = translate(_read_csv(source))
        folder = Path(destination)
        folder.mkdir(exist_ok=False)
        for name, rows in outputs.items():
            _write_csv(folder / (name + ".csv"), rows)
    except (OSError, ValueError, TypeError, OverflowError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
