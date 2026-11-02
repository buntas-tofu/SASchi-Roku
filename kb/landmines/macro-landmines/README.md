# Macro landmines: first collection

Status: candidate teaching corpus for migration practitioners, not an agency finding.
Twelve cards, original examples, source-backed explanations. No live SAS execution is claimed.

## Retrieval contract

Use one focused KB with no chunking so the failure mechanism, example, correction,
and evidence status arrive together. Separate indexes per macro feature are not
justified. Families are named in every card for lexical retrieval; they are not
new filter fields. Use corpus=macro-landmines and doc_class=macro_landmine with
the existing metadata vocabulary.

All cards are unreviewed and asserted. A primary source supports the mechanism,
but does not execute our example or establish cross-language equivalence.
Do not promote the whole collection to gate or receipt based on a documentation
citation. Scope is the cited Base SAS 9.x editions, not a claim about every Viya
or other SAS runtime.

## Cards

| ID | Topic | Family |
|---|---|---|
| [ML-001](ml-001-symput-timing.md) | A macro reference reads the old value inside its producing DATA step | timing |
| [ML-002](ml-002-call-execute-order.md) | CALL EXECUTE mixes immediate macro execution with queued SAS statements | timing |
| [ML-003](ml-003-scope-leakage.md) | A helper macro overwrites a caller or session variable | scope |
| [ML-004](ml-004-symputx-scope.md) | CALL SYMPUTX can write a different symbol table than intended | scope |
| [ML-005](ml-005-quoting-and-rescan.md) | Data containing commas, ampersands, or operators becomes macro syntax | quoting |
| [ML-006](ml-006-period-delimiter.md) | A suffix changes the variable name or consumes the dataset separator | resolution |
| [ML-007](ml-007-indirect-resolution.md) | An indirect reference needs another scan | resolution |
| [ML-008](ml-008-sysfunc-boundary.md) | DATA step function syntax does not transfer unchanged into %SYSFUNC | functions |
| [ML-009](ml-009-integer-evaluation.md) | Macro arithmetic silently discards a fractional result | arithmetic |
| [ML-010](ml-010-sql-empty-result.md) | SELECT INTO leaves an old value when the result has no rows | state |
| [ML-011](ml-011-generated-by-list.md) | A BY list is not a single FIRST. variable | generated-code |
| [ML-012](ml-012-scan-empty-fields.md) | %SCAN collapses empty list positions unless instructed otherwise | lists |

## Use and validation

The canonical inventory and source metadata are in [collections.json](../../collections.json).
Run `python3 tools/check_catalog.py` from the repository root to validate it.
Consumers should pin a Git commit and preserve evidence status and citations.
AWS-specific packaging is maintained by the separate Bedrock deployment project.
Only the twelve named cards belong in a teaching index; this README, SOURCES.md,
curation notes, and evaluation answers are outside that ingestion list.

## Evidence and growth

SOURCES.md records the public references. Internal curation records remain with the originating project and are not published here.
No third-party program corpus or full vendor manual is reproduced.

Next candidates: conditional %LET under DATA step IF, macro comments, autocall
search-path collisions, blank/missing loop bounds, nested quoting and %UNQUOTE,
and macros that switch aggregation grain. Each needs a named mechanism and
source review before joining the explicit source list.

For live validation, save runtime version, options, source hash, log, output,
and verdict per card. Use a fresh session to expose rather than inherit state.
Create independent evaluation cases with different data and compositions outside
this corpus. Running the teaching snippets tests their behavior; retrieving their
answers does not demonstrate generalization.
