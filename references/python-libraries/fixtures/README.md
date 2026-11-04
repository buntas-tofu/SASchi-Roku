# Hand-authored synthetic fixture

Status: independent static expected data, not live SAS, enterprise Python test output or Faker generation.

The five customers and eight orders exercise text IDs with leading zeros, a missing foreign-key match, two null monetary values, true zero, negative cents and a null-only group. [expected.json](expected.json) is frozen independently of any candidate engine. Compare against it using the [verification contract](../docs/verification.md). Never silently rewrite the oracle from implementation output.
