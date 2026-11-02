# SAS → DuckDB Migration Guide

Lowest entry for build outs and env control: [uv](https://docs.astral.sh/uv/)

### For single-node and government data work in Python

**[DuckDB](https://duckdb.org/docs/lts/clients/python/overview)** is the closest fit for `PROC SQL`, relational data access, SQL-based transformations, and analytical work across CSV, Parquet, JSON, and database sources. It excels at SQL-style queries over structured data and provides excellent integration with the Python ecosystem.

A reliable migration strategy is **semantic rather than one-to-one**: preserve the behavior of the SAS program first, then choose the DuckDB implementation that best *reflects* that behavior.

---

## 1. Data Loading / Importing

| SAS | DuckDB |
|---|---|
| `PROC IMPORT` (CSV) | `read_csv()` / `SELECT * FROM 'file.csv'` |
| `PROC IMPORT` (Parquet) | `read_parquet()` / `SELECT * FROM 'file.parquet'` |
| `PROC IMPORT` (Excel) | Excel extension / `read_xlsx()` for supported `.xlsx` files |
| `INFILE` / `INPUT` (fixed-width) | Positional parsing with explicit offsets/widths; use preprocessing, string slicing, or a dedicated fixed-width parser |
| `LIBNAME` | `ATTACH`, registered views/tables, or direct file/database access |
| `PROC SQL CONNECT TO` | DuckDB database connectors/extensions, e.g. PostgreSQL/MySQL scanners; use the appropriate client/connection layer for other systems |
| `FILENAME` | Direct filesystem paths and supported URLs/cloud locations |
| `PROC CIMPORT` / `CPORT` | Usually replace with Parquet/CSV or another interoperable format |
| `PROC XCOPY` | `COPY` or filesystem-level copy |

**Migration note:** Fixed-width `INFILE`/`INPUT` processing is positional parsing, not ordinary CSV parsing. Preserve field offsets, widths, informats, and conversion rules explicitly.

**Migration note:** SAS libraries often combine data access, metadata, formats, and naming conventions. A `LIBNAME` migration may therefore require more than simply changing the file path.

**Migration note:** For Parquet files, DuckDB can query them directly without loading into memory: `SELECT * FROM 'file.parquet'` or `SELECT * FROM 'data/*.parquet'` for multiple files. Use `read_parquet()` to materialize as a table. DuckDB's native Parquet integration includes predicate pushdown and column pruning for efficient queries.

---

## 2. Writing / Exporting Data

| SAS | DuckDB |
|---|---|
| `PROC EXPORT` (CSV) | `COPY (SELECT ...) TO 'out.csv' (HEADER)` |
| `PROC EXPORT` (Parquet) | `COPY (SELECT ...) TO 'out.parquet' (COMPRESSION 'ZSTD')` |
| `FILE` / `PUT` (custom flat file) | Build a formatted expression, then `COPY` |
| `PROC SQL CREATE TABLE` | `CREATE TABLE ... AS SELECT ...` |
| `PROC DATASETS` | `DROP TABLE`, `ALTER TABLE`, metadata commands |
| `PROC APPEND` | `INSERT INTO ... SELECT ...` or append through the chosen storage format |
| `ODS PDF/RTF/EXCEL/HTML` | No direct all-purpose equivalent; use Python reporting/export libraries or a BI/reporting layer |

**Migration note:** ODS is a reporting system, not simply a data-export feature. Replacing ODS often requires a separate reporting layer.

**Migration note:** For Parquet files, use `COPY (SELECT ...) TO 'file.parquet'` with optional compression codecs (e.g., `COMPRESSION 'SNAPPY'` or `'ZSTD'`). Parquet is the recommended format for large analytical datasets due to columnar storage, efficient compression, and wide ecosystem support. DuckDB writes Parquet with full type fidelity including nested structures.

---

## 3. Data Manipulation -- DATA Step Core

| SAS | DuckDB (SQL) |
|---|---|
| `DATA` step | `SELECT` / CTEs with computed columns |
| `SET` | `FROM table` or file scan |
| `SET a b c` (concatenate/union) | `UNION ALL` |
| `MERGE ... BY` | `JOIN ... ON ...` **only when the intended behavior is a relational join; SAS BY-group merge semantics may differ substantially with duplicate keys** |
| `RETAIN` | Window functions for cumulative/state-by-group patterns; recursive SQL for some stateful logic |
| `ARRAY` | Generate column expressions in Python, or use list/array functions where appropriate |
| `DO` / `DO WHILE` / `DO UNTIL` | Recursive CTEs for some iterative logic; otherwise Python control flow |
| `IF-THEN-ELSE` / `SELECT-WHEN` | `CASE WHEN ... THEN ... ELSE ... END` |
| `OUTPUT` (route rows) | Separate filtered queries or conditional flags followed by filtering |
| `LAG` / `DIF` | Window `LAG()` / arithmetic on lagged values **when previous-row semantics are intended** |
| `FIRST.var` / `LAST.var` | `ROW_NUMBER()` or boundary logic over a defined `PARTITION BY` / `ORDER BY` (confirm FIRST/LAST same) |
| `LENGTH` | `length()` or type/schema inspection; note SAS variable length is a schema attribute |
| `FORMAT` | Formatting at presentation/export time; date/numeric formatting functions |
| `INFORMAT` | Input parsing such as `strptime()` or explicit casts |
| `RENAME=` / `DROP=` / `KEEP=` | `SELECT col AS new_name` and projected columns |

### Important SAS DATA-step caveat

SAS DATA steps are **stateful and sequential**. Do not assume that every DATA-step statement has a direct SQL equivalent.

The most important cases requiring deliberate migration are:

- `RETAIN`
- `LAG` / `DIF`
- `FIRST.` / `LAST.`
- `BY`-group processing
- multiple `OUTPUT` statements
- arrays
- implicit iteration
- sum statements
- SAS automatic variables
- SAS missing-value semantics

For these, migrate the **behavior**, not merely the syntax. Testing and validating against the ground truth is essential.

---

## 4. Filtering / Subsetting

| SAS | DuckDB |
|---|---|
| `WHERE` | `WHERE` clause |
| `IF` (post-compute filter) | CTE/subquery + outer `WHERE` |
| `WHERE=` dataset option | Predicate can be pushed down where the query/source permits |
| `PROC SQL WHERE/HAVING` | Native SQL |
| `%IF %THEN` (macro-time) | Python control flow around query construction |

**Important:** `WHERE` in SAS and `IF` in a DATA step do not always have identical execution timing. Preserve the original calculation/filter order when translating.

---

## 5. Aggregating / Summarizing

| SAS | DuckDB |
|---|---|
| `PROC MEANS` / `SUMMARY` | `AVG()`, `SUM()`, `MEDIAN()`, etc. with `GROUP BY` |
| `PROC FREQ` | `GROUP BY` / `COUNT(*)` and related frequency logic |
| `PROC TABULATE` | `PIVOT` / conditional aggregation |
| `PROC SQL GROUP BY` | Native |
| `PROC REPORT` | Aggregate/query, then apply formatting through a reporting/export layer |
| `CLASS` statement | `GROUP BY` columns |
| `PROC RANK` | `NTILE(n) OVER (...)` or other ranking/window functions |

---

## 6. Sorting, Joining, Reshaping

| SAS | DuckDB |
|---|---|
| `PROC SORT` (+ `NODUPKEY`) | `ORDER BY`; for deduplication use `DISTINCT`, `DISTINCT ON`, window ranking, or another explicitly defined rule |
| `PROC TRANSPOSE` | `PIVOT` / `UNPIVOT` |
| `PROC SQL` joins | Native `JOIN` syntax |
| `HASH` object (lookup) | SAS `HASH` objects are procedural lookup structures; use a relational `JOIN` when the intended behavior is relational, otherwise reproduce the lookup/stateful behavior explicitly |
| `PROC COMPARE` | `EXCEPT` / `INTERSECT` plus explicit column/value comparisons |

**Important:** `PROC COMPARE` is more than a row-set difference. A production validation framework should compare schema, row counts, keys, null/missing behavior, numeric tolerances, and values column by column. Also, when possible, it is best to avoid distinct/sorting until *after* tables are reduced in size to avoid costly row-wise actions.

---

## 7. Macros (Automation and Reusability)

| SAS | DuckDB |
|---|---|
| `%MACRO` / `%MEND` | Python functions that construct/execute SQL, or DuckDB SQL for appropriate reusable expressions |
| `%LET` | Python variables; use parameters rather than unsafe string interpolation |
| `%IF %THEN %ELSE` | Python `if/else` around query construction |
| `%DO %END` | Python `for` loops around SQL generation/execution |
| `CALL SYMPUT` / `SYMPUTX` | Fetch a scalar into a Python variable |
| `PROC SQL INTO :` | Fetch query results into Python variables |
| `%INCLUDE` | Python `import` |
| Autocall macro libraries | Shared SQL macros and/or Python packages/modules |
| `SASAUTOS=` | Python package/module search path (`PYTHONPATH` and packaging) |

---

## 8. Date / Numeric Functions

| SAS | DuckDB |
|---|---|
| `INTCK` | `DATE_DIFF()` can cover some interval-counting use cases, but **SAS interval semantics must be tested** |
| `INTNX` | Date arithmetic / interval functions; **alignment behavior may require explicit implementation** |
| `YRDIF` | No universal one-function replacement; year-fraction conventions must be selected explicitly |
| `MDY`, `TODAY()`, `DATDIF` | Date constructors, `CURRENT_DATE`, `DATE_DIFF()` |
| Date informats/formats | Parsing with `STRPTIME()`; formatting with `STRFTIME()` |
| `ROUND` / `CEIL` / `FLOOR` | `ROUND()`, `CEIL()`, `FLOOR()` |
| `SUM` / `MEAN` / `STD` / `CV` | `SUM()`, `AVG()`, `STDDEV()`; calculate CV explicitly |
| FINANCE functions (`NPV`, `IRR`, depreciation, etc.) | Usually use an appropriate Python financial/numerical library |
| `PROC FCMP` | SQL macros for expression-like functions, or Python UDFs where appropriate |

### Date migration warning

`INTCK`, `INTNX`, `YRDIF`, business-day calculations, month-end rules, leap-year behavior, and interval alignment are common sources of subtle migration errors. Build representative test cases before declaring a SAS date calculation equivalent.

---

## 9. String / Text Handling

| SAS | DuckDB |
|---|---|
| `SUBSTR`, `SCAN`, `TRIM`, `STRIP` | `SUBSTR()`, split functions, `TRIM()` and related string functions |
| `CATX`, `CAT`, `CATS` | `CONCAT_WS()`, `CONCAT()` and explicit trimming |
| `COMPRESS` | `REGEXP_REPLACE()` or explicit replace logic |
| `PRXMATCH` / `PRXCHANGE` | Regex functions such as `REGEXP_MATCHES()` / `REGEXP_REPLACE()` |
| `INDEX` / `FIND` | `POSITION()` / `STRPOS()` |

**Migration note:** SAS character variables have fixed declared lengths and can be silently padded/truncated in ways that ordinary Python strings are not. Validate width and missing/blank behavior explicitly.

---

## 10. Statistical / Modeling

| SAS | DuckDB + Python |
|---|---|
| `PROC REG` | Prepare/query data in DuckDB, then use `statsmodels` or scikit-learn |
| `PROC LOGISTIC` | Prepare data in DuckDB, then use `statsmodels` or scikit-learn |
| `PROC GLM` / `MIXED` | Use appropriate `statsmodels` models after data preparation |
| `PROC ARIMA` / `FORECAST` / `ESM` | Prepare panel/series data in DuckDB, then use `statsmodels`, sktime, or another appropriate library |
| `PROC SURVEYSELECT` | Explicit sampling implementation; validate method, replacement, seed, stratification/cluster design, and selection probabilities |
| `PROC UNIVARIATE` | Profiling/summary functions plus explicit quantiles and distributions |
| `PROC HPFOREST` / `HPLOGISTIC` | scikit-learn, XGBoost, LightGBM, or another appropriate single-node ML library |

**Important:** Statistical procedure equivalence is about **model specification and inference**, not just API replacement. Match distributions, missing-value handling, reference coding, confidence intervals, weighting, convergence settings, and output definitions.

For sampling procedures such as `PROC SURVEYSELECT`, also match the sampling design, replacement rules, random seed behavior, stratification/cluster structure, and selection probabilities where applicable.

---

## 11. Memory, Performance & Scale Management

| SAS | DuckDB |
|---|---|
| `OPTIONS MEMSIZE=` / `SORTSIZE=` | `SET memory_limit='16GB'`, `SET threads=8` or equivalent configuration |
| `OPTIONS COMPRESS=` | DuckDB storage is compressed; Parquet supports explicit compression codecs |
| Indexes | DuckDB supports ART indexes, but analytical workloads often rely more on columnar storage, ordering, zonemaps, and predicate pushdown than traditional indexing |
| `HASH` object lookups | Prefer relational joins/lookups; optimizer chooses efficient join algorithms |
| `INOBS=` / `OUTOBS=` | `LIMIT` |
| `OPTIONS THREADS=` | `SET threads=n` |
| SAS Grid / Viya distributed execution | DuckDB is primarily single-node; this is a key distinction from distributed engines such as Spark |
| `PROC OPTIONS` / log review | `EXPLAIN` / `EXPLAIN ANALYZE` |
| `OPTIONS FULLSTIMER` | `EXPLAIN ANALYZE` and external profiling/OS metrics |
| Lazy execution | Query optimizer can push filters/projections and avoid unnecessary work |

>**DuckDB indexing note:** DuckDB supports ART indexes, but analytical workloads often benefit more from columnar storage, ordering, zonemaps, and predicate/projection pushdown than from manually created indexes.

### Performance guidance

Do not assume that DuckDB will automatically outperform every SAS workload. Performance depends on data format, I/O, query shape, memory, concurrency, code quality, and how faithfully the SAS semantics are reproduced. Benchmark. Benchmark. Benchmark.

The strongest performance case is often **columnar data + vectorized operations + single-node parallelism**.

---

## 12. Loading Packages / Extending

| SAS | DuckDB + Python |
|---|---|
| `PROC FCMP` | SQL macros or Python UDFs where appropriate |
| `PROC PROTO` (call C) | C/C++ extension mechanisms |
| SAS/IML | Fetch to NumPy/SciPy for matrix work |
| SAS/ETS | Prepare data in DuckDB; model with Python time-series/econometrics libraries |
| SAS/OR | Use OR-Tools, PuLP, SciPy, or another optimizer |
| `PROC PYTHON` / `PROC LUA` | N/A -- Python is the host environment |
| Shared macro/code repositories | Shared SQL macros and Python packages |
| Installing extensions | DuckDB extensions such as `httpfs`, `json`, `postgres`, `spatial`, etc. |

---

## 13. Data Quality, Auditing & Governance

| SAS | DuckDB |
|---|---|
| `PROC COMPARE` | Set comparisons plus explicit schema/value validation |
| `PROC CONTENTS` | `DESCRIBE`, `PRAGMA table_info()`, `information_schema` |
| `PROC FREQ` with missing | Explicit null-count/frequency queries |
| Audit trail / dataset versioning | No built-in SAS-style dataset versioning; pair with Delta Lake, dbt snapshots, or an external data-versioning system |
| `PROC CATALOG` | `information_schema` / DuckDB metadata functions |
| `PROC FORMAT` (code mappings) | Lookup table + `JOIN`, or `CASE` for small mappings |
| `DICTIONARY` tables | `information_schema`, DuckDB metadata functions |

### SAS missing-value warning

SAS numeric missing values are not identical to SQL `NULL`. Standard SAS missing (`.`) and special missing values (`._`, `.A`–`.Z`) may carry different meanings and ordering behavior.

For migrations where those distinctions matter, explicitly encode the missing categories rather than collapsing them all into one null representation.

---

## 14. Control Flow & Job Orchestration

| SAS | DuckDB + Python |
|---|---|
| `%INCLUDE` chaining | Python modules/functions that execute SQL steps |
| SAS EG / Studio process flows | Prefect, Dagster, Airflow, or Python scripts/notebooks |
| SAS Data Integration Studio | dbt-duckdb for SQL transformations and tests, or a Python orchestration layer |
| `SYSTASK` / `X` command | Python `subprocess` |
| `&SYSERR` / `&SYSCC` | `try/except`, explicit status handling, and process exit codes |

---

## 15. SAS Semantic Traps to Test Explicitly

A production migration should have a test suite covering at least these categories:

### Row order
SQL tables and relational operations do not inherently guarantee row order. SAS programs sometimes rely on explicit sorting and sequential DATA-step processing.

### BY-group processing
`FIRST.` / `LAST.` behavior should be translated from the SAS BY-group definition, not merely replaced with "first row" and "last row" logic.

### `LAG` / `DIF`
SAS DATA-step `LAG()` uses queue semantics. A SQL `LAG()` is appropriate only when that is the intended behavior.

### Missing values
Test SAS `.` and special missing values separately from SQL nulls.

### Dates
Test `INTCK`, `INTNX`, `YRDIF`, month-end dates, leap years, interval alignment, and any business-calendar logic.

### Numeric precision
Test currency and other fixed-point calculations with representative edge cases and confirm that no step silently converts exact decimals to floating point.

### Character variables
Check SAS variable lengths, blank padding, truncation behavior, and conversion between numeric and character types.

### Formats
Confirm that a SAS format used for presentation is not accidentally treated as a data transformation.

### Duplicate handling
Do not assume `NODUPKEY`, `DISTINCT`, and `DISTINCT ON` mean the same thing. Define which duplicate should survive.

### Multiple-output DATA steps
SAS can send different rows to different output datasets during one DATA-step iteration. Recreate that routing explicitly.

---

## 16. When to Use DuckDB

### DuckDB excels when:

- Team works with relational databases and SQL
- Joining/querying many files or formats
- You want SQL directly over Parquet/CSV/JSON
- You are replacing `PROC SQL` heavy programs
- You want a lightweight analytical engine on a single machine
- Need to integrate with multiple data sources (databases, files, APIs)

### Example architecture:

```text
SQL-heavy workflow:
sources → DuckDB → Python ecosystem
```

---

## 17. Migration Notes

### Precision

Use fixed-point `DECIMAL` types for monetary values where exact decimal arithmetic is required. Avoid silently converting those values to binary floating-point during downstream processing.

### Scale

Many large tabular workloads can run effectively on a single modern server with DuckDB, including datasets in the tens of millions of rows and beyond. Do not assume that a distributed framework is required simply because a SAS workload is described as "large."

Benchmark the actual workload, especially when moving from SAS datasets to Parquet.

### Reproducibility and auditability

DuckDB does not provide the same built-in governance model as a large SAS installation. Pair the compute layer with version-controlled code, explicit schemas, validation tests, lineage/versioning tools, and an orchestration system appropriate to the environment.

### SQL macros and reusable functions

DuckDB SQL macros are useful for reusable SQL expressions, but they are not a general replacement for the full SAS macro language. Use Python for program generation, orchestration, parameterization, and more complex control flow.

---

## 18. Practical Migration Strategy

For a real SAS-to-DuckDB migration, use this sequence:

```text
1. Inventory SAS programs
        ↓
2. Classify each step
   ├─ SQL / relational → DuckDB SQL
   ├─ DATA step / stateful → SQL with CTEs/window functions or Python
   ├─ statistical / ML → Python libraries (statsmodels, scikit-learn)
   ├─ reporting / ODS → Python reporting tools
   └─ orchestration / macro → Python functions + dbt
        ↓
3. Implement in DuckDB + Python
        ↓
4. Reproduce SAS semantics
        ↓
5. Validate row counts / keys / values /
   missing values / precision / outputs
        ↓
6. Benchmark
        ↓
7. Productionize and monitor
```

The goal is not to translate SAS syntax mechanically. The goal is to reproduce the **data contract, business logic, outputs, and operational behavior** using modern single-node data tooling.
