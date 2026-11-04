# First Julia test: reuse the frozen synthetic fixture

Status: proposed test, not Julia execution. No duplicate data is committed.

Use [customers.csv](../python-libraries/fixtures/customers.csv), [orders.csv](../python-libraries/fixtures/orders.csv) and [expected.json](../python-libraries/fixtures/expected.json). The frozen independent oracle describes five customers, eight orders, two missing amounts, one zero, a negative adjustment, an unmatched key and leading-zero identifiers.

Required outcome: preserve string keys and all eight orders; left join without dropping the orphan; group with deterministic order; compare row counts and nonmissing counts; expect total 4350 integer cents. The C segment has one row but an all-missing sum and requires `missing` rather than a default zero if following the source oracle.

Negative controls: converting `0007` to 7, dropping the orphan, reversing -400, treating zero as missing or replacing an all-missing sum with zero. Record Julia and package versions, command, first candidate output, independent comparisons and rejected controls before calling any result verified.

This verifies a small cross-engine tabular behavior, not complete DATA-step semantics. A later Julia trial should use Roku's existing frozen state and match-merge witnesses.
