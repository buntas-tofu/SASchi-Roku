"""Bounded decoded-JSON to Parquet preservation implementation.

Engineering evaluation code. This does not read SAS binaries.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import struct

import pyarrow as pa
import pyarrow.parquet as pq


NAMES = ("id", "text", "value", "date", "stamp", "all_missing", "status")
SOURCE_TYPES = ("char", "char", "numeric", "date", "numeric", "numeric", "numeric")
SCHEMA = pa.schema([(name, dtype) for name, dtype in zip(NAMES, (
    pa.string(), pa.string(), pa.float64(), pa.date32(), pa.float64(),
    pa.float64(), pa.float64()))])
TAGS = frozenset([".", "._"] + ["." + chr(c) for c in range(65, 91)])
DAY_OFFSET = -3653  # 1960-01-01 relative to the Parquet epoch 1970-01-01.
DESCRIPTOR_KEYS = frozenset(("name", "source_type", "byte_width", "label",
    "format", "informat", "units", "origin", "timezone", "value_labels"))
REQUIRED_METADATA = frozenset(("version", "policy", "source_format", "encoding",
    "columns", "row_count", "source_sha256", "parquet_sha256", "missing_tags",
    "versions"))
BINDING_KEY = b"preserve-v1:companion_sha256"


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON object key: " + key)
        result[key] = value
    return result


def _bad_constant(value):
    raise ValueError("non-finite JSON constant: " + value)


def _json(raw):
    return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=_pairs,
        parse_constant=_bad_constant,
        parse_int=lambda s: -0.0 if s == "-0" else int(s))


def _canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode("ascii")


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _hash_string(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _finite(value, where):
    _require(type(value) in (int, float), where + ": expected a JSON number")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(where + ": not binary64-compatible") from exc
    _require(math.isfinite(number), where + ": non-finite number")
    if type(value) is int:
        _require(int(number) == value, where + ": integer loses binary64 precision")
    return number


def _descriptor(source_format, encoding, columns):
    _require(isinstance(source_format, str) and bool(source_format),
        "source_format must be a nonempty string")
    _require(encoding in ("utf-8", "latin-1"), "unsupported encoding")
    _require(type(columns) is list and len(columns) == len(NAMES),
        "expected seven ordered descriptor columns")
    for index, column in enumerate(columns):
        _require(type(column) is dict and DESCRIPTOR_KEYS <= column.keys(),
            "absent descriptor properties")
        _require(column["name"] == NAMES[index], "wrong or duplicate column name/order")
        _require(column["source_type"] == SOURCE_TYPES[index], "wrong source_type")
        width = column["byte_width"]
        if index < 2:
            _require(type(width) is int and width >= 0, "invalid character byte_width")
        else:
            _require(width is None or (type(width) is int and width >= 0),
                "invalid numeric byte_width")
        for key in ("label", "format", "informat", "units", "origin", "timezone"):
            _require(column[key] is None or isinstance(column[key], str),
                "invalid descriptor property: " + key)
        labels = column["value_labels"]
        _require(labels is None or type(labels) is dict, "invalid value_labels")
        if labels is not None:
            for value, label in labels.items():
                _require(isinstance(value, str) and isinstance(label, str),
                    "invalid value-label entry")
                try:
                    number = float(value)
                except ValueError as exc:
                    raise ValueError("non-numeric value-label key") from exc
                _require(math.isfinite(number), "non-finite value-label key")
    # This also rejects non-JSON descriptor extensions rather than inventing values.
    _canonical(columns)


def _missing(cell):
    return type(cell) is dict and set(cell) == {"missing"}


def _build(source):
    _require(type(source) is dict and set(source) == {
        "source_format", "encoding", "columns", "rows"}, "invalid source fields")
    _descriptor(source["source_format"], source["encoding"], source["columns"])
    rows = source["rows"]
    _require(type(rows) is list, "rows must be an array")
    values = [[] for unused in NAMES]
    tags = []
    for row_index, row in enumerate(rows):
        _require(type(row) is list and len(row) == len(NAMES), "invalid row width")
        for col_index, cell in enumerate(row):
            name = NAMES[col_index]
            where = "row %d column %s" % (row_index, name)
            if col_index < 2:
                _require(type(cell) is dict and set(cell) == {"hex"}
                    and isinstance(cell["hex"], str)
                    and re.fullmatch(r"(?:[0-9a-fA-F]{2})*", cell["hex"]) is not None,
                    where + ": expected exact hexadecimal bytes")
                raw = bytes.fromhex(cell["hex"])
                _require(len(raw) == source["columns"][col_index]["byte_width"],
                    where + ": source byte width mismatch")
                decoded = raw.decode(source["encoding"], "strict")
                _require(decoded.encode(source["encoding"], "strict") == raw,
                    where + ": nonreversible decoding")
                values[col_index].append(decoded)
            elif _missing(cell):
                _require(isinstance(cell["missing"], str) and cell["missing"] in TAGS,
                    where + ": invalid missing tag")
                values[col_index].append(None)
                tags.append({"row": row_index, "column": name, "tag": cell["missing"]})
            elif col_index == 3:
                number = _finite(cell, where)
                _require(number.is_integer(), where + ": fractional source date")
                day = int(number) + DAY_OFFSET
                _require(-(2 ** 31) <= day < 2 ** 31, where + ": date32 overflow")
                values[col_index].append(day)
            else:
                values[col_index].append(_finite(cell, where))
    arrays = []
    for index, field in enumerate(SCHEMA):
        if index == 3:
            arrays.append(pa.array(values[index], type=pa.int32()).cast(pa.date32()))
        else:
            arrays.append(pa.array(values[index], type=field.type))
    return pa.Table.from_arrays(arrays, schema=SCHEMA), tags


def _binding(metadata):
    return _sha(_canonical({k: v for k, v in metadata.items() if k != "parquet_sha256"}))


def _read_validated(bundle_dir, expected_source_sha256):
    _require(_hash_string(expected_source_sha256), "invalid expected source SHA-256")
    bundle = Path(bundle_dir)
    metadata = _json((bundle / "metadata.json").read_bytes())
    _require(type(metadata) is dict and REQUIRED_METADATA <= metadata.keys(),
        "absent required metadata")
    _require(type(metadata["version"]) is int and metadata["version"] == 1,
        "invalid metadata version")
    _require(metadata["policy"] == "preserve-v1", "invalid policy")
    _descriptor(metadata["source_format"], metadata["encoding"], metadata["columns"])
    _require(type(metadata["row_count"]) is int and metadata["row_count"] >= 0,
        "invalid row_count")
    for key in ("source_sha256", "parquet_sha256"):
        _require(_hash_string(metadata[key]), "malformed " + key)
    _require(metadata["source_sha256"] == expected_source_sha256, "wrong source identity")
    versions = metadata["versions"]
    _require(type(versions) is dict and all(isinstance(versions.get(k), str)
        and bool(versions[k]) for k in ("python", "pyarrow")), "malformed runtime versions")
    raw = (bundle / "data.parquet").read_bytes()
    _require(_sha(raw) == metadata["parquet_sha256"], "changed Parquet hash")
    # Read exactly the bytes hashed above, avoiding directory partition inference.
    table = pq.read_table(pa.BufferReader(raw))
    _require(table.schema.equals(SCHEMA, check_metadata=False), "wrong ordered schema")
    _require(table.num_rows == metadata["row_count"], "row count mismatch")
    _require((table.schema.metadata or {}).get(BINDING_KEY)
        == _binding(metadata).encode("ascii"), "companion binding mismatch")
    tags = metadata["missing_tags"]
    _require(type(tags) is list, "missing_tags must be an array")
    indexed = {}
    previous = (-1, -1)
    for item in tags:
        _require(type(item) is dict and set(item) == {"row", "column", "tag"},
            "malformed missing tag")
        row, column, tag = item["row"], item["column"], item["tag"]
        _require(type(row) is int and 0 <= row < table.num_rows, "tag row out of range")
        _require(isinstance(column, str) and column in NAMES[2:], "unknown tag column")
        _require(isinstance(tag, str) and tag in TAGS, "unknown missing tag")
        key = (row, NAMES.index(column))
        _require(key not in indexed, "duplicate missing tag")
        _require(key > previous, "tags are not ordered row-major")
        previous = key
        _require(not table.column(column)[row].is_valid, "tag on non-null cell")
        indexed[key] = tag
    for col_index, name in enumerate(NAMES):
        column = table.column(name)
        if col_index == 3:
            column = column.cast(pa.int32())
        for row_index, cell in enumerate(column):
            if not cell.is_valid:
                _require(col_index >= 2 and (row_index, col_index) in indexed,
                    "null cell lacks exactly one missing tag")
            elif col_index < 2:
                raw_text = cell.as_py().encode(metadata["encoding"], "strict")
                _require(len(raw_text) == metadata["columns"][col_index]["byte_width"],
                    "reopened character width mismatch")
            elif col_index != 3:
                _require(math.isfinite(cell.as_py()), "non-finite reopened numeric value")
    return metadata, table, indexed


def validate(bundle_dir, expected_source_sha256):
    """Validate the complete bundle against an independently supplied source hash."""
    metadata, unused_table, unused_tags = _read_validated(bundle_dir, expected_source_sha256)
    return {"row_count": metadata["row_count"], "source_sha256": metadata["source_sha256"],
        "parquet_sha256": metadata["parquet_sha256"], "policy": metadata["policy"]}


def restore(bundle_dir, expected_source_sha256):
    """Validate, reopen the actual Parquet bytes, and reconstruct decoded source data."""
    validate(bundle_dir, expected_source_sha256)
    metadata, table, tags = _read_validated(bundle_dir, expected_source_sha256)
    columns = [table.column(name).cast(pa.int32()).to_pylist() if index == 3
        else table.column(name).to_pylist() for index, name in enumerate(NAMES)]
    rows = []
    for row_index in range(table.num_rows):
        row = []
        for col_index in range(len(NAMES)):
            value = columns[col_index][row_index]
            if value is None:
                row.append({"missing": tags[(row_index, col_index)]})
            elif col_index < 2:
                row.append({"hex": value.encode(metadata["encoding"], "strict").hex()})
            elif col_index == 3:
                row.append(value - DAY_OFFSET)
            else:
                row.append(value)
        rows.append(row)
    return {"source_format": metadata["source_format"], "encoding": metadata["encoding"],
        "columns": metadata["columns"], "rows": rows}


def _same_source(source, restored):
    _require(all(source[key] == restored[key] for key in ("source_format", "encoding", "columns")),
        "descriptor round-trip mismatch")
    _require(len(source["rows"]) == len(restored["rows"]), "row count round-trip mismatch")
    for row, output in zip(source["rows"], restored["rows"]):
        for index, (before, after) in enumerate(zip(row, output)):
            if index < 2:
                _require(bytes.fromhex(before["hex"]) == bytes.fromhex(after["hex"]),
                    "character byte round-trip mismatch")
            elif type(before) is dict:
                _require(before == after, "missing tag round-trip mismatch")
            elif index == 3:
                _require(before == after, "date round-trip mismatch")
            else:
                _require(struct.pack("<d", before) == struct.pack("<d", after),
                    "binary64 round-trip mismatch")


def convert(source_path, destination_dir):
    """Write a new bundle, refusing existing destinations and malformed input."""
    destination = Path(destination_dir)
    if os.path.lexists(destination):
        raise FileExistsError("destination already exists")
    source_raw = Path(source_path).read_bytes()
    source = _json(source_raw)
    table, tags = _build(source)
    metadata = {"version": 1, "policy": "preserve-v1",
        "source_format": source["source_format"], "encoding": source["encoding"],
        "columns": source["columns"], "row_count": len(source["rows"]),
        "source_sha256": _sha(source_raw), "missing_tags": tags,
        "versions": {"python": platform.python_version(), "pyarrow": pa.__version__}}
    table = table.replace_schema_metadata({BINDING_KEY: _binding(metadata).encode("ascii")})
    sink = pa.BufferOutputStream()
    # Plain numeric encoding retains the binary64 sign bit on both zero values.
    pq.write_table(table, sink, version="2.6", compression="NONE", use_dictionary=False)
    parquet_raw = sink.getvalue().to_pybytes()
    metadata["parquet_sha256"] = _sha(parquet_raw)
    metadata_raw = json.dumps(metadata, ensure_ascii=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    # All source and writer checks precede creation of the destination directory.
    destination.mkdir()
    try:
        (destination / "data.parquet").write_bytes(parquet_raw)
        (destination / "metadata.json").write_bytes(metadata_raw)
        _same_source(source, restore(destination, metadata["source_sha256"]))
    except BaseException:
        shutil.rmtree(destination)
        raise
    return validate(destination, metadata["source_sha256"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_json")
    parser.add_argument("destination_dir")
    args = parser.parse_args()
    convert(args.source_json, args.destination_dir)


if __name__ == "__main__":
    main()
