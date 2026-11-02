# SL-020: A readable SAS dataset can still lose meaning on conversion

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-018, DS-019; GP-03.
Coverage assessment: Existing interchange policy; catalog and encoding round trips need witnesses. An entry's existence is not an equivalence proof.

## Failure mechanism

Haven exposes SAS catalog input, encoding controls, labels, and tagged missing semantics. Reading numeric values successfully does not prove preservation of the metadata that downstream code interprets.

## Witness to build (not executed here)

Round-trip an identifier with leading zeros, a labeled value, a special missing tag, a date value, and multibyte text. Compare typed values and metadata separately.

## Preservation contract and mitigation (recommendation)

Retain a reviewed metadata sidecar with the converted table. Validate labels, format names, missing tags, widths, and encoding; do not claim Parquet alone preserves every SAS attribute.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- T03: [Haven conversion semantics](https://haven.tidyverse.org/articles/semantics.html). Scope: Haven current documentation; mutable URL. Consulted 2026-09-15.
- T04: [Haven SAS reader](https://haven.tidyverse.org/reference/read_sas.html). Scope: Haven current documentation; mutable URL. Consulted 2026-09-15.
