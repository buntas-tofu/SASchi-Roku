# SL-002: Missing values can change matching and filtering across engines

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-019, SQL-001.
Coverage assessment: Existing family; engine-specific combinations need explicit scope. An entry's existence is not an equivalence proof.

## Failure mechanism

Base SAS missing values, tagged special missings, dataframe nulls, and ANSI NULL are not interchangeable. PROC SQL and pandas can match missing keys where ordinary SQL equality does not.

## Witness to build (not executed here)

Join tables containing ordinary missing keys, different special-missing tags, zero, and a negative value. Separately test a missing value as an IF condition and as a relational operand.

## Preservation contract and mitigation (recommendation)

Write separate contracts for truth, ordering, equality, grouping, and joins. Retain missing tags until the consumer's policy is chosen. Avoid the blanket claim that all missing comparisons are false.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S08: [PROC SQL joins and missing keys](https://support.sas.com/documentation/cdl/en/sqlproc/62086/HTML/default/a001361784.htm). Scope: SAS 9.2 SQL Procedure User's Guide. Consulted 2026-09-15.
- T01: [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html). Scope: pandas 3.0.5 page as served; stable URL is mutable. Consulted 2026-09-15.
- T03: [Haven conversion semantics](https://haven.tidyverse.org/articles/semantics.html). Scope: Haven current documentation; mutable URL. Consulted 2026-09-15.
