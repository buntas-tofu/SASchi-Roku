# Julia packages relevant to SAS migration

Status: source-linked selection, not installed-package inspection or parity proof.

| Candidate | Relevant role | Explicit limitation |
|---|---|---|
| Julia Base, Dates, Statistics | Typed arrays, dates, reductions | No automatic SAS formats, tagged missings or PROC semantics |
| DataFrames.jl | Select, transform, joins, groupby | DATA-step state and match merge differ from relational joins |
| CSV.jl | Delimited table ingest and output | Explicit string IDs, dates, encoding and missing policy required |
| Tables.jl | Shared table interface | Source SAS metadata is not guaranteed |
| ReadStatTables.jl | SAS .sas7bdat and .xpt reader | SAS value labels limited; distinct missing tags collapse; writer experimental |
| Arrow.jl | Typed columnar exchange | Does not preserve all SAS source bytes or metadata |
| StatsModels.jl | Formula and contrasts | Contrast coding and reference categories need explicit mapping |
| GLM.jl | Linear and generalized linear model fitting | PROC-specific estimates, SE and tests need independent validation |
| MixedModels.jl | Mixed-effects model fitting | Optimizers, covariance and inferential DF may differ from PROC MIXED |

The official ReadStatTables.jl guide documents `readstat`, `readstatallmeta` and `writestat`. It warns SAS might not read produced `.sas7bdat` files. Its overview also identifies incomplete SAS value-label reading and collapsed missing values. This is a potentially lossy reader, not a general-purpose SAS acceptance oracle.

DataFrames.jl joins reject missing keys by default unless `matchmissing` is configured. This is a distinct decision from the source semantics, especially when SAS BY groups use missing keys.

For each modeling procedure, compare design matrices, categorical coding, weights, likelihood/objective, link function, convergence, covariance specification, degrees of freedom and output confidence intervals. Julia packages with similar statistical names are *candidates*, not blessed translations.
