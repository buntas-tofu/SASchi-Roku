# LQ-008: Generated tests can repeat the same misconception as generated code

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Proposed engineering control, not a newly run experiment.
Runtime status: no model experiment or SAS execution performed for this card.
Family: validation.

## Evidence and limits

Engineering inference from test-insufficiency research: more tests do not help if their expected values merely repeat the draft's assumption. A target language agreeing with another target is not automatically agreement with SAS.

## SAS migration scenario (illustrative)

A generated implementation and generated test both use a Cartesian join as the expected answer for a match-merge.

## Recommended control (inference)

Record each expected value's derivation independently. Use documented small witnesses, separately captured outputs, and mutation tests that must fail on the tempting wrong implementation.

## Proposed evaluation, not a measured result

Replace the implementation with a known wrong alternative. If the suite stays green, identify the untested contract rather than asking the model for more reassurance.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P03: [EvalPlus: rigorous evaluation of generated code](https://arxiv.org/abs/2305.01210v3). Scope: NeurIPS 2023 paper, arXiv v3; abstract consulted. Consulted 2026-09-15.
- S01: [MERGE statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000202970.htm). Scope: SAS 9.2 statement reference. Consulted 2026-09-15.
