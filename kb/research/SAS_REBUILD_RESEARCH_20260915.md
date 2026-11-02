# SAS rebuild and conversion landmines: research synthesis

Status: candidate research and implementation-priority proposal for the operator,
2026-09-15. Not an agency finding, runtime certification, or exhaustive systematic
review. The operator may use this to choose validation work; no new conversion
capability is enabled by these cards.

## Finding

The largest shared failure mode is a changed execution or statistical contract
hidden by plausible syntax. A reliable rebuild must preserve what constitutes a
row, when state changes, which observations enter an analysis, and what metadata
means. Translating statement names is insufficient.

This pass produced 25 source-grounded cards plus a machine-readable fixture queue.
Twelve separate cards cover LLM workflow failure modes. The combined source register
contains 43 primary documentation, original research, and community comparison
references. Most SAS sources are explicitly scoped historical 9.x documentation;
current Python/R pages were consulted for target behavior. This is deliberate
version scoping, not proof that a historical default applies to every current engine.

## Method and evidence boundaries

The starting point was the existing rulebook, semantics work, campaign adjudication,
and macro pack. Targeted searches then followed named behavior gaps into SAS
reference sections, usage notes, package-maintainer documentation, and CAMIS
comparisons. Original LLM papers were read at abstract level or in selected relevant
sections, as the source register records. No full-paper review is implied for every
citation, and no vendor manual or community program was bulk-copied.

Inclusion required a named mechanism, a source that supports its scope, an observable
consequence, and a proposed validation witness. Generic advice without a concrete
contract was left out. Existing rule families were included where a boundary case
or composition remains worth testing; they are not described as newly discovered
SAS behavior.

A documented rule, an original test design, an existing project receipt, and a
fresh live-SAS result are different evidence classes. This pass creates the first
two and reviews references to the third. It produces no fourth-class evidence.
All new cards remain asserted/unreviewed.

## What changes the migration plan

### 1. Preserve cardinality before comparing numbers

Two records for a key on one side and three on the other can become three rows
under match-merge or six under a relational join. An aggregate comparison can
conceal that change. Remerge and explicit OUTPUT add independent row-emission
contracts. The first validation pass should compare row identities, multiplicities,
and destination datasets before numeric tolerances.
Sources: [MERGE statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000202970.htm), [Remerging summary statistics](https://support.sas.com/techsup/notes/v8/4/308.html), [OUTPUT statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm).

### 2. Preserve event order and variable lifetime

A filter before group formation can change FIRST./LAST. relative to the same
predicate applied later. A LAG queue changes only when its occurrence executes.
Conditional reads, retained values, and output-time snapshots cannot be assumed
equivalent to a sequence of vectorized assignments. These are reasons to validate
the composed DATA step, not just helper functions.
Sources: [WHERE statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1xbr9r0s9veq0n137iftzxq4g7e.htm), [LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm), [RETAIN statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000214163.htm).

The corrected conditional-LAG rule and blocked-emitter behavior already exist in
the inspected release. The new cards retain those as regression lessons; they do
not report the repaired defects as still open.

### 3. Treat metadata as input to computation

Formats can combine class levels and generate transpose column names. Special
missing tags, labels, encodings, widths, and catalogs can therefore affect output
without changing the apparent numeric payload. A successful file read is not a
successful metadata migration.
Sources: [PROC MEANS CLASS statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000146731.htm), [PROC TRANSPOSE ID statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000063668.htm), [Haven conversion semantics](https://haven.tidyverse.org/articles/semantics.html), [Haven SAS reader](https://haven.tidyverse.org/reference/read_sas.html).

Recommendation: compare typed values and metadata as separate layers, then exercise
the downstream consumers that use that metadata. A portable sidecar needs a schema
and a reader; storing it beside a table without consuming it is not preservation.

### 4. Align the estimand and design before relaxing tolerance

Weight inclusion, divisor choices, quantile definitions, event coding, survey
domains, covariance structures, and tie methods can all select a different
calculation. These differences need explicit settings, not a larger tolerance.
Sources: [PROC MEANS WEIGHT statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000146736.htm), [Statistical computations in PROC MEANS](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000608466.htm), [PROC LOGISTIC odds-ratio reversal](https://support.sas.com/kb/39/085.html), [SURVEYMEANS domain analysis](https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_surveymeans_examples02.htm).

CAMIS provides useful original cross-language comparisons for mixed models and
MMRM. It shows why matching a formula is only a starting point. Its example
agreements remain bounded by their model specification and environment; they are
not receipts for our programs. Sources: [CAMIS: R versus SAS MMRM](https://psiaims.github.io/CAMIS/Comp/r-sas_mmrm.html), [CAMIS: R versus SAS random effect models](https://psiaims.github.io/CAMIS/Comp/r-sas_random_effects_models.html).

One concrete default trap is ordinary Cox regression: the cited PHREG contract
uses Breslow ties while ordinary R coxph uses Efron; coxph also documents multistate
exceptions. State the selected method instead of assuming either default is
universal. Sources: [PROC PHREG MODEL statement](https://support.sas.com/documentation/cdl/en/statug/66859/HTML/default/statug_phreg_syntax17.htm), [R survival coxph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html).

### 5. Specify the engine and ingest boundary

PROC SQL, FedSQL, and remote SQL do not share one missing-value contract. The
FedSQL reference documents mode-dependent behavior and special-missing information
loss. Raw INPUT end-of-record handling is also separate from CSV type inference:
an apparently malformed record can change how many physical lines become one
observation. Sources: [FedSQL null and missing modes](https://support.sas.com/documentation/cdl/en/fedsqlref/67364/HTML/default/n1c5ladx770rq4n11a0mi33q9pad.htm), [INFILE statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1rill4udj0tfun1fvce3j401plo.htm).

SAS-to-CAS rebuilding remains a wider research area. This pass establishes the
FedSQL mode issue, not comprehensive CAS thread, partition, or distributed-order
semantics. Those need their own engine-specific investigation.

## Coverage and fixture queue

Priority is engineering judgment based on downstream impact and breadth, not a
measured incidence rate. P0 means row/state/ingest contracts that can invalidate
later comparisons; P1 means transformation and estimator contracts; P2 means
stochastic or operational acceptance work. P2 does not mean optional when a program
uses that feature.

| Card | Priority | Existing rule or surface | Proposed coverage disposition |
|---|---|---|---|
| [SL-001](../landmines/sas-conversion-landmines/sl-001-match-merge.md) | P0 | DS-002, DS-003 | Existing rule family; retain as a regression anchor |
| [SL-002](../landmines/sas-conversion-landmines/sl-002-missing-keys.md) | P0 | DS-019, SQL-001 | Existing family; engine-specific combinations need explicit scope |
| [SL-003](../landmines/sas-conversion-landmines/sl-003-pdv-state.md) | P0 | DS-006; program execution model | Existing primitives; whole-step composition needs validation |
| [SL-004](../landmines/sas-conversion-landmines/sl-004-where-if.md) | P0 | DS-005, DS-006 | Adjacent coverage; explicit filter-order witness proposed |
| [SL-005](../landmines/sas-conversion-landmines/sl-005-explicit-output.md) | P0 | Program execution model; DS-006 adjacent | Dedicated output-cardinality fixture proposed |
| [SL-006](../landmines/sas-conversion-landmines/sl-006-character-width.md) | P0 | DS-015, DS-018 adjacent | Existing text family; transcoding and schema-order frontier |
| [SL-007](../landmines/sas-conversion-landmines/sl-007-lag-history.md) | P0 | DS-007 | Corrected rule and target gate exist; expand composition cases |
| [SL-008](../landmines/sas-conversion-landmines/sl-008-sort-survivors.md) | P0 | DS-008 | Existing family; explicit ordering and engine conditions remain necessary |
| [SL-009](../landmines/sas-conversion-landmines/sl-009-sql-remerge.md) | P0 | SQL-002 | Existing rule; downstream row-count consequences need end-to-end witnesses |
| [SL-010](../landmines/sas-conversion-landmines/sl-010-transpose-names.md) | P1 | DS-009 | Duplicate handling corrected; naming collisions and missing IDs are expansion targets |
| [SL-011](../landmines/sas-conversion-landmines/sl-011-format-grouping.md) | P1 | DS-010, ST-001, ST-015 | Existing format primitives; procedure-option combinations need review |
| [SL-012](../landmines/sas-conversion-landmines/sl-012-rounding-family.md) | P1 | DS-012, DS-020 | Half-away reference exists; fuzzing neighborhood remains a separate contract |
| [SL-013](../landmines/sas-conversion-landmines/sl-013-date-intervals.md) | P1 | DS-011 | Existing INTCK/INTNX family; options and parsing remain explicit |
| [SL-014](../landmines/sas-conversion-landmines/sl-014-raw-input.md) | P0 | DS-021 adjacent; raw INPUT is a separate surface | New raw-record boundary fixtures proposed |
| [SL-015](../landmines/sas-conversion-landmines/sl-015-weights.md) | P1 | ST-001 and procedure-specific statistical rules | Known corrected weight behavior; broaden procedure contrasts |
| [SL-016](../landmines/sas-conversion-landmines/sl-016-quantiles.md) | P1 | ST-002 | Existing mapping; weighted and approximate paths need separate scope |
| [SL-017](../landmines/sas-conversion-landmines/sl-017-logistic-contract.md) | P1 | ST-008; ST-007 adjacent | Rulebook covers settings; model-specific validation still required |
| [SL-018](../landmines/sas-conversion-landmines/sl-018-survey-domain.md) | P1 | SV-002; SV-001, SV-003 adjacent | Existing survey routing; verify variance design explicitly |
| [SL-019](../landmines/sas-conversion-landmines/sl-019-rng-contract.md) | P2 | ST-016, SV-006; stochastic tolerance tier | Existing stochastic policy; per-generator validation required |
| [SL-020](../landmines/sas-conversion-landmines/sl-020-metadata-roundtrip.md) | P0 | DS-018, DS-019; GP-03 | Existing interchange policy; catalog and encoding round trips need witnesses |
| [SL-021](../landmines/sas-conversion-landmines/sl-021-engine-mode.md) | P1 | SQL-001, DS-019 | Engine-mode frontier; no blanket Base SAS to CAS claim |
| [SL-022](../landmines/sas-conversion-landmines/sl-022-array-aliasing.md) | P1 | DS-016 | Existing array semantics; declaration order and retention need composition tests |
| [SL-023](../landmines/sas-conversion-landmines/sl-023-ods-lifecycle.md) | P2 | MC-007, MC-008, MC-009 | Operational acceptance beyond numeric fixtures |
| [SL-024](../landmines/sas-conversion-landmines/sl-024-mixed-model-contract.md) | P1 | ST-010 | Existing human-review/statistical routing; compare full model specification |
| [SL-025](../landmines/sas-conversion-landmines/sl-025-survival-ties.md) | P1 | ST-011 | Existing survival family; tied-event and risk-set fixtures needed |

The queue CSV records the same order and marks every proposed witness as not run.
An existing rule or test is an entry point for review, not proof that every option
combination in this table is covered.

## Recommended implementation sequence

**Wave A: composed execution.** Build original witnesses for filter placement,
explicit OUTPUT, conditional SET retention, unequal-duplicate merge, and SQL
remerge. Compare complete outputs and logs. Keep a deliberately wrong join,
shift, or filter-pushdown implementation that the tests must reject.

**Wave B: input and metadata.** Add short physical records, multibyte widths,
catalog-dependent grouping, formatted ID collisions, and tagged-missing round
trips. Bind tests to input bytes, schema, format definitions, and encoding.

**Wave C: estimator settings.** Freeze analysis populations, weights, design
matrices, contrasts, covariance models, tie handling, and degrees of freedom.
Only then choose tolerances for iterative numerical algorithms. Compare named
estimands and uncertainty, not only coefficient positions.

**Wave D: engine and operational behavior.** Pin FedSQL mode, driver, runtime,
RNG contract, procedure lifecycle, and required artifacts. Missing ODS datasets
and altered warnings must remain observable outcomes.

These are proposed waves, not implemented translator support.

## Acceptance record

Each promoted witness should bind:

1. SAS source and input hashes, product/version, host encoding, and relevant options.
2. Target source hash, locked dependencies, and actual execution command.
3. Expected-value derivation or independent SAS capture with its provenance.
4. Row count and identity, schema/metadata, values, logs, exit status, and side effects.
5. Comparator policy, including explicit missing-value handling and tolerance by output.
6. Passing positive case and failing known-wrong alternative.
7. The exact scope enabled by the result, with unsupported cases still blocked.

Teaching cards can explain these requirements but do not prove them. Their examples
and anticipated answers must stay separate from held-out KB evaluation.

## What remains open

Not exhaustively investigated here: Type III estimability under empty cells,
GEE correlation and robust covariance variants, optimizer-specific mixed-model
boundary behavior, hash-object duplicate and multidata modes, UPDATE/MODIFY
transaction semantics, compressed dataset precision, full informats and locale
parsing, DS2 and IML beyond the bounded matrix surface, and distributed CAS state.
The rulebook names several of these areas, but naming is not coverage.

No new third-party code corpus was ingested. No live SAS, target-language semantic
benchmark, local-model experiment, AWS upload, or retrieval benchmark was run in
this research pass. Package construction and checksum validation are separate
checks reported with the built packs.

## Source register

[SOURCES_20260915.json](SOURCES_20260915.json) records source IDs, URLs, consultation
date, and reading/version scope. Mutable pages are not archived content pins.
Recheck them against the actual runtime before implementing a version-sensitive rule.
