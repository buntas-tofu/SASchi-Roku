# First Julia evaluation: reuse the frozen synthetic fixture

Status: evaluation designed; its actual execution evidence belongs to the [bounded Julia trial](../../trials/julia-fixture/README.md).

The shared [customers.csv](../python-libraries/fixtures/customers.csv), [orders.csv](../python-libraries/fixtures/orders.csv) and [expected.json](../python-libraries/fixtures/expected.json) are unchanged. The reference covers five customers, eight orders, two missing amounts, one zero, a negative adjustment, an orphan order and leading-zero identifiers.

The first trial implements the same bounded contract in Base Julia and separately in DataFrames/CSV, followed by an independent comparator with eight mutation controls and two malformed-input refusals per implementation. Each actual pass requires a hosted Julia log and an environment receipt. A static check or Python execution is not a Julia result.

This is not yet an evaluation of SAS retained state, conditional LAG, BY match merges, native SAS missing tags or statistical inference. Subsequent trials can reuse Roku's frozen source cases without modifying their independent expected values.
