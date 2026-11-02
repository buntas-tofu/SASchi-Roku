---
name: sas-diagnose-state
description: Diagnose and repair SAS conversion mismatches involving conditional LAG queues, retained values, filtering, explicit OUTPUT or composed DATA steps. Use when row order and execution timing explain a wrong Python or R result.
metadata:
  status: initial-guidance
---

# Diagnose a stateful conversion mismatch

Status: initial diagnostic guidance for engineering use. A repair is accepted
only within the behavior and inputs actually compared.

Freeze the SAS slice, failing target, ordered inputs, observed outputs and chosen
comparison before repairing. Reproduce the mismatch and retain the failing code
and receipt. Use the smallest witness that distinguishes the suspected mechanisms;
do not simplify away the control flow that triggers the error.

Read [state boundaries](references/state.md). Trace each input iteration in source
order: state before execution, statements actually reached, queue operations,
retained updates and output events. Find the first divergence, then follow its
consequences. Input rows, LAG calls and output rows are different sequences.

Treat each LAG occurrence as its own queue. Conditional calls advance only when
executed. Separately determine whether the receiving variable is reset or retained.
Record initial values, sum-statement missing rules, filtering position and whether
an explicit OUTPUT replaces implicit output. A row that is not emitted may still
change queues and retained values. Across DATA steps, preserve the intermediate
rows and start the next step's execution context independently.

Choose a minimal repair that preserves the source's timing and observable contract.
Do not replace a conditional queue with an unconditional row shift, move filters,
reset state at an invented boundary, or redesign the algorithm without agreement.
If a macro or include controls the slice, resolve it or keep the diagnosis bounded.

Run the target and compare intermediate as well as final values, row count/order,
missing positions and types. Use captured SAS results where available, otherwise
label independent hand truth or a separately implemented witness. Exercise empty
and short inputs and repeated fresh invocations. Include a wrong variant that
would expose the diagnosed mechanism; do not weaken the comparison after failure.

Deliver the reproduced failure, first-divergence explanation, repair, unchanged
acceptance policy, execution receipt and residual uncertainty. A plausible trace
or Python/R agreement alone is not live-SAS evidence. Keep any later repairs and
broader claims separate from the preserved first attempt.
