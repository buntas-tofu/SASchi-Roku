# SL-017: Event and CLASS coding can reverse an odds ratio

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-008; ST-007 adjacent.
Coverage assessment: Rulebook covers settings; model-specific validation still required. An entry's existence is not an equivalence proof.

## Failure mechanism

PROC LOGISTIC's modeled event and CLASS reference/parameterization affect coefficient interpretation and odds-ratio direction. Similar formulas can encode different response and contrast definitions.

## Witness to build (not executed here)

Fit the same two-level predictor with event 1 versus event 0 and with both reference levels. Inspect the response profile and design matrix before comparing coefficients.

## Preservation contract and mitigation (recommendation)

Pin event, reference levels, parameterization, analysis rows, weights, and convergence conditions. Compare predictions and named contrasts as well as coefficient arrays.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S17: [PROC LOGISTIC odds-ratio reversal](https://support.sas.com/kb/39/085.html). Scope: SAS Usage Note 39085, 2010. Consulted 2026-09-15.
