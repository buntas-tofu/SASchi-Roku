# Julia reference for SASchi-Roku

Status: candidate reference dated 2026-11-04. No Julia runtime, SAS-to-Julia execution, enterprise package approval or universal translation capability is claimed.

Julia is a distinct programming language with multiple dispatch, specialized numerical code and a package ecosystem for tables and statistical models. It deserves its own reference, not a fifth entry in a Python-only library index.

| Need | Reference |
|---|---|
| Language and numerical semantics | [language.md](language.md) |
| Tabular, native SAS reader and statistical ecosystem | [ecosystem.md](ecosystem.md) |
| Approved environment and package pinning | [environment.md](environment.md) |
| SAS dataset interchange and metadata | [interchange.md](interchange.md) |
| Machine capability inventory | [capabilities.json](capabilities.json) |
| Risks and evaluation tasks | [RISKS.json](RISKS.json), [TASKS.json](TASKS.json) |
| Existing independent synthetic fixture | [fixture.md](fixture.md) |
| SAS-to-Julia migration considerations | [separate migration guide](../../docs/targets/sas-to-julia.md) |

[INDEX.json](INDEX.json) and [SOURCES.json](SOURCES.json) provide stable machine navigation and official upstream sources. The upstream site lists stable Julia 1.13.3 and LTS 1.10.13 as of review; actual enterprise versions are unknown.

## The authority boundary

Julia dependency facts live here. SAS source behavior remains in the preserved corpus, stamped KB, existing skills and independent trials. The public discovery catalog already holds a source-inspected ReadStatTables.jl record. It is not a successful import/export result.

No installed package, source-SAS execution, original executable software, new CI gate, source KB edit or MCP tool is introduced by this documentation landing. Standalone software licensing remains a separate decision.
