# SL-021: Moving PROC SQL to FedSQL can change missing-value semantics

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: SQL-001, DS-019.
Coverage assessment: Engine-mode frontier; no blanket Base SAS to CAS claim. An entry's existence is not an equivalence proof.

## Failure mechanism

FedSQL distinguishes ANSI-null and SAS-missing modes. The cited documentation describes different defaults by client path and loss of special missing tags when converted to null.

## Witness to build (not executed here)

Read .A, ordinary missing, blank text, and null through both declared modes. Compare equality predicates, joins, and the values written back to a SAS table.

## Preservation contract and mitigation (recommendation)

Record execution engine, connection path, mode, and data-source types. Do not treat PROC SQL, PROC FEDSQL, remote pass-through SQL, and CAS execution as one language implementation.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S21: [FedSQL null and missing modes](https://support.sas.com/documentation/cdl/en/fedsqlref/67364/HTML/default/n1c5ladx770rq4n11a0mi33q9pad.htm). Scope: SAS 9.4 FedSQL Language Reference, third edition. Consulted 2026-09-15.
