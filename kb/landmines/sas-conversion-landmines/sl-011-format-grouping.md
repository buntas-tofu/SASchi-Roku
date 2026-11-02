# SL-011: Formats can define groups rather than merely change display

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-010, ST-001, ST-015.
Coverage assessment: Existing format primitives; procedure-option combinations need review. An entry's existence is not an equivalence proof.

## Failure mechanism

PROC MEANS normally uses formatted CLASS values. GROUPINTERNAL, PRELOADFMT, MISSING, and multilabel formats alter the grouping contract; a multilabel format can assign one value to multiple groups.

## Witness to build (not executed here)

Map raw codes 1 and 2 to one label, then compare formatted grouping with GROUPINTERNAL. Add a missing class and an unobserved preloaded level as distinct cases.

## Preservation contract and mitigation (recommendation)

Carry the format catalog and procedure options through conversion. Compare group membership, zero-count levels, counts, and the output representative value separately.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S11: [PROC MEANS CLASS statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000146731.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
