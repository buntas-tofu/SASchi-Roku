# SL-016: The same percentile name can select a different estimator

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-002.
Coverage assessment: Existing mapping; weighted and approximate paths need separate scope. An entry's existence is not an equivalence proof.

## Failure mechanism

SAS exposes percentile-definition choices, while R quantile offers nine algorithms and defaults to type 7. Names such as median or quartile do not fix interpolation and boundary conventions.

## Witness to build (not executed here)

For sorted values 0,10,20,30 at p=0.25, R type 7 gives 7.5 while type 2 gives 5. This is a target-algorithm illustration, not a universal mapping for every SAS procedure.

## Preservation contract and mitigation (recommendation)

Select the actual SAS procedure, definition, exact/approximate method, and weight contract first. Verify any R or Python mapping on ties, small samples, endpoints, and missing values.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- T05: [R sample quantiles](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html). Scope: R development manual; pin actual installed R before implementation. Consulted 2026-09-15.
- S16: [Statistical computations in PROC MEANS](https://support.sas.com/documentation/cdl/en/proc/61895/HTML/default/a000608466.htm). Scope: Base SAS procedures, cited 9.x edition. Consulted 2026-09-15.
