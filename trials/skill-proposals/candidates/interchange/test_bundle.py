#!/usr/bin/env python3
"""Independent CLI checks; all generated fixtures and trials stay in output."""
import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "packet"
PROGRAM = HERE / "bundle.py"
RESULTS = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cli(action, source, destination, success=True):
    run = subprocess.run([sys.executable, str(PROGRAM), action, str(source), str(destination)],
                         capture_output=True, text=True)
    if success:
        assert run.returncode == 0, run.stderr
        return json.loads(run.stdout)
    assert run.returncode != 0, "Invalid bundle/source was accepted"
    assert run.stderr.startswith("error:"), run.stderr
    return run.stderr.strip()


def test(name, function):
    try:
        details = function()
        RESULTS.append({"test": name, "status": "PASS", "details": details})
    except Exception as error:
        RESULTS.append({"test": name, "status": "FAIL", "details": repr(error)})


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True), encoding="utf-8")


def read_table(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.reader(file, strict=True))


def main():
    main_source = PACKET / "main.json"
    empty_source = PACKET / "empty.json"
    fixture = json.loads(main_source.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="selftest-", dir=HERE) as temp:
        root = Path(temp)
        main_bundle = root / "main"
        empty_bundle = root / "empty"
        test("build main CLI", lambda: cli("build", main_source, main_bundle))
        test("check main CLI", lambda: cli("check", main_source, main_bundle))
        test("build empty CLI", lambda: cli("build", empty_source, empty_bundle))
        test("check empty CLI", lambda: cli("check", empty_source, empty_bundle))

        def literal_main():
            assert read_table(main_bundle / "data.csv") == [
                ["row_no", "id", "text", "amount", "event_day"],
                ["1", "0012", "A\r\nB  ", "1.25", "0"],
                ["2", "0012", "", "", "1"],
                ["3", "0003", "é     ", "", "-1"],
                ["4", "0004", "", "0", "2"],
            ]
            meta = json.loads((main_bundle / "metadata.json").read_text())
            assert meta["descriptor"] == fixture["descriptor"]
            assert meta["rows"] == [
                {"row_no": 1, "text_mode": "decoded", "text_raw_hex": "410d0a422020", "amount_missing": None},
                {"row_no": 2, "text_mode": "raw", "text_raw_hex": "410042202020", "amount_missing": ".A"},
                {"row_no": 3, "text_mode": "decoded", "text_raw_hex": "e92020202020", "amount_missing": "."},
                {"row_no": 4, "text_mode": "raw", "text_raw_hex": "812020202020", "amount_missing": None},
            ]
            assert (main_bundle / "source.json").read_bytes() == main_source.read_bytes()
            assert meta["source_sha256"] == digest(main_source)
            assert meta["data_sha256"] == digest(main_bundle / "data.csv")
            return "4 rows compared literally, including all fields, duplicate id and raw bytes"
        test("independent literal main contents and hashes", literal_main)

        def literal_empty():
            assert (empty_bundle / "data.csv").read_bytes() == b"row_no,id,text,amount,event_day\r\n"
            meta = json.loads((empty_bundle / "metadata.json").read_text())
            assert meta["rows"] == []
            assert meta["descriptor"] == fixture["descriptor"]
            assert (empty_bundle / "source.json").read_bytes() == empty_source.read_bytes()
        test("empty header, descriptor and exact source snapshot", literal_empty)

        def byte_domain():
            source = copy.deepcopy(fixture)
            source["descriptor"]["columns"][1]["width_bytes"] = 1
            source["rows"] = [{"row_no": 300 - i, "id": f"{i:04}", "text_hex": f"{i:02x}",
                               "amount": {"missing": ".A"}, "event_day": i - 128}
                              for i in range(256)]
            path, dest = root / "bytes.json", root / "bytes"
            dump(path, source)
            cli("build", path, dest)
            cli("check", path, dest)
            table = read_table(dest / "data.csv")[1:]
            rows = json.loads((dest / "metadata.json").read_text())["rows"]
            fallback = {0, 0x81, 0x8d, 0x8f, 0x90, 0x9d}
            for value, (row, companion) in enumerate(zip(table, rows)):
                raw = bytes([value])
                assert companion["row_no"] == 300 - value
                assert bytes.fromhex(companion["text_raw_hex"]) == raw
                assert companion["text_mode"] == ("raw" if value in fallback else "decoded")
                assert row == [str(300 - value), f"{value:04}",
                               "" if value in fallback else raw.decode("cp1252"), "", str(value - 128)]
                assert companion["amount_missing"] == ".A"
            return "256 source bytes; 6 raw fallbacks; all amount cells missing; nonascending positions retained"
        test("exhaustive single-byte domain and all-missing amounts", byte_domain)

        def text_sequences():
            payloads = [b'a"b,c', b"a\rb", b"a\nb", b"a\r\nb", b"NA", b"", b"  ", b"\tA \r\n", b"\\n"]
            tags = [".", "._"] + ["." + chr(i) for i in range(ord("A"), ord("Z") + 1)]
            source = copy.deepcopy(fixture)
            source["descriptor"]["extra_property"] = {"unavailable": None, "numeric": 12, "flags": [True, False]}
            source["rows"] = [{"row_no": i * 3, "id": "0012", "text_hex": payloads[i % len(payloads)].hex(),
                               "amount": {"missing": tag}, "event_day": -3}
                              for i, tag in enumerate(tags)]
            path, dest = root / "controls.json", root / "controls"
            dump(path, source)
            cli("build", path, dest)
            cli("check", path, dest)
            rows = read_table(dest / "data.csv")[1:]
            meta = json.loads((dest / "metadata.json").read_text())
            assert meta["descriptor"] == source["descriptor"]
            for i, (row, companion) in enumerate(zip(rows, meta["rows"])):
                assert row[2] == payloads[i % len(payloads)].decode("cp1252")
                assert companion["text_mode"] == "decoded"
                assert companion["amount_missing"] == tags[i]
            return "28 tags, 9 text sequences, arbitrary descriptor property, duplicate identifiers"
        test("quotes, delimiters, CR LF CRLF, empty and literal text, all SAS tags", text_sequences)

        def exact_decimal():
            source = copy.deepcopy(fixture)
            source["rows"] = [source["rows"][0]]
            text = json.dumps(source).replace('"amount": 1.25', '"amount": 9007199254740993.1234567890123456789')
            text = text.replace('"event_day": 0', '"event_day": -0.125')
            path, dest = root / "decimal.json", root / "decimal"
            path.write_text(text)
            cli("build", path, dest)
            cli("check", path, dest)
            assert read_table(dest / "data.csv")[1][3:] == ["9007199254740993.1234567890123456789", "-0.125"]
            return "Exact decimal digits and fractional raw day counts; no binary-float conversion"
        test("exact decimal amount and fractional raw day", exact_decimal)

        mutations = {
            "unsupported encoding": lambda s: s["descriptor"].update(encoding="UTF-8"),
            "unknown encoding": lambda s: s["descriptor"].update(encoding="unknown-codec"),
            "overwidth text": lambda s: s["rows"][0].update(text_hex="41" * 7),
            "duplicate row_no": lambda s: s["rows"][1].update(row_no=1),
            "boolean row_no": lambda s: s["rows"][0].update(row_no=True),
            "numeric id": lambda s: s["rows"][0].update(id=12),
            "overwidth id": lambda s: s["rows"][0].update(id="00012"),
            "NUL id": lambda s: s["rows"][0].update(id="A\0B"),
            "odd-length hex": lambda s: s["rows"][0].update(text_hex="1"),
            "nonhex text": lambda s: s["rows"][0].update(text_hex="ZZ"),
            "whitespace hex": lambda s: s["rows"][0].update(text_hex="41 42"),
            "invalid missing tag": lambda s: s["rows"][0].update(amount={"missing": "NA"}),
            "boolean amount": lambda s: s["rows"][0].update(amount=True),
            "null amount without tag": lambda s: s["rows"][0].update(amount=None),
            "missing date units": lambda s: s["descriptor"]["columns"][3].pop("unit"),
        }
        for number, (name, mutate) in enumerate(mutations.items()):
            def reject_source(number=number, mutate=mutate):
                source = copy.deepcopy(fixture)
                mutate(source)
                path, dest = root / f"bad-{number}.json", root / f"bad-{number}"
                dump(path, source)
                message = cli("build", path, dest, False)
                assert not dest.exists(), "Rejected source left an output directory"
                return message
            test("reject source before outputs: " + name, reject_source)

        for name, raw in [("duplicate JSON property", b'{"descriptor":{},"descriptor":{},"rows":[]}'),
                          ("nonfinite JSON", main_source.read_bytes().replace(b"1.25", b"NaN"))]:
            def bad_json(name=name, raw=raw):
                path, dest = root / (name + ".json"), root / name
                path.write_bytes(raw)
                message = cli("build", path, dest, False)
                assert not dest.exists()
                return message
            test("reject source before outputs: " + name, bad_json)

        def existing_destination():
            before = {p.name: p.read_bytes() for p in main_bundle.iterdir()}
            cli("build", main_source, main_bundle, False)
            assert before == {p.name: p.read_bytes() for p in main_bundle.iterdir()}
            occupied_file = root / "occupied-file"
            occupied_file.write_bytes(b"keep")
            cli("build", main_source, occupied_file, False)
            assert occupied_file.read_bytes() == b"keep"
            linked = root / "dangling-destination"
            linked.symlink_to(root / "absent")
            cli("build", main_source, linked, False)
            assert linked.is_symlink()
            return "Existing directory, file and dangling symlink preserved"
        test("existing destinations rejected unchanged", existing_destination)

        meta_mutations = {
            "raw byte association": lambda m: m["rows"][1].update(text_raw_hex=m["rows"][3]["text_raw_hex"]),
            "mode association": lambda m: m["rows"][1].update(text_mode="decoded"),
            "missing tag association": lambda m: m["rows"][1].update(amount_missing="."),
            "ordinary nonmissing marker": lambda m: m["rows"][0].update(amount_missing=".A"),
            "duplicate companion row": lambda m: m["rows"][1].update(row_no=1),
            "boolean companion row": lambda m: m["rows"][0].update(row_no=True),
            "companion order": lambda m: m["rows"].reverse(),
            "missing companion row": lambda m: m["rows"].pop(),
            "extra companion row": lambda m: m["rows"].append(m["rows"][0].copy()),
            "label": lambda m: m["descriptor"]["columns"][0].update(label="changed"),
            "unit": lambda m: m["descriptor"]["columns"][3].update(unit="seconds"),
            "timezone": lambda m: m["descriptor"]["columns"][3].update(timezone="UTC"),
            "catalog": lambda m: m["descriptor"].update(catalog_status="available"),
            "source hash": lambda m: m.update(source_sha256="0" * 64),
            "data hash": lambda m: m.update(data_sha256="0" * 64),
        }
        for number, (name, mutate) in enumerate(meta_mutations.items()):
            def reject_meta(number=number, mutate=mutate):
                dest = root / f"metadata-corruption-{number}"
                shutil.copytree(main_bundle, dest)
                path = dest / "metadata.json"
                meta = json.loads(path.read_text())
                mutate(meta)
                dump(path, meta)
                return cli("check", main_source, dest, False)
            test("reject metadata corruption: " + name, reject_meta)

        data_mutations = {
            "identifier conversion": lambda data: data.replace(b"0012", b"12", 1),
            "decoded text": lambda data: data.replace(b"A\r\nB  ", b"A\nB ", 1),
            "nonmissing numeric": lambda data: data.replace(b"1.25", b"1.26", 1),
            "raw day": lambda data: data.replace(b"1.25,0", b"1.25,100", 1),
            "raw fallback populated": lambda data: data.replace(b"2,0012,,,1", b"2,0012,replaced,,1"),
            "missing amount populated": lambda data: data.replace(b"2,0012,,,1", b"2,0012,,0,1"),
            "row order": lambda data: b"row_no,id,text,amount,event_day\r\n4,0004,,0,2\r\n" + data.split(b"\r\n", 1)[1],
        }
        for number, (name, mutate) in enumerate(data_mutations.items()):
            def reject_data(number=number, mutate=mutate):
                dest = root / f"data-corruption-{number}"
                shutil.copytree(main_bundle, dest)
                path = dest / "data.csv"
                previous = path.read_bytes()
                updated = mutate(previous)
                assert updated != previous
                path.write_bytes(updated)
                meta_path = dest / "metadata.json"
                meta = json.loads(meta_path.read_text())
                meta["data_sha256"] = digest(path)
                dump(meta_path, meta)
                return cli("check", main_source, dest, False)
            test("reject data corruption even with refreshed hash: " + name, reject_data)

        def swapped():
            dest = root / "swapped"
            shutil.copytree(main_bundle, dest)
            shutil.copyfile(empty_bundle / "metadata.json", dest / "metadata.json")
            return cli("check", main_source, dest, False)
        test("reject swapped empty companion", swapped)

        def changed_source():
            path = root / "reformatted-source.json"
            dump(path, fixture)
            assert path.read_bytes() != main_source.read_bytes()
            return cli("check", path, main_bundle, False)
        test("reject semantically equal but byte-different source", changed_source)

        def corrupt_archive():
            dest = root / "archive-corrupt"
            shutil.copytree(main_bundle, dest)
            (dest / "source.json").write_bytes(b"{}")
            return cli("check", main_source, dest, False)
        test("reject corrupt archived source", corrupt_archive)

        def malformed_metadata():
            dest = root / "malformed-meta"
            shutil.copytree(main_bundle, dest)
            (dest / "metadata.json").write_bytes(b'{"rows": [], "rows": []}')
            return cli("check", main_source, dest, False)
        test("reject duplicate metadata property", malformed_metadata)

    receipt = {"status": "local synthetic-envelope test evidence, not SAS binary or Parquet validation",
               "executed_at_utc": datetime.now(timezone.utc).isoformat(),
               "python": sys.version, "platform": platform.platform(),
               "writer_sha256": digest(PROGRAM), "test_runner_sha256": digest(Path(__file__)),
               "main_source_sha256": digest(main_source), "empty_source_sha256": digest(empty_source),
               "passed": sum(r["status"] == "PASS" for r in RESULTS), "total": len(RESULTS),
               "tests": RESULTS}
    # A new receipt filename keeps earlier runs available.
    receipt_path = HERE / ("test-results-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": receipt["passed"], "total": receipt["total"], "receipt": str(receipt_path)}))
    return 0 if receipt["passed"] == receipt["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
