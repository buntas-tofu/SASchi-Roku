"""Candidate translation of packet/source.sas; live SAS execution is pending."""

import csv
import math
import os
from pathlib import Path
import re
import sys

INPUT_COLUMNS = {
    "left": ("key", "left_seq", "a", "shared"),
    "right": ("key", "right_seq", "b", "shared"),
}
OUTPUT_COLUMNS = (
    "key", "left_seq", "right_seq", "a", "b", "shared",
    "from_left", "from_right",
)
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


def _key(value):
    return (0, 0) if value is None else (1, value)


def _validate(tables):
    if not isinstance(tables, dict) or set(tables) != set(INPUT_COLUMNS):
        raise ValueError("Expected exactly the left and right input tables")
    for name, columns in INPUT_COLUMNS.items():
        rows = tables[name]
        if not isinstance(rows, list):
            raise TypeError(name + " must be a list of dictionaries")
        previous = None
        for i, row in enumerate(rows):
            if not isinstance(row, dict) or set(row) != set(columns):
                raise ValueError(f"{name} row {i + 1}: incorrect columns")
            for column in columns:
                value = row[column]
                if value is not None:
                    if isinstance(value, bool) or not isinstance(value, (int, float)):
                        raise TypeError(f"{name} row {i + 1}: {column} must be numeric or None")
                    try:
                        finite = math.isfinite(value)
                    except OverflowError:
                        finite = False
                    if not finite:
                        raise ValueError(f"{name} row {i + 1}: nonfinite {column}")
                    if column == "key" and value != math.floor(value):
                        raise ValueError(f"{name} row {i + 1}: key must be an integer")
            current = _key(row["key"])
            if previous is not None and current < previous:
                raise ValueError(f"{name} is not sorted at row {i + 1}")
            previous = current


def translate(tables):
    """Merge ordered numeric tables without changing the caller's objects."""
    _validate(tables)
    left, right = tables["left"], tables["right"]
    li = ri = 0
    result = []
    while li < len(left) or ri < len(right):
        if ri == len(right) or (
            li < len(left) and _key(left[li]["key"]) <= _key(right[ri]["key"])
        ):
            group = left[li]["key"]
        else:
            group = right[ri]["key"]
        pdv = dict.fromkeys(OUTPUT_COLUMNS)
        pdv["from_left"] = pdv["from_right"] = 0
        while True:
            read_left = li < len(left) and left[li]["key"] == group
            read_right = ri < len(right) and right[ri]["key"] == group
            if not (read_left or read_right):
                break
            # Only a new observation writes its columns. MERGE reads left first.
            if read_left:
                pdv.update(left[li])
                pdv["from_left"] = 1
                li += 1
            if read_right:
                pdv.update(right[ri])
                pdv["from_right"] = 1
                ri += 1
            result.append(pdv.copy())
    return {"want": result}


def _parse_number(text, location):
    if text == "":
        return None
    if NUMBER.fullmatch(text.strip()) is None:
        raise ValueError(location + ": invalid numeric CSV field")
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(location + ": nonfinite numeric CSV field")
    return value


def read_tables(directory):
    tables = {}
    for name, columns in INPUT_COLUMNS.items():
        with (Path(directory) / (name + ".csv")).open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            if next(reader, None) != list(columns):
                raise ValueError(name + ": incorrect CSV header")
            rows = []
            for line, cells in enumerate(reader, 2):
                if not cells:
                    continue
                if len(cells) != len(columns):
                    raise ValueError(f"{name} line {line}: incorrect field count")
                rows.append({column: _parse_number(cell, f"{name}:{line}:{column}")
                             for column, cell in zip(columns, cells)})
            tables[name] = rows
    return tables


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        raise ValueError("Usage: python3 converted.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY")
    source, destination = args
    if os.path.lexists(destination):
        raise FileExistsError("Destination already exists: " + destination)
    result = translate(read_tables(source))
    Path(destination).mkdir()
    with (Path(destination) / "want.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result["want"])


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
