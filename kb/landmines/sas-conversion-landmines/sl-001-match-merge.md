# SL-001: Many-to-many MERGE is not a relational join

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-002, DS-003.
Coverage assessment: Existing rule family; retain as a regression anchor. An entry's existence is not an equivalence proof.

## Failure mechanism

Within a BY group, SAS match-merge does not form every pair. Source order, retained values, shared column names, and unequal group sizes affect the result.

## Witness to build (not executed here)

One key appears twice in A and three times in B, with distinct non-key column names. The documented match-merge produces three rows; an equijoin produces six. Compare row content as well as count.

## Preservation contract and mitigation (recommendation)

Validate key multiplicity and source order before choosing a target join. Do not call pandas validate='many_to_many' a cardinality check: that setting permits the case without checking uniqueness.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S01: [MERGE statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000202970.htm). Scope: SAS 9.2 statement reference. Consulted 2026-09-15.
- T01: [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html). Scope: pandas 3.0.5 page as served; stable URL is mutable. Consulted 2026-09-15.
