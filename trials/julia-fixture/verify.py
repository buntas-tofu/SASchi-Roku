#!/usr/bin/env python3
"""Independent comparator and mutation controls for the frozen Julia fixture.

This validator uses the original hand-authored JSON oracle. It does not run
Julia or assert that a supplied TSV was produced by Julia. That is the runner's
separate responsibility. Python standard library only.
"""
import argparse
import copy
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "references/python-libraries/fixtures"
FREEZE = Path(__file__).with_name("freeze.json")
FIELDS = ("segment", "row_count", "non_null_amounts", "sum_cents")


def git_blob_sha(path):
    content = path.read_bytes()
    header = b"blob " + str(len(content)).encode("ascii") + b"\0"
    return hashlib.sha1(header + content).hexdigest()


def check_freeze():
    frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
    for name, expected in frozen["original_fixture_git_blobs"].items():
        if git_blob_sha(FIXTURE / name) != expected:
            raise AssertionError("Frozen fixture drift: " + name)
    return frozen


def read_result(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise AssertionError("TSV schema mismatch")
        rows = list(reader)
    if not rows:
        raise AssertionError("No observed rows")
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise AssertionError("Malformed TSV data")
    typed = []
    for row in rows:
        for field in ("row_count", "non_null_amounts"):
            if not re.fullmatch(r"(?:0|[1-9][0-9]*)", row[field]):
                raise AssertionError("Noninteger count: " + field)
        amount = row["sum_cents"]
        if amount != "NULL" and not re.fullmatch(r"-?(?:0|[1-9][0-9]*)", amount):
            raise AssertionError("Invalid cents")
        typed.append({
            "segment": row["segment"],
            "row_count": int(row["row_count"]),
            "non_null_amounts": int(row["non_null_amounts"]),
            "sum_cents": None if amount == "NULL" else int(amount),
        })
    return typed


def compare(rows, oracle):
    expected = [
        {k: r[k] for k in ("segment", "row_count", "non_null_amounts", "sum_cents")}
        for r in oracle["segment_summary"]
    ]
    if rows != expected:
        raise AssertionError("Grouped rows differ from frozen independent oracle")
    if sum(r["row_count"] for r in rows) != oracle["counts"]["orders"]:
        raise AssertionError("Total row count incorrect")
    if sum(r["row_count"] - r["non_null_amounts"] for r in rows) != oracle["counts"]["missing_amounts"]:
        raise AssertionError("Missingness count incorrect")
    if sum(r["sum_cents"] for r in rows if r["sum_cents"] is not None) != oracle["net_amount_cents"]:
        raise AssertionError("Net amount differs")


def mutation_controls(correct, oracle):
    controls = {}
    def must_reject(name, mutation):
        rows = copy.deepcopy(correct)
        mutation(rows)
        try:
            compare(rows, oracle)
        except AssertionError:
            controls[name] = "rejected"
        else:
            raise AssertionError("Comparator missed negative control: " + name)
    must_reject("dropped_orphan", lambda r: r.pop(0))
    must_reject("negative_amount_sign_flip", lambda r: r[1].update(sum_cents=1650))
    must_reject("null_only_sum_as_zero", lambda r: r[-1].update(sum_cents=0))
    must_reject("zero_treated_as_missing", lambda r: r[2].update(non_null_amounts=2))
    must_reject("wrong_row_count", lambda r: r[1].update(row_count=4))
    must_reject("swapped_order", lambda r: r.reverse())
    must_reject("leading_zero_key_mismatch", lambda r: r[1].update(row_count=1))
    must_reject("duplicated_segment", lambda r: r.append(copy.deepcopy(r[1])))
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    frozen = check_freeze()
    oracle = json.loads((FIXTURE / "expected.json").read_text(encoding="utf-8"))
    rows = read_result(args.result)
    compare(rows, oracle)
    controls = mutation_controls(rows, oracle)
    receipt = {
        "status": "passed",
        "source": "pre-existing hand-authored fixture; no native SAS execution",
        "runtime_verification": "requires separate Julia invocation log",
        "source_fixture_git_blobs": frozen["original_fixture_git_blobs"],
        "observed_sha256": hashlib.sha256(args.result.read_bytes()).hexdigest(),
        "positive_group_rows_checked": len(rows),
        "negative_controls_rejected": len(controls),
        "controls": controls,
    }
    if args.receipt:
        if args.receipt.exists():
            raise FileExistsError("Refusing to overwrite existing receipt")
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
