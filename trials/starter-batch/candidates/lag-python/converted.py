"""Bounded translation of packet/source.sas, using None for numeric missing."""

from __future__ import annotations

import argparse
from collections import deque
import csv
import math
from pathlib import Path


COLUMNS = ("row_id", "value", "prev", "prev2", "change")


def _numeric(value: object) -> float | None:
    """Accept finite numbers, numeric CSV text, or ordinary missing values."""
    if value is None or isinstance(value, str) and not value.strip():
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise TypeError("value must be numeric, numeric text, or missing")
    if isinstance(value, float) and math.isnan(value):
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("numeric input must be finite or ordinary missing")
    return result


def translate(rows: list[dict]) -> list[dict]:
    """Return new rows in source order with independent fresh LAG queues.

    Numeric results are floats or None. Numeric text is accepted for direct
    interoperability with csv.DictReader. Character keys are copied unchanged.
    """
    lag1 = deque([None])
    lag2 = deque([None, None])
    result = []
    for row in rows:
        row_id = row["row_id"]
        if not isinstance(row_id, str):
            raise TypeError("row_id must be a string")
        value = _numeric(row["value"])
        prev = lag1.popleft()
        lag1.append(value)
        prev2 = lag2.popleft()
        lag2.append(value)
        change = None if value is None or prev is None else value - prev
        if change is not None and not math.isfinite(change):
            change = None
        result.append({
            "row_id": row_id,
            "value": value,
            "prev": prev,
            "prev2": prev2,
            "change": change,
        })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    with args.input_csv.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["row_id", "value"]:
            raise ValueError("input header must be row_id,value")
        rows = list(reader)
        if any(None in row or row["value"] is None for row in rows):
            raise ValueError("each input row must contain exactly two cells")
    converted = translate(rows)
    with args.output_csv.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(converted)


if __name__ == "__main__":
    main()
