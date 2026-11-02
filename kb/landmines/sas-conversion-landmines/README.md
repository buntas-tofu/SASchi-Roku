# SAS conversion and rebuild landmines

Status: candidate reference collection for migration practitioners, not an agency finding.
25 cards. No new live-SAS or model evaluation result is claimed.

## Retrieval and evidence

Use whole-card retrieval with no chunking. These cards may share an index with
other whole-card public collections using corpus=sas-conversion-landmines and
doc_class=conversion_landmine. A pack is a versioned content boundary, not a requirement
to provision a separate index.

All cards are asserted/unreviewed. Sources support their scoped claims; proposed
scenarios and mitigations are marked as inference or unexecuted witness designs.
Historical project defects must not be described as current defects without
checking the current implementation. Broader LLM papers are not SAS benchmarks.

## Index

| ID | Topic |
|---|---|
| [SL-001](sl-001-match-merge.md) | Many-to-many MERGE is not a relational join |
| [SL-002](sl-002-missing-keys.md) | Missing values can change matching and filtering across engines |
| [SL-003](sl-003-pdv-state.md) | DATA step variables do not all reset in the same way |
| [SL-004](sl-004-where-if.md) | Moving a filter can change FIRST./LAST. and group results |
| [SL-005](sl-005-explicit-output.md) | An explicit OUTPUT changes row emission for the whole step |
| [SL-006](sl-006-character-width.md) | Character width and encoding are part of the data contract |
| [SL-007](sl-007-lag-history.md) | Conditional LAG tracks invocation history, not previous rows |
| [SL-008](sl-008-sort-survivors.md) | Tie order decides which duplicate survives |
| [SL-009](sl-009-sql-remerge.md) | A grouped PROC SQL query can still return detail rows |
| [SL-010](sl-010-transpose-names.md) | TRANSPOSE uses formatted IDs and a specific duplicate policy |
| [SL-011](sl-011-format-grouping.md) | Formats can define groups rather than merely change display |
| [SL-012](sl-012-rounding-family.md) | ROUND, ROUNDE, and ROUNDZ differ beyond a decimal-place label |
| [SL-013](sl-013-date-intervals.md) | Calendar boundaries are not elapsed-duration division |
| [SL-014](sl-014-raw-input.md) | A short input record can consume the next line or become missing |
| [SL-015](sl-015-weights.md) | A WEIGHT column does not identify a universal weighted estimator |
| [SL-016](sl-016-quantiles.md) | The same percentile name can select a different estimator |
| [SL-017](sl-017-logistic-contract.md) | Event and CLASS coding can reverse an odds ratio |
| [SL-018](sl-018-survey-domain.md) | Subsetting raw rows is not generally equivalent to domain analysis |
| [SL-019](sl-019-rng-contract.md) | Equal seeds do not establish equal random streams across languages |
| [SL-020](sl-020-metadata-roundtrip.md) | A readable SAS dataset can still lose meaning on conversion |
| [SL-021](sl-021-engine-mode.md) | Moving PROC SQL to FedSQL can change missing-value semantics |
| [SL-022](sl-022-array-aliasing.md) | A SAS array can alias variables rather than copy their values |
| [SL-023](sl-023-ods-lifecycle.md) | A procedure can finish without creating the expected ODS dataset |
| [SL-024](sl-024-mixed-model-contract.md) | Matching a mixed-model formula does not match its covariance or inference |
| [SL-025](sl-025-survival-ties.md) | Cox regression defaults can differ on tied events |

## Use and validation

The canonical inventory and source metadata are in [collections.json](../../collections.json).
Run `python3 tools/check_catalog.py` from the repository root to validate it.
Consumers should pin a Git commit and preserve evidence status and citations.
AWS-specific packaging is maintained by the separate Bedrock deployment project.
Only the named cards belong in a teaching index. Research reports, source registers,
proposed test queues, and evaluation answers are outside that ingestion list.

The [SAS research synthesis](../../research/SAS_REBUILD_RESEARCH_20260915.md) explains coverage and priorities.
