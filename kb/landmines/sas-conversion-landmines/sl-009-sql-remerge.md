# SL-009: A grouped PROC SQL query can still return detail rows

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: SQL-002.
Coverage assessment: Existing rule; downstream row-count consequences need end-to-end witnesses. An entry's existence is not an equivalence proof.

## Failure mechanism

PROC SQL may calculate group summaries and remerge them with detail columns. A target GROUP BY that collapses groups or rejects the query is not automatically equivalent.

## Witness to build (not executed here)

For two rows in a group with values 2 and 6, select the group, the detail value, and its group mean. A remerge can retain two rows with a mean of 4 on each.

## Preservation contract and mitigation (recommendation)

Translate the documented shape with a window operation or aggregate-plus-join after checking nulls and duplicates. Adding a detail column to GROUP BY can change the statistic rather than repair it.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S07: [Remerging summary statistics](https://support.sas.com/techsup/notes/v8/4/308.html). Scope: SAS Usage Note 4308; older documented PROC SQL behavior. Consulted 2026-09-15.
