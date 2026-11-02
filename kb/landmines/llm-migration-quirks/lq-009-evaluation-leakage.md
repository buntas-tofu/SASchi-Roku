# LQ-009: Retrieving an answer key can make a KB look more capable than it is

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Research-motivated local evaluation design; no contamination rate measured.
Runtime status: no model experiment or SAS execution performed for this card.
Family: evaluation.

## Evidence and limits

LiveCodeBench addresses contamination in coding evaluation. In a retrieval pipeline, indexing the local evaluation questions or verdicts creates a more direct leakage route.

## SAS migration scenario (illustrative)

A held-out prompt asks about the same probe whose expected answer is indexed verbatim.

## Recommended control (inference)

Keep evaluation inputs and answers outside ingestion. Split related variants by scenario family and record the corpus revision used for every evaluation.

## Proposed evaluation, not a measured result

Use new compositions and inputs absent from the teaching cards. Report answer retrieval separately from independent behavioral generalization.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P09: [LiveCodeBench](https://arxiv.org/abs/2403.07974). Scope: Research abstract; contamination-aware coding evaluation. Consulted 2026-09-15.
