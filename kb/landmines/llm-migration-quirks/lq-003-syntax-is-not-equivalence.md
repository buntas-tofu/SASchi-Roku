# LQ-003: Code that parses and runs can still implement the wrong program

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Research-backed evaluation limitation; the SAS witness is a proposed test.
Runtime status: no model experiment or SAS execution performed for this card.
Family: validation.

## Evidence and limits

EvalPlus showed that stronger test sets expose generated-code errors missed by smaller benchmarks. Project-level translation research also treats validation across interacting components as a distinct problem.

## SAS migration scenario (illustrative)

A draft replaces a many-to-many SAS match-merge with a database join. Both programs finish, but the join expands the row count.

## Recommended control (inference)

Separate syntax, execution, schema, row multiplicity, values, warnings, and side effects in the report. Each passing level proves only its own assertions.

## Proposed evaluation, not a measured result

Use an unequal-duplicate join case and compare key multiplicities and complete rows. A parse-only score must never be relabeled semantic equivalence.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P03: [EvalPlus: rigorous evaluation of generated code](https://arxiv.org/abs/2305.01210v3). Scope: NeurIPS 2023 paper, arXiv v3; abstract consulted. Consulted 2026-09-15.
- P08: [Scalable, Validated Code Translation of Entire Projects](https://mengwangoxf.github.io/Papers/PLDI25.pdf). Scope: PLDI 2025, selected full-text sections; project-level translation. Consulted 2026-09-15.
