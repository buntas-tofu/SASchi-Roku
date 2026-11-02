# SL-008: Tie order decides which duplicate survives

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-008.
Coverage assessment: Existing family; explicit ordering and engine conditions remain necessary. An entry's existence is not an equivalence proof.

## Failure mechanism

NODUPKEY retention depends on tie ordering. EQUALS supports retaining the first observation in a BY group, but first only has meaning relative to a reproducible input sequence.

## Witness to build (not executed here)

Give two equal keys different payloads, then reverse input order. Under explicit EQUALS the retained payload should follow the first input row. Repeat with the actual input engine rather than assuming its read order.

## Preservation contract and mitigation (recommendation)

Pin BY order, EQUALS/NOEQUALS, collation, and tie-breakers. Compare retained row identities, not just the number of unique keys.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S09: [PROC SORT: retaining the first BY observation](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a002473667.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
