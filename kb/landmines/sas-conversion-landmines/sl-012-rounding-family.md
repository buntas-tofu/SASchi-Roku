# SL-012: ROUND, ROUNDE, and ROUNDZ differ beyond a decimal-place label

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: DS-012, DS-020.
Coverage assessment: Half-away reference exists; fuzzing neighborhood remains a separate contract. An entry's existence is not an equivalence proof.

## Failure mechanism

ROUND treats approximate half ties differently from ROUNDE and ROUNDZ. ROUND and ROUNDE also perform fuzzing, while ROUNDZ does not. A generic round helper may preserve neither ties nor nearby floating-point behavior.

## Witness to build (not executed here)

Test positive and negative half-unit boundaries, nearby representable numbers, and a non-decimal rounding unit. Include exact ties and near ties separately.

## Preservation contract and mitigation (recommendation)

Name the SAS function, unit, numeric domain, and comparison tolerance. Do not infer full equivalence from a few decimal examples or substitute string formatting for arithmetic.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S12: [ROUNDZ and rounding-family distinctions](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p1u0w0omad7fyxn1unu83odr6vy2.htm). Scope: SAS 9.3 function reference. Consulted 2026-09-15.
