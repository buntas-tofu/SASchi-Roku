# SAS to Julia: candidate migration considerations

Status: source-linked planning guidance dated 2026-11-04. No SAS-to-Julia conversion has been executed or validated here. This is not a general conversion recipe, a supported target announcement, or a replacement for the existing SAS rulebook.

## Why Julia is worth considering

Julia permits direct, explicitly typed numerical loops as well as DataFrames operations, and offers packages for basic statistics and model fitting. It is a plausible additional target for bounded scientific, numerical and data-processing SAS programs when the runtime and required packages are approved. But **behavioral equivalence comes before tool choice**.

## Source constructs and candidate Julia mechanisms

| SAS behavior | Julia candidate | Critical acceptance distinction |
|---|---|---|
| DATA step and SET | Julia loops and DataFrames | Iteration, retained variables, implicit state and output timing |
| RETAIN, sum statements, LAG | Explicit state/queue, possibly verified group functions | LAG queue is not merely previous row |
| FIRST.var and LAST.var | Sort plus explicit group-boundary tests | Nested BY order and flags |
| WHERE vs subsetting IF | Pre-filter vs post-state row decision | State can differ even when output row count matches |
| MERGE [inputs] BY key | Explicit match-merge or relational join only if correct | Duplicate keys, exhausted inputs, missing overwrites |
| PROC SORT/NODUPKEY | Sort, unique with specified key policy | Tie precedence, ordering and rows dropped |
| PROC SQL | DataFrames join/groupby or an approved Julia SQL library | Missing join keys, cardinality, nulls, output order |
| PROC MEANS/SUMMARY | Statistics and grouped reductions | Missing counts, sample SD, weights, denominators |
| PROC REG/GLM/LOGISTIC | StatsModels and GLM | Categorical contrasts, likelihood/link, inferential outputs |
| PROC MIXED | MixedModels | Optimizer, ML/REML, covariance and degrees of freedom |
| LENGTH, SUBSTR | Unicode string/code-unit handling | SAS fixed byte widths, padding and encoding |
| SAS DATE/DATETIME and interval functions | Dates, explicit epoch mapping | Origin 1960-01-01, month-end, timezone and precision |
| Macro and INCLUDE | Dependency inventory before using Julia functions | Code-generation phases and unresolved source dependencies |
| SAS7BDAT/XPT files | ReadStatTables and an archive+metadata sidecar | Special missing tags and value labels are not fully preserved |

## Five high-priority traps

**Missing values.** Julia's `missing` is not SAS's whole missing-value system. ReadStatTables currently collapses distinct special missings and does not offer complete SAS value-label read support. A direct round-trip is therefore not proven lossless. Archive the original file and retain per-cell metadata for tags.

**DATA-step state.** Conditional LAG calls, RETAIN, BY group boundaries and WHERE/IF sequencing must be modeled at the correct stage. A vector shift that yields matching row counts can still be wrong. Use Roku's frozen state tests as candidate evaluation cases.

**Match merge and joins.** SAS BY match merge is a sequential operation, particularly when keys repeat. DataFrames join semantics are relational and missing join keys raise by default unless `matchmissing` is configured. Never assume the two operations are equal.

**Dates and text.** Julia has native dates and Unicode strings, but SAS origin, numeric storage, declared character byte lengths, truncation and formats still require independent preservation rules.

**Inference.** Regression or mixed-model execution is not proof of PROC-level equivalence. Compare model matrix, coding/reference levels, weights, optimization, standard errors, degrees of freedom, test statistics and output definitions.

## First bounded evaluation

Reuse Roku's [frozen relational fixture](../../references/python-libraries/fixtures/expected.json), with five customers, eight orders, a leading-zero key, an unmatched customer, two missing cents, a true zero, a negative adjustment and an all-missing group. Require Julia to reproduce independently expected rows, grouping, exact total 4350 cents, all-null group as `missing`, and rejection of bad controls.

Once a Julia environment is authorized, the second phase should target [state timing](../../trials/state-filter-timing/README.md), [merge/width](../../trials/state-boundaries/README.md), and [archival/analytical interchange](../../trials/parquet-dual-path/README.md). These trials are sources of frozen cases, **not** prior Julia evidence.

## Accepted workflow for a new trial

1. Record SAS program, macro/include context, inputs, expected output and ordering.
2. Identify a documented Julia API or mark `no verified equivalent`; do not guess through unsupported procedure gaps.
3. Record approved Julia runtime, package versions, Project/Manifest, input hashes and intended metadata losses.
4. Freeze an independent oracle before producing a Julia candidate; do not leak expected responses into generation packets.
5. Run candidate code under the approved environment, saving first delivery, failures, outputs and precise commands.
6. Test values, state, types, nulls, order, inference and deliberately wrong controls.
7. Hand off source/target artifacts and limits to the existing acceptance gates; never certify from matching method names.

The [crosswalk JSON](sas-to-julia-crosswalk.json) lists the candidate cases. [Julia language reference](../../references/julia/README.md) owns dependency details; SAS semantics and acceptance remain with the existing Roku KB and SASchi-Go.
