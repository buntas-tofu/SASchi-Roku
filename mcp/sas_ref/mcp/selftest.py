"""Self-test for the sas-ref MCP server.

Two levels: direct function asserts over the real kb/ (structural, so a
future re-sync does not break the test), then a protocol-level pass through
an in-memory fastmcp Client (tools/list, a real tool call, a resource read,
a prompt fetch). Run: python -m sas_ref.mcp.selftest
"""

import asyncio
import sys

from sas_ref.mcp import sources
from sas_ref.mcp.server import (mcp, lookup_rule, search_rules, get_landmines,
                                search_landmine_cards, lookup_capability,
                                capability_status, search_corpus,
                                get_conversion_guide, conversion_contract,
                                search_evidence, search_reference,
                                read_reference)

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name} {detail}")
        FAILURES.append(name)


def direct() -> None:
    kb = sources.resolve_kb()
    check("kb resolves", kb.is_dir(), str(kb))
    rb = sources.rulebook()
    rules = rb.get("rules", [])
    check("rulebook loads", len(rules) > 50, f"{len(rules)} rules")
    check("rulebook stamp", bool(sources.stamp("rulebook").get("source_commit")))
    r = lookup_rule("DS-001")
    check("lookup_rule DS-001", "rule" in r and r["rule"].get("rule_id") == "DS-001")
    check("lookup_rule has landmines field",
          "silent_difference_checks" in r.get("rule", {}))
    check("lookup_rule footer", "_provenance" in r)
    s = search_rules("merge datasets")
    check("search_rules nonempty", s.get("count", 0) > 0)
    lm = get_landmines(family="DS")
    check("get_landmines DS nonempty", lm.get("count", 0) > 0)
    cards = search_landmine_cards("symput")
    check("cards search hits ml-001",
          any(c["name"] == "ml-001-symput-timing" for c in cards.get("cards", [])))
    check("cards inventory", len(sources.landmine_cards()) >= 49,
          str(len(sources.landmine_cards())))
    cap = lookup_capability("SET")
    check("lookup_capability SET", cap.get("count", 0) > 0)
    st = capability_status("stmt")
    check("capability rollup stmt", "stmt" in st.get("rollup", {}))
    cor = search_corpus("fizzbuzz")
    check("search_corpus fizzbuzz", cor.get("count", 0) > 0)
    check("corpus index size", len(sources.corpus_index()) == 56,
          str(len(sources.corpus_index())))
    g = get_conversion_guide("r")
    check("guide r", len(g.get("guide", "")) > 500)
    check("guide targets", set(sources.convert_targets()) >= {"duckdb", "polars", "r"},
          str(sources.convert_targets()))
    cc = conversion_contract()
    check("contract invariants", bool(cc.get("contract")) and bool(cc.get("global_policies")))
    ev = search_evidence("binary64")
    check("evidence search", ev.get("count", 0) > 0
          and any(h["doc"] == "BINARY64.md" for h in ev.get("hits", [])))
    idx = sources.reference_index()
    check("reference index loads", bool(idx.get("docsets")))
    cm = sources.capability()
    universes = {d["id"]: d["universe"]
                 for d in cm.get("reference_frame", {}).get("documents", [])
                 if d.get("universe") is not None}
    for ds, data in sorted(idx.get("docsets", {}).items()):
        if ds in universes:
            check(f"reference reconcile {ds}", data.get("count") == universes[ds],
                  f"{data.get('count')} vs manifest {universes[ds]}")
        missing = [n for n, m in data.get("entries", {}).items()
                   if not (sources.kb() / "reference" / m["file"]).is_file()]
        check(f"reference files present {ds}", not missing, str(missing[:3]))
    e = sources.reference_entry("stmt", "SET Statement")
    check("read SET Statement page-pinned", "SET Statement" in e["text"] and e["page"] > 0)
    sr = search_reference("merge")
    check("search_reference nonempty", sr.get("count", 0) > 0)


async def protocol() -> None:
    from fastmcp import Client
    async with Client(mcp) as c:
        tools = await c.list_tools()
        names = {t.name for t in tools}
        expect = {"lookup_rule", "search_rules", "get_landmines",
                  "search_landmine_cards", "lookup_capability",
                  "capability_status", "search_corpus",
                  "get_conversion_guide", "conversion_contract",
                  "search_evidence", "search_reference", "read_reference"}
        check("protocol tools/list", expect <= names, str(names))
        res = await c.list_resources()
        uris = {str(r.uri) for r in res}
        check("protocol resources", {"sasref://rulebook", "sasref://capability",
                                      "sasref://semantics/reference",
                                      "sasref://census/macro"} <= uris, str(uris))
        prompts = await c.list_prompts()
        pnames = {p.name for p in prompts}
        check("protocol prompts", {"convert", "landmine_audit", "coverage_gap"} <= pnames,
              str(pnames))
        out = await c.call_tool("lookup_rule", {"rule_id": "ST-001"})
        check("protocol call lookup_rule", out is not None)
        out = await c.call_tool("capability_status", {})
        check("protocol call capability_status", out is not None)
        out = await c.call_tool("read_reference", {"docset": "dso", "entry": "ALTER= Data Set Option"})
        check("protocol call read_reference", out is not None)
        body = await c.read_resource("sasref://census/macro")
        first = body[0] if body else None
        text = getattr(first, "text", None)
        if text is None and first is not None:
            try:
                text = first[0].text
            except (TypeError, IndexError, AttributeError):
                text = ""
        check("protocol read census", len(text or "") > 100, str(len(text or "")))
        pr = await c.get_prompt("convert", {"sas_source": "data x; set y; run;",
                                            "target": "polars"})
        check("protocol prompt convert", any("advisory" in m.text.casefold()
                                             or "DRAFT" in m.text for m in pr.messages
                                             if hasattr(m, "text")) or bool(pr.messages))


def main() -> int:
    direct()
    asyncio.run(protocol())
    if FAILURES:
        print(f"selftest: {len(FAILURES)} failure(s): {FAILURES}")
        return 1
    print("selftest: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
