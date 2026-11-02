# SL-005: An explicit OUTPUT changes row emission for the whole step

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: Program execution model; DS-006 adjacent.
Coverage assessment: Dedicated output-cardinality fixture proposed. An entry's existence is not an equivalence proof.

## Failure mechanism

An explicit OUTPUT statement replaces automatic end-of-iteration output. Its position captures the current variable values, and multiple executions can emit multiple rows.

## Witness to build (not executed here)

A single iteration assigns x=4, outputs, assigns x=9, and outputs again. Expect two rows, 4 and 9, with no additional automatic row. A conditionally skipped OUTPUT may yield no row.

## Preservation contract and mitigation (recommendation)

Represent output as an event, not a final dataframe snapshot. Compare destination datasets, emission order, row multiplicity, and values at each output point.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S06: [OUTPUT statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
