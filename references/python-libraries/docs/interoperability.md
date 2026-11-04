# Cross-library interoperability contract

Status: proposed engineering guidance, not proof of lossless interchange or SAS equivalence.

| Boundary | Candidate representation | Must verify |
|---|---|---|
| Faker to arrays/tables | generated rows with explicit keys | locale, version, uniqueness, schema, relationship rules |
| NumPy to tabular engines | typed arrays and validity mask | dtype, null/NaN, precision, overflow |
| Polars to DuckDB | Arrow or Parquet / supported relation | string IDs, date types, nulls, join cardinality and order |
| DuckDB to Polars | typed relation or Parquet | schema, SQL NULL, decimal and temporal precision |
| Analytical table to archive | typed data plus source-byte and metadata companion | SAS labels, formats, encodings and special missing tags |

A Parquet file opening successfully is not proof that original SAS metadata or tagged missing cells survived. Review source and destination hashes when needed; preserve a companion representation for values metadata cannot carry.

SAS-mapping authority remains with [Polars conversion guide](../../../kb/convert/sas_to_polars.md), [DuckDB conversion guide](../../../kb/convert/sas_to_duckdb.md) and the established trials.
