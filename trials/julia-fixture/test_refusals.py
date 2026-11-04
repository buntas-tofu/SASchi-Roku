#!/usr/bin/env python3
"""Test candidates refuse malformed source input without creating output."""
import argparse
import csv
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "references/python-libraries/fixtures"


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("julia")
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--project", default="")
    args = parser.parse_args()
    customers = (FIXTURE / "customers.csv").read_text(encoding="utf-8")
    orders = (FIXTURE / "orders.csv").read_text(encoding="utf-8")
    mutations = {
        "duplicate_parent_key": (customers + "0007,Z\n", orders),
        "malformed_leading_zero_key": (customers, orders.replace("o1,0007,", "o1,007,")),
    }
    for label, (cdata, odata) in mutations.items():
        with tempfile.TemporaryDirectory() as working:
            here = Path(working)
            cpath, opath, out = here / "customers.csv", here / "orders.csv", here / "out.tsv"
            cpath.write_text(cdata, encoding="utf-8")
            opath.write_text(odata, encoding="utf-8")
            command = [args.julia, "--startup-file=no"]
            if args.project:
                command.append("--project=" + args.project)
            command += [str(args.candidate), str(cpath), str(opath), str(out)]
            completed = subprocess.run(command, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True, timeout=180)
            if completed.returncode == 0 or out.exists():
                raise AssertionError("Bad input accepted or emitted output: " + label)
            print("Rejected malformed fixture:", label)


if __name__ == "__main__":
    run()
