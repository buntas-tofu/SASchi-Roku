"""Reproduce the original mismatch against preserved hand-derived expectations."""

import copy
import csv
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PATHS = ["where_path", "if_path"]
COLS = ["row_id", "value", "prev", "total"]


def load_rows(path):
    with path.open(newline="") as stream:
        return [{"row_id": row["row_id"],
                 "value": None if row["value"] == "" else float(row["value"]),
                 "eligible": int(row["eligible"])} for row in csv.DictReader(stream)]


def first_difference(actual, expected):
    if list(actual) != PATHS:
        return {"kind": "table names/order", "actual": list(actual), "expected": PATHS}
    for path in PATHS:
        if len(actual[path]) != len(expected[path]):
            return {"kind": "row count", "path": path,
                    "actual": len(actual[path]), "expected": len(expected[path])}
        for pos, (got, want) in enumerate(zip(actual[path], expected[path]), 1):
            if list(got) != COLS:
                return {"kind": "columns/order", "path": path, "row": pos,
                        "actual": list(got), "expected": COLS}
            for column in COLS:
                if got[column] != want[column]:
                    return {"kind": "cell", "path": path, "row": pos,
                            "row_id": want["row_id"], "column": column,
                            "actual": got[column], "expected": want[column]}
    return None


def main():
    spec = importlib.util.spec_from_file_location(
        "frozen_buggy", ROOT / "evidence" / "frozen_packet" / "buggy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    destination = ROOT / "evidence" / "original_run"
    destination.mkdir(exist_ok=False)
    result = {}
    for name in ["main", "leading", "all-missing", "empty", "silent", "single"]:
        rows = load_rows(ROOT / "evidence" / "frozen_packet" / (name + ".csv"))
        saved = copy.deepcopy(rows)
        observed = module.translate(rows)
        expected = json.loads((ROOT / "evidence" / "hand_expected" / (name + ".json")).read_text())
        diff = first_difference(observed, expected)
        result[name] = {"first_difference": diff, "input_preserved": rows == saved}
        (destination / (name + ".json")).write_text(json.dumps(observed, indent=2) + "\n")
    (destination / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    with (ROOT / "evidence" / "history.txt").open("a") as stream:
        stream.write("06. Ran frozen buggy.py on all six fixtures. Original mismatches reproduced on main and leading; remaining fixtures match hand expectations. This diagnostic command deliberately exits 1 for a reproduced mismatch.\n")
    return 1 if result["main"]["first_difference"] else 0


if __name__ == "__main__":
    sys.exit(main())
