# LQ-012: A well-formed record can contain a false claim or unusable citation

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Project-derived design concern; no new corpus-wide accuracy estimate.
Runtime status: no model experiment or SAS execution performed for this card.
Family: evidence.

## Evidence and limits

Project-derived workflow failure: schema validity, confidence labels, and a completed extraction count can be mistaken for factual review. Test coverage research provides a related warning about measuring the wrong acceptance condition.

## SAS migration scenario (illustrative)

A valid JSON record names a real file but its claimed line does not support the asserted SAS behavior.

## Recommended control (inference)

Validate locator existence, source revision, relevance, factual support, and executable scope separately. Preserve unknown and contradicted dispositions; do not force every source to produce a landmine.

## Proposed evaluation, not a measured result

Include a valid record with an incorrect citation and an accurate record in an alternative locator format. The gate should distinguish semantic support from formatting.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P03: [EvalPlus: rigorous evaluation of generated code](https://arxiv.org/abs/2305.01210v3). Scope: NeurIPS 2023 paper, arXiv v3; abstract consulted. Consulted 2026-09-15.
