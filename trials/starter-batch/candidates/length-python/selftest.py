"""Independent literal witnesses and reproducible target execution checks."""

import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
PACKET = ROOT / "packet"
spec = importlib.util.spec_from_file_location("converted", OUT / "converted.py")
converted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converted)

# These expected values were hand-derived from the supplied source and descriptor.
EXPECTED = {
    "main": [("l7", "KITE      ", 4),
             ("l2", "ABCDEFGHIJ", 10),
             ("l9", "Q         ", 1)],
    "edge": [("e9", " AB       ", 3),
             ("e2", "AB\t       ", 3),
             ("e7", "          ", 1),
             ("e4", "          ", 1)],
    "single": [("s1", " Z        ", 2)],
    "empty": [],
}


def compare(actual, expected):
    assert all(list(row) == ["row_id", "text", "len"] for row in actual)
    assert [(r["row_id"], r["text"], r["len"]) for r in actual] == expected
    assert all(type(r["len"]) is int for r in actual)
    assert all(len(r["text"].encode("ascii")) == 10 for r in actual)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


checks = []
for name, expected in EXPECTED.items():
    _, rows = read_csv(PACKET / f"{name}.csv")
    original = copy.deepcopy(rows)
    actual = converted.translate(rows)
    compare(actual, expected)
    assert rows == original
    assert actual is not rows
    assert all(a is not b for a, b in zip(actual, rows))
    compare(converted.translate(rows), expected)
    path = OUT / f"{name}.actual.csv"
    subprocess.run([sys.executable, str(OUT / "converted.py"),
                    str(PACKET / f"{name}.csv"), str(path)], check=True)
    header, actual_csv = read_csv(path)
    assert header == ["row_id", "text", "len"]
    for row in actual_csv:
        row["len"] = int(row["len"])
    compare(actual_csv, expected)
    checks.append(f"{name}: API and CLI exact comparison, {len(expected)} rows")

CASES = [
    ("", "          ", 1),
    ("          ", "          ", 1),
    ("\t", "\t         ", 1),
    ("A\t", "A\t        ", 2),
    (" \t ", " \t        ", 2),
    ("  A  ", "  A       ", 3),
    (" A B ", " A B      ", 4),
    ("         A", "         A", 10),
    ("123456789\t", "123456789\t", 10),
    ("A,\"B", "A,\"B      ", 4),
    ("A\n", "A\n        ", 2),
    ("A\r", "A\r        ", 2),
]
rows = [{"row_id": str(i), "text": value} for i, (value, _, _) in enumerate(CASES)]
expected = [(str(i), stored, length) for i, (_, stored, length) in enumerate(CASES)]
compare(converted.translate(rows), expected)
custom = OUT / "witness.input.csv"
with custom.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=["row_id", "text"])
    writer.writeheader()
    writer.writerows(rows)
subprocess.run([sys.executable, str(OUT / "converted.py"), str(custom),
                str(OUT / "witness.actual.csv")], check=True)
_, csv_rows = read_csv(OUT / "witness.actual.csv")
for row in csv_rows:
    row["len"] = int(row["len"])
compare(csv_rows, expected)
checks.append("12 additional literal witnesses: API and CLI exact comparison")

# A deliberate whitespace-trimming mutation loses the terminal tab in this case.
wrong = converted.translate([{"row_id": "trap", "text": "AB\t"}])
wrong[0]["len"] = max(1, len(wrong[0]["text"].rstrip()))
try:
    compare(wrong, [("trap", "AB\t       ", 3)])
except AssertionError:
    checks.append("negative control rejected: generic rstrip returns 2 for AB\\t")
else:
    raise AssertionError("comparator accepted the deliberate mutation")

probe = subprocess.run([sys.executable, "-c", "import converted"], cwd=OUT,
                       check=True, text=True, capture_output=True)
assert not probe.stdout and not probe.stderr
checks.append("import without CLI arguments succeeded silently")

# csv serialization of numeric missing uses an empty cell. This DATA step never
# produces a missing LENGTH value, even when its character argument is blank.
buffer = io.StringIO(newline="")
writer = csv.DictWriter(buffer, fieldnames=["row_id", "text", "len"])
writer.writerow({"row_id": "m", "text": "          ", "len": None})
assert next(csv.reader(io.StringIO(buffer.getvalue())))[2] == ""
checks.append("standard CSV numeric-missing serialization emits a blank cell")

identities = {}
for path in [PACKET / "request.txt", PACKET / "source.sas",
             PACKET / "skill/SKILL.md", *sorted(PACKET.glob("*.csv")),
             OUT / "converted.py", OUT / "selftest.py"]:
    identities[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
receipt = {
    "status": "target-runtime evidence only; no live SAS comparison",
    "environment": {"python": sys.version, "platform": platform.platform(),
                    "executable": sys.executable},
    "checks": checks,
    "sha256": identities,
}
(OUT / "evidence.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
