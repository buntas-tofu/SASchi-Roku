"""Bounded translation of the supplied DATA step, using ASCII text width 10."""

import argparse
import csv


def translate(rows):
    """Return fresh rows in source order without changing the input dictionaries."""
    result = []
    for row in rows:
        row_id = row["row_id"]
        text = row["text"]
        if not isinstance(row_id, str) or not isinstance(text, str):
            raise TypeError("row_id and text must be decoded strings")
        if len(row_id) > 8:
            raise ValueError("row_id exceeds the width-8 input contract")
        if not text.isascii() or len(text) > 10:
            raise ValueError("text must contain at most 10 ASCII bytes")
        stored_text = text.ljust(10, " ")
        length = max(1, len(stored_text.rstrip(" ")))
        result.append({"row_id": row_id, "text": stored_text, "len": length})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    args = parser.parse_args(argv)
    with open(args.input_csv, encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["row_id", "text"]:
            raise ValueError("input header must be row_id,text")
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values())
               for row in rows):
            raise ValueError("each input record must have exactly two fields")
    converted = translate(rows)
    with open(args.output_csv, "w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=["row_id", "text", "len"])
        writer.writeheader()
        writer.writerows(converted)


if __name__ == "__main__":
    main()
