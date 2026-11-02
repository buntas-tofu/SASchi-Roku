#!/usr/bin/env python3
"""Reversible synthetic-envelope CSV bundle, using Python 3.11+ stdlib only."""

import argparse
import csv
from decimal import Decimal
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys


HEADER = ["row_no", "id", "text", "amount", "event_day"]
ENCODINGS = {"windows-1252": "cp1252", "cp1252": "cp1252"}
MISSING_TAG = re.compile(r"\.(?:[A-Z_])?\Z")
HEX = re.compile(r"(?:[0-9a-fA-F]{2})*\Z")


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def reject_constant(value):
    raise ContractError(f"Nonfinite JSON number is unsupported: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON property: {key}")
        result[key] = value
    return result


def read_json_bytes(data):
    return json.loads(data.decode("utf-8"), parse_float=Decimal,
                      parse_constant=reject_constant, object_pairs_hook=unique_object)


def json_text(value):
    """Write exact JSON decimal values without binary-float conversion."""
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True)
    if type(value) is int:
        return str(value)
    if isinstance(value, Decimal):
        require(value.is_finite(), "Nonfinite decimal is unsupported")
        return str(value)
    if type(value) is list:
        return "[" + ",".join(json_text(item) for item in value) + "]"
    if type(value) is dict:
        return "{" + ",".join(json_text(k) + ":" + json_text(v)
                              for k, v in value.items()) + "}"
    raise ContractError(f"Unsupported JSON value type: {type(value).__name__}")


def json_bytes(value):
    return (json_text(value) + "\n").encode("utf-8")


def same_value(left, right):
    """Type-sensitive JSON comparison, independent of object property order."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (left.keys() == right.keys()
                and all(same_value(left[k], right[k]) for k in left))
    if type(left) is list:
        return len(left) == len(right) and all(same_value(a, b) for a, b in zip(left, right))
    return left == right


def numeric(value, name):
    require(type(value) is int or isinstance(value, Decimal),
            f"{name} must be a finite JSON number, not text, bool or null")
    if isinstance(value, Decimal):
        require(value.is_finite(), f"{name} must be finite")
    return str(value)


def expected(source_bytes):
    source = read_json_bytes(source_bytes)
    require(type(source) is dict, "Source must be a JSON object")
    descriptor = source.get("descriptor")
    rows = source.get("rows")
    require(type(descriptor) is dict, "descriptor must be an object")
    require(type(rows) is list, "rows must be a list")
    encoding = descriptor.get("encoding")
    require(type(encoding) is str and encoding.lower() in ENCODINGS,
            "Unsupported encoding; supported names are windows-1252 and cp1252")
    codec = ENCODINGS[encoding.lower()]
    columns = descriptor.get("columns")
    require(type(columns) is list and len(columns) == 4
            and all(type(c) is dict for c in columns),
            "descriptor.columns must contain the four column descriptors")
    require([c.get("name") for c in columns] == HEADER[1:],
            "Source columns must be ordered id,text,amount,event_day")
    for column, kind in zip(columns, ["character", "character", "numeric", "numeric"]):
        require(column.get("type") == kind, f"Wrong physical type for {column['name']}")
    for column in columns[:2]:
        width = column.get("width_bytes")
        require(type(width) is int and width >= 0,
                f"{column['name']}.width_bytes must be a nonnegative integer")
    require(type(columns[3].get("unit")) is str and bool(columns[3]["unit"]),
            "event_day must declare its raw units")

    table = [HEADER.copy()]
    companions = []
    seen = set()
    for index, row in enumerate(rows):
        require(type(row) is dict, f"Row {index} must be an object")
        require(all(key in row for key in ["row_no", "id", "text_hex", "amount", "event_day"]),
                f"Row {index} lacks a required property")
        row_no = row["row_no"]
        require(type(row_no) is int, f"Row {index}: row_no must be an integer")
        require(row_no not in seen, f"Duplicate row_no: {row_no}")
        seen.add(row_no)
        identifier = row["id"]
        require(type(identifier) is str, f"Row {row_no}: id must be text")
        require("\0" not in identifier, f"Row {row_no}: id contains NUL")
        try:
            id_bytes = identifier.encode(codec, errors="strict")
        except UnicodeEncodeError as error:
            raise ContractError(f"Row {row_no}: id is not representable in {encoding}") from error
        require(len(id_bytes) <= columns[0]["width_bytes"],
                f"Row {row_no}: id exceeds descriptor byte width")
        raw_hex = row["text_hex"]
        require(type(raw_hex) is str and HEX.fullmatch(raw_hex) is not None,
                f"Row {row_no}: text_hex must be contiguous pairs of hex digits")
        raw = bytes.fromhex(raw_hex)
        require(len(raw) <= columns[1]["width_bytes"],
                f"Row {row_no}: text exceeds descriptor byte width")
        try:
            decoded = raw.decode(codec, errors="strict")
        except UnicodeDecodeError:
            decoded = None
        mode = "raw" if decoded is None or "\0" in decoded else "decoded"
        text_cell = "" if mode == "raw" else decoded
        amount = row["amount"]
        if type(amount) is dict:
            require(set(amount) == {"missing"} and type(amount["missing"]) is str
                    and MISSING_TAG.fullmatch(amount["missing"]) is not None,
                    f"Row {row_no}: missing amount must have one original SAS tag")
            amount_cell = ""
            missing = amount["missing"]
        else:
            amount_cell = numeric(amount, f"Row {row_no} amount")
            missing = None
        event_day = numeric(row["event_day"], f"Row {row_no} event_day")
        table.append([str(row_no), identifier, text_cell, amount_cell, event_day])
        companions.append({"row_no": row_no, "text_mode": mode,
                           "text_raw_hex": raw.hex(), "amount_missing": missing})
    stream = io.StringIO(newline="")
    csv.writer(stream, delimiter=",", quotechar='"', doublequote=True,
               quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n").writerows(table)
    data = stream.getvalue().encode("utf-8")
    metadata = {"source_sha256": sha256(source_bytes), "data_sha256": sha256(data),
                "descriptor": descriptor, "rows": companions}
    return data, metadata, table


def check(source_path, directory):
    source_bytes = Path(source_path).read_bytes()
    wanted_data, wanted_metadata, wanted_table = expected(source_bytes)
    directory = Path(directory)
    require(directory.is_dir() and not directory.is_symlink(), "Bundle must be a real directory")
    for name in ("data.csv", "metadata.json", "source.json"):
        path = directory / name
        require(path.is_file() and not path.is_symlink(), f"Missing or linked bundle file: {name}")
    data = (directory / "data.csv").read_bytes()
    metadata = read_json_bytes((directory / "metadata.json").read_bytes())
    require(type(metadata) is dict, "metadata.json must be an object")
    require(metadata.get("source_sha256") == sha256(source_bytes), "Source hash mismatch")
    require(metadata.get("data_sha256") == sha256(data), "Data hash mismatch")
    require(same_value(metadata, wanted_metadata), "Metadata differs from source-derived contract")
    require((directory / "source.json").read_bytes() == source_bytes,
            "Archived source bytes differ from supplied source")
    csv.field_size_limit(sys.maxsize)
    actual_table = list(csv.reader(io.StringIO(data.decode("utf-8"), newline=""),
                                  delimiter=",", quotechar='"', doublequote=True, strict=True))
    require(actual_table == wanted_table, "CSV fields, positions or order differ from source")
    require(data == wanted_data, "CSV transport bytes are not the canonical source projection")
    return {"status": "checked", "row_count": len(wanted_table) - 1,
            "source_sha256": sha256(source_bytes), "data_sha256": sha256(data)}


def build(source_path, directory):
    destination = Path(directory)
    require(not os.path.lexists(destination), "Destination already exists")
    source_bytes = Path(source_path).read_bytes()
    data, metadata, unused_table = expected(source_bytes)
    require(destination.parent.is_dir(), "Destination parent directory must exist")
    # mkdir is the exclusive reservation; all source validation precedes it.
    destination.mkdir()
    try:
        (destination / "data.csv").write_bytes(data)
        (destination / "metadata.json").write_bytes(json_bytes(metadata))
        (destination / "source.json").write_bytes(source_bytes)
        result = check(source_path, destination)
    except BaseException:
        shutil.rmtree(destination)
        raise
    result["status"] = "built-and-checked"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "check"])
    parser.add_argument("source", type=Path)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.exit(2, "error: Python 3.11+ is required\n")
    try:
        result = (build if args.action == "build" else check)(args.source, args.directory)
    except (ContractError, OSError, ValueError, TypeError, KeyError, csv.Error, OverflowError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
