# SL-024: Matching a mixed-model formula does not match its covariance or inference

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-010.
Coverage assessment: Existing human-review/statistical routing; compare full model specification. An entry's existence is not an equivalence proof.

## Failure mechanism

CAMIS comparisons distinguish mean-model coding, supported covariance structures, estimation methods, and degrees-of-freedom calculations. Similar fixed effects can coexist with different standard errors, contrasts, or boundary diagnostics.

## Witness to build (not executed here)

Use unbalanced repeated measurements, specify an unstructured residual covariance, and compare the fitted covariance and named treatment contrast with an independently specified target model.

## Preservation contract and mitigation (recommendation)

Pin covariance structure, ML/REML or likelihood approximation, degrees-of-freedom method, contrasts, optimizer, and convergence checks. Compare estimands and covariance parameters before relaxing numeric tolerances.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- C01: [CAMIS: R versus SAS MMRM](https://psiaims.github.io/CAMIS/Comp/r-sas_mmrm.html). Scope: Community-authored comparison; current mutable page, its examples are not our receipts. Consulted 2026-09-15.
- C02: [CAMIS: R versus SAS random effect models](https://psiaims.github.io/CAMIS/Comp/r-sas_random_effects_models.html). Scope: Community-authored comparison; current mutable page. Consulted 2026-09-15.
