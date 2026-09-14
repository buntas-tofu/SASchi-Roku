#!/usr/bin/env python3
"""check_corpus_index.py : prove the corpus and its index agree.

The Roku contract says TASKS.csv is the machine-readable index and stays in
lockstep with the corpus, and TASKS.md carries the same table for a person.
Until this script existed nothing checked any of that, so the claim was a
promise rather than a gate.

Four checks, each one a way the index can drift from the corpus:

  1. every corpus/*.sas has exactly one TASKS.csv row
  2. every TASKS.csv row names a file that exists
  3. the url and page revision in a row match the url and page revision in that
     file's own provenance header. This is the check that ties the index to the
     artifact, rather than to another copy of the index.
  4. TASKS.md carries the same file and revision for every row

Exit 0 when all four hold, 1 otherwise, and every finding prints. Stdlib only,
so CI needs no install and the room's no-dependency rule holds.

Floor: no em dashes, no ellipses.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOM = Path(__file__).resolve().parent.parent
CORPUS = ROOM / "corpus"
INDEX = ROOM / "TASKS.csv"
HUMAN = ROOM / "TASKS.md"

HEADER_URL = re.compile(r"^/\* Source: (\S+)", re.MULTILINE)
HEADER_REV = re.compile(r"page revision (\d+)")
MD_ROW = re.compile(r"^\|\s*\[`corpus/([^`]+)`\][^|]*\|[^|]*\|\s*(\d+)\s*\|", re.MULTILINE)


def findings() -> list[str]:
    out: list[str] = []
    if not INDEX.is_file():
        return [f"no index at {INDEX}"]
    if not CORPUS.is_dir():
        return [f"no corpus at {CORPUS}"]

    with INDEX.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    seen: dict[str, int] = {}
    for row in rows:
        name = (row.get("file") or "").strip()
        if not name:
            out.append("a TASKS.csv row has no file")
            continue
        seen[name] = seen.get(name, 0) + 1
    for name, count in sorted(seen.items()):
        if count > 1:
            out.append(f"TASKS.csv lists {name} {count} times")

    on_disk = {p.name for p in sorted(CORPUS.glob("*.sas"))}
    for name in sorted(on_disk - set(seen)):
        out.append(f"{name} is in the corpus with no TASKS.csv row")
    for name in sorted(set(seen) - on_disk):
        out.append(f"{name} has a TASKS.csv row and no file in the corpus")

    for row in rows:
        name = (row.get("file") or "").strip()
        if name not in on_disk:
            continue
        text = (CORPUS / name).read_text(encoding="utf-8", errors="replace")
        head = text[:600]
        m_url = HEADER_URL.search(head)
        m_rev = HEADER_REV.search(head)
        if m_url is None or m_rev is None:
            out.append(f"{name} has no readable provenance header, so nothing pins it")
            continue
        if (row.get("url") or "").strip() != m_url.group(1):
            out.append(
                f"{name} url disagrees: index {row.get('url')!r}, header {m_url.group(1)!r}")
        if (row.get("revision") or "").strip() != m_rev.group(1):
            out.append(
                f"{name} revision disagrees: index {row.get('revision')!r}, header {m_rev.group(1)!r}")

    if HUMAN.is_file():
        md = HUMAN.read_text(encoding="utf-8")
        md_rows = MD_ROW.findall(md)
        if len(md_rows) != len(rows):
            out.append(
                f"TASKS.md has {len(md_rows)} rows against TASKS.csv's {len(rows)}")
        md_by_file = {name: rev for name, rev in md_rows}
        for row in rows:
            name = (row.get("file") or "").strip()
            if name not in md_by_file:
                out.append(f"{name} is in TASKS.csv and not in TASKS.md")
            elif md_by_file[name] != (row.get("revision") or "").strip():
                out.append(
                    f"{name} revision disagrees between TASKS.csv ({row.get('revision')}) "
                    f"and TASKS.md ({md_by_file[name]})")
    else:
        out.append(f"no human index at {HUMAN}")

    return out


def main() -> int:
    problems = findings()
    total = len(list(CORPUS.glob("*.sas"))) if CORPUS.is_dir() else 0
    print(f"corpus files: {total}")
    if problems:
        print(f"FAIL: {len(problems)} finding(s)")
        for p in problems:
            print(f"  {p}")
        return 1
    print("PASS: the corpus, TASKS.csv, TASKS.md, and every provenance header agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
