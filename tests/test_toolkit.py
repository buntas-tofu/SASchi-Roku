"""Behavioral checks for relocation and the catalog's evidence boundaries."""

import contextlib
import copy
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


catalog = module("catalog", ROOT / "scripts/check_toolkit.py")
harvest = module("harvest", ROOT / "tools/fetch_rosetta_sas.py")
index = module("index", ROOT / "scripts/check_corpus_index.py")


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(catalog.CATALOG.read_text())

    def test_catalog_and_generated_index(self):
        self.assertEqual(catalog.validate(self.data), [])
        self.assertEqual(catalog.render_index(self.data), catalog.INDEX.read_text())

    def test_duplicate_identity_refuses(self):
        self.data["resources"].append(copy.deepcopy(self.data["resources"][0]))
        self.assertTrue(any("duplicate ID" in x for x in catalog.validate(self.data)))

    def test_unresolved_origin_cannot_be_promoted(self):
        item = next(x for x in self.data["resources"] if x["url"] is None)
        item["evidence"]["status"] = "source-inspected"
        self.assertTrue(any("must stay unresolved" in x for x in catalog.validate(self.data)))

    def test_missing_provenance_refuses(self):
        del self.data["resources"][0]["evidence"]["source_url"]
        self.assertTrue(catalog.validate(self.data))

    def test_unpinned_source_refuses(self):
        self.data["resources"][0]["evidence"]["source_url"] = "https://github.com/example/repo/blob/main/README.md"
        self.assertTrue(any("does not pin" in x for x in catalog.validate(self.data)))

    def test_invalid_historical_count_refuses(self):
        item = next(x for x in self.data["resources"] if x["historical_census"])
        item["historical_census"]["sas_files"] = -1
        self.assertTrue(any("census" in x for x in catalog.validate(self.data)))


class RelocationTests(unittest.TestCase):
    def test_defaults_and_compatibility(self):
        nested = ROOT / "references/rosetta-code"
        self.assertEqual(harvest.ROOT, nested)
        self.assertEqual(index.ROOM, nested)
        self.assertEqual(catalog.check_paths(ROOT), [])
        self.assertEqual(index.findings(), [])
        self.assertEqual(sorted(p.name for p in (ROOT / "corpus").glob("*.sas")),
                         sorted(p.name for p in (nested / "corpus").glob("*.sas")))

    def test_broken_compatibility_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(catalog.check_paths(Path(tmp))), 3)

    def test_header_index_drift_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "reference"
            shutil.copytree(index.ROOM, copy_root)
            csv_path = copy_root / "TASKS.csv"
            text = csv_path.read_text()
            csv_path.write_text(text.replace("410510", "1"))
            with patch.multiple(index, CORPUS=copy_root / "corpus", INDEX=csv_path,
                                HUMAN=copy_root / "TASKS.md"):
                self.assertTrue(any("revision disagrees" in x for x in index.findings()))

    def test_harvest_check_and_refresh_use_nested_destination(self):
        # Fake upstream exercises actual extraction, check, write and index generation.
        # No network request and no writes to the repository collection.
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / "references/rosetta-code"
            corpus = nested / "corpus"
            corpus.mkdir(parents=True)
            wiki = "=={{header|SAS}}==\n<syntaxhighlight>data _null_; run;</syntaxhighlight>\n"
            with patch.multiple(harvest, ROOT=nested, CORPUS_DIR=corpus,
                                TASKS_CSV=nested / "TASKS.csv", TASKS_MD=nested / "TASKS.md"), \
                    patch.object(harvest, "category_members", return_value=["Example"]), \
                    patch.object(harvest, "page_wikitext", return_value=(wiki, 12)), \
                    patch.object(harvest.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
                with patch("sys.argv", ["harvest", "--check"]):
                    self.assertEqual(harvest.main(), 1)
                self.assertEqual(list(corpus.iterdir()), [])
                self.assertFalse((nested / "TASKS.csv").exists())
                with patch("sys.argv", ["harvest"]):
                    self.assertEqual(harvest.main(), 0)
                before = {p.name: p.read_bytes() for p in nested.rglob("*") if p.is_file()}
                with patch("sys.argv", ["harvest", "--check"]):
                    self.assertEqual(harvest.main(), 0)
                with patch("sys.argv", ["harvest"]):
                    self.assertEqual(harvest.main(), 0)
                self.assertEqual(before, {p.name: p.read_bytes() for p in nested.rglob("*") if p.is_file()})
                with patch.multiple(index, CORPUS=corpus, INDEX=nested / "TASKS.csv",
                                    HUMAN=nested / "TASKS.md"):
                    self.assertEqual(index.findings(), [])
            self.assertFalse((Path(tmp) / "corpus").exists())


if __name__ == "__main__":
    unittest.main()
