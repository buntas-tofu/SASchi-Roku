# Polars dependency guide

Status: candidate library reference, not SAS equivalence or enterprise-runtime verification.

**Scope:** Expression-oriented dataframes, scans, joins and aggregations. SAS row-by-row state must be modeled separately.

**Recommended role:** typed eager and lazy dataframe transformations.

## Review hazards

- Infer and validate schema before joining; customer IDs remain strings.
- Grouping and joins do not imply stable SAS observation order.
- Distinguish nulls, NaNs and missing tags; guard all-null group sums.
- Relational joins with duplicate keys may differ from SAS match merges.
- Do not presume every lazy plan is streamable.

## Curated API surface

| Symbol | Use |
|---|---|
| `pl.scan_csv` | lazy CSV |
| `pl.scan_parquet` | lazy Parquet |
| `pl.col` | column expression |
| `LazyFrame.join` | join |
| `LazyFrame.group_by` | aggregate |
| `LazyFrame.collect_schema` | schema inspection |
| `LazyFrame.collect` | run plan |
| `LazyFrame.sink_parquet` | write plan |

The structured [api.json](api.json) additionally names the required checks. This is not an exhaustive API mirror.

## Example syntax

```python
import polars as pl
lf = pl.scan_csv('fixtures/orders.csv', schema_overrides={'customer_id': pl.String})
print(lf.collect_schema())
```

The snippet is illustrative, not a recorded accepted execution. Check installed library versions, an independent expected result, and the actual runtime before relying on outputs.

## Upstream sources

- [PL-001](https://docs.pola.rs/user-guide/)
- [PL-002](https://docs.pola.rs/api/python/stable/reference/)
- [PL-003](https://docs.pola.rs/user-guide/lazy/schemas/)

For SAS-specific semantics use the existing `kb/convert/` documentation and trials. See the [shared test oracle](../docs/verification.md).
