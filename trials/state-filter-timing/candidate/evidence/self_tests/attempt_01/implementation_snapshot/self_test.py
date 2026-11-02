"""Run reproducible local validation. All expectations are independent of targets."""

from collections import OrderedDict
import contextlib
import copy
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PACKET = ROOT.parent / "packet"
PATHS = ["where_path", "if_path"]
COLS = ["row_id", "value", "prev", "total"]
from reproduce_original import first_difference, load_rows


def dump_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_rows(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def prefix_witness(rows):
    """Index/prefix definition, independent of the streaming target implementation.

    Used only with small integer/dyadic values, where these sums are exact.
    """
    result = {}
    for path in PATHS:
        processed = [i for i, row in enumerate(rows)
                     if path == "if_path" or row["eligible"] == 1]
        output = []
        for sequence_position, i in enumerate(processed):
            if rows[i]["eligible"] != 1:
                continue
            prior = processed[sequence_position - 1] if sequence_position else None
            total = 10 + sum(rows[j]["value"] for j in processed[:sequence_position + 1]
                             if rows[j]["value"] is not None)
            output.append({"row_id": rows[i]["row_id"], "value": rows[i]["value"],
                           "prev": None if prior is None else rows[prior]["value"],
                           "total": total})
        result[path] = output
    return result


def make_cases():
    cases = []
    for name in ["main", "leading", "all-missing", "empty", "silent", "single"]:
        expected = json.loads((ROOT / "evidence" / "hand_expected" / (name + ".json")).read_text())
        rows = load_rows(PACKET / (name + ".csv"))
        assert prefix_witness(rows) == expected
        cases.append((name, "supplied_hand_trace", rows, expected))
    number = 0
    for size in range(5):
        for combinations in itertools.product(list(itertools.product([None, -2, 3], [0, 1])), repeat=size):
            rows = [{"row_id": f"{position:04d}", "value": value, "eligible": eligible}
                    for position, (value, eligible) in enumerate(combinations)]
            cases.append((f"exhaustive_{number:04d}", "indexed_prefix_witness", rows, prefix_witness(rows)))
            number += 1
    text_rows = [
        {"row_id": "0007", "value": 1.25, "eligible": 1},
        {"row_id": "NA", "value": None, "eligible": 1},
        {"row_id": ' A,#"x" ', "value": -0.5, "eligible": 0},
        {"row_id": "0010", "value": 2.25, "eligible": 1},
        {"row_id": ''.join(chr(i) for i in range(32, 127)), "value": 0, "eligible": 1},
    ]
    cases.append(("text_transport", "indexed_prefix_witness", text_rows, prefix_witness(text_rows)))
    precise = [{"row_id": "0001", "value": 1.2345678901234567, "eligible": 1},
               {"row_id": "NA", "value": None, "eligible": 1}]
    precise_expected = [dict(zip(COLS, row)) for row in [
        ["0001", 1.2345678901234567, None, 11.234567890123456],
        ["NA", None, 1.2345678901234567, 11.234567890123456]]]
    cases.append(("precision", "literal_binary64_expectation", precise,
                  {path: copy.deepcopy(precise_expected) for path in PATHS}))
    overflow = [{"row_id": f"o{i}", "value": value, "eligible": 1}
                for i, value in enumerate([1e308, 1e308, None, 2])]
    overflow_expected = [dict(zip(COLS, row)) for row in [
        ["o0", 1e308, None, 1e308], ["o1", 1e308, 1e308, None],
        ["o2", None, 1e308, None], ["o3", 2, None, 2]]]
    cases.append(("overflow_recovery", "document_based_inference", overflow,
                  {path: copy.deepcopy(overflow_expected) for path in PATHS}))
    return cases


def assert_result(actual, expected):
    assert isinstance(actual, OrderedDict), "Python API must return OrderedDict"
    diff = first_difference(actual, expected)
    assert diff is None, diff
    for path in PATHS:
        assert isinstance(actual[path], list)
        for row in actual[path]:
            assert type(row["row_id"]) is str
            assert all(value is None or type(value) in (int, float)
                       for column, value in row.items() if column != "row_id")


def tree_state(path):
    if path.is_symlink():
        return {"link": str(path.readlink())}
    if path.is_file():
        return {"bytes": path.read_bytes().hex()}
    if path.is_dir():
        return {p.name: tree_state(p) for p in sorted(path.iterdir())}
    return {"missing": True}


def load_output(path):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == COLS, (str(path), reader.fieldnames)
        return [{column: (row[column] if column == "row_id"
                          else None if row[column] == "" else float(row[column]))
                 for column in COLS} for row in reader]


def wrong_variant(rows, variant):
    result = {}
    for path in PATHS:
        queue = None
        total = 10
        output = []
        for row in rows:
            early = variant == "early_filter_both" or (variant == "skip_missing_queue" and path == "where_path")
            if early and row["eligible"] != 1:
                continue
            prev = queue
            if variant != "skip_missing_queue" or row["value"] is not None:
                queue = row["value"]
            if row["value"] is not None:
                total += row["value"]
            if row["eligible"] == 1:
                output.append({"row_id": row["row_id"], "value": row["value"],
                               "prev": prev, "total": total})
        result[path] = output
    return result


def main():
    runs = ROOT / "evidence" / "self_tests"
    runs.mkdir(exist_ok=True)
    attempt = 1
    while (runs / f"attempt_{attempt:02d}").exists():
        attempt += 1
    run = runs / f"attempt_{attempt:02d}"
    run.mkdir()
    snapshots = run / "implementation_snapshot"
    snapshots.mkdir()
    for name in ["converted.py", "converted.R", "self_test.py", "test_api.R"]:
        shutil.copyfile(ROOT / name, snapshots / name)
    receipt = {"status": "RUNNING", "start_utc": datetime.now(timezone.utc).isoformat(),
               "python": sys.version, "platform": platform.platform(), "commands": [],
               "checks": {}}
    dump_json(run / "receipt.json", receipt)

    def command(label, args):
        start = time.monotonic()
        process = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        (run / (label + ".stdout.txt")).write_text(process.stdout)
        (run / (label + ".stderr.txt")).write_text(process.stderr)
        entry = {"label": label, "command": args, "exit_code": process.returncode,
                 "duration_seconds": round(time.monotonic() - start, 6)}
        receipt["commands"].append(entry)
        dump_json(run / "receipt.json", receipt)
        return process

    try:
        cases = make_cases()
        write_rows(run / "suite_case_index.csv", ["case_id", "basis"],
                   [{"case_id": name, "basis": basis} for name, basis, rows, expected in cases])
        write_rows(run / "suite_input.csv", ["case_id", "row_id", "value", "eligible"],
                   [dict(case_id=name, **row) for name, basis, rows, expected in cases for row in rows])
        write_rows(run / "suite_expected.csv", ["case_id", "path"] + COLS,
                   [dict(case_id=name, path=path, **row) for name, basis, rows, expected in cases
                    for path in PATHS for row in expected[path]])
        saved_argv = sys.argv
        import_destination = run / "must_not_exist_after_import"
        sys.argv = [str(ROOT / "converted.py"), str(PACKET / "main.csv"), str(import_destination)]
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
                spec = importlib.util.spec_from_file_location("converted_under_test", ROOT / "converted.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
        finally:
            sys.argv = saved_argv
        assert captured.getvalue() == "" and not import_destination.exists()
        for name, basis, rows, expected in cases:
            saved = copy.deepcopy(rows)
            actual = module.translate(rows)
            assert_result(actual, expected)
            assert saved == rows, name
            assert_result(module.translate([]), {path: [] for path in PATHS})
            assert_result(module.translate(rows), expected)
            if actual["where_path"]:
                old_if = copy.deepcopy(actual["if_path"])
                actual["where_path"][0]["total"] = -987654321
                assert actual["if_path"] == old_if
                assert_result(module.translate(rows), expected)
                assert saved == rows
        receipt["checks"]["python_api_cases"] = len(cases)
        receipt["checks"]["python_import_is_quiet"] = True
        write_rows(run / "python_api_cases.csv", ["case_id", "status"],
                   [{"case_id": case[0], "status": "PASS"} for case in cases])
        process = command("r_version", ["Rscript", "--version"])
        assert process.returncode == 0
        process = command("r_api", ["Rscript", str(ROOT / "test_api.R"), str(ROOT), str(run)])
        assert process.returncode == 0, process.stdout + process.stderr
        receipt["checks"]["r_api_cases"] = len(cases)
        main_rows = cases[0][2]
        main_expected = cases[0][3]
        kills = {}
        for variant in ["early_filter_both", "late_filter_both", "skip_missing_queue"]:
            diff = first_difference(wrong_variant(main_rows, variant), main_expected)
            assert diff is not None, variant
            kills[variant] = diff
        dump_json(run / "wrong_variants.json", kills)
        receipt["checks"]["wrong_variants_rejected"] = len(kills)
        cli = run / "cli"
        cli.mkdir()
        cli_count = 0
        commands = {"python": ["python3", str(ROOT / "converted.py")],
                    "r": ["Rscript", str(ROOT / "converted.R")]}
        for name, basis, rows, expected in cases:
            if name.startswith("exhaustive_"):
                continue
            if basis == "supplied_hand_trace":
                source = PACKET / (name + ".csv")
            else:
                source = cli / (name + ".input.csv")
                write_rows(source, ["row_id", "value", "eligible"], rows)
            for runtime, prefix in commands.items():
                destination = cli / f"{name}_{runtime}"
                process = command(f"cli_{name}_{runtime}", prefix + [str(source), str(destination)])
                assert process.returncode == 0, process.stdout + process.stderr
                assert sorted(path.name for path in destination.iterdir()) == ["if_path.csv", "where_path.csv"]
                actual = OrderedDict((path, load_output(destination / (path + ".csv"))) for path in PATHS)
                assert_result(actual, expected)
                cli_count += 1
        receipt["checks"]["cli_success_runs"] = cli_count
        existing = run / "existing_destinations"
        existing.mkdir()
        directory = existing / "directory"
        directory.mkdir()
        (directory / "sentinel.txt").write_bytes(b"leave this alone\x00\xff")
        (directory / "where_path.csv").write_text("original data\n")
        regular_file = existing / "file"
        regular_file.write_text("keep file\n")
        empty_dir = existing / "empty_directory"
        empty_dir.mkdir()
        linked_dir = existing / "linked_directory"
        linked_dir.symlink_to(directory, target_is_directory=True)
        broken_link = existing / "broken_link"
        broken_link.symlink_to(existing / "absent_target")
        original = tree_state(existing)
        refusal_count = 0
        for runtime, prefix in commands.items():
            for destination in [directory, regular_file, empty_dir, linked_dir, broken_link]:
                process = command(f"refuse_{runtime}_{destination.name}",
                                  prefix + [str(PACKET / "main.csv"), str(destination)])
                assert process.returncode != 0, "existing destination accepted"
                assert tree_state(existing) == original, "existing destination changed"
                refusal_count += 1
        receipt["checks"]["existing_destination_refusals"] = refusal_count
        manifest = json.loads((ROOT / "evidence" / "input_manifest.json").read_text())
        for name, frozen in manifest.items():
            for base in [PACKET, ROOT / "evidence" / "frozen_packet"]:
                assert hashlib.sha256((base / name).read_bytes()).hexdigest() == frozen["sha256"], name
        receipt["checks"]["original_and_frozen_files_unchanged"] = len(manifest)
        receipt["status"] = "PASS"
    except BaseException as error:
        receipt["status"] = "FAIL"
        receipt["failure"] = repr(error)
        (run / "failure_traceback.txt").write_text(traceback.format_exc())
        traceback.print_exc()
    finally:
        receipt["end_utc"] = datetime.now(timezone.utc).isoformat()
        dump_json(run / "receipt.json", receipt)
        with (ROOT / "evidence" / "history.txt").open("a") as stream:
            stream.write(f"Self-test attempt {attempt:02d}: {receipt['status']}. Snapshot, commands, output, expectations and any traceback retained in evidence/self_tests/attempt_{attempt:02d}/.\n")
    print(json.dumps({"attempt": attempt, "status": receipt["status"], "checks": receipt["checks"]}, indent=2))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
