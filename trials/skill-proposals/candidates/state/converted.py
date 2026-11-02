"""Translation of the supplied two-step SAS slice, using ordinary missing only."""

import csv
from pathlib import Path
import sys


STAGE_COLUMNS = ("row_id", "value", "prev", "total")
WANT_COLUMNS = STAGE_COLUMNS + ("delta",)


def translate(rows):
    """Run fresh step-local state and return independent stage and want rows."""
    total = 10.0
    lag_queue = None
    stage = []
    for row in rows:
        value = None if row["value"] is None else float(row["value"])
        prev = None
        if row["take"] == 1:
            prev, lag_queue = lag_queue, value
        if value is not None:
            total += value
        if row["emit"] == 1:
            stage.append(dict(row_id=row["row_id"], value=value,
                              prev=prev, total=total))

    want = []
    for row in stage:
        delta = (None if row["value"] is None or row["prev"] is None
                 else row["value"] - row["prev"])
        want.append(dict(row, delta=delta))
    return dict(stage=stage, want=want)


def read_input(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [dict(row_id=row["row_id"],
                     value=None if row["value"] == "" else float(row["value"]),
                     take=int(row["take"]), emit=int(row["emit"]))
                for row in csv.DictReader(handle)]


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        raise SystemExit("Usage: converted.py INPUT.csv NEW_OUTPUT_DIRECTORY")
    result = translate(read_input(args[0]))
    directory = Path(args[1])
    directory.mkdir(parents=True, exist_ok=False)
    for name, columns in (("stage", STAGE_COLUMNS), ("want", WANT_COLUMNS)):
        with (directory / (name + ".csv")).open(
                "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(result[name])


if __name__ == "__main__":
    main()
