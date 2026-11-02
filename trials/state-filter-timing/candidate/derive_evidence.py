"""Materialize independently hand-derived fixtures before implementing repair."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLS = ["row_id", "value", "prev", "total"]

# These literal expectations were traced from source.sas, not from a target run.
EXPECTED = {
    "main": {
        "where_path": [["r9", 5, None, 15], ["r8", None, 5, 15],
                       ["r4", 3, None, 18], ["r6", 9, 3, 27],
                       ["r7", -4, 9, 23]],
        "if_path": [["r9", 5, None, 15], ["r8", None, 100, 115],
                    ["r4", 3, 7, 125], ["r6", 9, 3, 134],
                    ["r7", -4, 2, 132]],
    },
    "leading": {
        "where_path": [["NA", 8, None, 18]],
        "if_path": [["NA", 8, 100, 118]],
    },
    "single": {
        "where_path": [["s1", 8, None, 18]],
        "if_path": [["s1", 8, None, 18]],
    },
    "all-missing": {
        "where_path": [["m1", None, None, 10], ["m3", None, None, 10]],
        "if_path": [["m1", None, None, 10], ["m3", None, None, 10]],
    },
    "empty": {"where_path": [], "if_path": []},
    "silent": {"where_path": [], "if_path": []},
}

# One row per physical input position. "not reached" differs from numeric missing.
# Fields: row_id, eligible, executes, queue_before, prev, queue_after,
#         total_before, total_after, output_position.
MAIN_TRACE = {
    "where_path": [
        ["r9", 1, True, None, None, 5, 10, 15, 1],
        ["r2", 0, False, 5, "not reached", 5, 15, 15, None],
        ["r8", 1, True, 5, 5, None, 15, 15, 2],
        ["r1", 0, False, None, "not reached", None, 15, 15, None],
        ["r4", 1, True, None, None, 3, 15, 18, 3],
        ["r6", 1, True, 3, 3, 9, 18, 27, 4],
        ["r3", 0, False, 9, "not reached", 9, 27, 27, None],
        ["r7", 1, True, 9, 9, -4, 27, 23, 5],
    ],
    "if_path": [
        ["r9", 1, True, None, None, 5, 10, 15, 1],
        ["r2", 0, True, 5, 5, 100, 15, 115, None],
        ["r8", 1, True, 100, 100, None, 115, 115, 2],
        ["r1", 0, True, None, None, 7, 115, 122, None],
        ["r4", 1, True, 7, 7, 3, 122, 125, 3],
        ["r6", 1, True, 3, 3, 9, 125, 134, 4],
        ["r3", 0, True, 9, 9, 2, 134, 136, None],
        ["r7", 1, True, 2, 2, -4, 136, 132, 5],
    ],
}


def main():
    expected_dir = ROOT / "evidence" / "hand_expected"
    expected_dir.mkdir(exist_ok=False)
    for name, tables in EXPECTED.items():
        typed = {path: [dict(zip(COLS, row)) for row in rows]
                 for path, rows in tables.items()}
        (expected_dir / (name + ".json")).write_text(
            json.dumps(typed, indent=2) + "\n", encoding="utf-8")
        folder = expected_dir / name
        folder.mkdir()
        for path, rows in typed.items():
            with (folder / (path + ".csv")).open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=COLS)
                writer.writeheader()
                writer.writerows(rows)
    header = ["path", "input_position", "row_id", "eligible", "lag_and_sum_reached",
              "queue_before", "prev_assigned", "queue_after", "total_before",
              "total_after", "output_position"]
    with (ROOT / "evidence" / "main_hand_trace.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        for path, rows in MAIN_TRACE.items():
            for pos, row in enumerate(rows, 1):
                writer.writerow([path, pos] + row)
    with (ROOT / "evidence" / "history.txt").open("a") as stream:
        stream.write("05. Wrote independent literal expectations for all six fixtures and the physical-row main trace before writing either repair. No target implementation generated these expectations.\n")
    print("Wrote hand-derived expectations for 6 fixtures and 16 main trace rows.")


if __name__ == "__main__":
    main()
