# Faker dependency guide

Status: candidate library reference, not SAS equivalence or enterprise-runtime verification.

**Scope:** Localized, plausible synthetic records; not de-identification, relational correctness or business-rule proof.

**Recommended role:** synthetic test data.

## Review hazards

- Seed, locale, provider version and call order jointly affect generated values.
- Do not treat realistic generated contacts as safe real-world destinations.
- Use separate surrogate keys, explicit date bounds and deliberate negative cases.

## Curated API surface

| Symbol | Use |
|---|---|
| `Faker(locale)` | set locale |
| `seed_instance(seed)` | control one generator |
| `name()` | person-like text |
| `safe_email()` | test-only email |
| `date_between(start_date,end_date)` | bounded date |
| `unique` | uniqueness pool |
| `add_provider` | custom source |

The structured [api.json](api.json) additionally names the required checks. This is not an exhaustive API mirror.

## Example syntax

```python
from faker import Faker
fake = Faker('en_US')
fake.seed_instance(1729)
record = {'name': fake.name(), 'email': fake.safe_email()}
```

The snippet is illustrative, not a recorded accepted execution. Check installed library versions, an independent expected result, and the actual runtime before relying on outputs.

## Upstream sources

- [FK-001](https://faker.readthedocs.io/en/master/)
- [FK-002](https://github.com/joke2k/faker)
- [FK-003](https://pypi.org/project/Faker/)

For SAS-specific semantics use the existing `kb/convert/` documentation and trials. See the [shared test oracle](../docs/verification.md).
