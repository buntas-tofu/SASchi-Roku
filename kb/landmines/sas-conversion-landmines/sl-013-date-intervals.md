# SL-013: Calendar boundaries are not elapsed-duration division

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-011.
Coverage assessment: Existing INTCK/INTNX family; options and parsing remain explicit. An entry's existence is not an equivalence proof.

## Failure mechanism

INTCK defaults to counting discrete interval boundaries; continuous counting is anchored to the start date. Date and datetime intervals must match the value's units.

## Witness to build (not executed here)

Compare January 31 to February 1 using month intervals: the discrete count is one while the continuous count is zero. Add leap-day and month-end cases before selecting a target offset operation.

## Preservation contract and mitigation (recommendation)

Record epoch, units, interval, method, alignment, and date-parsing policy. Keep INTNX alignment tests separate; an INTCK result does not validate INTNX SAME.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S13: [INTCK function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p1md4mx2crzfaqn14va8kt7qvfhr.htm). Scope: SAS 9.3 function reference. Consulted 2026-09-15.
