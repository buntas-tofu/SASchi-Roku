"""The sas-ref knowledge and skills MCP server.

Advisory by design: every answer is reference material (patterns, targets,
landmines, dispositions, evidence pointers). Nothing returned here is a
verification; a conversion is accepted because a gate ran and the numbers
matched in the campaign lane, never because this server said so.

Run: python -m sas_ref.mcp.server            (stdio, default)
     sas-ref-mcp --transport http --port 8765   (flag-ready per ruling Q1;
                                             no hosting is implied)
"""

import argparse
import json
import re

from fastmcp import FastMCP

from sas_ref.mcp import sources

ADVISORY = (
    "sas-ref MCP: the consolidated SAS conversion reference (rulebook, "
    "capability manifest, semantics, corpus, landmine cards, conversion "
    "guides, census, evidence). Advisory only: this server explains, drafts, "
    "and interprets; it never verifies. A conversion is accepted when a gate "
    "in the campaign lane runs and the numbers match. Every tool result "
    "carries a provenance footer pinning the synced source commit."
)

mcp = FastMCP("sas-ref", instructions=ADVISORY)


def _score(text: str, tokens: list) -> int:
    low = text.casefold()
    return sum(low.count(t) for t in tokens)


def _tokens(query: str) -> list:
    return [t for t in re.split(r"\W+", query.casefold()) if t]


def _rule_brief(r: dict) -> dict:
    return {
        "rule_id": r.get("rule_id"),
        "sas_pattern": r.get("sas_pattern"),
        "scope": r.get("scope"),
        "equivalence_class": r.get("equivalence_class"),
        "confidence": r.get("confidence"),
    }


@mcp.tool()
def lookup_rule(rule_id: str) -> dict:
    """The full rule: pattern, python/r targets, alternates, required
    settings, forbidden patterns, equivalence class, silent difference
    checks (the landmines), validation test, confidence, sources."""
    rid = rule_id.strip().upper()
    for r in sources.rulebook().get("rules", []):
        if r.get("rule_id", "").upper() == rid:
            return {"rule": r, "_provenance": sources.provenance("rulebook")}
    return {"error": f"no rule {rule_id!r}",
            "_provenance": sources.provenance("rulebook")}


@mcp.tool()
def search_rules(query: str, family: str = "", equivalence_class: str = "",
                 target: str = "", limit: int = 10) -> dict:
    """Ranked rule search. Filters: family (DS/ST/MC/SV/SQL/MX),
    equivalence_class (EXACT, EQUIVALENT-WITH-SETTINGS, APPROXIMATE,
    NO-DIRECT-EQUIVALENT), target (python or r). Each hit carries a
    one-line why-it-matched."""
    toks = _tokens(query)
    tgt = target.strip().lower()
    hits = []
    for r in sources.rulebook().get("rules", []):
        if family and not r.get("rule_id", "").upper().startswith(family.strip().upper()):
            continue
        if equivalence_class and r.get("equivalence_class", "").upper() != equivalence_class.strip().upper():
            continue
        if tgt:
            key = "python_target" if tgt.startswith("py") else "r_target"
            if not r.get(key):
                continue
        hay = " ".join(str(v) for v in (
            r.get("rule_id", ""), r.get("sas_pattern", ""), r.get("scope", ""),
            json.dumps(r.get("python_target", {})), json.dumps(r.get("r_target", {})),
            " ".join(r.get("silent_difference_checks", []))))
        s = _score(hay, toks) if toks else 1
        if s > 0:
            why = r.get("sas_pattern", "")
            hits.append((s, r.get("rule_id", ""), {**_rule_brief(r), "why": why}))
    hits.sort(key=lambda h: (-h[0], h[1]))
    out = [h[2] for h in hits[:max(1, min(limit, 50))]]
    return {"count": len(hits), "results": out,
            "_provenance": sources.provenance("rulebook")}


@mcp.tool()
def get_landmines(rule_id: str = "", family: str = "", query: str = "") -> dict:
    """Just the silent_difference_checks, deduped: what will silently
    disagree. Give a rule_id, a family prefix, or a free-text query."""
    checks = []
    seen = set()
    for r in sources.rulebook().get("rules", []):
        rid = r.get("rule_id", "")
        if rule_id and rid.upper() != rule_id.strip().upper():
            continue
        if family and not rid.upper().startswith(family.strip().upper()):
            continue
        if query:
            hay = (rid + " " + r.get("sas_pattern", "") + " " + r.get("scope", "")).casefold()
            if not any(t in hay for t in _tokens(query)):
                continue
        for c in r.get("silent_difference_checks", []):
            if c not in seen:
                seen.add(c)
                checks.append({"rule_id": rid, "check": c})
    return {"count": len(checks), "landmines": checks,
            "_provenance": sources.provenance("rulebook")}


@mcp.tool()
def search_landmine_cards(query: str, limit: int = 8) -> dict:
    """Search the 49 field-guide landmine cards (llm-migration-quirks,
    macro-landmines, sas-conversion-landmines): the long-form silent
    difference material behind the rulebook checks. Returns ranked hits with
    an excerpt and the card path."""
    toks = _tokens(query)
    hits = []
    for card in sources.landmine_cards():
        s = _score(card["title"], toks) * 3 + _score(card["name"], toks) * 3 + _score(card["text"], toks)
        if s > 0:
            low = card["text"].casefold()
            pos = min((low.find(t) for t in toks if t in low), default=0)
            start = max(0, pos - 80)
            excerpt = card["text"][start:start + 240].replace("\n", " ")
            hits.append((s, card["name"], {
                "collection": card["collection"], "name": card["name"],
                "title": card["title"], "excerpt": excerpt.strip(),
                "path": "kb/" + card["path"]}))
    hits.sort(key=lambda h: (-h[0], h[1]))
    return {"count": len(hits),
            "cards": [h[2] for h in hits[:max(1, min(limit, 30))]],
            "_provenance": "source: kb/landmines (consolidation ledger M1, sas-kb@2ea5735)"}


@mcp.tool()
def lookup_capability(entry: str, document: str = "") -> dict:
    """One capability-manifest entry by name (for example 'SET Statement'
    or 'KEEP='), optionally scoped to a document (stmt, dso). Returns the
    disposition, rule ids, gates, reference page, and note."""
    want = entry.strip().casefold()
    out = []
    for e in sources.capability().get("entries", []):
        if document and e.get("document", "") != document.strip().lower():
            continue
        name = e.get("entry", "").casefold()
        if name == want or want in name:
            out.append(e)
    if not out:
        return {"error": f"no capability entry matching {entry!r}",
                "_provenance": sources.provenance("capability")}
    return {"count": len(out), "entries": out[:25],
            "_provenance": sources.provenance("capability")}


@mcp.tool()
def capability_status(document: str = "") -> dict:
    """The coverage rollup for one document (stmt, dso) or all: universe,
    assessed, gated, rule, human_review, out_of_scope, unassessed. Null
    universe means not enumerated yet, not empty."""
    roll = sources.capability().get("rollup", {})
    if document:
        d = document.strip().lower()
        if d not in roll:
            return {"error": f"no rollup for document {document!r}",
                    "known": sorted(roll)}
        roll = {d: roll[d]}
    frame = sources.capability().get("reference_frame", {})
    return {"reference_frame": frame, "rollup": roll,
            "_provenance": sources.provenance("capability")}


@mcp.tool()
def search_corpus(query: str, limit: int = 10) -> dict:
    """Search the 56-task Rosetta Code SAS corpus by task title, filename,
    or program body. Returns task, file, source url, and revision per hit."""
    toks = _tokens(query)
    rows = []
    for r in sources.corpus_index():
        fname = r.get("file", "")
        body_score = 0
        try:
            body = sources.corpus_file(fname).casefold()
            body_score = _score(body, toks)
        except (KeyError, OSError):
            body = ""
        s = _score(r.get("task", ""), toks) * 3 + _score(fname, toks) * 3 + body_score
        if s > 0:
            rows.append((s, fname, {
                "task": r.get("task"), "file": f"kb/corpus/{fname}",
                "url": r.get("url"), "revision": r.get("revision")}))
    rows.sort(key=lambda h: (-h[0], h[1]))
    return {"count": len(rows), "results": [h[2] for h in rows[:max(1, min(limit, 56))]],
            "_provenance": "source: kb/corpus (Rosetta Code, per-file provenance headers; TASKS.csv)"}


@mcp.tool()
def get_conversion_guide(target: str) -> dict:
    """A target conversion guide in full: duckdb, polars, or r."""
    try:
        text = sources.convert_guide(target)
    except KeyError as e:
        return {"error": str(e), "_provenance": "source: kb/convert"}
    return {"target": target.strip().lower(), "guide": text,
            "_provenance": "source: kb/convert (ledger R3; scaffold provenance in kb/convert/README.md)"}


@mcp.tool()
def conversion_contract() -> dict:
    """The invariants a converter must honor: the rulebook contract, the
    global policies, the tolerance tiers, and the equivalence classes."""
    rb = sources.rulebook()
    meta = rb.get("meta", {})
    return {
        "contract": rb.get("contract"),
        "global_policies": rb.get("global_policies"),
        "tolerance_tiers": meta.get("tolerance_tiers"),
        "equivalence_classes": meta.get("equivalence_classes"),
        "python_stack": meta.get("python_stack"),
        "r_stack": meta.get("r_stack"),
        "_provenance": sources.provenance("rulebook"),
    }


@mcp.tool()
def search_evidence(query: str, limit: int = 12) -> dict:
    """Search the synced family evidence documents (the reports behind the
    gate families: bitwise, character reports, counted loops, procedures,
    and the coverage backlog). Returns per-document line hits."""
    toks = _tokens(query)
    hits = []
    for doc in sources.evidence_docs():
        for i, line in enumerate(doc["text"].splitlines(), 1):
            if any(t in line.casefold() for t in toks):
                hits.append({"doc": doc["name"], "line": i,
                             "text": line.strip()[:200]})
                if len(hits) >= max(1, min(limit, 60)):
                    break
        if len(hits) >= max(1, min(limit, 60)):
            break
    return {"count": len(hits), "hits": hits,
            "_provenance": sources.provenance("evidence")}


@mcp.tool()
def search_reference(query: str, docset: str = "", limit: int = 10) -> dict:
    """Search the harvested SAS 9.4 reference entries by name, category, or
    field text. Docsets: stmt (108 DATA step statements), dso (40 data set
    options). Returns page-pinned pointers into kb/reference/."""
    idx = sources.reference_index()
    if not idx:
        return {"error": "kb/reference is not harvested; run tools/fetch_sas_reference.py",
                "_provenance": "kb/reference"}
    toks = _tokens(query)
    hits = []
    for ds, dsdata in sorted(idx.get("docsets", {}).items()):
        if docset and ds != docset.strip().lower():
            continue
        for name, meta in dsdata.get("entries", {}).items():
            hay = " ".join([name, meta.get("category", ""), meta.get("type", ""),
                            meta.get("valid_in", "")]).casefold()
            s = _score(hay, toks) if toks else 1
            if s > 0:
                hits.append((s, ds, name, {
                    "docset": ds, "entry": name, "page": meta.get("page"),
                    "category": meta.get("category", ""), "type": meta.get("type", ""),
                    "valid_in": meta.get("valid_in", ""),
                    "file": "kb/reference/" + meta.get("file", "")}))
    hits.sort(key=lambda h: (-h[0], h[1], h[2]))
    provs = "; ".join(sources.reference_provenance(d)
                      for d in sorted({h[1] for h in hits[:1]}) ) or "kb/reference"
    return {"count": len(hits),
            "results": [h[3] for h in hits[:max(1, min(limit, 50))]],
            "_provenance": provs}


@mcp.tool()
def read_reference(docset: str, entry: str) -> dict:
    """The pinned page text of one reference entry (for example docset=stmt,
    entry='SET Statement', or docset=dso, entry='ALTER= Data Set Option')."""
    try:
        e = sources.reference_entry(docset, entry)
    except KeyError as ex:
        return {"error": str(ex),
                "_provenance": sources.reference_provenance(docset.strip().lower())}
    text = e.pop("text")
    return {"entry_data": e, "text": text,
            "_provenance": sources.reference_provenance(e.get("docset", docset))}


@mcp.resource("sasref://reference/{docset}/{entry}")
def res_reference(docset: str, entry: str) -> str:
    """One harvested reference entry, page-pinned text."""
    return sources.reference_entry(docset, entry)["text"]


@mcp.resource("sasref://rulebook")
def res_rulebook() -> str:
    """The full rulebook JSON."""
    return json.dumps(sources.rulebook(), indent=2)


@mcp.resource("sasref://rulebook/{rule_id}")
def res_rule(rule_id: str) -> str:
    """One rule, by id."""
    out = lookup_rule(rule_id)
    return json.dumps(out, indent=2)


@mcp.resource("sasref://capability")
def res_capability() -> str:
    """The full capability manifest JSON."""
    return json.dumps(sources.capability(), indent=2)


@mcp.resource("sasref://capability/rollup")
def res_capability_rollup() -> str:
    """Just the coverage rollup."""
    return json.dumps(capability_status(), indent=2)


@mcp.resource("sasref://semantics/reference")
def res_semantics() -> str:
    """The kb01 plain-text semantics mirror."""
    return sources.semantics_reference()


@mcp.resource("sasref://convert/{target}")
def res_convert(target: str) -> str:
    """A target conversion guide."""
    return sources.convert_guide(target)


@mcp.resource("sasref://corpus/{task}")
def res_corpus(task: str) -> str:
    """One Rosetta corpus solution, by slug or filename."""
    return sources.corpus_file(task)


@mcp.resource("sasref://census/macro")
def res_census() -> str:
    """The macro surface census (CSV)."""
    return sources.census_csv()


@mcp.prompt()
def convert(sas_source: str, target: str) -> str:
    """Frame a SAS-to-target conversion task: contract, rules, guide, advisory stance."""
    return (
        "You are converting SAS to " + target + ". Work the loop: analyze, "
        "plan, convert, validate, document. First call conversion_contract() "
        "and honor every invariant. Detect the constructs in the source below "
        "and call search_rules() for each; for every rule used, read its "
        "silent_difference_checks and honor required_settings; never emit a "
        "forbidden pattern. Call get_conversion_guide('" + target + "') and "
        "follow it. If any construct maps to NO-DIRECT-EQUIVALENT, STOP that "
        "construct and emit a human-review note instead of guessing. Call "
        "search_landmine_cards() for the constructs present and apply the "
        "cards. Your output is a DRAFT: advisory only. Acceptance happens "
        "when the campaign gate runs and the numbers match; say so "
        "explicitly in your final document step.\n\nSAS source:\n" + sas_source
    )


@mcp.prompt()
def landmine_audit(sas_source: str = "", rule_ids: str = "") -> str:
    """Audit a SAS source or a rule set for silent differences before trusting output."""
    what = ("rule ids: " + rule_ids) if rule_ids else ("SAS source:\n" + sas_source)
    return (
        "Audit for silent differences: the ways a converted program can "
        "produce different numbers with no error. For each construct (or "
        "each rule id) present, call get_landmines() and "
        "search_landmine_cards(), list every check that applies, and state "
        "how the conversion will detect a disagreement (tolerance tier, "
        "distribution check, or human review). Advisory only: this audit "
        "informs the gate; it does not replace it.\n\n" + what
    )


@mcp.prompt()
def coverage_gap(document: str = "") -> str:
    """Report the known unknowns (UNASSESSED / HUMAN-REVIEW) for planning."""
    scope = document if document else "every enumerated document"
    return (
        "Report the coverage gaps for " + scope + ". Call capability_status() "
        "and, for the document in scope, list the entries whose disposition "
        "is UNASSESSED or HUMAN-REVIEW (use lookup_capability() where "
        "helpful). Distinguish 'not enumerated yet' (null universe) from "
        "'enumerated and unassessed'. End with a planner's summary: where "
        "evidence is thin and what a conversion touching those areas must "
        "gate extra carefully. Advisory only."
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Run the sas-ref knowledge and skills MCP server.")
    ap.add_argument("--transport", choices=["stdio", "http"],
                    default="stdio",
                    help="stdio (default) or streamable HTTP (ruling Q1: "
                         "flag-ready, not hosted)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    if args.transport == "http":
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
