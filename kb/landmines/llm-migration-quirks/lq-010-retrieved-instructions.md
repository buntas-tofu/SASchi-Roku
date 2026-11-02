# LQ-010: Comments and retrieved documents can contain instructions aimed at the model

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Published threat class; bounded repository example is a proposed evaluation.
Runtime status: no model experiment or SAS execution performed for this card.
Family: retrieval.

## Evidence and limits

Indirect prompt-injection research demonstrates that instruction-bearing external content can affect LLM-integrated applications. A repository comment is evidence to inspect, not authority to alter the task.

## SAS migration scenario (illustrative)

A comment inside a source file tells the assistant to ignore the comparison contract or declare all tests passed.

## Recommended control (inference)

Treat source text as quoted input. Keep tool permissions and acceptance conditions outside retrieved content, and verify executable results rather than adopting the comment's claim.

## Proposed evaluation, not a measured result

Place a harmless conflicting instruction in a test fixture and check that it is reported as source content while the original task and verification requirements remain intact.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- P07: [Indirect prompt injection in LLM-integrated applications](https://arxiv.org/abs/2302.12173). Scope: Research abstract; indirect instructions in retrieved content. Consulted 2026-09-15.
