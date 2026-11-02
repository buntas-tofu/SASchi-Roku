# SL-004: Moving a filter can change FIRST./LAST. and group results

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-005, DS-006.
Coverage assessment: Adjacent coverage; explicit filter-order witness proposed. An entry's existence is not an equivalence proof.

## Failure mechanism

WHERE filters input before BY groups are established; a subsetting IF acts later. Equivalent-looking predicates therefore need not preserve group-boundary logic.

## Witness to build (not executed here)

For one group with rows keep=0 then keep=1, compare WHERE keep=1 followed by FIRST.key with subsetting IF keep=1 followed by FIRST.key. Only the WHERE version makes the surviving row the first row of its filtered group.

## Preservation contract and mitigation (recommendation)

Preserve the sequence of input selection, group formation, state changes, and output. Do not push a filter upstream merely as an optimization.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S03: [WHERE statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1xbr9r0s9veq0n137iftzxq4g7e.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
