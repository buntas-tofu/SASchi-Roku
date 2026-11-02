# LQ-005: Self-critique and model agreement are not independent semantic oracles

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Mixed published evidence; independent-oracle requirement is an engineering recommendation.
Runtime status: no model experiment or SAS execution performed for this card.
Family: validation.

## Evidence and limits

One study found limitations in intrinsic correction without external feedback; another reports intrinsic correction ability under different conditions. Neither licenses a blanket claim that self-review always works or never works.

## SAS migration scenario (illustrative)

Two drafts repeat the same attractive but incorrect rule, then a third explanation declares agreement to be proof.

## Recommended control (inference)

Use critique to find candidates. Resolve the disputed behavior with a pinned source, counterexample, or execution result whose origin is independent of the draft.

## Proposed evaluation, not a measured result

Present a plausible wrong contract and a documented counterexample. Measure whether the model changes the executable behavior, not just the wording of its confidence.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P05: [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798). Scope: Research abstract; intrinsic correction without external feedback. Consulted 2026-09-15.
- P06: [Large Language Models have Intrinsic Self-Correction Ability](https://arxiv.org/abs/2406.15673). Scope: Research abstract; counterpoint on task and prompting dependence. Consulted 2026-09-15.
