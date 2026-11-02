# Resource catalog

Status: Discovery catalog for maintainer use; reference inspection is not runtime validation or a redistribution grant.

Generated from [resources.json](resources.json). Edit that file, then run
`python3 scripts/check_toolkit.py --write-index` from the repository root.

39 resources. Source/lookup review date: 2026-11-02.

September census counts describe the original testbed, not today's upstream.
GitHub license identifiers are dated API observations, not per-file rights
reviews. Unknown identifiers and upstream origins remain explicit.

## analysis

| Resource | Use | Evidence |
|---|---|---|
| [mishamsk/sas-lexer](https://github.com/mishamsk/sas-lexer) | Static SAS lexer with a Rust core and Python bindings; useful for source inventories with documented contextual limitations. | source-inspected; [source](https://github.com/mishamsk/sas-lexer/blob/7cd39aba21776f4ebbaa2689707e0c45f6097dce/README.md); license ID: AGPL-3.0 |

## comparison

| Resource | Use | Evidence |
|---|---|---|
| [PSIAIMS/CAMIS](https://github.com/PSIAIMS/CAMIS) | Cross-software statistical comparison reference identified in Garage research. | source-inspected; [source](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/research/SOURCES_20260915.json) |
| [ceyson/polars_proc_compare](https://github.com/ceyson/polars_proc_compare) | Polars implementation of SAS PROC COMPARE-style structural and value reports, including missing-value comparisons. | source-inspected; [source](https://github.com/ceyson/polars_proc_compare/blob/1f72b6150ddb2389541f2ee16ef7bd2a767292c8/README.md); license ID: MIT |
| [kulbshar/proccompy](https://github.com/kulbshar/proccompy) | Python dataframe comparator modeled on SAS PROC COMPARE, with per-column tolerances and SAS-style text listings. | source-inspected; [source](https://github.com/kulbshar/proccompy/blob/d56c006daeeffa379e391505914f3d8545837375/README.md); license ID: Apache-2.0 |

## dataframe

| Resource | Use | Evidence |
|---|---|---|
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | Python data analysis toolkit referenced by the gathered migration research. | source-inspected; [source](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/research/SOURCES_20260915.json) |

## family

| Resource | Use | Evidence |
|---|---|---|
| [buntas-tofu/SASchi-Garage](https://github.com/buntas-tofu/SASchi-Garage) | Authored teaching cards, migration landmines, research and evidence maps. | source-inspected; [source](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/README.md) |
| [buntas-tofu/SASchi-Go](https://github.com/buntas-tofu/SASchi-Go) | SAS translation implementation, bounded semantic profiles and verification gates. | source-inspected; [source](https://github.com/buntas-tofu/SASchi-Go/blob/34915047c03c72e4498d8ea540ee804b14038476/docs/OPERATIONS.md) |

## format

| Resource | Use | Evidence |
|---|---|---|
| [apache/parquet-format](https://github.com/apache/parquet-format) | Apache Parquet storage-format specification, identified in the gathered sas-ref vendor shelf. | source-inspected; [source](https://github.com/sas-ref/blob/9760721edf0c7fccae15b41a331a8cae904ec0e5/vendor/README.md); license ID: Apache-2.0 |
| [scarnecchia/sas2parquet](https://github.com/scarnecchia/sas2parquet) | R batch conversion project for SAS7BDAT to zstd-compressed Parquet using DuckDB read_stat and Arrow. | source-inspected; [source](https://github.com/scarnecchia/sas2parquet/blob/1b103d348e5f32a9c3bfb06a9680fe97c4838f01/README.md); license ID: unknown |

## interop

| Resource | Use | Evidence |
|---|---|---|
| [dylanmeysmans/duckdb-read-stat](https://github.com/dylanmeysmans/duckdb-read-stat) | DuckDB ReadStat community extension; README shows reads of SAS7BDAT and XPT files via read_stat. | source-inspected; [source](https://github.com/dylanmeysmans/duckdb-read-stat/blob/029c59b8514402dc4270dd6d9d3c9da9037a95fc/README.md); license ID: MIT |
| [tidyverse/haven](https://github.com/tidyverse/haven) | R statistical-file interchange, including SAS readers and metadata representations. | source-inspected; [source](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/research/SOURCES_20260915.json) |
| [alipatti/polars_io](https://github.com/alipatti/polars_io) | Lazy Polars SAS7BDAT/XPT reader using pyreadstat with documented predicate and projection pushdown. | source-inspected; [source](https://github.com/alipatti/polars_io/blob/83e7486ba563210aee4666229a3af916f000b277/README.md); license ID: unknown |
| [Roche/pyreadstat](https://github.com/Roche/pyreadstat) | Python ReadStat wrapper reading SAS datasets and catalogs into pandas or Polars frames with metadata support. | source-inspected; [source](https://github.com/Roche/pyreadstat/blob/e6e23bc0021875f35fccc3c2707c3e5151c130bb/README.md); license ID: NOASSERTION |
| [junyuan-chen/ReadStatTables.jl](https://github.com/junyuan-chen/ReadStatTables.jl) | Julia Tables.jl interface using ReadStat to read SAS7BDAT/XPT, with metadata, labels and date handling. | source-inspected; [source](https://github.com/junyuan-chen/ReadStatTables.jl/blob/9c07e788241d44be667b9690f593491827bf2a25/README.md); license ID: MIT |

## sas-testbed

| Resource | Use | Evidence |
|---|---|---|
| [atorus-research/atorus-sas-macros](https://github.com/atorus-research/atorus-sas-macros) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 31 SAS files at 2026-09-08; license ID: MIT |
| [Boemska/macrocore](https://github.com/Boemska/macrocore) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 76 SAS files at 2026-09-08; license ID: MIT |
| [CausalInference/GFORMULA-SAS](https://github.com/CausalInference/GFORMULA-SAS) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 11 SAS files at 2026-09-08; license ID: MIT |
| [cdisc-org/COSMoS](https://github.com/cdisc-org/COSMoS) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 31 SAS files at 2026-09-08; license ID: MIT |
| [danielegiardiello/Prediction_performance_survival](https://github.com/danielegiardiello/Prediction_performance_survival) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 6 SAS files at 2026-09-08; license ID: GPL-3.0 |
| [eleanormurray/CausalSurvivalAnalysisWorkshop](https://github.com/eleanormurray/CausalSurvivalAnalysisWorkshop) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 1 SAS files at 2026-09-08; license ID: unknown |
| [friendly/SAS-macros](https://github.com/friendly/SAS-macros) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 463 SAS files at 2026-09-08; license ID: unknown |
| [HHS-AHRQ/MEPS](https://github.com/HHS-AHRQ/MEPS) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 58 SAS files at 2026-09-08; license ID: unknown |
| [PaulSchmidtGit/Heritability](https://github.com/PaulSchmidtGit/Heritability) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 11 SAS files at 2026-09-08; license ID: unknown |
| [phuse-org/phuse-scripts](https://github.com/phuse-org/phuse-scripts) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 164 SAS files at 2026-09-08; license ID: MIT |
| [RhoInc/sas-statistical-data-checks](https://github.com/RhoInc/sas-statistical-data-checks) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 14 SAS files at 2026-09-08; license ID: MIT |
| [sascommunities/learning-sas-by-example-2nd](https://github.com/sascommunities/learning-sas-by-example-2nd) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 3 SAS files at 2026-09-08; license ID: Apache-2.0 |
| [sascommunities/sas-cert-prep-data](https://github.com/sascommunities/sas-cert-prep-data) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 8 SAS files at 2026-09-08; license ID: Apache-2.0 |
| [sascommunities/sas-global-forum-2019](https://github.com/sascommunities/sas-global-forum-2019) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 152 SAS files at 2026-09-08; license ID: Apache-2.0 |
| [sascommunities/sas-prog-for-r-users](https://github.com/sascommunities/sas-prog-for-r-users) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 83 SAS files at 2026-09-08; license ID: CC-BY-4.0 |
| [sasjs/core](https://github.com/sasjs/core) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 408 SAS files at 2026-09-08; license ID: MIT |
| [sassoftware/enlighten-apply](https://github.com/sassoftware/enlighten-apply) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 23 SAS files at 2026-09-08; license ID: Apache-2.0; archived at lookup |
| [sassoftware/sas-code-examples](https://github.com/sassoftware/sas-code-examples) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 51 SAS files at 2026-09-08; license ID: Apache-2.0 |
| [sassoftware/sas-iml-packages](https://github.com/sassoftware/sas-iml-packages) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 42 SAS files at 2026-09-08; license ID: Apache-2.0 |
| [sasutils/macros](https://github.com/sasutils/macros) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 49 SAS files at 2026-09-08; license ID: GPL-3.0 |
| [wyp1125/SAS-Clinical-Trials-Toolkit](https://github.com/wyp1125/SAS-Clinical-Trials-Toolkit) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 22 SAS files at 2026-09-08; license ID: GPL-3.0 |
| [yabwon/SAS_PACKAGES](https://github.com/yabwon/SAS_PACKAGES) | Repository included in the 2026-09-08 SAS macro testbed census. | repository-resolved; [source](https://github.com/sas-campaign/blob/4a32c5338d0225a117fb14fd016942385c780e06/docs/macro_surface_census.md); 48 SAS files at 2026-09-08; license ID: MIT |

## scaffold

| Resource | Use | Evidence |
|---|---|---|
| [sas_migration collected scaffold](https://github.com/sas-ref/blob/9760721edf0c7fccae15b41a331a8cae904ec0e5/vendor/README.md) | Collected migration starter kit with Python/R skill templates and DuckDB, Polars and R guides. | upstream-unresolved; [source](https://github.com/sas-ref/blob/9760721edf0c7fccae15b41a331a8cae904ec0e5/vendor/README.md) |

## training

| Resource | Use | Evidence |
|---|---|---|
| [Bayer-Group/sas2r](https://github.com/Bayer-Group/sas2r) | Clinical R programming recipe knowledge hub aimed at SAS users; not a direct SAS source-code converter. | source-inspected; [source](https://github.com/Bayer-Group/sas2r/blob/4f40c303584bc6ac366081529e53f492d3b28554/README.md); license ID: MIT |

## translation

| Resource | Use | Evidence |
|---|---|---|
| [CSOIreland/Code-Transcompiler-using-LLMs-public](https://github.com/CSOIreland/Code-Transcompiler-using-LLMs-public) | Statistical-agency LLM translation framework; README documents CSO use for SAS-to-R and configurable review iterations. | source-inspected; [source](https://github.com/CSOIreland/Code-Transcompiler-using-LLMs-public/blob/7c0ca2f605aab2e76346d33b286d9dd40ba8d749/README.md); license ID: MIT |

## Reading the record

Each JSON record carries a stable ID, tags, discovery source and revision,
additional locations, evidence limits and provenance notes. A source revision
pins the discovery record; it does not pretend to pin every external project.
The collected migration scaffold has no known upstream URL. The training
modules' original and consolidated locations are recorded as one resource.
