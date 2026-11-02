"""Hand-derived bounded witnesses, not captured SAS output."""

import contextlib
from copy import deepcopy
import csv
import importlib.util
import io
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
EVIDENCE = OUT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
COLUMNS = ["row_id", "value", "prev", "prev2", "change"]

# Literal expected tables were derived from the supplied source and SAS docs.
EXPECTED = {
    "main": [
        ["l7", 12.0, None, None, None],
        ["l2", 18.0, 12.0, None, 6.0],
        ["l9", 15.0, 18.0, 12.0, -3.0],
        ["l1", 9.0, 15.0, 18.0, -6.0],
    ],
    "edge": [
        ["e9", 5.0, None, None, None],
        ["e2", None, 5.0, None, None],
        ["e7", -2.0, None, 5.0, None],
        ["e4", 0.0, -2.0, None, 2.0],
    ],
    "single": [["s1", -3.0, None, None, None]],
    "empty": [],
}


def check(actual, expected):
    assert len(actual) == len(expected), (actual, expected)
    for got, want in zip(actual, expected):
        assert list(got) == COLUMNS, got
        assert list(got.values()) == want, (got, want)
        assert isinstance(got["row_id"], str)
        assert all(v is None or type(v) is float for v in list(got.values())[1:])


spec = importlib.util.spec_from_file_location("converted", OUT / "converted.py")
module = importlib.util.module_from_spec(spec)
captured = io.StringIO()
with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
    spec.loader.exec_module(module)
assert captured.getvalue() == ""
print("PASS import: no CLI execution or output")

for name, expected in EXPECTED.items():
    source = ROOT / "packet" / (name + ".csv")
    with source.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    before = deepcopy(rows)
    result = module.translate(rows)
    check(result, expected)
    assert rows == before
    assert result is not rows
    assert all(a is not b for a, b in zip(rows, result))
    check(module.translate(rows), expected)
    destination = EVIDENCE / (name + ".csv")
    run = subprocess.run([sys.executable, str(OUT / "converted.py"), str(source), str(destination)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert run.stdout == "" and run.stderr == ""
    with destination.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == COLUMNS
        cli_rows = list(reader)
    normalized = []
    for row in cli_rows:
        normalized.append({key: value if key == "row_id" else None if value == "" else float(value) for key, value in row.items()})
    check(normalized, expected)
    print(f"PASS {name}: API, CLI, exact table, fresh calls, input unchanged ({len(expected)} rows)")

# Numeric API input and multiple missing values.
rows = [{"row_id": key, "value": value} for key, value in zip(["a", "b", "c", "d", "e"], [None, -0.5, 1.25, None, None])]
check(module.translate(rows), [
    ["a", None, None, None, None],
    ["b", -0.5, None, None, None],
    ["c", 1.25, -0.5, None, 1.75],
    ["d", None, 1.25, -0.5, None],
    ["e", None, None, 1.25, None],
])
print("PASS typed API: leading and consecutive missing values, exact binary fractions (5 rows)")

# All keys fit within 8 UTF-8 bytes, without normalization or trimming.
keys = [' A ', 'é中', 'x,"y', 'a\nb', 'a\r\nb']
character_source = EVIDENCE / "character-input.csv"
character_output = EVIDENCE / "character-output.csv"
with character_source.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["row_id", "value"])
    writer.writerows((key, i + 1) for i, key in enumerate(keys))
subprocess.run([sys.executable, str(OUT / "converted.py"), str(character_source), str(character_output)], check=True)
with character_output.open(encoding="utf-8", newline="") as stream:
    out_keys = [row["row_id"] for row in csv.DictReader(stream)]
assert [key.encode("utf-8") for key in out_keys] == [key.encode("utf-8") for key in keys]
print("PASS UTF-8 character field byte round-trip: spaces, non-ASCII, quotes, commas, LF, CRLF (5 rows)")

# Negative control: wrongly do not enqueue missing inputs.
def wrong_skip_missing(rows):
    history = []
    out = []
    for row in rows:
        value = float(row["value"]) if row["value"] else None
        prev = history[-1] if history else None
        prev2 = history[-2] if len(history) > 1 else None
        out.append(dict(zip(COLUMNS, [row["row_id"], value, prev, prev2, None if value is None or prev is None else value - prev])))
        if value is not None:
            history.append(value)
    return out

with (ROOT / "packet" / "edge.csv").open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
try:
    check(wrong_skip_missing(rows), EXPECTED["edge"])
except AssertionError as failure:
    (EVIDENCE / "negative-control.txt").write_text(str(failure) + "\n", encoding="utf-8")
    print("PASS negative control: comparator rejected missing-skipping lag variant; mismatch retained")
else:
    raise AssertionError("negative control incorrectly accepted")

print("ALL SELF-TESTS PASSED; no live SAS comparison")
