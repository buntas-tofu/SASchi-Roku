# Frozen independent oracle and validation contract

Status: hand-authored synthetic testbed, not enterprise or live-SAS validation.

Inputs: `fixtures/customers.csv` and `fixtures/orders.csv`. Exact expected values: `fixtures/expected.json`. This is deliberate static data, not Faker output.

Required checks: preserve customer IDs as strings including leading zeros; read five customers and eight orders; two amounts are null, one is zero, one is -400; left join without dropping the unmatched customer `9999`. Sum signed integer cents, not formatted strings. The net is 4350 cents.

Group by display segment. A has three rows, two non-null amounts and sum 850; B has three, three and 3000; C has one, zero and **null** sum; the unmatched group has one, one and 500. Compare in stable segment order.

Negative controls should catch key coercion to integers, dropped orphan, wrong sign, null/zero conflation and an all-null sum emitted as zero. Do not replace the expected JSON with target-engine output.

Record each engine version, command, positive assertions, rejected controls, failures, skips and input/output hashes. Agreeing Python engines do not certify SAS semantics.
