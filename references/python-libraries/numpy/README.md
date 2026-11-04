# NumPy dependency guide

Status: candidate library reference, not SAS equivalence or enterprise-runtime verification.

**Scope:** Vectorized arrays, dtypes, masked reductions and numeric comparisons. Not a relational table engine or SAS DATA-step engine.

**Recommended role:** typed arrays and numerical computation.

## Review hazards

- Preserve leading-zero IDs as text, not floating point.
- Integer cents need an explicit null mask and overflow check.
- NaN, NULL and SAS tagged missing values are not interchangeable.
- Random seeds need pinned generator/NumPy versions for literal comparisons.

## Curated API surface

| Symbol | Use |
|---|---|
| `np.asarray` | array conversion |
| `np.array` | typed arrays |
| `np.sum` | reduction |
| `np.isfinite` | finite mask |
| `np.testing.assert_allclose` | tolerant comparison |
| `np.random.default_rng` | RNG construction |

The structured [api.json](api.json) additionally names the required checks. This is not an exhaustive API mirror.

## Example syntax

```python
import numpy as np
cents = np.array([1250, 2300, -400, 0, 500, 700], dtype=np.int64)
assert int(cents.sum()) == 4350
```

The snippet is illustrative, not a recorded accepted execution. Check installed library versions, an independent expected result, and the actual runtime before relying on outputs.

## Upstream sources

- [NP-001](https://numpy.org/doc/stable/)
- [NP-002](https://numpy.org/doc/stable/reference/)
- [NP-003](https://numpy.org/doc/stable/reference/random/generator.html)

For SAS-specific semantics use the existing `kb/convert/` documentation and trials. See the [shared test oracle](../docs/verification.md).
