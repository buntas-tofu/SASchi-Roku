# SL-025: Cox regression defaults can differ on tied events

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-011.
Coverage assessment: Existing survival family; tied-event and risk-set fixtures needed. An entry's existence is not an equivalence proof.

## Failure mechanism

The cited PROC PHREG documentation defaults to Breslow ties; ordinary R coxph defaults to Efron, with documented exceptions for multistate models. Matching the formula does not align the likelihood.

## Witness to build (not executed here)

Use tied event times plus censoring and compare explicitly selected Breslow and Efron fits. Add delayed entry as a separate risk-set test rather than assuming right-censoring coverage includes it.

## Preservation contract and mitigation (recommendation)

Pin tie method, event/censor coding, time scale, entry/exit intervals, strata, and baseline-survival method. Assess risk sets and log likelihood before comparing coefficients.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S26: [PROC PHREG MODEL statement](https://support.sas.com/documentation/cdl/en/statug/66859/HTML/default/statug_phreg_syntax17.htm). Scope: SAS/STAT 13.1; tie-handling options. Consulted 2026-09-15.
- T06: [R survival coxph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html). Scope: R development manual; pin actual installed survival version. Consulted 2026-09-15.
