# LQ-011: A review ticket in a comment does not block unsafe partial execution

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Historical project lesson, not a claim that the current emitter still has this defect.
Runtime status: no model experiment or SAS execution performed for this card.
Family: artifact.

## Evidence and limits

Project-derived workflow failure: unsupported control flow can be discarded while its body survives as executable output. This is an integration defect whether an LLM or deterministic emitter produced the fragment.

## SAS migration scenario (illustrative)

A false IF condition becomes a TODO comment but its assignment executes unconditionally in the target program.

## Recommended control (inference)

Make a blocked translation non-executable by default. Align artifact status, diagnostic report, and process exit code; preserve dependencies between unsupported control flow and its body.

## Proposed evaluation, not a measured result

Supply unsupported enclosing control flow and assert that no normal runnable artifact is emitted. Keep historical defects distinct from current implementation status.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P08: [Scalable, Validated Code Translation of Entire Projects](https://mengwangoxf.github.io/Papers/PLDI25.pdf). Scope: PLDI 2025, selected full-text sections; project-level translation. Consulted 2026-09-15.
