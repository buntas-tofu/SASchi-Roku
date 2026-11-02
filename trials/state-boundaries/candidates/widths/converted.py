"""Bounded translation of the two supplied DATA steps using decoded ASCII values."""

import csv
import math
from pathlib import Path
import sys

INPUT_COLUMNS = ("row_id", "raw", "suffix", "flag")
OUTPUT_COLUMNS = {
    "stage": ("row_id", "short", "joined", "tag"),
    "want": ("row_id", "short", "copy", "wrapped", "joined", "tag", "n", "z"),
    "descriptor": ("table", "column", "bytes"),
}
# These are compiled attributes of the supplied source, independent of rows.
WIDTHS = (
    ("stage", "short", 3), ("stage", "joined", 6), ("stage", "tag", 1),
    ("want", "short", 5), ("want", "copy", 2), ("want", "wrapped", 8),
    ("want", "joined", 6), ("want", "tag", 1),
)


def _text(value, name, width=None):
    if not isinstance(value, str) or any(not 32 <= ord(c) <= 126 for c in value):
        raise ValueError(f"{name} must be printable ASCII text")
    if width is not None and len(value) != width:
        raise ValueError(f"{name} must already contain exactly {width} bytes")
    if name == "row_id" and not value:
        raise ValueError("row_id must be nonempty")
    return value


def _fixed(value, width):
    """SAS character assignment: retain the left bytes, then blank-pad."""
    return value[:width].ljust(width, " ")


def translate(tables):
    """Return fresh stage, want and descriptor tables without changing inputs."""
    if not isinstance(tables, dict) or "have" not in tables:
        raise ValueError("tables must contain have")
    have = tables["have"]
    if not isinstance(have, list):
        raise ValueError("have must be a list of typed dictionaries")
    stage = []
    for row in have:
        if not isinstance(row, dict) or set(row) != set(INPUT_COLUMNS):
            raise ValueError("have rows must contain row_id, raw, suffix, flag")
        row_id = _text(row["row_id"], "row_id")
        raw = _text(row["raw"], "raw", 6)
        suffix = _text(row["suffix"], "suffix", 2)
        flag = row["flag"]
        if type(flag) not in (int, float) or not math.isfinite(flag) or flag not in (0, 1):
            raise ValueError("flag must be numeric 0 or 1")
        short = _fixed(raw, 3)
        joined = _fixed(short + suffix, 6)
        # The first source assignment is tag='Y', so both branches use width 1.
        tag = _fixed("Y" if flag else "LONG", 1)
        stage.append(dict(row_id=row_id, short=short, joined=joined, tag=tag))

    want = []
    for row in stage:
        # LENGTH precedes SET: stage's width 3 enters a width 5 target variable.
        short = _fixed(row["short"], 5)
        copy = _fixed(short, 2)
        short = _fixed(short + "!", 5)
        wrapped = _fixed("[" + short + "]", 8)
        z = len(short.rstrip(" "))
        want.append(dict(row_id=row["row_id"], short=short, copy=copy,
                         wrapped=wrapped, joined=row["joined"], tag=row["tag"],
                         n=max(1, z), z=z))
    descriptor = [dict(table=t, column=c, bytes=w) for t, c, w in WIDTHS]
    return {"stage": stage, "want": want, "descriptor": descriptor}


def _read_have(directory):
    path = Path(directory) / "have.csv"
    with path.open("r", encoding="ascii", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        if next(reader, None) != list(INPUT_COLUMNS):
            raise ValueError("have.csv has an incorrect header or column order")
        rows = []
        for cells in reader:
            if len(cells) != len(INPUT_COLUMNS):
                raise ValueError("have.csv has an incorrect field count")
            row = dict(zip(INPUT_COLUMNS, cells))
            if not row["flag"]:
                raise ValueError("flag cannot be missing")
            try:
                row["flag"] = float(row["flag"])
            except ValueError as error:
                raise ValueError("flag must be numeric 0 or 1") from error
            rows.append(row)
    return rows


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        raise ValueError("usage: python3 converted.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY")
    source, destination = args
    target = Path(destination)
    if target.exists() or target.is_symlink():
        raise FileExistsError("output destination already exists")
    result = translate({"have": _read_have(source)})
    target.mkdir()  # Exclusive creation also protects against an intervening creator.
    for name, columns in OUTPUT_COLUMNS.items():
        with (target / (name + ".csv")).open("w", encoding="ascii", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(result[name])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, csv.Error) as error:
        print(f"conversion failed: {error}", file=sys.stderr)
        raise SystemExit(1)
