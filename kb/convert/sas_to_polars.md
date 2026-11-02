# SAS → Polars Migration Guide

Lowest entry for build outs and env control: [uv](https://docs.astral.sh/uv/)

### For single-node and government data work in Python

**[Polars](https://docs.pola.rs/api/python/stable/reference/index.html)** is the closest fit for DataFrame-style transformations and reusable Python pipelines, especially where SAS DATA-step logic can be expressed as vectorized expressions. It excels at high-performance data manipulation with a focus on type safety and lazy evaluation.

A reliable migration strategy is **semantic rather than one-to-one**: preserve the behavior of the SAS program first, then choose the Polars implementation that best *reflects* that behavior.

---

## 1. Data Loading / Importing

| SAS | Polars |
|---|---|
| `PROC IMPORT` (CSV) | `pl.read_csv(path)` |
| `PROC IMPORT` (Excel) | `pl.read_excel(path)` (via supported Excel engine) |
| `INFILE` / `INPUT` (fixed-width) | Positional parsing with string slicing or other parsing expressions; use a dedicated fixed-width parser when appropriate |
| `LIBNAME` | No direct library/catalog analogue; read files or databases directly |
| `PROC SQL CONNECT TO` | `pl.read_database()` / `pl.read_database_uri()` using supported database drivers such as ADBC or ConnectorX |
| `FILENAME` | Direct paths and supported cloud/object-store sources |
| `PROC CIMPORT` / `CPORT` | Usually replace with Parquet/CSV or another interoperable format |
| `PROC XCOPY` | Standard Python/filesystem operations |

**Migration note:** Fixed-width `INFILE`/`INPUT` processing is positional parsing, not ordinary CSV parsing. Preserve field offsets, widths, informats, and conversion rules explicitly.

**Migration note:** SAS libraries often combine data access, metadata, formats, and naming conventions. A `LIBNAME` migration may therefore require more than simply changing the file path.
**Migration Note:** When working with parquet files, use `pl.read_parquet()` for eager loading (immediate in-memory DataFrame) and `pl.scan_parquet()` for lazy loading with query optimization.


---

## 2. Writing / Exporting Data

| SAS | Polars |
|---|---|
| `PROC EXPORT` | `df.write_csv()`, `df.write_parquet()`, `df.write_excel()` |
| `FILE` / `PUT` (custom flat file) | Build a formatted string expression, then write the file |
| `PROC SQL CREATE TABLE` | Materialize a DataFrame/LazyFrame or write to Parquet/database |
| `PROC DATASETS` | Manage files/dataframes/schema through Python and storage-layer operations |
| `PROC APPEND` | `pl.concat()` for in-memory frames; use an appropriate table/storage layer for durable append workflows |
| `ODS PDF/RTF/EXCEL/HTML` | `write_excel()` covers basic Excel output; complex reports require another library |

**Migration note:** ODS is a reporting system, not simply a data-export feature. Replacing ODS often requires a separate reporting layer.
**Migration Note:** For writing parquet files, use `df.write_parquet()` when data is in memory, or `lf.sink_parquet()` on LazyFrames to stream results to disk *without* collecting into memory (more efficient for large datasets).


---

## 3. Data Manipulation -- DATA Step Core

| SAS | Polars |
|---|---|
| `DATA` step | `.with_columns()` |
| `SET` | `pl.scan_parquet()`, `pl.scan_csv()`, etc. |
| `SET a b c` (concatenate/union) | `pl.concat([df1, df2, df3])` |
| `MERGE ... BY` | `.join(...)` only when the intended behavior is a relational join; reproduce SAS BY-group behavior explicitly when needed |
| `RETAIN` | Window expressions for many cumulative patterns; some sequential state requires a different design |
| `ARRAY` | Expression expansion over selected columns, list/array operations, or reshape/explode |
| `DO` / `DO WHILE` / `DO UNTIL` | Python control flow around vectorized Polars operations |
| `IF-THEN-ELSE` / `SELECT-WHEN` | `pl.when(...).then(...).otherwise(...)` |
| `OUTPUT` (route rows) | `.filter()` into separate DataFrames/LazyFrames |
| `LAG` / `DIF` | `.shift()` / `.diff()` with explicit ordering |
| `FIRST.var` / `LAST.var` | Group-aware expressions or row-number/boundary logic |
| `LENGTH` | String length / schema inspection |
| `FORMAT` | Formatting at presentation/export time |
| `INFORMAT` | Parsing such as `.str.strptime()` or `.cast()` |
| `RENAME=` / `DROP=` / `KEEP=` | `.rename()`, `.drop()`, `.select()` |

### Important SAS DATA-step caveat

SAS DATA steps are **stateful and sequential**. Do not assume that every DATA-step statement has a direct vectorized DataFrame equivalent.

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

| SAS | Polars |
|---|---|
| `WHERE` | `.filter(...)` |
| `IF` (post-compute filter) | `.with_columns(...)` then `.filter(...)` |
| `WHERE=` dataset option | Predicate pushdown in `scan_*` lazy pipelines |
| `PROC SQL WHERE/HAVING` | `.filter()` before/after `.group_by().agg()` as appropriate |
| `%IF %THEN` (macro-time) | Python control flow around expression construction |

**Important:** `WHERE` in SAS and `IF` in a DATA step do not always have identical execution timing. Preserve the original calculation/filter order when translating.

---

## 5. Aggregating / Summarizing

| SAS | Polars |
|---|---|
| `PROC MEANS` / `SUMMARY` | `.group_by(...).agg(...)` |
| `PROC FREQ` | `.group_by(...).len()`, `.value_counts()` |
| `PROC TABULATE` | `.pivot()` / `.unpivot()` as appropriate |
| `PROC SQL GROUP BY` | `.group_by().agg()` |
| `PROC REPORT` | Aggregate, then pair with reporting/export tools |
| `CLASS` statement | Columns passed to `.group_by()` |
| `PROC RANK` | `.rank()` and quantile/bucketing expressions |

---

## 6. Sorting, Joining, Reshaping

| SAS | Polars |
|---|---|
| `PROC SORT` (+ `NODUPKEY`) | `.sort()`; `.unique(subset=[...])` |
| `PROC TRANSPOSE` | `.pivot()` / `.unpivot()` |
| `PROC SQL` joins | `.join(...)` |
| `HASH` object (lookup) | Use joins or appropriate lookup structures; do not assume a relational join reproduces every SAS `HASH` behavior |
| `PROC COMPARE` | Anti-joins, joins, and `assert_frame_equal()` for tests |

**Important:** `PROC COMPARE` is more than a row-set difference. A production validation framework should compare schema, row counts, keys, null/missing behavior, numeric tolerances, and values column by column. Also, when possible, it is best to avoid distinct/sorting until *after* tables are reduced in size to avoid costly row-wise actions.

---

## 7. Macros (Automation and Reusability)

| SAS | Polars / Python |
|---|---|
| `%MACRO` / `%MEND` | Python functions returning expressions/LazyFrames |
| `%LET` | Python variables |
| `%IF %THEN %ELSE` | Python `if/else` around expression construction |
| `%DO %END` | Python loops around expression/pipeline construction |
| `CALL SYMPUT` / `SYMPUTX` | `.item()` / scalar extraction |
| `PROC SQL INTO :` | Scalar/series extraction from the result |
| `%INCLUDE` | Python `import` |
| Autocall macro libraries | Shared Python packages/modules |
| `SASAUTOS=` | Python package/module search path |

---

## 8. Date / Numeric Functions

| SAS | Polars |
|---|---|
| `INTCK` | `.dt` methods or explicit interval calculations; test SAS semantics |
| `INTNX` | `.dt.offset_by()` and explicit alignment logic |
| `YRDIF` | Explicit day/month/year-fraction logic |
| `MDY`, `TODAY()`, `DATDIF` | Date constructors, Python date values, and `.dt` methods |
| Date informats/formats | `.str.strptime()` / `.dt.strftime()` |
| `ROUND` / `CEIL` / `FLOOR` | `.round()`, `.ceil()`, `.floor()` |
| `SUM` / `MEAN` / `STD` / `CV` | `.sum()`, `.mean()`, `.std()`; calculate CV explicitly |
| FINANCE functions (`NPV`, `IRR`, depreciation, etc.) | Usually use an appropriate Python financial/numerical library |
| `PROC FCMP` | Native Polars expressions where possible; Python functions only when needed |

### Date migration warning

`INTCK`, `INTNX`, `YRDIF`, business-day calculations, month-end rules, leap-year behavior, and interval alignment are common sources of subtle migration errors. Build representative test cases before declaring a SAS date calculation equivalent.

---

## 9. String / Text Handling

| SAS | Polars |
|---|---|
| `SUBSTR`, `SCAN`, `TRIM`, `STRIP` | `.str.slice()`, `.str.split()`, `.str.strip_chars()` |
| `CATX`, `CAT`, `CATS` | `pl.concat_str(...)` |
| `COMPRESS` | `.str.replace_all()` |
| `PRXMATCH` / `PRXCHANGE` | `.str.contains()`, `.str.extract()`, `.str.replace_all()` |
| `INDEX` / `FIND` | String search functions such as `.str.find()` |

**Migration note:** SAS character variables have fixed declared lengths and can be silently padded/truncated in ways that ordinary Python strings are not. Validate width and missing/blank behavior explicitly.

---

## 10. Statistical / Modeling

| SAS | Polars / Python |
|---|---|
| `PROC REG` | Prepare data with Polars, then use `statsmodels` or scikit-learn |
| `PROC LOGISTIC` | Prepare data with Polars, then use `statsmodels` or scikit-learn |
| `PROC GLM` / `MIXED` | Use appropriate `statsmodels` models after data preparation |
| `PROC ARIMA` / `FORECAST` / `ESM` | Prepare panel/series data with Polars, then use `statsmodels`, sktime, or another appropriate library |
| `PROC SURVEYSELECT` | `.sample(...)` for simple cases; use specialized sampling/statistical logic for complex designs |
| `PROC UNIVARIATE` | `.describe()`, `.quantile()`, and statistical libraries |
| `PROC HPFOREST` / `HPLOGISTIC` | scikit-learn, XGBoost, LightGBM, or another appropriate single-node ML library, using Polars for feature preparation |

**Important:** Statistical procedure equivalence is about **model specification and inference**, not just API replacement. Match distributions, missing-value handling, reference coding, confidence intervals, weighting, convergence settings, and output definitions.

For sampling procedures such as `PROC SURVEYSELECT`, also match the sampling design, replacement rules, random seed behavior, stratification/cluster structure, and selection probabilities where applicable.

---

## 11. Memory, Performance & Scale Management

| SAS | Polars |
|---|---|
| `OPTIONS MEMSIZE=` / `SORTSIZE=` | Multithreaded automatically; resource usage is generally controlled through execution/environment configuration |
| `OPTIONS COMPRESS=` | Parquet supports explicit compression codecs |
| Indexes | No general-purpose index model; relies on columnar scans and query optimization |
| `HASH` object lookups | Prefer joins or appropriate lookup structures |
| `INOBS=` / `OUTOBS=` | `.head()` or lazy `.limit()` |
| `OPTIONS THREADS=` | Multithreaded execution by default |
| SAS Grid / Viya distributed execution | Polars is primarily single-node; distributed execution should not be treated as a drop-in replacement for SAS Grid/Viya |
| `PROC OPTIONS` / log review | `.explain()` on LazyFrames |
| `OPTIONS FULLSTIMER` | Use current Polars profiling/diagnostic tools appropriate to the execution engine |
| Lazy execution | `scan_*` + `.collect()` builds and optimizes a lazy plan |

### Performance guidance

Do not assume that Polars will automatically outperform every SAS workload. Performance depends on data format, I/O, query shape, memory, concurrency, code quality, and how faithfully the SAS semantics are reproduced. Benchmark. Benchmark. Benchmark.

The strongest performance case is often **columnar data + vectorized operations + single-node parallelism**.

---

## 12. Loading Packages / Extending

| SAS | Polars / Python |
|---|---|
| `PROC FCMP` | Native expressions or Python functions; prefer native/vectorized operations |
| `PROC PROTO` (call C) | Rust-based plugins for native custom operations where justified |
| SAS/IML | `.to_numpy()` and NumPy/SciPy |
| SAS/ETS | Prepare data in Polars; model with Python time-series/econometrics libraries |
| SAS/OR | Use OR-Tools, PuLP, SciPy, or another optimizer |
| `PROC PYTHON` / `PROC LUA` | N/A -- Python is the host environment |
| Shared macro/code repositories | Shared Python packages/modules |
| Installing extensions | Python package extras and appropriate plugin packages |

---

## 13. Data Quality, Auditing & Governance

| SAS | Polars |
|---|---|
| `PROC COMPARE` | Joins/anti-joins plus `assert_frame_equal()` in automated tests |
| `PROC CONTENTS` | `df.schema`, `df.columns`, `df.dtypes` |
| `PROC FREQ` with missing | `.null_count()` and explicit frequency calculations |
| Audit trail / dataset versioning | No built-in SAS-style dataset versioning; pair with Delta Lake, dbt snapshots, or an external data-versioning system |
| `PROC CATALOG` | Python/schema metadata; no direct catalog equivalent |
| `PROC FORMAT` (code mappings) | Lookup-table `.join()`, `.replace()`, or conditional expressions |
| `DICTIONARY` tables | Inspect schema/dataframe metadata directly |

### SAS missing-value warning

SAS numeric missing values are not identical to Polars `null`. Standard SAS missing (`.`) and special missing values (`._`, `.A`–`.Z`) may carry different meanings and ordering behavior.

For migrations where those distinctions matter, explicitly encode the missing categories rather than collapsing them all into one null representation.

---

## 14. Control Flow & Job Orchestration

| SAS | Polars / Python |
|---|---|
| `%INCLUDE` chaining | Python modules/functions that build and execute Polars pipelines |
| SAS EG / Studio process flows | Prefect, Dagster, Airflow, or Python scripts/notebooks |
| SAS Data Integration Studio | dbt plus Python/Polars components, or plain orchestrated scripts |
| `SYSTASK` / `X` command | Python `subprocess` |
| `&SYSERR` / `&SYSCC` | `try/except`, explicit status handling, and process exit codes |

---

## 15. SAS Semantic Traps to Test Explicitly

A production migration should have a test suite covering at least these categories:

### Row order
Relational operations do not inherently guarantee row order. SAS programs sometimes rely on explicit sorting and sequential DATA-step processing. Use explicit `.sort()` when order matters.

### BY-group processing
`FIRST.` / `LAST.` behavior should be translated from the SAS BY-group definition, not merely replaced with "first row" and "last row" logic.

### `LAG` / `DIF`
SAS DATA-step `LAG()` uses queue semantics. Polars `.shift()` or `.diff()` is appropriate only when that is the intended behavior.

### Missing values
Test SAS `.` and special missing values separately from Polars nulls.

### Dates
Test `INTCK`, `INTNX`, `YRDIF`, month-end dates, leap years, interval alignment, and any business-calendar logic.

### Numeric precision
Test currency and other fixed-point calculations with representative edge cases and confirm that no step silently converts exact decimals to floating point.

### Character variables
Check SAS variable lengths, blank padding, truncation behavior, and conversion between numeric and character types.

### Formats
Confirm that a SAS format used for presentation is not accidentally treated as a data transformation.

### Duplicate handling
Do not assume `NODUPKEY` and `unique()` mean the same thing. Define which duplicate should survive.

### Multiple-output DATA steps
SAS can send different rows to different output datasets during one DATA-step iteration. Recreate that routing explicitly.

---

## 16. When to Use Polars

### Polars excels when:

- Team works with DataFrame/expression pipelines
- You want strict schemas and vectorized transformations
- You are building reusable feature-engineering components
- Downstream Python code will consume the transformed data
- Need type safety and compile-time optimization
- Working with large datasets that benefit from lazy evaluation

### Example architecture:

```text
DataFrame-heavy workflow:
sources → Polars → Python ecosystem
```

---

## 17. Migration Notes

### Precision

Use appropriate numeric types for monetary values where exact decimal arithmetic is required. Avoid silently converting those values to binary floating-point during downstream processing.

### Scale

Many large tabular workloads can run effectively on a single modern server with Polars, including datasets in the tens of millions of rows and beyond. Do not assume that a distributed framework is required simply because a SAS workload is described as "large."

Benchmark the actual workload, especially when moving from SAS datasets to Parquet.

### Reproducibility and auditability

Polars does not provide the same built-in governance model as a large SAS installation. Pair the compute layer with version-controlled code, explicit schemas, validation tests, lineage/versioning tools, and an orchestration system appropriate to the environment.

### Lazy evaluation benefits

Polars' lazy evaluation with `scan_*` methods enables query optimization across multiple operations. Use lazy evaluation for complex pipelines to benefit from predicate pushdown, projection pruning, and other optimizations.

---

## 18. Practical Migration Strategy

For a real SAS-to-Polars migration, use this sequence:

```text
1. Inventory SAS programs
        ↓
2. Classify each step
   ├─ DATA step transformations → Polars expressions
   ├─ Simple filters/aggregations → Polars operations
   ├─ Complex stateful logic → Python + Polars
   ├─ statistical / ML → Python libraries (statsmodels, scikit-learn)
   ├─ reporting / ODS → Python reporting tools
   └─ orchestration / macro → Python functions
        ↓
3. Implement in Polars + Python
        ↓
4. Reproduce SAS semantics
        ↓
5. Validate row counts / keys / values /
   missing values / precision / outputs
        ↓
6. Benchmark and optimize lazy evaluation
        ↓
7. Productionize and monitor
```

The goal is not to translate SAS syntax mechanically. The goal is to reproduce the **data contract, business logic, outputs, and operational behavior** using modern single-node data tooling.
