# SL-023: A procedure can finish without creating the expected ODS dataset

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P2, an engineering judgment, not an observed frequency.
Related rulebook entries: MC-007, MC-008, MC-009.
Coverage assessment: Operational acceptance beyond numeric fixtures. An entry's existence is not an equivalence proof.

## Failure mechanism

ODS requests manage output objects that a procedure actually creates. An unclosed interactive procedure or suppressing an object with procedure options can prevent the requested dataset from appearing.

## Witness to build (not executed here)

Run two interactive procedure steps with an ODS OUTPUT request between them, then repeat with an explicit QUIT and correctly scoped request. Check actual dataset creation rather than the printed report.

## Preservation contract and mitigation (recommendation)

Declare required datasets, schemas, log conditions, and procedure lifecycle. Treat missing artifacts as failures even when the job process finishes. Separate output suppression from preventing object generation.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S23: [Interactive procedure and ODS lifecycle](https://support.sas.com/kb/37/105.html). Scope: SAS Usage Note 37105; consulted current page. Consulted 2026-09-15.
