#!/usr/bin/env python3
"""Replay one archived translation candidate against an independent scoped oracle."""

import argparse
import datetime
from decimal import Decimal, InvalidOperation
import hashlib
import json
import platform
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / "references/rosetta-code/corpus/sum_and_product_of_an_array.sas"
SOURCE_SHA256 = "06eca942365b06dec7e0f99b077856b4b33391e8addee0b39a44c0170987ea1a"
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_records(stdout):
    return [line.split() for line in stdout.splitlines()]


def matches(stdout, expected):
    """One record, exact finite numeric value, exact ordinary-missing token."""
    records = logical_records(stdout)
    if len(records) != 1 or len(records[0]) != 2:
        return False
    value, missing = records[0]
    if missing != expected[0][1] or not NUMBER.fullmatch(value):
        return False
    try:
        observed = Decimal(value)
        return observed.is_finite() and observed == Decimal(expected[0][0])
    except InvalidOperation:
        return False


def execute(path, cwd):
    try:
        result = subprocess.run([sys.executable, "-I", str(path.resolve())],
                                cwd=cwd, capture_output=True, text=True, timeout=5)
        return {"exit_code": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr, "timed_out": False}
    except subprocess.TimeoutExpired:
        return {"exit_code": None, "stdout": "", "stderr": "timeout",
                "timed_out": True}


def verify(candidate):
    if digest(SOURCE) != SOURCE_SHA256:
        raise ValueError("source differs from the trial's complete-program pin")
    oracle_path = HERE / "oracle.json"
    oracle = json.loads(oracle_path.read_text())
    expected = oracle["logical_records"]
    # Closed-form arithmetic is independent of the candidate's array/loop path.
    n = 100
    derived = n * (n + 1) * (2 * n + 1) // 6
    if expected != [[str(derived), "."]]:
        raise ValueError("oracle differs from the declared arithmetic/missing contract")
    candidate_hash = digest(candidate)
    controls = {}
    with tempfile.TemporaryDirectory(prefix="roku-translation-trial-") as temp:
        work = Path(temp)
        observed = execute(candidate, work)
        candidate_pass = (observed["exit_code"] == 0 and not observed["stderr"]
                          and matches(observed["stdout"], expected))
        # Plausible wrong observations use the very same subprocess and comparator.
        for name, records in oracle["negative_controls"].items():
            output = "\n".join(" ".join(row) for row in records) + "\n"
            control = work / "negative.py"
            control.write_text(f"print({output!r}, end='')\n")
            result = execute(control, work)
            controls[name] = {"observed_records": logical_records(result["stdout"]),
                              "exit_code": result["exit_code"],
                              "rejected": result["exit_code"] == 0
                              and not result["stderr"]
                              and not matches(result["stdout"], expected)}
        # A real alternative algorithm catches the tempting repair suggested by title.
        wrong = work / "invented_product.py"
        wrong.write_text("import math\na = [i * i for i in range(1, 101)]\n"
                         "print(sum(a), math.prod(a))\n")
        result = execute(wrong, work)
        controls["executed_product_repair"] = {
            "observed_records": logical_records(result["stdout"]),
            "exit_code": result["exit_code"],
            "rejected": result["exit_code"] == 0 and not result["stderr"]
            and not matches(result["stdout"], expected)}
    unchanged = digest(candidate) == candidate_hash
    passed = candidate_pass and unchanged and all(x["rejected"] for x in controls.values())
    return {
        "schema_version": 1,
        "status": "Bounded Python replay for maintainer review; not live-SAS equivalence or a skill success rate",
        "executed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": {"candidate_generations": 1, "candidate_executions_this_replay": 1,
                  "negative_controls": len(controls), "live_sas_executions": 0},
        "environment": {"python": platform.python_version(),
                        "implementation": platform.python_implementation(),
                        "system": platform.system(), "machine": platform.machine()},
        "source_sha256": SOURCE_SHA256,
        "candidate_sha256": candidate_hash,
        "verifier_sha256": digest(Path(__file__)),
        "oracle_sha256": digest(oracle_path),
        "generation_skill": {"name": "sas-translate",
                             "commit": "03fc5b3916b7423619b5e4308604215feb6b2c96",
                             "sha256": "6cdb948823b5fb1caccfee7c3c4754892bdb617a0b7da526272bbd21220ac91c"},
        "comparison": oracle["comparison"],
        "expected_records": expected,
        "candidate": {**observed, "observed_records": logical_records(observed["stdout"]),
                      "passed": candidate_pass, "unchanged_after_execution": unchanged},
        "negative_controls": controls,
        "verdict": "PASS" if passed else "FAIL",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=HERE / "converted.py")
    parser.add_argument("--receipt", type=Path,
                        help="Optional new receipt path; existing files are never overwritten")
    args = parser.parse_args()
    try:
        result = verify(args.candidate)
        text = json.dumps(result, indent=2) + "\n"
        if args.receipt:
            with args.receipt.open("x", encoding="utf-8") as stream:
                stream.write(text)
        print(text, end="")
        return 0 if result["verdict"] == "PASS" else 1
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
