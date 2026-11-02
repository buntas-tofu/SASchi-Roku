# SAS → R + DuckDB Migration Guide


Lowest entry for build outs and env control: [uvr](https://github.com/nbafrank/uvr), a consistent platform as uv for python (pins R version). Alternative, is [renv](https://github.com/nbafrank/uvr) which creates lock files w/o pinned R version.

### For single-node and government data work in R

DuckDB is the SQL execution and analytical storage layer; R is the statistical, modeling, visualization, and general-purpose programming ecosystem.

SAS workloads are best migrated as a **layered R + DuckDB ecosystem**, not as a single replacement language. DuckDB is particularly useful for SQL-heavy transformations, joins, aggregations, and data that should remain on disk or in columnar formats rather than being pulled entirely into R memory. R remains the primary environment for statistical modeling, specialized procedures, visualization, reporting, and procedural logic.

- **[DuckDB](https://duckdb.org/docs/current/clients/r)** preferred execution for SQL-heavy relational workloads, joins, aggregations, window functions, and Parquet/CSV querying. It can operate in-process without requiring a separate database server.
- **[DB Interface](https://dbi.r-dbi.org/)** provides the R database interface; **dbplyr** allows transformations with dplyr syntax while translating them to SQL for DuckDB or another database.
- **[dplyr](https://rstudio.github.io/cheatsheets/html/data-transformation.html) / tidyverse** for data manipulation and can work either locally in R or lazily through DuckDB via `dbplyr`.
- **[data.table](https://machinelearningplus.com/data-manipulation/datatable-in-r-complete-guide/)** is a strong choice for high-performance in-memory transformations and SAS DATA-step patterns involving `BY` groups, keyed lookups, and in-place updates.
- **stats, lme4, survival, fable, survey**, and related packages replace much of the statistical-procedure ecosystem around `PROC REG`, `PROC MIXED`, `PROC LIFETEST`, `PROC ARIMA`, `PROC SURVEYSELECT`
- **arrow** provides a natural bridge to Parquet and other columnar data, while DuckDB can query those files directly.
- **[quarto](https://rstudio.github.io/cheatsheets/html/quarto.html) / [rmarkdown](https://rstudio.github.io/cheatsheets/html/rmarkdown.html)** replace ODS reporting layer.
- **targets** and an external scheduler/orchestrator can replace parts of SAS Enterprise Guide, Studio, Data Integration, and scheduled process flows.

The migration strategy is **semantic rather than a perfect one-to-one**: preserve the SAS program's behavior, classify each step by workload type, choose DuckDB/SQL, dplyr/dbplyr, data.table, base R or a specialized R package based on the required semantics and scale.

---

## 1. Data Loading / Importing

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `PROC IMPORT` (CSV) | `read_csv_auto()` / `read_csv()` | `read.csv()` | `fread()` | `readr::read_csv()` |
| `PROC IMPORT` (Parquet) | `SELECT * FROM 'file.parquet'` | `arrow::read_parquet()` | `arrow::read_parquet()` then `setDT()` | `arrow::read_parquet()` |
| `PROC IMPORT` (Excel) | `INSTALL excel; LOAD excel;` then `read_xlsx()` for `.xlsx` (no `.xls` support) | `readxl::read_excel()` | `readxl::read_excel()` then `setDT()` | `readxl::read_excel()` |
| `INFILE` / `INPUT` (fixed-width) | Read/parse in R, then register/import into DuckDB | `read.fwf()` | Preprocess or use `readr::read_fwf()` | `readr::read_fwf()` |
| `LIBNAME` | DuckDB database/file, or `DBI` connection to another engine | File paths, connections, `DBI` | Same | Same, often through `DBI`/`dbplyr` |
| `PROC SQL CONNECT TO` | `DBI::dbConnect(duckdb::duckdb())` or another DBI backend | `DBI::dbConnect()` + `dbGetQuery()` | `DBI` connection + downstream data.table | `dbplyr` for lazy SQL translation |
| `FILENAME` | DuckDB file readers or external files; use R for non-tabular protocols | Filesystem paths, URLs, connections | Same | Same |
| `PROC CIMPORT` / `CPORT` | Prefer Parquet/CSV or migrate SAS datasets into R first | `.rds`, Parquet, etc. | Same | Same; `arrow::read_parquet()` |
| `PROC XCOPY` | Filesystem copy or DuckDB/Parquet staging | `file.copy()` | Same | Same |
| SAS `.sas7bdat` files | Read with `haven`, then write/register as Parquet or DuckDB tables | `haven::read_sas()` | `haven::read_sas()` then `setDT()` | `haven::read_sas()` |

**Migration note:** Fixed-width `INFILE`/`INPUT` processing is positional parsing, not ordinary CSV parsing. Preserve field offsets, widths, informats, and conversion rules explicitly.

**Migration note:** SAS libraries often combine data access, metadata, formats, and naming conventions. A `LIBNAME` migration may therefore require more than simply changing the file path. `haven::read_sas()` is often the most direct way to bring existing `.sas7bdat` datasets into R during a transition period.

**Migration note:** For Parquet files, use `arrow::read_parquet()` for full in-memory loading into R, or `arrow::open_dataset()` for lazy queries on larger-than-RAM datasets (works with dplyr verbs, then `collect()` to materialize). DuckDB can also query Parquet files directly with `SELECT * FROM 'file.parquet'` without loading into R memory first.

## 1A. DuckDB as the Analytical SQL Layer

DuckDB is useful when a SAS workload is fundamentally relational or when intermediate datasets are too large or unnecessary to materialize as R data frames. It can query CSV and Parquet directly, persist tables in a DuckDB database file, and execute SQL in-process from R through `DBI`.

Typical architecture:

```text
SAS source files / feeds
        ↓
  R ingestion / validation
        ↓
  Parquet / DuckDB
        ↓
  DuckDB SQL transformations
        ↓
  dbplyr / DBI
        ↓
  R data.frame / tibble
        ↓
 statistical modeling / visualization / reporting
```

Use DuckDB when the work is primarily:

- joins, filters, aggregations, and window functions;
- SQL-heavy `PROC SQL` workloads;
- large CSV/Parquet datasets that should not all be loaded into R memory;
- repeated analytical queries over persistent local data;
- staging and intermediate transformations before an R modeling step.

Do **not** force all SAS DATA-step logic into SQL. Stateful procedural behavior, complex row-by-row logic, SAS-specific missing-value behavior, and specialized statistical procedures are often better implemented in R.

A useful division of responsibility is:

- **DuckDB:** relational transformation, filtering, joins, aggregation, windowing, staging, and analytical SQL.
- **dplyr/dbplyr:** readable R interface to SQL when the operation can be translated cleanly.
- **data.table:** high-performance in-memory and stateful tabular operations.
- **base R:** general-purpose and sequential procedural logic.
- **specialized R packages:** statistics, ML, survival analysis, time series, survey methods, visualization, and reporting.

---

## 2. Writing / Exporting Data

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `PROC EXPORT` (CSV) | `COPY ... TO 'file.csv' (HEADER)` | `write.csv()` | `fwrite()` | `readr::write_csv()` |
| `PROC EXPORT` (Parquet) | `COPY ... TO 'file.parquet'` | `arrow::write_parquet()` | `arrow::write_parquet()` | `arrow::write_parquet()` |
| `FILE` / `PUT` (custom flat file) | Usually generate in R; DuckDB is not a general text-template engine | `sprintf()` + `writeLines()` | Same, often vectorized | Same, or `glue::glue()` |
| `PROC SQL CREATE TABLE` | `CREATE TABLE AS SELECT ...` | Assign an R object; `DBI::dbWriteTable()` for persistent DB tables | Same | `dbplyr` + `compute()` / `copy_to()` or `DBI::dbWriteTable()` |
| `PROC DATASETS` | `DROP TABLE`, `ALTER TABLE`, `DROP VIEW` for database objects | `rm()`, `file.remove()`, `saveRDS()`/`readRDS()` | Same | Same through DBI/dbplyr when applicable |
| `PROC APPEND` | `INSERT INTO ... SELECT ...` | `rbind()` | `rbindlist()` | `bind_rows()` |
| `ODS PDF/RTF/EXCEL/HTML` | Usually hand off final tables/data to R reporting tools | `quarto`/`rmarkdown`, `openxlsx`, `officer` | Same | `gt`/`flextable`/Quarto |

**Migration note:** ODS is a reporting system, not simply a data-export feature. `rmarkdown`/`quarto` combined with `gt`, `flextable`, or `officer` is the closest overall replacement, but replicate specific ODS templates deliberately rather than assuming a default theme matches.

**Migration note:** For Parquet files, use `arrow::write_parquet()` with optional compression codecs (e.g., `compression = "snappy"` or `"zstd"`). Parquet is the recommended format for large datasets due to columnar storage and efficient compression. DuckDB can write directly to Parquet with `COPY (SELECT ...) TO 'file.parquet'`.

---

## 3. Data Manipulation -- DATA Step Core

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `DATA` step | `SELECT`/`CREATE TABLE AS` for the relational parts of a DATA step | Vector/data-frame assignment | `DT[, new_col := expr]` | `mutate()` |
| `SET` | `SELECT * FROM table`; for `SET a b c`, `UNION ALL` | Reading/reference an existing data frame | Existing `data.table` or `rbindlist()` for concatenation | Existing tibble or `bind_rows()` for concatenation |
| `SET a b c` (concatenate/union) | `UNION ALL` | `rbind(a, b, c)` | `rbindlist(list(a, b, c))` | `dplyr::bind_rows(a, b, c)` |
| `MERGE ... BY` | SQL `JOIN`, only when relational-join behavior is intended | `merge()` **only when the intended behavior is a relational join; SAS BY-group merge semantics may differ substantially with duplicate keys** | `DT1[DT2, on = "key"]` joins, only when relational-join behavior is intended | `left_join()`/`inner_join()`/etc., only when relational-join behavior is intended |
| `RETAIN` | Window functions for simple cumulative state; otherwise move stateful logic to R | Cumulative functions or explicit loop/state object | Cumulative functions or explicit sequential updates | Cumulative functions or `purrr::accumulate()` for general state |
| `ARRAY` | Not a natural SQL concept; handle in R | Operate over columns with `sapply()`/`lapply()`, or matrix-style indexing | `.SDcols` with `lapply(.SD, ...)` | `across()` over selected columns |
| `DO` / `DO WHILE` / `DO UNTIL` | Not a natural SQL concept; handle in R | `for`, `while`, `repeat` control flow | Same R control flow around `data.table` operations | Same R control flow; prefer vectorized/`purrr::map()` alternatives where possible |
| `IF-THEN-ELSE` / `SELECT-WHEN` | `CASE WHEN ... THEN ... ELSE ... END` | `ifelse()`, `if/else`, `switch()` | `fifelse()`, `fcase()` | `dplyr::if_else()`, `dplyr::case_when()` |
| `OUTPUT` (route rows) | Separate `SELECT ... WHERE ...` queries per condition | Subset into separate objects with logical indexing | Separate `DT[cond]` subsets | `dplyr::filter()` into separate tibbles, or `group_split()` |
| `LAG` / `DIF` | `LAG`/`LEAD` window functions only for unconditional previous/next-row semantics; SAS queue semantics require R | `lag()` / explicit indexing only for previous-row semantics; explicit state for SAS queue behavior | `shift()` only for previous-row semantics; explicit state for SAS queue behavior | `lag()` / `lead()` with explicit ordering; explicit state when SAS queue semantics matter |
| `FIRST.var` / `LAST.var` | Window functions or row-number logic **after reproducing SAS BY ordering** | Explicit comparison after reproducing sort/order | `.SD[1]` / `.SD[.N]` after reproducing SAS BY ordering | `slice_head()` / `slice_tail()` after `arrange()` and `group_by()` |
| `LENGTH` | Note SAS variable length is a schema/storage attribute, not just string length | `nchar()` for strings | `nchar()`; column type controlled via `data.table` schema | `stringr::str_length()` |
| `FORMAT` | Not a data transformation; apply at presentation/export time | `format()`, `sprintf()` at presentation time | Same, applied at print/export time | `scales::` functions, or formatting at presentation/export time |
| `INFORMAT` | `CAST()`/`TRY_CAST()`, or parse before loading | `as.Date()`, `as.numeric()`, explicit parsing functions | Same, or `data.table::as.IDate()`/`as.ITime()` | `readr::parse_date()`, `lubridate::ymd()`, etc. |
| `RENAME=` / `DROP=` / `KEEP=` | `SELECT col AS new_name`, column subsetting in `SELECT` list | `names(df)[...] <- ...`, column subsetting with `[ , cols]` | `setnames()`, `DT[, !c("col")]`, `DT[, ..cols]` | `rename()`, `select()` |

### Important SAS DATA-step caveat

SAS DATA steps are **stateful and sequential**. Do not assume that every DATA-step statement has a direct base R, data.table, or dplyr equivalent.

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

For these, migrate the **behavior**, not merely the syntax. `data.table`'s `by =` grouping and in-place `:=` updates are often the closest match to SAS's sequential, BY-group-aware DATA step; base R loops with explicit indexing are the most literal (if slowest) translation when order-dependent state truly cannot be vectorized.

---

## 4. Filtering / Subsetting

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `WHERE` | `WHERE col = ...` | `df[df$col == x, ]`, `subset()` | `DT[col == x]` | `filter()` |
| `IF` (post-compute filter) | Compute in a CTE/subquery, then `WHERE` | Compute column, then subset | `DT[, new := expr][cond]` | `mutate()` then `filter()` |
| `WHERE=` dataset option | Push predicate into SQL when the source supports it | Filter after read, unless the source connection supports pushdown | Filter during/after read as appropriate | Predicate pushdown via `dbplyr` |
| `PROC SQL WHERE/HAVING` | `WHERE` / `HAVING` | `subset()`, or `DBI::dbGetQuery()` | `DT[cond, .(agg), by = group][agg_cond]` | `filter()` before/after `group_by() %>% summarise()` |
| `%IF %THEN` (macro-time) | R control flow around SQL generation/execution | `if/else` | Same | Same, often inside functions |

**Important:** `WHERE` in SAS and `IF` in a DATA step do not always have identical execution timing. Preserve the original calculation/filter order when translating.

---

## 5. Aggregating / Summarizing

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `PROC MEANS` / `SUMMARY` | `SELECT group, AVG(x), STDDEV_SAMP(x) ... GROUP BY group` | `aggregate()`, `tapply()` | `DT[, .(mean = mean(x), sd = sd(x)), by = group]` | `group_by() %>% summarise()` |
| `PROC FREQ` | `COUNT(*) ... GROUP BY` | `table()` | `DT[, .N, by = group]` | `count()` |
| `PROC TABULATE` | `GROUP BY` plus conditional aggregation / `PIVOT` where appropriate | `xtabs()`, `reshape()` | `dcast()` | `tidyr::pivot_wider()` |
| `PROC SQL GROUP BY` | `GROUP BY` | `aggregate()`, or `DBI::dbGetQuery()` | `DT[, .(...), by = group]` | `group_by() %>% summarise()` |
| `PROC REPORT` | Aggregate in SQL, then hand off to R reporting | Aggregate/summarize, then format | Same | Same; pair with `gt`/`flextable` |
| `CLASS` statement | `GROUP BY` / model-specific classification | Grouping variable passed to `aggregate()`/`tapply()` | Columns passed to `by =` | Columns passed to `group_by()` |
| `PROC RANK` | `RANK()` / `NTILE()` window functions | `rank()`, `cut()`/`quantile()` | `frank()`, `cut()` | `ntile()`, `percent_rank()` |

**Missing-value warning:** SAS summary functions and R summary functions do not have identical defaults. R commonly requires explicit `na.rm = TRUE`, while SAS procedures generally exclude standard numeric missing values from many summaries. DuckDB's SQL aggregate behavior should also be tested against the SAS result when missing values are present. Test all-missing, partially-missing, and special-missing cases explicitly.

---

## 6. Sorting, Joining, Reshaping

| SAS | DuckDB / SQL | base R | data.table | dplyr / tidyverse |
|---|---|---|---|---|
| `PROC SORT` (+ `NODUPKEY`) | `ORDER BY`; `SELECT DISTINCT`, or `ROW_NUMBER()` with an explicit tiebreak rule | `order()`; `duplicated()`/`unique()` | `setorder()`; `unique(DT, by = "key")` | `arrange()`; `distinct()` |
| `PROC TRANSPOSE` | `PIVOT` / conditional aggregation where appropriate | `reshape()`, `t()` | `dcast()` / `melt()` | `pivot_wider()` / `pivot_longer()` |
| `PROC SQL` joins | SQL `JOIN` | `merge()` | `DT1[DT2, on = "key"]`, `merge.data.table()` | `left_join()`, `inner_join()`, `full_join()`, `anti_join()`, etc. |
| `HASH` object (lookup) | SQL joins or lookup tables for relational lookups; use R for procedural/stateful HASH behavior | Named vectors/lists or `match()` | Keyed `data.table` lookups (`DT[key]`) | `left_join()` for relational lookups; do not assume it reproduces every SAS `HASH` behavior |
| `PROC COMPARE` | SQL row counts/keys plus set-difference and explicit value comparisons | `all.equal()` plus explicit schema/value checks | `fsetdiff()` plus explicit schema/value checks | `waldo::compare()`, `testthat::expect_equal()` |

**Important:** `PROC COMPARE` is more than a row-set difference. A production validation framework should compare schema, row counts, keys, null/missing behavior, numeric tolerances, and values column by column. DuckDB can efficiently perform large-scale row/key checks; R tools such as `waldo` and `testthat` are useful for readable and automated validation.

---

## 7. Macros (Automation and Reusability)

| SAS | base R | data.table | R / tidyverse |
|---|---|---|---|
| `%MACRO` / `%MEND` | R functions | R functions operating on `data.table` objects | R functions, often written to accept tidy-eval expressions |
| `%LET` | R variables | Same | Same |
| `%IF %THEN %ELSE` | `if/else` around code construction | Same | Same |
| `%DO %END` | `for` loops around code generation/execution | Same | `purrr::map()`/`map_dfr()` for iteration-as-data patterns |
| `CALL SYMPUT` / `SYMPUTX` | Assign to a variable in the calling environment | Same | Same |
| `PROC SQL INTO :` | `DBI::dbGetQuery()` result assigned to a variable | Same | Same, often via `dbplyr::collect()` |
| `%INCLUDE` | `source()` | Same | Same |
| Autocall macro libraries | Shared R packages, or functions sourced from a common location | Same | Same |
| `SASAUTOS=` | R package search path (`.libPaths()`) | Same | Same |

**Migration note:** SAS macros mix text substitution, conditional logic, and code generation in one system. R functions replace most of this cleanly, but macros that generate SAS *code as text* (rather than compute a value) may need to become functions that build and evaluate R expressions (`rlang::expr()`/`eval()`), not ordinary functions.

---

## 8. Date / Numeric Functions

| SAS | base R | data.table | tidyverse |
|---|---|---|---|
| `INTCK` | Manual interval counting with `difftime()`; **SAS interval semantics must be tested** | Same, vectorized over a `data.table` column | `lubridate::interval()` / period arithmetic; test SAS semantics |
| `INTNX` | Manual date arithmetic (`seq.Date()`, custom offset logic); **alignment behavior may require explicit implementation** | Same | `lubridate::%m+%`, `add_with_rollback()`, and explicit alignment logic |
| `YRDIF` | No universal one-function replacement; year-fraction conventions must be selected explicitly | Same | `lubridate::time_length(interval, "years")`, with explicit convention choice |
| `MDY`, `TODAY()`, `DATDIF` | `as.Date()`, `Sys.Date()`, `difftime()` | Same | `lubridate::make_date()`, `lubridate::today()` |
| Date informats/formats | `as.Date(x, format = ...)`, `format()` | Same | `lubridate::ymd()`, `lubridate::dmy()`, `format()` |
| `ROUND` / `CEIL` / `FLOOR` | `round()`, `ceiling()`, `floor()` | Same, vectorized | Same |
| `SUM` / `MEAN` / `STD` / `CV` | `sum()`, `mean()`, `sd()`; calculate CV explicitly | `DT[, .(sum = sum(x), mean = mean(x), sd = sd(x))]`; calculate CV explicitly | `summarise(across(...))`; calculate CV explicitly |


### Date migration warning

Critical Tests: `INTCK`, `INTNX`, `YRDIF`, business-day calculations, month-end rules, leap-year behavior, and interval alignment are common sources of subtle migration errors. Build representative test cases before declaring a SAS date calculation equivalent. The `lubridate` package covers most of this ground but does not replicate every SAS interval convention by default -- check month-end and "same day next month" edge cases explicitly.

---

## 9. String / Text Handling

| SAS | base R | data.table | stringr |
|---|---|---|---|
| `SUBSTR`, `SCAN`, `TRIM`, `STRIP` | `substr()`, `strsplit()`, `trimws()` | Same base functions, vectorized over columns | `str_sub()`, `str_split()`, `str_trim()` |
| `CATX`, `CAT`, `CATS` | `paste()`, `paste0()` | Same | `str_c()` |
| `COMPRESS` | `gsub()` | Same | `str_remove_all()` |
| `PRXMATCH` / `PRXCHANGE` | `grepl()`, `regmatches()`, `gsub()` (POSIX or PCRE regex) | Same base functions | `str_detect()`, `str_extract()`, `str_replace_all()` |
| `INDEX` / `FIND` | `regexpr()`, `gregexpr()` | Same | `str_locate()` |

**Migration note:** SAS character variables have fixed declared lengths and can be silently padded/truncated in ways that ordinary R character vectors are not (for example, SAS can say read only first 12 CHAR for column). Validate width and missing/blank behavior explicitly, especially when round-tripping through `haven::read_sas()`.

---

## 10. Statistical / Modeling

| SAS | R package(s) |
|---|---|
| `PROC REG` | `lm()` (base R `stats`) |
| `PROC LOGISTIC` | `glm(family = binomial)` |
| `PROC GLM` / `MIXED` | `lm()`/`aov()`; `lme4::lmer()` or `nlme::lme()` for mixed models |
| `PROC ARIMA` / `FORECAST` / `ESM` | `fable` and related time-series packages; `forecast` may be appropriate when maintaining an existing R codebase |
| `PROC SURVEYSELECT` | Explicit sampling with `sample()`, or `sampling`/`survey` package functions; validate method, replacement, seed, stratification/cluster design, and selection probabilities |
| `PROC UNIVARIATE` | `summary()`, `quantile()`, `psych::describe()` |
| `PROC HPFOREST` / `HPLOGISTIC` | `ranger`, `randomForest`, `xgboost`, or `tidymodels` for a unified single-node ML workflow |
| `PROC LIFETEST` / `PHREG` | `survival::survfit()` / `survival::coxph()` |
| `PROC SURVEYMEANS` / `SURVEYREG` | `survey` package (`svydesign()`, `svymean()`, `svyglm()`) |

**Important:** Statistical procedure equivalence is about **model specification and inference**, not just API replacement. Match distributions, missing-value handling, reference coding (`contrasts()` in R vs. SAS's default parameterization), confidence intervals, weighting, convergence settings, and output definitions.

For sampling procedures such as `PROC SURVEYSELECT`, also match the sampling design, replacement rules, random seed behavior (note `set.seed()` and SAS RNG seeds do not produce comparable draws), stratification/cluster structure, and selection probabilities where applicable.

---

## 11. Memory, Performance & Scale Management

| SAS | DuckDB / SQL | base R | data.table | tidyverse |
|---|---|---|---|---|
| `OPTIONS MEMSIZE=` / `SORTSIZE=` | Spill/query execution managed by DuckDB; workload can remain on disk rather than materializing all rows in R | Managed by the OS/R session; increase RAM or process in chunks | Memory-efficient and multithreaded via `setDTthreads()` | Standard R memory model; use `dbplyr`, `arrow`, or DuckDB for larger-than-RAM work |
| `OPTIONS COMPRESS=` | Prefer Parquet compression or DuckDB storage; choose based on access pattern | `.rds` supports compression | `fwrite()`/`fread()` support compressed I/O | `arrow::write_parquet()` supports compression codecs |
| Indexes | DuckDB uses its own execution/storage structures; do not assume a SAS index maps directly to a persistent DuckDB index | No general-purpose index model in base data frames | `setkey()`/`setindex()` for in-memory lookups/filters | No native indexing; `dbplyr` can push work to DuckDB |
| `HASH` object lookups | SQL joins/lookups for relational behavior; R for procedural/stateful behavior | Named vector/list lookups, or `match()` | Keyed `data.table` binary-search lookups | `left_join()`; for very large lookups, push to DuckDB |
| `INOBS=` / `OUTOBS=` | `LIMIT` / `FETCH` | `head()` | `DT[1:n]` | `head()`, `slice_head()` |
| `OPTIONS THREADS=` | DuckDB manages parallel query execution | `parallel`, `future`, or `foreach` for explicit parallelism | `setDTthreads(n)` | Depends on backend; DuckDB/Arrow can provide parallel execution |

### Performance guidance

Do not assume that R or DuckDB will automatically outperform every SAS workload.

A useful rule is:

- **DuckDB** for large relational operations, SQL-heavy transformations, joins, aggregations, window functions, and data that should remain on disk/columnar.
- **data.table** for large in-memory transformations and stateful tabular operations.
- **dplyr/dbplyr** when readable R syntax should compile to SQL and execute in DuckDB.
- **base R** for procedural/stateful logic that does not naturally map to SQL.

For datasets that exceed available RAM, prefer querying Parquet or DuckDB tables rather than forcing everything into an R memory. `arrow` is useful for columnar interchange and file-oriented workflows; DuckDB is useful when SQL transformations and joins are central.

---

## 12. Data Quality, Auditing & Governance

| SAS | DuckDB / SQL | base R | data.table | tidyverse |
|---|---|---|---|---|
| Dataset versioning | Pair DuckDB/Parquet with version-controlled code, metadata, and an external data-versioning/lineage system | Pair with `renv`, version control, and data-versioning tools | Same | Same |
| `PROC COMPARE` | SQL row counts, key checks, set differences, and explicit value comparisons | `all.equal()`; explicit schema/value checks | `fsetdiff()` plus explicit schema/value checks | `waldo::compare()`, `testthat::expect_equal()` |
| `PROC CONTENTS` | DuckDB metadata/catalog queries; `information_schema` where applicable | `str()`, `summary()`, attributes | `str(DT)`, column classes | `glimpse()` |
| `PROC FREQ` with missing | `GROUP BY` with explicit `IS NULL` handling | `table(x, useNA = "always")` | `DT[, .N, by = .(x, is.na(x))]` | `count(x, .drop = FALSE)` with explicit NA handling |
| `PROC CATALOG` | DuckDB catalog plus explicit metadata/catalog tables | `ls()`, package/namespace inspection | Same | Same |
| `PROC FORMAT` (code mappings) | Lookup/reference tables joined in SQL | Named vector lookup, `factor()` with explicit levels/labels | Lookup-table join via keyed data.table | `recode()`, `case_when()`, or `left_join()` |
| `DICTIONARY` tables | DBI metadata APIs, DuckDB catalog queries, and `information_schema` where applicable | `ls()`, `environment()`, object attributes | Same | Same through DBI/dbplyr where applicable |

### SAS missing-value warning

SAS numeric missing values are not identical to R's `NA`. Standard SAS missing (`.`) and special missing values (`._`, `.A`–`.Z`) may carry different meanings and ordering behavior, and R has *no native concept* of SAS-style special missing categories (`NA` is a single sentinel, though `NaN` is distinct). DuckDB uses SQL `NULL`, which is another semantic boundary that must be tested rather than assumed equivalent.

For migrations where those distinctions matter, explicitly encode the missing categories (for example, as a factor level or separate flag column) before data enters DuckDB or R, and define how they should behave in joins, filters, sorting, arithmetic, and aggregates.

---

## 13. Control Flow & Job Orchestration

| SAS | R |
|---|---|
| `%INCLUDE` chaining | `source()` chains, or a package of functions |
| SAS EG / Studio process flows | R scripts/R Markdown notebooks, `targets` pipelines, or an external orchestrator (Airflow, cron) |
| SAS Data Integration Studio | `targets` (dependency-aware pipelines) plus R scripts, or dbt for SQL-heavy steps paired with R for the rest |
| `SYSTASK` / `X` command | `system()`, `system2()`, `processx` |
| `&SYSERR` / `&SYSCC` | `tryCatch()`, condition handling, and explicit process exit codes (`quit(status = ...)`) |

---

# 14. SAS Semantic Traps to Test Explicitly

### Row order
Base R data frames and `data.table`/dplyr operations do not always guarantee row order the way sequential SAS DATA-step processing does. Sort explicitly when order matters.

### BY-group processing
`FIRST.` / `LAST.` behavior should be translated from the SAS BY-group definition, not merely replaced with "first row" and "last row" logic -- confirm the sort order that defines the group is reproduced exactly.

### `LAG` / `DIF`
SAS DATA-step `LAG()` uses queue semantics tied to DATA-step execution order. `data.table::shift()` or `dplyr::lag()` is appropriate only when simple previous-row semantics (not queued/conditional lag) is the intended behavior.

### Missing values
Test SAS `.` and special missing values separately from R's `NA`/`NaN`. Confirm sort order and arithmetic behavior for missing values match expectations (R's `NA` propagates differently than SAS missing in some aggregate functions).

### Dates
Test `INTCK`, `INTNX`, `YRDIF`, month-end dates, leap years, interval alignment, and any business-calendar logic against `lubridate`/base R equivalents.

### Numeric precision
Test currency and other calculations with representative edge cases. SAS numeric variables are generally stored as 8-byte floating-point, so do not infer fixed-point storage from a SAS `FORMAT`. R also uses double-precision numeric values by default. Where exact decimal arithmetic is a business requirement, choose an explicit representation and validation strategy.

### Character variables
Check SAS variable lengths, blank padding, truncation behavior, and conversion between numeric and character types -- R does not enforce fixed-width character storage the way SAS does.

### Formats
Confirm that a SAS format used for presentation is not accidentally treated as a data transformation. In R, keep display formatting (via `format()`/`scales`) separate from the underlying stored value, mirroring the SAS `FORMAT` vs. data distinction.

### Duplicate handling
Do not assume `NODUPKEY`, `unique()`, and `distinct()` mean the same thing. Define which duplicate should survive (first, last, or based on a tiebreak rule) and implement that rule explicitly.

### Multiple-output DATA steps
SAS can send different rows to different output datasets during one DATA-step iteration. Recreate that routing explicitly with separate filtering/subsetting steps in R.

### Factors vs. character vectors
R's `factor` type has no direct SAS analogue and can silently reorder levels, coerce unexpected values to `NA`, or change behavior in modeling functions. Decide deliberately when a SAS classification/coded variable should become an R factor versus stay a plain character/numeric column.

---

# 15. DuckDB + R Ecosystem | Which/When?

### DuckDB / SQL

- the workload is primarily relational or SQL-heavy;
- joins, aggregations, filters, window functions, and set operations dominate;
- CSV or Parquet data is larger than is possible to load into R;
- you want persistent local analytical tables without operating a separate database server;
- the same intermediate data will be queried repeatedly;
- you want SQL to remain close to the original `PROC SQL` implementation.

### dplyr / dbplyr

- transformations can be expressed relationally and translated cleanly to SQL;
- the team wants R syntax while DuckDB performs the heavy execution;
- you want the same conceptual code to work across DuckDB and other DBI-compatible backends.

### data.table

- performance and memory efficiency matter for large in-memory datasets;
- you are replicating SAS BY-group, keyed-lookup, or in-place update patterns;
- the logic is procedural or stateful rather than naturally relational;
- your team is comfortable with `DT[i, j, by]` syntax.

### base R

- the task is small, one-off, or exploratory;
- you want minimal dependencies;
- you need general-purpose control flow or sequential state;
- the logic is easier to express procedurally than as SQL.

### Specialized R ecosystem

When doing things DUCKDB cannot:

- statistical modeling: `stats`, `lme4`, `survival`, `survey`, etc.;
- time series: `fable` and related packages;
- machine learning: `tidymodels`, `ranger`, `xgboost`, and others;
- visualization: `ggplot2`;
- reporting: Quarto, `gt`, `flextable`, `officer`;
- reproducible environments: `renv`;
- pipelines: `targets`;
- columnar data interchange: `arrow`.

### Combined ?

```text
SQL-heavy
sources → DuckDB → R ecosystem

DataFrame-heavy
sources → data.table → R ecosystem
```

```text
                SAS workload
                     │
          ┌──────────┴──────────┐
          │ classify each step  │
          └──────────┬──────────┘
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   relational     stateful      statistical
       │             │             │
 DuckDB/SQL     R/data.table    R packages
       │             │             │
       └─────────────┼─────────────┘
                     │
             R analysis layer
                     │
        Quarto / reporting / APIs
                     │
          targets / orchestration
```

Goal isn't DuckDB or R reproduce every SAS subsystem. It is use each workload to the layer that best preserves its semantics, performance, and operational requirements.

# 16. Migration Notes

### Precision

R's native numeric type is IEEE 754 double-precision floating point, the same general concern as in most modern languages. Use packages such as `Rmpfr` or careful integer-cent representations for monetary values where exact decimal arithmetic is required, and *avoid silently* introducing floating-point rounding during downstream processing.

### Scale

Many large tabular workloads can run effectively on a single machine using `data.table`, especially for datasets in the tens of millions of rows. For workloads that exceed available RAM, use DuckDB and/or Arrow to keep data in columnar/on-disk form and query it from R through `DBI`/`dbplyr`.
Benachmark. Benchmark. Benchmark.

### Reproducibility and auditability

Base R, data.table, and the tidyverse do not provide the same built-in governance model as a large SAS installation.

Pair layers with version-controlled code, `renv` for reproducible package environments, explicit schemas/validation (e.g., `pointblank`), lineage/versioning tools, and an orchestration system (e.g., `targets`) appropriate to the environment.

### Reusable functions vs. the SAS macro language

Ordinary R functions and packages are usually a cleaner replacement for SAS macros than trying to reproduce macro-style text substitution. Reserve `rlang`/tidy-eval metaprogramming for the cases where a macro was truly generating code dynamically, not for ordinary parameterized logic.

### Reconciliation testing

For regulated material workloads, migration should be treated as a **behavioral equivalence exercise**, not simply a code conversion.

Useful validation layers include:

1. Row counts
2. Distinct-key counts
3. Null/missing-value counts
4. Numeric aggregates
5. Distributional checks
6. Record-level reconciliation
7. Duplicate checks
8. Boundary/date checks
9. Statistical-model validation
10. cell-wise accuray for perfect exexcution

---

# 17. Practical Migration Strategy

For a real SAS-to-R migration, use this sequence:

```text
1. Inventory SAS programs
        ↓
2. Classify each step
   ├─ SQL / relational
   ├─ DATA step / stateful
   ├─ statistical / ML
   ├─ reporting / ODS
   └─ orchestration / macro
        ↓
3. Choose implementation
   ├─ DuckDB / SQL for relational workloads
   ├─ dplyr / dbplyr for readable SQL-backed transformations
   ├─ data.table for high-performance/stateful in-memory logic
   ├─ base R for procedural logic
   ├─ R statistical/ML packages
   └─ orchestration/reporting tools (targets, Quarto)
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

The goal is not to translate SAS syntax mechanically. The goal is to reproduce the **data contract, business logic, outputs, and operational behavior** using a layered DuckDB + R architecture: SQL where the workload is relational, R where procedural or statistical semantics matter, and explicit validation at the boundaries.
