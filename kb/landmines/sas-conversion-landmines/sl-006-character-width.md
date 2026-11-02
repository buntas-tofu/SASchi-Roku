# SL-006: Character width and encoding are part of the data contract

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-015, DS-018 adjacent.
Coverage assessment: Existing text family; transcoding and schema-order frontier. An entry's existence is not an equivalence proof.

## Failure mechanism

An early occurrence can establish a character variable's length before a longer value is assigned. Byte widths can also become insufficient during transcoding; a character count is not always a storage-byte count.

## Witness to build (not executed here)

Assign a short literal before a longer literal, then repeat with a declared length before the first assignment. Separately test multibyte text during encoding conversion with a fixed storage width.

## Preservation contract and mitigation (recommendation)

Capture type, length, encoding, declaration order, and truncation behavior. Do not silently widen columns while claiming exact legacy behavior; classify widening as a deliberate correction if desired.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S04: [Ways to Create Variables](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000695113.htm). Scope: SAS language concepts; cited 9.x edition. Consulted 2026-09-15.
- S24: [FedSQL data types and transcoding](https://support.sas.com/documentation/cdl/en/fedsqlref/67364/HTML/default/n19bf2z7e9p646n0z224cokuj567.htm). Scope: SAS 9.4 FedSQL third edition; byte-width warning. Consulted 2026-09-15.
