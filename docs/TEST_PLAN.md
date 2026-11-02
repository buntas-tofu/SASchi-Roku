---
title: Phased skill evaluation plan
status: active
---

# Phased skill evaluation plan

Status: the principal accepted the starter batch on 2026-11-01. Maintainers may
execute and review that batch. Later phases are a planning sequence, not executed
results or a claim of general conversion reliability.

The principal described the starter as representative enough to establish an
analysis process and identify further skill directions. This records that scope.

| Phase | Proposed work | Advance when |
|---|---|---|
| 1. Assessment | Complete program, missing include/macro, unsupported procedure in an explicit capability profile, source versus dataset conversion | Inventories and limits match supplied evidence; no invented execution |
| 2. Individual behavior | MEAN, SUBSTR, LENGTH, CAT/CATX, ROUND, INTCK, COMPRESS, INPUT, FIRST/LAST, unconditional LAG in Python and R | Independent expected values, preserved rows/types/order, negative controls |
| 3. State and composition | Conditional LAG, retained state, WHERE versus IF, explicit OUTPUT, duplicate/missing merge keys, character widths through transforms | Whole-program outputs and state transitions match a declared contract |
| 4. Parquet | Ordinary types; dates and IDs; labels/catalogs/special missings; empty/encoding cases | Reopened typed values and metadata sidecars meet a recorded loss policy |
| 5. Repeatability | Six fresh tasks, three attempts each, with and without skill: 36 proposed generations | All first attempts retained, equivalent resources, descriptive results without population claims |
| 6. Catalog and MCP | Exact/ambiguous/stale/missing/conflicting retrieval, hostile retrieved instructions and tool failures | Provenance and uncertainty survive retrieval; MCP tests wait for an implementation |

## Accepted starter

Run phase 1's four assessments and phase 2's LENGTH and unconditional LAG in
both Python and R, eight task/target combinations. Review this batch before
expanding. Use original synthetic source and fixtures; no raw archive content.
The previous sum-array trial is now a regression, not a held-out task.

Before generation, freeze source, input, skill revision, request, rubric and
comparison policy. Evaluators receive inputs, not expected columns, sibling
reference implementations or previous answers. Preserve their first delivered
artifacts; repairs are separate attempts. Record runtime and exposed model
identity/settings, with unavailable fields explicit. Score decisions as well as
values. Negative controls must demonstrate that the comparison detects errors.

SAS execution is a separate evidence milestone across phases. Agreement between
Python, R and hand-derived expectations is not a live-SAS comparison. Source
module references are candidate teaching evidence, not authority for unseen cases.

See [the starter contract](../trials/starter-batch/CONTRACT.md) and its [recorded
results](../trials/starter-batch/README.md) for the bounded test surface. Future skill directions are proposals until
observed needs justify a scope and independent evaluation.
