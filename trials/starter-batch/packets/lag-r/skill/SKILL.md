---
name: sas-translate
description: Translate a scoped SAS program to Python or R with explicit behavior contracts and execution comparisons. Use for program migration or conversion repair; dataset export without program translation is a separate task.
metadata:
  status: initial-guidance
---

# Translate with evidence

Status: initial workflow guidance for engineering use. A conversion is a candidate
until its stated behavior is tested; no general or live-SAS equivalence is implied.

Establish source, inputs, includes, macro context, intended outputs and the chosen
target. Work from the user's existing assessment when available. Keep unresolved
dependencies visible. Preserve requested behavior; algorithm redesign is a separate
decision when it changes output, ordering, precision or side effects.

For each bounded slice, state what will be compared before writing the target:
typed values, schema and descriptors, row multiplicity/order, missingness, text,
metadata, statistical settings and external artifacts as applicable. Choose exact
comparisons for discrete behavior and justified numeric tolerances for approximate
behavior. Do not loosen a comparison after a failure merely to accept the result.

Consult [the evidence map](references/evidence.md) for the mechanisms present.
Library convenience operations need witnesses where SAS behavior matters:
many-to-many match MERGE, missing keys, DATA-step state, conditional LAG calls,
explicit OUTPUT, character padding, date intervals and statistical defaults.

If using SASchi-Go, inspect the actual installed version and its supported profile.
Translate and run only admitted source. Unsupported tickets and partial inspection
are not successful conversion. If targeting R manually, use R's own execution and
evidence; an R fixture twin is not evidence that a general R emitter exists.

Execute the target when the task includes implementation and an appropriate
environment is available. Compare with an independent expected result: captured
SAS output when available, separately derived hand truth for a bounded case, or
an independently implemented witness. Label which one was used. Running the same
helper twice is not independent evidence. Include a deliberately wrong variant
when it meaningfully tests whether the comparator can detect the migration trap.

If SAS is unavailable, report target-runtime evidence and the unproved SAS
boundary. If the target cannot run, deliver candidate code with the exact missing
runtime or input; do not write a passing receipt. Retain failed comparisons for
diagnosis without publishing them as accepted output.

Deliver code, reproducible invocation, source/input identity, environment, comparison
policy, observed verdict and remaining unsupported behavior. Keep confidence,
syntax validity and execution acceptance separate.
