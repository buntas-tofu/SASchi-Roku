---
name: sas-conversion
description: Drive the SAS conversion loop over the sas-ref MCP tools.
version: 0.1.0
status: active
author: Matthew Haubach (buntas-tofu), Hermes Agent
license: GFDL-1.2
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sas, conversion, mcp, advisory, rulebook]
    related_skills: [sas-kb-maintenance]
---

# SAS Conversion Skill

The analyze, plan, convert, validate, document loop over the SASchi-Roku
knowledge MCP. This skill interprets and drafts; it never verifies. A
conversion is accepted only when a gate in the campaign lane runs and the
numbers match. Dependency stance: requires the sas-ref MCP server (this
repository's `mcp/` subproject) and a resolved `kb/`.

## When to Use

- Converting SAS programs, steps, or macros to Python (pandas, polars,
  duckdb) or R.
- Reviewing a converted program for silent semantic differences.
- Planning a conversion and needing the coverage picture first.

Don't use for: accepting or signing off a conversion (that is the gate's
job, in the campaign lane), or for maintaining the knowledge base itself
(use `sas-kb-maintenance`).

## Prerequisites

- The sas-ref MCP server is wired into the client (repository-root
  `.mcp.json`, or an install of `sas-ref-mcp`; see `mcp/README.md`).
- Tool names below are the server's exact names; if one is missing, the
  server and this skill have drifted: fix the pair together, never one side.

## Procedure

1. **Load the contract.** Call `conversion_contract`. Record the tolerance
   tier for each construct class you will touch (closed form, iterative,
   stochastic) and the five contract invariants. Criterion: every later
   numeric comparison names its tier.
2. **Inventory the constructs.** For each SAS statement, data set option,
   function, or macro facility in the source, call `lookup_capability`.
   Record the disposition. `UNASSESSED` or a null universe means a coverage
   gap: flag it, plan extra evidence, never assume. Criterion: every
   construct in the source has a disposition on paper.
3. **Pull the rules.** For each construct, `search_rules` with the
   construct as the query, then `lookup_rule` on the chosen rule id. One
   blessed target per language per rule: do not mix alternates unless the
   rule's `alternates_when` applies to your data shape. Criterion: every
   construct maps to a rule id or to a human-review note.
4. **Surface the landmines before writing code.** `get_landmines` for the
   chosen rules and families, plus `search_landmine_cards` for each
   construct family; the cards carry the long-form silent-difference
   material. Criterion: every `silent_difference_checks` entry for the
   chosen rules is written down with the mechanism that will detect a
   disagreement.
5. **Follow the target guide.** `get_conversion_guide` for the target
   (duckdb, polars, r). `required_settings` are mandatory, not advisory;
   `forbidden_patterns` must not appear anywhere in the draft. Criterion: a
   self-grep of the draft finds zero forbidden patterns and every required
   setting present.
6. **Draft the conversion.** Write the target program. Where a construct is
   `NO-DIRECT-EQUIVALENT`: STOP that construct and emit a human-review
   ticket instead of a guess. Pull worked evidence with `search_corpus`
   (a similar Rosetta task) and `search_evidence` (the family report).
   Criterion: the draft compiles or parses in its target language.
7. **Hand off to the gate.** The draft, its rule ids, its landmine
   checklist, and its tolerance tiers go to the campaign lane's gates.
   Stochastic-tier outputs are validated as distributions, never as draws.
   Criterion: the handoff package is complete enough for a gate to run
   without asking you anything.
8. **Document.** Record the rules used with the rulebook stamp version
   (the `_provenance` footer), the cards consulted, the guide followed, the
   human-review tickets, and the advisory statement. Criterion: a reader
   can reproduce your reasoning from the document alone.

MCP-native clients can collapse steps 1 through 5 with the server prompts:
`convert` (the full framing), `landmine_audit` (step 4 alone), and
`coverage_gap` (the planning picture from step 2).

## Pitfalls

- The most valuable output of this loop is not the code, it is the
  landmine checklist. A conversion that runs and disagrees silently is the
  failure mode the whole reference exists to prevent.
- `search_rules` ranks by keyword; a thin result set means re-query with
  the SAS syntax as written in the source (for example `SET a b;`), not
  with prose about it.
- A capability entry with `rule_ids` empty and disposition `RULE` or
  `GATED` is mid-migration upstream: treat it as `UNASSESSED` for planning.
- The knowledge base is a copy under stamp control; if a rule looks wrong,
  that is an upstream conversation, not a local edit (see
  `sas-kb-maintenance`).

## Verification

The loop is complete when: every construct has a disposition; every rule
used is named with its stamp version; the landmine checklist exists and
each check names its detection mechanism; the draft contains no forbidden
pattern and every required setting; and the handoff states, in writing,
that acceptance belongs to the gate.
