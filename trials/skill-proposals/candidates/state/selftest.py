"""Reproducible checks; independent witnesses are inferred, not live SAS truth."""
import contextlib
import copy
import csv
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        spec.loader.exec_module(module)
    assert out.getvalue() == ""
    return module


def witness(rows):
    # Independent indexed construction, separate from the repaired execution loop.
    selected = [i for i, row in enumerate(rows) if row["take"] == 1]
    previous = dict(zip(selected[1:], [rows[i]["value"] for i in selected[:-1]]))
    totals = list(itertools.accumulate(
        (0 if row["value"] is None else row["value"] for row in rows)))
    stage = [dict(row_id=row["row_id"], value=row["value"],
                  prev=previous.get(i), total=10 + totals[i])
             for i, row in enumerate(rows) if row["emit"] == 1]
    want = [dict(row, delta=None if row["value"] is None or row["prev"] is None
                 else row["value"] - row["prev"]) for row in stage]
    return dict(stage=stage, want=want)


def compare(actual, expected):
    assert list(actual) == ["stage", "want"]
    for table, columns in (("stage", ["row_id", "value", "prev", "total"]),
                           ("want", ["row_id", "value", "prev", "total", "delta"])):
        assert len(actual[table]) == len(expected[table]), table
        for a, e in zip(actual[table], expected[table]):
            assert list(a) == columns
            assert isinstance(a["row_id"], str)
            for column in columns[1:]:
                assert a[column] is None or type(a[column]) in (int, float)
            assert a == e, (table, a, e)


def csv_result(path):
    result = {}
    for table, columns in (("stage", ["row_id", "value", "prev", "total"]),
                           ("want", ["row_id", "value", "prev", "total", "delta"])):
        with (path / (table + ".csv")).open(newline="") as handle:
            reader = csv.DictReader(handle)
            assert reader.fieldnames == columns
            result[table] = [dict(row_id=row["row_id"], **{
                column: None if row[column] == "" else float(row[column])
                for column in columns[1:]}) for row in reader]
    return result


def wrong_variant(rows, kind):
    stage = []
    total, queue, prev = 10, None, None
    for row in rows:
        if kind == "early_filter" and not row["emit"]:
            continue
        if kind != "retained_receiver":
            prev = None
        value = row["value"]
        if row["take"]:
            prev = queue
        if row["take"] or kind == "unconditional_queue":
            queue = value
        if kind == "ordinary_addition":
            total = None if total is None or value is None else total + value
        elif value is not None:
            total += value
        if row["emit"]:
            stage.append(dict(row_id=row["row_id"], value=value, prev=prev, total=total))
    want = [dict(row, delta=None if row["value"] is None or row["prev"] is None
                 else row["value"] - row["prev"]) for row in stage]
    if kind == "step_two_original_input":
        want = witness([dict(row, emit=1) for row in rows])["want"]
    return dict(stage=stage, want=want)


def first_difference(actual, expected):
    for table in ("stage", "want"):
        if len(actual[table]) != len(expected[table]):
            return dict(table=table, difference="row count",
                        actual=len(actual[table]), expected=len(expected[table]))
        for i, (a, e) in enumerate(zip(actual[table], expected[table]), 1):
            for key in e:
                if a[key] != e[key]:
                    return dict(table=table, position=i, row_id=e["row_id"],
                                column=key, actual=a[key], expected=e[key])
    raise AssertionError("Wrong variant escaped the comparison")


def main():
    repaired = load_module("repaired", ROOT / "converted.py")
    buggy = load_module("frozen_buggy", ROOT / "evidence/frozen/buggy.py")
    first = json.loads((ROOT / "evidence/first_observed_mismatch.json").read_text())
    rows = repaired.read_input(ROOT / "evidence/frozen/main.csv")
    assert buggy.translate(rows) == first["actual"]
    compare(witness(rows), first["expected"])
    compare(repaired.translate(rows), first["expected"])

    count = 0
    possibilities = list(itertools.product((None, -2.0, 0.0, 3.0), (0, 1), (0, 1)))
    for n in range(4):
        for items in itertools.product(possibilities, repeat=n):
            case = [dict(row_id="x" + str(i), value=v, take=t, emit=e)
                    for i, (v, t, e) in enumerate(items)]
            before = copy.deepcopy(case)
            expected = witness(case)
            compare(repaired.translate(case), expected)
            assert case == before
            compare(repaired.translate(case), expected)
            compare(repaired.translate([]), dict(stage=[], want=[]))
            count += 1

    result = repaired.translate(rows)
    original = copy.deepcopy(rows)
    result["want"][0]["total"] = -999
    assert result["stage"][0]["total"] == 15
    result["stage"][0]["row_id"] = "changed"
    assert rows == original
    compare(repaired.translate(rows), first["expected"])

    negative = {kind: first_difference(wrong_variant(rows, kind), first["expected"])
                for kind in ("early_filter", "unconditional_queue", "retained_receiver",
                             "ordinary_addition", "step_two_original_input")}

    run = Path(tempfile.mkdtemp(prefix="run-", dir=ROOT / "evidence"))
    edge = run / "key_edges.csv"
    keys = ["00000001", "NA", "a,b", 'q"k', "#key", "a b", ""]
    with edge.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["row_id", "value", "take", "emit"])
        writer.writerows((key, value, 1, 1) for key, value in zip(keys, [0.5, -1.25, "", 2.5, 0, 1, -2]))
    fixtures = [ROOT / "evidence/frozen" / (name + ".csv")
                for name in ("main", "single", "silent", "empty")] + [edge]
    cli_receipts = []
    for fixture in fixtures:
        expected = witness(repaired.read_input(fixture))
        for language, command in (("python", [sys.executable, str(ROOT / "converted.py")]),
                                   ("R", ["Rscript", str(ROOT / "converted.R")])):
            destination = run / (language + "_" + fixture.stem)
            proc = subprocess.run(command + [str(fixture), str(destination)],
                                  text=True, capture_output=True)
            assert proc.returncode == 0, proc.stderr
            assert proc.stdout == "" and proc.stderr == "", (language, proc.stdout, proc.stderr)
            compare(csv_result(destination), expected)
            before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in destination.iterdir()}
            repeat = subprocess.run(command + [str(fixture), str(destination)],
                                    text=True, capture_output=True)
            assert repeat.returncode != 0
            after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in destination.iterdir()}
            assert before == after
            cli_receipts.append(dict(language=language, fixture=fixture.name,
                                     output=str(destination), exit_code=proc.returncode,
                                     existing_directory_exit_code=repeat.returncode,
                                     existing_directory_message=repeat.stderr.strip()))

    r = subprocess.run(["Rscript", str(ROOT / "selftest.R"), str(ROOT)],
                       text=True, capture_output=True)
    assert r.returncode == 0, r.stderr
    assert r.stderr == "", r.stderr
    assert "R API cases passed: 4369" in r.stdout
    receipt = dict(status="PASS against independent inferred witnesses; no SAS runtime",
                   python_version=platform.python_version(),
                   R_output=r.stdout.strip(), python_api_cases=count,
                   repeated_call_policy="Every exhaustive case called twice, with an empty call between cases",
                   caller_preservation=True, import_source_no_cli=True,
                   stage_want_independence=True, negative_controls=negative,
                   cli=cli_receipts)
    (run / "validation_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
