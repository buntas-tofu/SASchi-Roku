"""Hand-trace tests and transport checks; run from any directory."""
import copy
import csv
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("converted", HERE / "converted.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HEADERS = {
    "stage": ["row_id", "short", "joined", "tag"],
    "want": ["row_id", "short", "copy", "wrapped", "joined", "tag", "n", "z"],
    "descriptor": ["table", "column", "bytes"],
}
# Literal results derived by tracing the supplied source before target execution.
MAIN_STAGE = [
    ("0007", "ABC", "ABCZ  ", "L"),
    ("NA", " A ", " A Q? ", "Y"),
    ("x3", "   ", "      ", "L"),
    ("x4", 'A"B', 'A"B ! ', "L"),
    ("x5", "XY ", "XY R  ", "Y"),
]
MAIN_WANT = [
    ("0007", "ABC  ", "AB", "[ABC  ] ", "ABCZ  ", "L", 3, 3),
    ("NA", " A   ", " A", "[ A   ] ", " A Q? ", "Y", 2, 2),
    ("x3", "     ", "  ", "[     ] ", "      ", "L", 1, 0),
    ("x4", 'A"B  ', 'A"', '[A"B  ] ', 'A"B ! ', "L", 3, 3),
    ("x5", "XY   ", "XY", "[XY   ] ", "XY R  ", "Y", 2, 2),
]
BOUND_STAGE = [("b1", "AB ", "AB    ", "L"),
               ("b2", "ABC", "ABC12 ", "Y"), ("b3", "ABC", "ABC34 ", "L")]
BOUND_WANT = [("b1", "AB   ", "AB", "[AB   ] ", "AB    ", "L", 2, 2),
              ("b2", "ABC  ", "AB", "[ABC  ] ", "ABC12 ", "Y", 3, 3),
              ("b3", "ABC  ", "AB", "[ABC  ] ", "ABC34 ", "L", 3, 3)]
DESCRIPTOR = [("stage", "short", 3), ("stage", "joined", 6), ("stage", "tag", 1),
              ("want", "short", 5), ("want", "copy", 2), ("want", "wrapped", 8),
              ("want", "joined", 6), ("want", "tag", 1)]
TRACES = {
    "main": (MAIN_STAGE, MAIN_WANT),
    "boundary": (BOUND_STAGE, BOUND_WANT),
    "blank": ([("blank", "   ", "      ", "L")],
              [("blank", "     ", "  ", "[     ] ", "      ", "L", 1, 0)]),
    "single-false": ([("false", "X  ", "X  Y  ", "L")],
                     [("false", "X    ", "X ", "[X    ] ", "X  Y  ", "L", 1, 1)]),
    "empty": ([], []),
}


def expected(case):
    stage, want = TRACES[case]
    return {name: [dict(zip(HEADERS[name], cells)) for cells in rows]
            for name, rows in (("stage", stage), ("want", want), ("descriptor", DESCRIPTOR))}


def read_table(path, columns, numeric=()):
    with path.open(encoding="ascii", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == columns
        rows = list(reader)
    for row in rows:
        assert None not in row and None not in row.values()
        for col in numeric:
            row[col] = None if row[col] == "" else float(row[col])
    return rows


def compare(got, wanted):
    assert list(got) == list(HEADERS)
    assert got == wanted, (got, wanted)
    for name, rows in got.items():
        for row in rows:
            assert list(row) == HEADERS[name]
    for table, column, width in DESCRIPTOR:
        assert all(len(row[column].encode("ascii")) == width for row in got[table])


def write_tables(directory, tables):
    directory.mkdir()
    for name, rows in tables.items():
        with (directory / (name + ".csv")).open("w", encoding="ascii", newline="") as handle:
            writer = csv.DictWriter(handle, HEADERS[name], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def cli(executable, source, destination, success=True):
    command = executable + [str(source), str(destination)]
    result = subprocess.run(command, text=True, capture_output=True)
    assert (result.returncode == 0) == success, (command, result.stdout, result.stderr)


def run():
    executables = [[sys.executable, "-B", str(HERE / "converted.py")],
                   ["Rscript", "--vanilla", str(HERE / "converted.R")]]
    with tempfile.TemporaryDirectory(prefix="widths-tests-", dir=ROOT / "scratch") as tmp:
        work = Path(tmp)
        for case in TRACES:
            source = ROOT / "packet" / "cases" / case
            have = read_table(source / "have.csv", list(mod.INPUT_COLUMNS), ("flag",))
            before = copy.deepcopy(have)
            truth = expected(case)
            got = mod.translate({"have": have})
            compare(got, truth)
            assert have == before
            compare(mod.translate({"have": []}), expected("empty"))
            compare(mod.translate({"have": have}), truth)
            write_tables(work / (case + "-truth"), truth)
            for language, executable in zip(("python", "r"), executables):
                destination = work / (case + "-" + language)
                cli(executable, source, destination)
                reopened = {name: read_table(destination / (name + ".csv"), columns,
                           ("n", "z") if name == "want" else ("bytes",) if name == "descriptor" else ())
                            for name, columns in HEADERS.items()}
                compare(reopened, truth)
                old_bytes = {p.name: p.read_bytes() for p in destination.iterdir()}
                cli(executable, source, destination, success=False)
                assert old_bytes == {p.name: p.read_bytes() for p in destination.iterdir()}
                occupied_file = work / (case + "-" + language + "-occupied")
                occupied_file.write_bytes(b"keep this file")
                cli(executable, source, occupied_file, success=False)
                assert occupied_file.read_bytes() == b"keep this file"
        # Repeated identifiers are independent observations; all printable bytes survive
        # the transport in an opaque identifier, including leading/trailing spaces.
        ascii_id = "".join(map(chr, range(32, 127))) + " "
        extra = [{"row_id": ascii_id, "raw": "NA    ", "suffix": ',"', "flag": flag}
                 for flag in (0, 1)]
        extra_dir = work / "ascii-input"
        extra_dir.mkdir()
        with (extra_dir / "have.csv").open("w", newline="", encoding="ascii") as handle:
            writer = csv.DictWriter(handle, mod.INPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(extra)
        extra_truth = {
            "stage": [dict(zip(HEADERS["stage"], (ascii_id, "NA ", 'NA ," ', tag)))
                      for tag in ("L", "Y")],
            "want": [dict(zip(HEADERS["want"], (ascii_id, "NA   ", "NA", "[NA   ] ", 'NA ," ', tag, 2, 2)))
                     for tag in ("L", "Y")],
            "descriptor": expected("empty")["descriptor"],
        }
        compare(mod.translate({"have": extra}), extra_truth)
        write_tables(work / "ascii-truth", extra_truth)
        for language, executable in zip(("python", "r"), executables):
            destination = work / ("ascii-" + language)
            cli(executable, extra_dir, destination)
            reopened = {name: read_table(destination / (name + ".csv"), columns,
                        ("n", "z") if name == "want" else ("bytes",) if name == "descriptor" else ())
                        for name, columns in HEADERS.items()}
            compare(reopened, extra_truth)
        # Input-domain rejection happens before destination creation.
        for index, (column, value) in enumerate((
            ("raw", "short"), ("suffix", "\x00 "), ("raw", "AB\t   "),
            ("row_id", ""), ("row_id", "caf\u00e9"), ("flag", 2), ("flag", None))):
            bad = dict(extra[0])
            bad[column] = value
            try:
                mod.translate({"have": [bad]})
            except ValueError:
                pass
            else:
                raise AssertionError((column, value))
            bad_dir = work / ("bad-input-" + str(index))
            bad_dir.mkdir()
            with (bad_dir / "have.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, mod.INPUT_COLUMNS)
                writer.writeheader()
                writer.writerow(bad)
            for language, executable in zip(("python", "r"), executables):
                destination = work / ("bad-" + str(index) + "-" + language)
                cli(executable, bad_dir, destination, success=False)
                assert not destination.exists()
        # Comparator sensitivity: one plausible wrong output for each trap.
        for name, column, wrong in (("stage", "tag", "LONG"), ("stage", "joined", "ABCZ "),
                                    ("want", "short", "ABC! "), ("want", "short", "ABCDE"),
                                    ("want", "copy", "ABC"), ("want", "wrapped", "[ABC]   ")):
            mutant = copy.deepcopy(expected("main"))
            mutant[name][0][column] = wrong
            try:
                compare(mutant, expected("main"))
            except AssertionError:
                pass
            else:
                raise AssertionError("undetected mutant")
        for column, wrong in (("n", 0), ("z", 1)):
            mutant = copy.deepcopy(expected("blank"))
            mutant["want"][0][column] = wrong
            try:
                compare(mutant, expected("blank"))
            except AssertionError:
                pass
            else:
                raise AssertionError("undetected blank mutant")
        rtest = subprocess.run(["Rscript", "--vanilla", str(HERE / "selftest.R"), str(work)],
                               text=True, capture_output=True)
        assert rtest.returncode == 0, (rtest.stdout, rtest.stderr)
        print(rtest.stdout.strip())
    print("PASS: Python API; 5 supplied cases; 2 supplemental rows; both CLIs; 7 domain rejections per CLI; 8 rejected mutants")


if __name__ == "__main__":
    run()
