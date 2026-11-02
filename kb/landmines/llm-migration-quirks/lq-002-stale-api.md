# LQ-002: A once-valid API can be wrong for the installed version

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Publication-backed risk; no local model/version failure rate measured.
Runtime status: no model experiment or SAS execution performed for this card.
Family: dependency.

## Evidence and limits

The library-evolution study examined deprecated APIs in code completion. Version drift is distinct from inventing an API, and a remembered snippet may be historically correct.

## SAS migration scenario (illustrative)

A generated dataframe operation uses an old argument or method even though the environment lock specifies a newer major release.

## Recommended control (inference)

Supply the lockfile and installed signatures with the task. Run the exact emitted operation, including keyword arguments, on the pinned environment before promotion.

## Proposed evaluation, not a measured result

Repeat a bounded task against two explicitly different dependency versions and check whether the proposed operation follows each documented contract.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P02: [LLMs Meet Library Evolution](https://arxiv.org/abs/2406.09834v3). Scope: ICSE 2025 paper, arXiv v3; abstract consulted. Consulted 2026-09-15.
