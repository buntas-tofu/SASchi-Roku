# LQ-007: A model can mistake explicit business logic for a language defect

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Local-review-derived concern; SAS LAG documentation supports the mechanism, not an LLM prevalence claim.
Runtime status: no model experiment or SAS execution performed for this card.
Family: interpretation.

## Evidence and limits

Project-derived risk: a source program deliberately resets or clips a value, and an extraction calls that behavior a SAS divergence. Language rules and application choices need separate evidence.

## SAS migration scenario (illustrative)

A program invokes LAG and then explicitly resets a first-group result. A draft removes the reset while claiming to fix LAG.

## Recommended control (inference)

Trace the source statements and their order. Preserve the application's behavior unless a separate change is authorized; describe a proposed correction as a change, not as equivalence.

## Proposed evaluation, not a measured result

Pair programs that differ only by an explicit reset. Require the translation and explanation to preserve that difference.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- S02: [LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm). Scope: SAS 9.3 function reference. Consulted 2026-09-15.
