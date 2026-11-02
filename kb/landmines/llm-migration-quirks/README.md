# LLM failure modes in SAS migration

Status: candidate reference collection for migration practitioners, not an agency finding.
12 cards. No new live-SAS or model evaluation result is claimed.

## Retrieval and evidence

Use whole-card retrieval with no chunking. These cards may share an index with
other whole-card public collections using corpus=llm-migration-quirks and
doc_class=llm_failure_mode. A pack is a versioned content boundary, not a requirement
to provision a separate index.

All cards are asserted/unreviewed. Sources support their scoped claims; proposed
scenarios and mitigations are marked as inference or unexecuted witness designs.
Historical project defects must not be described as current defects without
checking the current implementation. Broader LLM papers are not SAS benchmarks.

## Index

| ID | Topic |
|---|---|
| [LQ-001](lq-001-invented-api.md) | A plausible package or API is not an executable capability |
| [LQ-002](lq-002-stale-api.md) | A once-valid API can be wrong for the installed version |
| [LQ-003](lq-003-syntax-is-not-equivalence.md) | Code that parses and runs can still implement the wrong program |
| [LQ-004](lq-004-context-omission.md) | A long prompt can contain a rule that the model fails to use |
| [LQ-005](lq-005-self-review.md) | Self-critique and model agreement are not independent semantic oracles |
| [LQ-006](lq-006-keyword-contamination.md) | Matching a keyword does not establish a relevant SAS construct |
| [LQ-007](lq-007-business-logic-rewrite.md) | A model can mistake explicit business logic for a language defect |
| [LQ-008](lq-008-shared-oracle.md) | Generated tests can repeat the same misconception as generated code |
| [LQ-009](lq-009-evaluation-leakage.md) | Retrieving an answer key can make a KB look more capable than it is |
| [LQ-010](lq-010-retrieved-instructions.md) | Comments and retrieved documents can contain instructions aimed at the model |
| [LQ-011](lq-011-partial-conversion.md) | A review ticket in a comment does not block unsafe partial execution |
| [LQ-012](lq-012-structured-confidence.md) | A well-formed record can contain a false claim or unusable citation |

## Use and validation

The canonical inventory and source metadata are in [collections.json](../../collections.json).
Run `python3 tools/check_catalog.py` from the repository root to validate it.
Consumers should pin a Git commit and preserve evidence status and citations.
AWS-specific packaging is maintained by the separate Bedrock deployment project.
Only the named cards belong in a teaching index. Research reports, source registers,
proposed test queues, and evaluation answers are outside that ingestion list.

The [LLM research synthesis](../../research/LLM_MIGRATION_QUIRKS_20260915.md) explains evidence and limits.
