"""Independent bounded witnesses; uses only this isolated workspace."""

import copy
import csv
import hashlib
import importlib.util
from pathlib import Path
import random
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUT = {"left": ["key", "left_seq", "a", "shared"],
         "right": ["key", "right_seq", "b", "shared"]}
COLS = ["key", "left_seq", "right_seq", "a", "b", "shared", "from_left", "from_right"]
HAND = {
    "main": [
        [None, 1, 11, 10, 100, 101, 1, 1],
        [None, 2, 11, 20, 100, 2, 1, 1],
        [1, 3, 12, 30, 200, 102, 1, 1],
        [1, 4, 13, 40, 300, None, 1, 1],
        [1, 5, 13, 50, 300, 5, 1, 1],
        [2, 6, None, 60, None, 6, 1, 0],
        [3, None, 14, None, 400, 104, 0, 1],
        [4, 7, 15, 70, 500, None, 1, 1],
    ],
    "right-long": [
        [5, 1, 1, None, 20, 100, 1, 1],
        [5, 1, 2, None, 30, None, 1, 1],
        [5, 1, 3, None, 40, 300, 1, 1],
    ],
    "missing-only": [[None, 1, 1, None, None, None, 1, 1]],
    "empty": [],
    "left-empty": [[None, None, 1, None, 8, 9, 0, 1],
                   [2, None, 2, None, None, None, 0, 1]],
    "right-empty": [[None, 1, None, 8, None, 9, 1, 0],
                    [2, 2, None, None, None, None, 1, 0]],
}


def read_csv(path, columns):
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == columns, (path, reader.fieldnames)
        return [{c: None if r[c] == "" else float(r[c]) for c in columns} for r in reader]


def write_csv(path, columns, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def witness(tables):
    # Closed-form position witness, independent of the translation's row buffer.
    keys = {row["key"] for rows in tables.values() for row in rows}
    result = []
    for key in sorted(keys, key=lambda k: (k is not None, k or 0)):
        left = [r for r in tables["left"] if r["key"] == key]
        right = [r for r in tables["right"] if r["key"] == key]
        for i in range(max(len(left), len(right))):
            l = left[min(i, len(left) - 1)] if left else {}
            r = right[min(i, len(right) - 1)] if right else {}
            shared = right[i]["shared"] if i < len(right) else left[i]["shared"]
            result.append(dict(zip(COLS, [key, l.get("left_seq"), r.get("right_seq"),
                                         l.get("a"), r.get("b"), shared,
                                         int(bool(left)), int(bool(right))])))
    return {"want": result}


def compare(actual, expected):
    assert list(actual) == ["want"]
    assert actual == expected, (actual, expected)
    for row in actual["want"]:
        assert list(row) == COLS
        assert all(v is None or isinstance(v, (int, float)) for v in row.values())


def run(args, success=True):
    done = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    assert (done.returncode == 0) == success, (args, done.returncode, done.stdout, done.stderr)
    return done


def main():
    spec = importlib.util.spec_from_file_location("converted", HERE / "converted.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = random.Random(20261102)
    cases = []
    for name, rows in HAND.items():
        source = ROOT / "packet" / "cases" / name
        tables = {t: read_csv(source / (t + ".csv"), cols) for t, cols in INPUT.items()}
        expected = {"want": [dict(zip(COLS, row)) for row in rows]}
        assert witness(tables) == expected
        cases.append((name, tables, expected))
    for number in range(80):
        tables = {t: [] for t in INPUT}
        for key in [None, -9, 0, 2, 8]:
            for table, seq, value in [("left", "left_seq", "a"), ("right", "right_seq", "b")]:
                for _ in range(rng.randrange(5)):
                    sequence = len(tables[table]) + 1
                    tables[table].append({"key": key, seq: sequence,
                                          value: rng.choice([None, -7, 0, 1.25, 1e-100]),
                                          "shared": rng.choice([None, -2, 0, 0.1, 3.141592653589793])})
        cases.append((f"generated-{number:02}", tables, witness(tables)))
    empty = {"left": [], "right": []}
    with tempfile.TemporaryDirectory(prefix="selftest-", dir=ROOT) as tmp:
        scratch = Path(tmp)
        for name, tables, expected in cases:
            before = copy.deepcopy(tables)
            compare(module.translate(tables), expected)
            assert tables == before
            compare(module.translate(empty), {"want": []})
            compare(module.translate(tables), expected)
            output = module.translate(tables)
            if output["want"]:
                output["want"][0]["shared"] = 123456789
                compare(module.translate(tables), expected)
                assert tables == before
            directory = scratch / name
            directory.mkdir()
            for table, columns in INPUT.items():
                write_csv(directory / (table + ".csv"), columns, tables[table])
            write_csv(directory / "expected.csv", COLS, expected["want"])
            for language, args in [
                ("python", ["python3", str(HERE / "converted.py")]),
                ("r", ["Rscript", "--vanilla", str(HERE / "converted.R")]),
            ]:
                destination = scratch / (name + "-" + language)
                run(args + [str(directory), str(destination)])
                compare({"want": read_csv(destination / "want.csv", COLS)}, expected)
                original = (destination / "want.csv").read_bytes()
                run(args + [str(directory), str(destination)], success=False)
                assert list(destination.iterdir()) == [destination / "want.csv"]
                assert (destination / "want.csv").read_bytes() == original
        # Each input is validated, including when the other input is empty.
        for table in INPUT:
            for keys in [[2, 1], [0, None], [None, 3, 2]]:
                tables = copy.deepcopy(empty)
                tables[table] = [dict.fromkeys(INPUT[table], 1) for k in keys]
                for row, key in zip(tables[table], keys):
                    row["key"] = key
                before = copy.deepcopy(tables)
                try:
                    module.translate(tables)
                except ValueError as exc:
                    assert "not sorted" in str(exc)
                else:
                    raise AssertionError("Unsorted API input accepted")
                assert tables == before
                name = "bad-" + table + "-" + str(len(keys)) + "-" + str(keys[0])
                directory = scratch / name
                directory.mkdir()
                for t, cols in INPUT.items():
                    write_csv(directory / (t + ".csv"), cols, tables[t])
                for language, args in [("python", ["python3", str(HERE / "converted.py")]),
                                       ("r", ["Rscript", "--vanilla", str(HERE / "converted.R")])]:
                    destination = scratch / (name + "-" + language)
                    done = run(args + [str(directory), str(destination)], success=False)
                    assert "not sorted" in done.stderr
                    assert not destination.exists()
        r_result = run(["Rscript", "--vanilla", str(HERE / "selftest.R"), str(scratch)])
        print(r_result.stdout.strip())
    # Deliberately wrong last-right-value and Cartesian-row variants must fail.
    main_expected = {"want": [dict(zip(COLS, row)) for row in HAND["main"]]}
    wrong_shared = copy.deepcopy(main_expected)
    wrong_shared["want"][1]["shared"] = 101
    wrong_shared["want"][4]["shared"] = None
    wrong_flags = copy.deepcopy(main_expected)
    wrong_flags["want"][1]["from_right"] = 0
    wrong_cartesian = copy.deepcopy(main_expected)
    wrong_cartesian["want"].extend(copy.deepcopy(main_expected["want"][2:5]))
    for wrong in [wrong_shared, wrong_flags, wrong_cartesian]:
        try:
            compare(wrong, main_expected)
        except AssertionError:
            pass
        else:
            raise AssertionError("Comparator accepted a deliberately wrong variant")
    print("PASS: 6 packet cases (16 rows); 80 generated cases; 86 Python API cases")
    print("PASS: 172 successful CLI runs; 172 existing-destination refusals; 12 unsorted CLI refusals")
    print("PASS: exact values/order/schema, blank missing CSV, fresh calls, input preservation, 3 wrong variants rejected")
    for name in ["converted.py", "converted.R"]:
        print(name, "sha256", hashlib.sha256((HERE / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
