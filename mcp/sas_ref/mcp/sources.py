"""KB loading and resolution for the sas-ref MCP.

Exportability contract (operator ruling, 2026-11-02): the server never
welds itself to one checkout. The kb/ root resolves in this order:

  1. SAS_REF_KB    : direct path to a kb/ directory
  2. SAS_REF_ROOT  : path to a repository root containing kb/
  3. discovery     : walk up from the current working directory, then from
                     this file, looking for a directory that holds both
                     agent-manifest.json and kb/

Every synced layer carries a SOURCE.json stamp; the loaders surface it so
tool results can attach a provenance footer. Nothing here writes.
"""

import csv
import json
import os
from functools import lru_cache
from pathlib import Path


class KBNotFound(RuntimeError):
    pass


def _looks_like_root(p: Path) -> bool:
    return (p / "agent-manifest.json").is_file() and (p / "kb").is_dir()


def resolve_kb() -> Path:
    env_kb = os.environ.get("SAS_REF_KB")
    if env_kb:
        p = Path(env_kb).expanduser().resolve()
        if not p.is_dir():
            raise KBNotFound(f"SAS_REF_KB points at a missing directory: {p}")
        return p
    env_root = os.environ.get("SAS_REF_ROOT")
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if not (p / "kb").is_dir():
            raise KBNotFound(f"SAS_REF_ROOT has no kb/ directory: {p}")
        return p / "kb"
    here = Path.cwd().resolve()
    for cand in [here, *here.parents]:
        if _looks_like_root(cand):
            return cand / "kb"
    pkg = Path(__file__).resolve()
    for cand in pkg.parents:
        if _looks_like_root(cand):
            return cand / "kb"
    raise KBNotFound(
        "cannot locate kb/; set SAS_REF_KB or SAS_REF_ROOT, or run from "
        "inside a sas-ref checkout")


@lru_cache(maxsize=1)
def kb() -> Path:
    return resolve_kb()


def _layer(name: str) -> Path:
    p = kb() / name
    if not p.is_dir():
        raise KBNotFound(f"kb/{name} is missing; the knowledge base is incomplete")
    return p


@lru_cache(maxsize=8)
def stamp(layer: str) -> dict:
    """The SOURCE.json stamp of a synced layer (empty dict if unstamped)."""
    f = kb() / layer / "SOURCE.json"
    if not f.is_file():
        return {}
    return json.loads(f.read_text(encoding="utf-8"))


def provenance(layer: str) -> str:
    s = stamp(layer)
    if not s:
        return f"source: kb/{layer} (unstamped)"
    repo = s.get("source_repo", "?")
    if "/" in repo:
        repo = repo.rstrip("/").split("/")[-1].removesuffix(".git")
    return (f"source: {repo}@{s.get('source_commit', '?')[:7]} "
            f"v{s.get('version', '?')} copied {s.get('copied_at', '?')}")


@lru_cache(maxsize=1)
def rulebook() -> dict:
    return json.loads((_layer("rulebook") / "sasconversionrulebook.json")
                      .read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def capability() -> dict:
    return json.loads((_layer("capability") / "capability-manifest.json")
                      .read_text(encoding="utf-8"))


def semantics_reference() -> str:
    return (_layer("semantics") / "sas_semantics_reference.txt").read_text(
        encoding="utf-8")


def census_csv() -> str:
    return (_layer("census") / "macro_surface_census.csv").read_text(
        encoding="utf-8")


def convert_targets() -> list:
    return sorted(p.stem.replace("sas_to_", "")
                  for p in _layer("convert").glob("sas_to_*.md"))


def convert_guide(target: str) -> str:
    t = target.strip().lower()
    if t.startswith("sas_to_"):
        t = t[len("sas_to_"):]
    f = _layer("convert") / f"sas_to_{t}.md"
    if not f.is_file():
        raise KeyError(f"no conversion guide for target {target!r}; "
                       f"available: {convert_targets()}")
    return f.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def corpus_dir() -> Path:
    """The corpus location, discovered across instance shapes:
    kb/corpus (professional instance), references/rosetta-code/corpus
    (public toolkit instance), corpus (compat roots). One codebase, any
    shape; the marker is TASKS.csv beside the files."""
    root = kb().parent
    for cand in (kb() / "corpus",
                 root / "references" / "rosetta-code" / "corpus",
                 root / "corpus"):
        if (cand / "TASKS.csv").is_file():
            return cand
        if (cand.parent / "TASKS.csv").is_file() and any(cand.glob("*.sas")):
            return cand  # sibling-index layout (the toolkit instance)
    raise KBNotFound("no corpus directory found (looked for TASKS.csv beside "
                     "or above kb/corpus, references/rosetta-code/corpus, corpus)")


@lru_cache(maxsize=1)
def corpus_tasks_csv() -> Path:
    d = corpus_dir()
    return d / "TASKS.csv" if (d / "TASKS.csv").is_file() else d.parent / "TASKS.csv"


@lru_cache(maxsize=1)
def corpus_index() -> list:
    with open(corpus_tasks_csv(), newline="",
              encoding="utf-8") as f:
        return list(csv.DictReader(f))


def corpus_file(name: str) -> str:
    slug = name if name.endswith(".sas") else name + ".sas"
    f = corpus_dir() / slug
    if not f.is_file():
        raise KeyError(f"no corpus file {name!r}")
    return f.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def landmine_cards() -> list:
    """Every card under kb/landmines/ as {collection, name, title, text}."""
    out = []
    for md in sorted(_layer("landmines").glob("*/*.md")):
        if md.name.upper() in {"README.MD", "SOURCES.MD"}:
            continue
        text = md.read_text(encoding="utf-8")
        title = md.stem
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        out.append({"collection": md.parent.name, "name": md.stem,
                    "title": title, "text": text,
                    "path": str(md.relative_to(kb()))})
    return out


@lru_cache(maxsize=1)
def evidence_docs() -> list:
    """The synced evidence documents as {name, text}."""
    out = []
    for f in sorted(_layer("evidence").iterdir()):
        if f.is_file() and f.suffix == ".md":
            out.append({"name": f.name,
                        "text": f.read_text(encoding="utf-8")})
    return out


@lru_cache(maxsize=1)
def reference_index() -> dict:
    """kb/reference/index.json (empty dict when the layer is not harvested)."""
    f = kb() / "reference" / "index.json"
    if not f.is_file():
        return {}
    return json.loads(f.read_text(encoding="utf-8"))


def reference_entry(docset: str, entry: str) -> dict:
    """One harvested reference entry with its pinned page text."""
    idx = reference_index()
    ds = idx.get("docsets", {}).get(docset.strip().lower())
    if ds is None:
        raise KeyError(f"unknown docset {docset!r}; harvested: "
                       f"{sorted(idx.get('docsets', {}))}")
    entries = ds.get("entries", {})
    hit = entries.get(entry)
    name = entry
    if hit is None:
        low = entry.strip().casefold()
        cands = [k for k in entries if k.casefold() == low]
        if not cands:
            cands = [k for k in entries if low in k.casefold()]
        if not cands:
            raise KeyError(f"no reference entry {entry!r} in docset {docset!r}")
        name = cands[0]
        hit = entries[name]
    text = (kb() / "reference" / hit["file"]).read_text(encoding="utf-8")
    out = dict(hit)
    out["entry"] = name
    out["text"] = text
    return out


def reference_provenance(docset: str) -> str:
    f = kb() / "reference" / "extracted" / docset / "PROVENANCE.json"
    if not f.is_file():
        return f"source: kb/reference/{docset} (unstamped)"
    prov = json.loads(f.read_text(encoding="utf-8"))
    return (f"source: {prov.get('docset_id')} 9.4 pdf {prov.get('pdf_sha256', '?')[:12]} "
            f"retrieved {prov.get('retrieved_at', '?')}")
