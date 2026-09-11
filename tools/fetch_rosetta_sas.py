#!/usr/bin/env python3
"""fetch_rosetta_sas.py : the SASchi-Roku harvest pipeline.

Fetches every SAS solution in Rosetta Code's Category:SAS through the
MediaWiki API and either refreshes this repository's corpus or, with
--check, reports how the repository differs from upstream without
writing anything. Pure standard library; one request per task, throttled.

The corpus is a provenance-pinned snapshot: one .sas file per task under
corpus/, each opening with a header comment that pins the source URL, the
page revision the text was extracted from, and the retrieval time.
TASKS.csv and TASKS.md are generated indexes over the same state.

Refresh semantics:

- A task whose extracted text is unchanged keeps its existing file and
  its original retrieval stamp: no churn for content that did not move.
- A task whose text changed, or that is new upstream, is written with
  the fetched revision id and the current retrieval time.
- A file whose task is no longer a category member is removed (git
  history is the recovery); the removal is reported, never silent.
- A page whose SAS section carries no code block is reported and not
  written.

Check semantics: fetch everything, compare, write nothing, and exit 1
when the repository would change (files or indexes), 0 when it is
current. Revision drift whose text is unchanged is reported as
information, not as a difference.

Usage:

  python3 tools/fetch_rosetta_sas.py            # refresh the repository
  python3 tools/fetch_rosetta_sas.py --check    # report drift; exit 1 if any
  python3 tools/fetch_rosetta_sas.py --limit N  # debug: inspect the first N
                                                # tasks; never prunes, never
                                                # rewrites the indexes
"""

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://rosettacode.org/w/api.php"
CATEGORY = "Category:SAS"
CATEGORY_URL = "https://rosettacode.org/wiki/" + CATEGORY.replace(" ", "_")
ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus"
TASKS_CSV = ROOT / "TASKS.csv"
TASKS_MD = ROOT / "TASKS.md"
UA = ("SASchi-Roku harvest pipeline "
      "(https://github.com/buntas-tofu/SASchi-Roku)")

HEADER_RE = re.compile(r"^==\s*\{\{header\|SAS(?:\|[^}]*)?\}\}\s*==\s*$", re.M)
NEXT_LEVEL_RE = re.compile(r"^==[^=]", re.M)
CODE_BLOCK_RES = [
    re.compile(r"<syntaxhighlight\b[^>]*>(.*?)</syntaxhighlight>", re.S | re.I),
    re.compile(r"<lang\b[^>]*>(.*?)</lang>", re.S | re.I),
]
EXISTING_TITLE_RE = re.compile(r"Rosetta Code task '(.*?)', page revision (\d+)\.")
EXISTING_RETRIEVED_RE = re.compile(r"Retrieved (\S+?)\. \*/")


def api_get(params: dict) -> dict:
    params["format"] = "json"
    params["formatversion"] = "2"
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("unreachable")


def category_members() -> list[str]:
    out = []
    cont = {}
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": CATEGORY,
            "cmnamespace": "0",
            "cmlimit": "500",
        }
        params.update(cont)
        d = api_get(params)
        out.extend(m["title"] for m in d["query"]["categorymembers"])
        if "continue" not in d:
            break
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}
    return out


def page_wikitext(title: str):
    d = api_get({
        "action": "query",
        "prop": "revisions",
        "rvprop": "ids|content",
        "rvslots": "main",
        "titles": title,
    })
    page = d["query"]["pages"][0]
    if page.get("missing"):
        return None, None
    rev = page["revisions"][0]
    slot = rev["slots"]["main"]
    return slot.get("*") or slot.get("content"), rev.get("revid")


def sas_sections(content: str) -> list[str]:
    sections = []
    for m in HEADER_RE.finditer(content):
        end = NEXT_LEVEL_RE.search(content, m.end())
        sections.append(content[m.end(): end.start() if end else None])
    return sections


def extract_blocks(section: str) -> list[str]:
    blocks = []
    for rx in CODE_BLOCK_RES:
        blocks.extend(m.group(1).strip("\n") for m in rx.finditer(section))
    return blocks


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return s[:80] or "task"


def page_url(title: str) -> str:
    return "https://rosettacode.org/wiki/" + urllib.parse.quote(
        title.replace(" ", "_"))


def build_file_text(title: str, revid: int, retrieved: str,
                    blocks: list[str]) -> str:
    header = (
        f"/* Source: {page_url(title)}\n"
        f"   Rosetta Code task '{title}', page revision {revid}.\n"
        f"   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved"
        f" {retrieved}. */\n"
    )
    parts = [header]
    for i, b in enumerate(blocks, 1):
        if len(blocks) > 1:
            parts.append(f"\n/* --- {title}: example {i} of"
                         f" {len(blocks)} --- */\n")
        parts.append(b)
    return "\n".join(parts) + "\n"


def split_header(text: str):
    marker = "*/\n"
    i = text.find(marker)
    if i == -1:
        return text, ""
    return text[: i + len(marker)], text[i + len(marker):]


def existing_state(path: Path):
    if not path.exists():
        return None
    header, payload = split_header(path.read_text())
    m = EXISTING_TITLE_RE.search(header)
    r = EXISTING_RETRIEVED_RE.search(header)
    return {
        "title": m.group(1) if m else "",
        "revid": int(m.group(2)) if m else 0,
        "retrieved": r.group(1) if r else "",
        "payload": payload,
    }


def index_label(rows: list[dict]) -> str:
    dates = sorted(set(r["retrieved"] for r in rows))
    first, last = dates[0][:10], dates[-1][:10]
    if first == last:
        return f"snapshot {first}"
    return f"snapshot {first} (refreshed {last})"


def index_csv_text(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["file", "task", "url", "revision",
                                        "retrieved"], lineterminator="\r\n")
    w.writeheader()
    for r in rows:
        w.writerow({"file": r["file"], "task": r["task"], "url": r["url"],
                    "revision": r["revid"], "retrieved": r["retrieved"]})
    return buf.getvalue()


def index_md_text(rows: list[dict]) -> str:
    lines = [
        "# Task Index",
        "",
        f"{len(rows)} tasks from {CATEGORY_URL}, {index_label(rows)}.",
        "Machine-readable form: [`TASKS.csv`](TASKS.csv).",
        "",
        "| File | Rosetta Code task | Revision |",
        "|------|-------------------|----------|",
    ]
    for r in rows:
        lines.append(
            f"| [`corpus/{r['file']}`](corpus/{r['file']})"
            f" | [{r['task']}]({r['url']}) | {r['revid']} |")
    return "\n".join(lines) + "\n"


def index_diff(old_csv: str, new_csv: str) -> list[str]:
    def rows(text):
        return {r["file"]: r for r in csv.DictReader(io.StringIO(text))}
    out = []
    old, new = rows(old_csv), rows(new_csv)
    for f in sorted(set(old) | set(new)):
        if f not in new:
            out.append(f"- {f} (removed)")
        elif f not in old:
            out.append(f"+ {f} (new)")
        elif old[f] != new[f]:
            fields = [k for k in old[f] if old[f][k] != new[f].get(k)]
            detail = ", ".join(sorted(fields))
            out.append(f"~ {f} (index fields: {detail})")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="SASchi-Roku harvest pipeline")
    ap.add_argument("--check", action="store_true",
                    help="report drift against upstream; write nothing")
    ap.add_argument("--limit", type=int, default=None,
                    help="debug: inspect the first N tasks only")
    args = ap.parse_args()
    debug_limited = args.limit is not None

    now_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    titles = category_members()
    if args.limit:
        titles = titles[: args.limit]
    print(f"upstream: {len(titles)} main-namespace members in {CATEGORY}")

    rows = []
    for i, title in enumerate(titles, 1):
        content, revid = page_wikitext(title)
        blocks = []
        if content is not None:
            for sec in sas_sections(content):
                blocks.extend(extract_blocks(sec))
        if not blocks:
            state = "missing-page" if content is None else "no-sas-code"
            print(f"[{i}/{len(titles)}] {state}: {title}")
            time.sleep(0.4)
            continue
        path = CORPUS_DIR / f"{slugify(title)}.sas"
        current = existing_state(path)
        new_payload = split_header(
            build_file_text(title, revid or 0, "T", blocks))[1]
        if current is None:
            action, retrieved, pinned_revid = "new", now_utc, revid or 0
        elif current["payload"] != new_payload:
            action, retrieved, pinned_revid = "changed", now_utc, revid or 0
        else:
            action, retrieved = "unchanged", current["retrieved"]
            pinned_revid = current["revid"]
        rows.append({"file": path.name, "task": title, "url": page_url(title),
                     "revid": pinned_revid, "action": action,
                     "retrieved": retrieved, "path": path, "blocks": blocks,
                     "current": current})
        if action != "unchanged":
            print(f"[{i}/{len(titles)}] {action}: {title}")
        elif current and current["revid"] != revid:
            print(f"[{i}/{len(titles)}] info: {title}: revision"
                  f" {current['revid']} -> {revid} (text unchanged)")
        time.sleep(0.4)

    changes = [r for r in rows if r["action"] != "unchanged"]

    pruned = []
    if not debug_limited and TASKS_CSV.exists():
        present = {r["file"] for r in rows}
        with open(TASKS_CSV, newline="") as fh:
            for old in csv.DictReader(fh):
                if old.get("file") and old["file"] not in present:
                    p = CORPUS_DIR / old["file"]
                    if p.exists():
                        if not args.check:
                            p.unlink()
                        pruned.append(old["file"])
        for name in pruned:
            print(f"pruned (no longer a category member): {name}")

    idx_changed = False
    idx_lines = []
    if not debug_limited:
        new_csv = index_csv_text(rows)
        new_md = index_md_text(rows)
        old_csv = (TASKS_CSV.open("r", encoding="utf-8", newline="").read()
                   if TASKS_CSV.exists() else "")
        old_md = (TASKS_MD.open("r", encoding="utf-8", newline="").read()
                  if TASKS_MD.exists() else "")
        idx_changed = new_csv != old_csv or new_md != old_md
        idx_lines = index_diff(old_csv, new_csv)
        for ln in idx_lines:
            print(f"index: {ln}")

    print(f"summary: {len(rows)} tasks fetched, {len(changes)} file changes,"
          f" {len(pruned)} pruned, index"
          f" {'differs' if idx_changed else 'current'}")

    if args.check:
        if changes or pruned or idx_changed:
            print("check: repository is NOT current; run without --check to"
                  " refresh")
            return 1
        print("check: repository is current against upstream")
        return 0

    for r in changes:
        text = build_file_text(r["task"], r["revid"], r["retrieved"],
                               r["blocks"])
        r["path"].write_text(text)
        print(f"wrote {r['path'].name}")
    if idx_changed and not debug_limited:
        TASKS_CSV.write_text(index_csv_text(rows), newline="")
        TASKS_MD.write_text(index_md_text(rows), newline="")
        print("refreshed: TASKS.csv, TASKS.md")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
