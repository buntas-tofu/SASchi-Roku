# SL-015: A WEIGHT column does not identify a universal weighted estimator

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-001 and procedure-specific statistical rules.
Coverage assessment: Known corrected weight behavior; broaden procedure contrasts. An entry's existence is not an equivalence proof.

## Failure mechanism

PROC MEANS has defined handling for zero, negative, and missing weights, with EXCLNPWGT changing inclusion. VARDEF controls the divisor. Other procedures can apply different rules to the same weight column.

## Witness to build (not executed here)

Use nonmissing responses paired with positive, zero, negative, and missing weights. Compare N, total weight, mean, and variance under explicit VARDEF and EXCLNPWGT choices.

## Preservation contract and mitigation (recommendation)

Write the estimator formula and inclusion mask before choosing a library function. Match response-missing handling separately; agreement on the mean does not establish variance or degrees-of-freedom parity.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S15: [PROC MEANS WEIGHT statement](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000146736.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
- S16: [Statistical computations in PROC MEANS](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000608466.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
