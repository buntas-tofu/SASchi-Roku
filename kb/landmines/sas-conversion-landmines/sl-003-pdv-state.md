# SL-003: DATA step variables do not all reset in the same way

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P0, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-006; program execution model.
Coverage assessment: Existing primitives; whole-step composition needs validation. An entry's existence is not an equivalence proof.

## Failure mechanism

Variables read by SET/MERGE have retention behavior different from ordinary assignment-created variables. RETAIN adds another state lifetime. A row-wise rewrite can erase or accidentally extend that state.

## Witness to build (not executed here)

Use a one-row lookup read only when _N_=1, then process three observations from a second input. The lookup value should remain available on later iterations; a scratch assignment without retention needs a separate expectation.

## Preservation contract and mitigation (recommendation)

Model variable origin, initialization, step boundaries, and reset points. Validate conditional SET separately from a dataframe join or a global dictionary.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S05: [RETAIN statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000214163.htm). Scope: SAS 9.2 statement reference. Consulted 2026-09-15.
