# SL-010: TRANSPOSE uses formatted IDs and a specific duplicate policy

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-009.
Coverage assessment: Duplicate handling corrected; naming collisions and missing IDs are expansion targets. An entry's existence is not an equivalence proof.

## Failure mechanism

PROC TRANSPOSE derives output names from formatted ID values. Duplicates stop the procedure unless LET selects the last occurrence; missing ID values are excluded with a warning.

## Witness to build (not executed here)

Choose two distinct raw IDs that format to the same label, then values whose normalized output names collide. Test with and without LET and include a missing ID.

## Preservation contract and mitigation (recommendation)

Validate names after formatting and normalization. Do not replace duplicate handling with an averaging pivot. Compare schema, selected value, warning status, and row loss.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S10: [PROC TRANSPOSE ID statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000063668.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
