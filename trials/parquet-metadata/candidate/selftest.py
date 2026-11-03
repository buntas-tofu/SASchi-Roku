"""Candidate self-tests, separate from the unseen parent acceptance.

Run with the supplied Python runtime:
    python selftest.py --packet PACKET_DIR --work NEW_TEMP_DIRECTORY
The work directory is created by this script and must not already exist.
"""

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import sys

import pyarrow as pa
import pyarrow.parquet as pq

import converted as candidate


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def assert_roundtrip(before, after):
    assert {k: v for k, v in before.items() if k != "rows"} == {
        k: v for k, v in after.items() if k != "rows"}
    assert len(before["rows"]) == len(after["rows"])
    for row, output in zip(before["rows"], after["rows"]):
        for index, (expected, actual) in enumerate(zip(row, output)):
            if index < 2:
                assert bytes.fromhex(expected["hex"]) == bytes.fromhex(actual["hex"])
            elif isinstance(expected, dict) or index == 3:
                assert expected == actual
            else:
                assert struct.pack("<d", expected) == struct.pack("<d", actual)


def write_csv(path, headers, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def make_bridge(bundle, output):
    """Self-test adapter, reopening Parquet rather than copying source cells."""
    output.mkdir()
    metadata = json.loads((bundle / "metadata.json").read_text())
    table = pq.read_table(bundle / "data.parquet")
    tags = {(tag["row"], tag["column"]): tag["tag"] for tag in metadata["missing_tags"]}
    cells = []
    for row in range(table.num_rows):
        for index, name in enumerate(table.column_names):
            value = table[name][row].as_py()
            kind = "text_hex" if index < 2 else "date_iso" if name == "date" else "float64_hex"
            if value is None:
                payload = ""
            elif index < 2:
                payload = value.encode("utf-8").hex()
            elif name == "date":
                payload = value.isoformat()
            else:
                payload = struct.pack("<d", value).hex()
            cells.append((row, name, kind, payload, tags.get((row, name), "")))
    properties, labels = [], []
    for descriptor in metadata["columns"]:
        name = descriptor["name"]
        for key, value in descriptor.items():
            if key in ("name", "value_labels"):
                continue
            kind = "null" if value is None else "string" if isinstance(value, str) else "number"
            payload = "" if value is None else value.encode("utf-8").hex() if kind == "string" else str(value)
            properties.append((name, key, kind, payload))
        properties.append((name, "encoding", "string", metadata["encoding"].encode("utf-8").hex()))
        for value, label in (descriptor.get("value_labels") or {}).items():
            labels.append((name, struct.pack("<d", float(value)).hex(), label.encode("utf-8").hex()))
    write_csv(output / "cells.csv", ("row", "column", "kind", "value", "tag"), cells)
    write_csv(output / "columns.csv", ("column", "property", "type", "value"), properties)
    write_csv(output / "labels.csv", ("column", "value_hex", "label_hex"), labels)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    args = parser.parse_args()
    args.work.mkdir()
    here = Path(__file__).resolve().parent
    results = {"status": "candidate self-tests only; independent acceptance not observed",
        "versions": {"python": platform.python_version(), "pyarrow": pa.__version__,
            "r": subprocess.check_output(["Rscript", "--version"], text=True).strip()},
        "valid": [], "invalid": [], "adversarial": [], "additional": []}
    for source in sorted((args.packet / "cases").glob("*.json")):
        raw = source.read_bytes()
        expected = json.loads(raw)
        bundle = args.work / source.stem
        candidate.convert(str(source), str(bundle))
        candidate.validate(bundle, digest(raw))
        assert_roundtrip(expected, candidate.restore(str(bundle), digest(raw)))
        bridge = args.work / (source.stem + "-bridge")
        make_bridge(bundle, bridge)
        receipt = subprocess.check_output(["Rscript", str(here / "consume_selftest.R"),
            str(here / "consume.R"), str(bridge)], text=True).strip()
        results["valid"].append({"case": source.name, "rows": len(expected["rows"]),
            "tags": len(json.loads((bundle / "metadata.json").read_text())["missing_tags"]),
            "r_result": receipt})
    for source in sorted((args.packet / "invalid").glob("*.json")):
        destination = args.work / ("invalid-" + source.stem)
        try:
            candidate.convert(source, destination)
        except Exception as error:
            assert not destination.exists(), "invalid input created destination"
            results["invalid"].append({"case": source.name,
                "exception": type(error).__name__, "message": str(error)})
        else:
            raise AssertionError("invalid case accepted: " + source.name)

    main_source = args.packet / "cases" / "main.json"
    main_hash = digest(main_source.read_bytes())
    original_bundle = args.work / "main"
    original_metadata = json.loads((original_bundle / "metadata.json").read_text())
    mutations = {
        "wrong-source-hash": lambda meta: meta.update(source_sha256="1" * 64),
        "bad-parquet-hash": lambda meta: meta.update(parquet_sha256="0" * 64),
        "absent-versions": lambda meta: meta.pop("versions"),
        "malformed-version": lambda meta: meta.update(version=True),
        "malformed-versions": lambda meta: meta.update(versions={"python": None, "pyarrow": 26}),
        "wrong-row-count": lambda meta: meta.update(row_count=99),
        "duplicate-tag": lambda meta: meta["missing_tags"].append(copy.deepcopy(meta["missing_tags"][0])),
        "out-of-range-tag": lambda meta: meta["missing_tags"][0].update(row=100),
        "unknown-tag": lambda meta: meta["missing_tags"][0].update(tag=".AA"),
        "unknown-tag-column": lambda meta: meta["missing_tags"][0].update(column="bogus"),
        "tag-on-non-null": lambda meta: meta["missing_tags"][0].update(column="value"),
        "untagged-null": lambda meta: meta["missing_tags"].pop(),
        "unordered-tags": lambda meta: meta["missing_tags"].reverse(),
        "malformed-tag-row": lambda meta: meta["missing_tags"][0].update(row=False),
        "changed-descriptor": lambda meta: meta["columns"][0].update(label="altered"),
    }
    def rejection(name, path):
        for function in (candidate.validate, candidate.restore):
            try:
                function(path, main_hash)
            except Exception:
                pass
            else:
                raise AssertionError(name + " was not rejected by " + function.__name__)
        results["adversarial"].append(name)

    for name, mutation in mutations.items():
        path = args.work / ("mutated-" + name)
        shutil.copytree(original_bundle, path)
        metadata = copy.deepcopy(original_metadata)
        mutation(metadata)
        (path / "metadata.json").write_text(json.dumps(metadata))
        rejection(name, path)
        # Rebind structurally valid mutations so individual validation checks,
        # rather than only the companion-integrity check, also get exercised.
        if name not in {"absent-versions", "changed-descriptor", "bad-parquet-hash"}:
            table = pq.read_table(original_bundle / "data.parquet")
            payload = {k: v for k, v in metadata.items() if k != "parquet_sha256"}
            bound = digest(json.dumps(payload, ensure_ascii=True, sort_keys=True,
                separators=(",", ":"), allow_nan=False).encode("ascii"))
            table = table.replace_schema_metadata({b"preserve-v1:companion_sha256": bound.encode("ascii")})
            pq.write_table(table, path / "data.parquet", use_dictionary=False)
            metadata["parquet_sha256"] = digest((path / "data.parquet").read_bytes())
            (path / "metadata.json").write_text(json.dumps(metadata))
            rejection(name + "-rebound", path)

    for name, change in {
        "wrong-schema-type": lambda table: table.set_column(2, "value", table["value"].cast(pa.float32())),
        "wrong-schema-order": lambda table: table.select(list(reversed(table.column_names))),
        "changed-row-count": lambda table: table.slice(0, 1),
    }.items():
        path = args.work / name
        shutil.copytree(original_bundle, path)
        pq.write_table(change(pq.read_table(original_bundle / "data.parquet")), path / "data.parquet")
        metadata = copy.deepcopy(original_metadata)
        metadata["parquet_sha256"] = digest((path / "data.parquet").read_bytes())
        (path / "metadata.json").write_text(json.dumps(metadata))
        rejection(name, path)

    corrupt = args.work / "corrupt-parquet-bytes"
    shutil.copytree(original_bundle, corrupt)
    parquet = bytearray((corrupt / "data.parquet").read_bytes())
    parquet[len(parquet) // 2] ^= 1
    (corrupt / "data.parquet").write_bytes(parquet)
    rejection("corrupt-parquet-bytes", corrupt)
    absent = args.work / "absent-companion"
    shutil.copytree(original_bundle, absent)
    (absent / "metadata.json").unlink()
    rejection("absent-companion", absent)
    malformed = args.work / "malformed-companion"
    shutil.copytree(original_bundle, malformed)
    (malformed / "metadata.json").write_text("{")
    rejection("malformed-companion", malformed)

    snapshot = {p.name: p.read_bytes() for p in original_bundle.iterdir()}
    try:
        candidate.convert(main_source, original_bundle)
    except FileExistsError:
        pass
    else:
        raise AssertionError("existing destination accepted")
    assert snapshot == {p.name: p.read_bytes() for p in original_bundle.iterdir()}
    results["additional"].append("existing destination unchanged")

    standalone = args.work / "standalone-source.json"
    standalone.write_bytes(main_source.read_bytes())
    relocated = args.work / "relocated-bundle"
    candidate.convert(standalone, relocated)
    standalone.unlink()
    renamed = args.work / "bundle-without-source"
    relocated.rename(renamed)
    assert_roundtrip(json.loads(main_source.read_bytes()), candidate.restore(renamed, main_hash))
    results["additional"].append("restoration after relocation and source deletion")

    extra = json.loads(main_source.read_bytes())
    extra["columns"][0]["extension"] = {"unknown": None, "empty": ""}
    extra["rows"][0][2] = 0.0
    extra["rows"][1][2] = -0.0
    extra["rows"][0][4] = 5e-324
    extra["rows"][1][4] = 1.7976931348623157e308
    extra_source = args.work / "extra.json"
    extra_source.write_text(json.dumps(extra))
    extra_bundle = args.work / "extra"
    candidate.convert(extra_source, extra_bundle)
    assert_roundtrip(extra, candidate.restore(extra_bundle, digest(extra_source.read_bytes())))
    results["additional"].append("descriptor extensions, both zero signs, subnormal and maximum finite binary64")
    dates = json.loads(main_source.read_bytes())
    dates["rows"][0][3] = -(2 ** 31) + 3653
    dates["rows"][1][3] = (2 ** 31 - 1) + 3653
    dates_source = args.work / "date-extremes.json"
    dates_source.write_text(json.dumps(dates))
    dates_bundle = args.work / "date-extremes"
    candidate.convert(dates_source, dates_bundle)
    assert_roundtrip(dates, candidate.restore(dates_bundle, digest(dates_source.read_bytes())))
    results["additional"].append("full date32 endpoints in Python")

    nul_id = json.loads(main_source.read_bytes())
    nul_id["rows"][0][0] = {"hex": "41004220"}
    nul_source = args.work / "nul-id.json"
    nul_source.write_text(json.dumps(nul_id))
    nul_bundle = args.work / "nul-id"
    candidate.convert(nul_source, nul_bundle)
    assert_roundtrip(nul_id, candidate.restore(nul_bundle, digest(nul_source.read_bytes())))
    nul_bridge = args.work / "nul-id-bridge"
    make_bridge(nul_bundle, nul_bridge)
    rejected = subprocess.run(["Rscript", "-e",
        "a <- commandArgs(TRUE); source(a[1]); consume(a[2])",
        str(here / "consume.R"), str(nul_bridge)], text=True, capture_output=True)
    assert rejected.returncode != 0 and "embedded NUL" in rejected.stderr
    results["additional"].append("Python preserves NUL id; R visibly rejects its unrepresentable character id")

    source_bridge = args.work / "main-bridge"
    for name, change in {
        "text-tag": lambda rows: rows[0].update(tag=".A"),
        "missing-numeric-payload": lambda rows: rows[2].update(value=""),
        "wrong-cell-order": lambda rows: rows[0].update(row="2"),
    }.items():
        bad_bridge = args.work / ("r-invalid-" + name)
        shutil.copytree(source_bridge, bad_bridge)
        with (bad_bridge / "cells.csv").open(newline="") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames
            rows = list(reader)
        change(rows)
        with (bad_bridge / "cells.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        rejected = subprocess.run(["Rscript", "-e",
            "a <- commandArgs(TRUE); source(a[1]); consume(a[2])",
            str(here / "consume.R"), str(bad_bridge)], text=True, capture_output=True)
        assert rejected.returncode != 0, name
        results["additional"].append("R rejects " + name)

    cli_bundle = args.work / "cli"
    subprocess.run([sys.executable, str(here / "converted.py"), str(main_source), str(cli_bundle)], check=True)
    assert_roundtrip(json.loads(main_source.read_bytes()), candidate.restore(cli_bundle, main_hash))
    results["additional"].append("conversion CLI")
    (args.work / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
