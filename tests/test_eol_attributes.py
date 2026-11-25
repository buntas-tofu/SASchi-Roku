"""Line-ending attributes are load-bearing, so they get a test.

The corpus gates pin sha256 over file bytes. A blanket ``text=auto eol=lf`` rule
renormalises any CRLF blob the next time it is staged, and 132 evidence, receipt
and stamp files carry CRLF or mixed endings *because that is what was measured*
when the receipt was written. Renormalising one of them invalidates the pin that
cites it, and nothing else in this repo would fail.

Git resolves attributes with the LAST matching pattern winning, so a rule
appended after the exemption block silently lifts it. These tests fail when that
happens, in either direction:

* the frozen trees must resolve ``text`` to ``unset`` (no conversion at all), and
* the corpus and docs must still resolve to ``text`` set with ``eol=lf``.
"""

from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FROZEN_PREFIX = "trials/"
FROZEN_FILES = (
    "kb/census/macro_surface_census.csv",
    "references/rosetta-code/TASKS.csv",
)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return result.stdout


def attribute(path: str, name: str) -> str:
    """Return the resolved value of one attribute for one path."""
    out = git("check-attr", name, "--", path).strip()
    # "<path>: <attr>: <value>"
    return out.rsplit(":", 1)[-1].strip()


@unittest.skipUnless(
    shutil.which("git") and (ROOT / ".git").exists(),
    "needs a git worktree to resolve attributes",
)
class EolAttributeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tracked = [p for p in git("ls-files").splitlines() if p]

    def frozen(self) -> list[str]:
        return [
            p
            for p in self.tracked
            if p.startswith(FROZEN_PREFIX) or p in FROZEN_FILES
        ]

    def test_frozen_trees_are_declared(self) -> None:
        frozen = self.frozen()
        self.assertGreater(
            len(frozen), 100, "the exemption is declared over a population, not a file"
        )

    def test_frozen_trees_take_no_end_of_line_conversion(self) -> None:
        offenders = [p for p in self.frozen() if attribute(p, "text") != "unset"]
        self.assertEqual(
            offenders[:10],
            [],
            f"{len(offenders)} frozen path(s) would be renormalised on the next add, "
            "which invalidates the sha256 pins that cite them",
        )

    def test_corpus_and_docs_normalise_to_lf(self) -> None:
        sas = [p for p in self.tracked if p.endswith(".sas")]
        self.assertTrue(sas, "the corpus must be present")
        for path in (sas[0], "README.md"):
            self.assertEqual(attribute(path, "text"), "set", path)
            self.assertEqual(attribute(path, "eol"), "lf", path)

    def test_write_once_stores_crlf_where_it_is_claimed(self) -> None:
        """The exemption only holds if the blobs themselves still carry CRLF."""
        crlf = [
            p
            for p in self.frozen()
            if b"\r\n" in (ROOT / p).read_bytes()
        ]
        self.assertGreater(
            len(crlf), 100, "the stamped receipts are expected to keep their CRLF bytes"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
