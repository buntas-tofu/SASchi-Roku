# SL-007: Conditional LAG tracks invocation history, not previous rows

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-007.
Coverage assessment: Corrected rule and target gate exist; expand composition cases. An entry's existence is not an equivalence proof.

## Failure mechanism

Each LAG occurrence has a queue. It advances only when that occurrence executes, and a BY boundary does not by itself flush the queue.

## Witness to build (not executed here)

On values 10,20,30,40, invoke one LAG occurrence only on rows two and four. Expected returns at those invocations are missing and 20, rather than 10 and 30 from an unconditional shift.

## Preservation contract and mitigation (recommendation)

Distinguish conditional invocation from conditional use of an unconditional result. Include two independent occurrences, missing arguments, LAG2, and explicit group reset logic in the next fixtures.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S02: [LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm). Scope: SAS 9.3 function reference. Consulted 2026-09-15.
