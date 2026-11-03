---
title: Phased skill evaluation plan
status: active
---

# Phased skill evaluation plan

Status: the principal accepted the starter batch on 2026-11-01 and three follow-on
workflows on 2026-11-02. Maintainers may review their recorded bounded results.
Unrun portions of the phases remain proposals, not executed results or a claim
of general conversion reliability.

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
results](../trials/starter-batch/README.md) for the bounded test surface.

## Accepted follow-on workflows, 2026-11-02

[Decision 0002](decisions/0002-three-skill-proposals.md) records approval to develop
and evaluate three distinct skills. The [follow-on package](../trials/skill-proposals/README.md)
preserves frozen expectations and unmodified first deliveries.

| Workflow | Executed/reviewed surface | Remaining boundary |
|---|---|---|
| Dependency and macro inventory | Transitive includes, competing macro definitions, unresolved hook, synthetic provenance; seven review criteria passed | Actual SAS-generated source and observed runtime context |
| Character and metadata contract | Decoded synthetic envelopes to reopened CSV and raw-byte/tag companions; 12 parent checks passed | SAS-binary reader, base R consumer and Parquet round trip |
| Stateful failure diagnosis | Original failure reproduced; two-step Python/R repairs match stage and want through 16 interface/case checks; six incorrect outputs rejected | Live SAS, BY/WHERE, merge semantics and broader state combinations |

These 35 machine checks and artifact review are one exploratory invocation per
new skill. Python and R repairs came from the same state evaluator. The earlier
ASCII/NUL gap is retained unchanged; an explicit raw representation in a new
contract does not retroactively broaden acceptance of the old R interface.
Other individual-behavior cases and later-phase slices remain unrun except as
recorded below.

## State filtering follow-up, 2026-11-02

After the principal requested a return to skill work, the agent selected WHERE
versus subsetting IF as the next bounded part of phase 3. This is an implementation
choice within the plan, not a principal-specified fixture list. The
[trial contract and results](../trials/state-filter-timing/README.md) preserve one
fresh paired Python/R delivery using the existing state-diagnosis skill.

All six artifact-review criteria and 31 parent machine checks passed: 24
case/target/interface comparisons, the reproduced original failure, and six
rejected wrong outputs. Every comparison covers both independent DATA-step
outputs. WHERE is written after state updates but still filters before processing;
subsetting IF rejects output only after preceding state changes. Row counts match
even when values differ. Native Python and R ran; SAS did not.

The instructions remain unchanged. Parent acceptance stays with the six supplied
cases and declared interfaces. Agent-expanded self-tests are retained separately.
BY boundaries, merge keys, R metadata consumption, Parquet and live-SAS capture
remain open work.

## Accepted group, merge and width batch, 2026-11-02

The principal accepted the next immediate batch: group boundaries, merge behavior
and character-width propagation. The [frozen contract](../trials/state-boundaries/CONTRACT.md)
defines 16 cases across three fresh evaluations using existing skills. The parent
oracle and adapters were frozen before dispatch. Each evaluation supplies both
Python and R, so targets are paired rather than independently generated.

The planned checks cover nested FIRST/LAST flags and queue state, duplicate and
ordinary-missing merge keys with shared columns, and fixed widths through two
DATA steps into reopened CSV plus a width companion. Exact printable-ASCII scope
does not close the earlier NUL gap or establish general metadata interchange.
Parquet, broader repeatability and MCP remain separate phases.

[Recorded results](../trials/state-boundaries/README.md): all 89 parent checks
and 12 artifact criteria passed against unchanged first deliveries under Python
3.12.3 and native R 4.3.3. The 89 comprise 64 case/target/interface comparisons,
12 unsorted-input refusals, one reproduced original failure and 12 rejected wrong
outputs. No skill instruction changed. Expanded evaluator self-tests, including
a reported overflow failure and repair, remain separate from parent acceptance.

The width companion is now exercised in base R under the narrow ASCII contract.
The wider metadata contract, Parquet round trips, live-SAS capture and the
with/without skill repeatability study remain unrun. Numeric overflow/recovery is
a candidate additional vector inferred from the evaluator's recorded failure.
