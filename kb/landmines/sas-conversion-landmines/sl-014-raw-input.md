# SL-014: A short input record can consume the next line or become missing

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-021 adjacent; raw INPUT is a separate surface.
Coverage assessment: New raw-record boundary fixtures proposed. An entry's existence is not an equivalence proof.

## Failure mechanism

INFILE FLOWOVER, MISSOVER, and TRUNCOVER differ when the requested field is shorter than its informat width or absent. A CSV reader's line policy does not establish formatted INPUT equivalence.

## Witness to build (not executed here)

Read records '1', '22', and '33333' with a five-column numeric informat under each end-of-record option. Record both resulting values and the number of consumed physical lines.

## Preservation contract and mitigation (recommendation)

Inventory INPUT style, informats, delimiters, quoting, line endings, and INFILE options. Distinguish raw-record parsing from PROC IMPORT type guessing; both require their own fixture.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S14: [INFILE statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1rill4udj0tfun1fvce3j401plo.htm). Scope: SAS 9.3 statement reference. Consulted 2026-09-15.
