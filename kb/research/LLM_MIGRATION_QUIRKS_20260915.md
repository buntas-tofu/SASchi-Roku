# LLM quirks in SAS migration: evidence and controls

Status: candidate engineering synthesis for the operator, 2026-09-15.
Not an agency finding or a benchmark of current local models.

## Conclusion

Use an LLM to propose a translation or a semantic hypothesis, then verify its
observable claims. Fluency, agreement, valid JSON, and a successful parse are
different properties from preserved behavior. The new twelve-card collection
makes those distinctions searchable.

## Published findings and their limits

- Package hallucinations were observed in a defined Python/JavaScript generation
  study. That supports checking package identity, not importing its aggregate
  percentages into our SAS scorecard. Source: [Package hallucinations in code-generating LLMs](https://arxiv.org/abs/2406.10279).
- Deprecated API use has been studied separately from fabricated API use. Pinning
  dependencies and checking installed signatures addresses a different failure
  from validating the intended mathematics. Source: [LLMs Meet Library Evolution](https://arxiv.org/abs/2406.09834v3).
- Larger functional test sets exposed code errors missed by weaker suites.
  Benchmark rankings depend on the instrument as well as the model.
  Source: [EvalPlus: rigorous evaluation of generated code](https://arxiv.org/abs/2305.01210v3).
- Long-context retrieval in the cited study depended on the position of relevant
  material. Our models and prompts need their own measurement.
  Source: [Lost in the Middle](https://arxiv.org/abs/2307.03172).
- Intrinsic self-correction results are conditional on task, model, and prompting.
  The cited papers disagree with a simplistic universal conclusion. External
  evidence remains useful regardless of which self-critique approach is chosen.
  Sources: [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798), [Large Language Models have Intrinsic Self-Correction Ability](https://arxiv.org/abs/2406.15673).
- Retrieved content can carry instructions directed at an assistant. Source
  comments must not acquire authority over verification or tool use.
  Source: [Indirect prompt injection in LLM-integrated applications](https://arxiv.org/abs/2302.12173).
- Project translation needs validation across interacting components; translating
  isolated snippets is a narrower capability. Source: [Scalable, Validated Code Translation of Entire Projects](https://mengwangoxf.github.io/Papers/PLDI25.pdf).
- Contamination-aware evaluation is a separate discipline from teaching a model
  with examples. Keep local retrieval answer keys out of the KB.
  Source: [LiveCodeBench](https://arxiv.org/abs/2403.07974).

These papers motivate controls. Most are older studies and several were consulted
at abstract level. This is not a current model leaderboard or evidence that every
listed issue occurs at the same rate in every model.

## What the local review adds

The campaign's targeted adjudication identified irrelevant keyword matches,
application-specific behavior misdescribed as SAS semantics, and false feature
claims. Its reviewed sample was selected, not random; it cannot estimate corpus-wide
accuracy. The private lineage note records exact files and revisions.

A historical emitter defect let unsupported control flow become comments while its
body still executed. The inspected current changelog records the blocking fix and
other rule corrections. We preserve the lesson as an acceptance case without
asserting that the current implementation still fails.

Local extraction receipts measure that something was generated and parsed. Their
source locators and claims still need relevance and factual review. A missing or
contradicted finding is a valid research disposition; forcing every document to
yield a landmine rewards invention.

## Practical workflow

1. Give the drafter the exact construct, source/version, dependency lock, and output contract.
2. Require an evidence record separate from generated code: source locator, proposed behavior,
   assumptions, unsupported surface, and confidence basis.
3. Validate imports, signatures, parsing, and completeness without treating those checks as semantics.
4. Run independent small witnesses and compare row/state/schema/value behavior.
5. Block incomplete programs; a TODO is not an execution barrier.
6. Evaluate new cases outside the teaching corpus and retain every failure and denominator.

For a future local-model measurement, record model revision, prompt and context
hashes, generation settings, response completeness, tool environment, and scoring
rules. Repeat enough cases to characterize instability; do not assume temperature
zero or a repeated answer proves truth or independence. This is an experiment
proposal, not a measured claim about deterministic serving.

## Deliverables and exclusions

The twelve whole-card documents are listed in
[the corpus index](../landmines/llm-migration-quirks/README.md).
They remain asserted/unreviewed and contain illustrative scenarios, not benchmark
scores. Internal campaign records, model identities, raw drafts, and evaluation
answer keys are not ingested. No local model was invoked during this pass.
