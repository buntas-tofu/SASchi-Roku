# SL-022: A SAS array can alias variables rather than copy their values

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-016.
Coverage assessment: Existing array semantics; declaration order and retention need composition tests. An entry's existence is not an equivalence proof.

## Failure mechanism

A SAS ARRAY groups variables for indexed access; its name is not a separate ordinary dataset variable. Initialization and temporary arrays also affect retention.

## Witness to build (not executed here)

Declare an array over x and y, assign through the second element, and inspect y. Then assign y directly and inspect that array element; a copied Python list will not reproduce both directions automatically.

## Preservation contract and mitigation (recommendation)

Preserve aliasing, bounds, variable order, and initialization lifetime. Resolve special variable lists against the correct compile-time schema.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S22: [ARRAY statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p08do6szetrxe2n136ush727sbuo.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
