# DuckDB dependency guide

Status: candidate library reference, not SAS equivalence or enterprise-runtime verification.

**Scope:** In-process SQL and typed relations. Reading analytical tables does not preserve all SAS source metadata or procedural semantics.

**Recommended role:** embedded analytical SQL and Parquet access.

## Review hazards

- CSV inference may remove leading zeros; force text keys.
- COUNT(*) counts rows; COUNT(amount) excludes null; SUM(all-null) is NULL.
- Order is undefined without ORDER BY; join duplication requires checks.
- Use explicit connection and parameterized values; untrusted SQL and external extensions require review.

## Curated API surface

| Symbol | Use |
|---|---|
| `duckdb.connect` | explicit connection |
| `DuckDBPyConnection.sql` | relations |
| `DuckDBPyConnection.execute` | SQL execution |
| `read_csv` | CSV scan |
| `read_parquet` | Parquet scan |
| `COUNT(*)` | row count |
| `COUNT(expr)` | non-null count |
| `SUM(expr)` | aggregate |
| `COPY TO` | export |

The structured [api.json](api.json) additionally names the required checks. This is not an exhaustive API mirror.

## Example syntax

```sql
SELECT segment, COUNT(*) AS rows, COUNT(amount_cents) AS observed,
       SUM(amount_cents) AS amount_cents_sum
FROM typed_orders
GROUP BY segment ORDER BY segment;
```

The snippet is illustrative, not a recorded accepted execution. Check installed library versions, an independent expected result, and the actual runtime before relying on outputs.

## Upstream sources

- [DB-001](https://duckdb.org/docs/stable/clients/python/overview)
- [DB-002](https://duckdb.org/docs/stable/sql/functions/aggregates)
- [DB-003](https://duckdb.org/docs/stable/data/csv/overview)

For SAS-specific semantics use the existing `kb/convert/` documentation and trials. See the [shared test oracle](../docs/verification.md).
