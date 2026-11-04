# Python library reference shelf

Status: candidate, source-linked dependency guidance dated 2026-11-03. Not a release, SAS-equivalence finding, or approved enterprise package inventory.

| Library | Entry | Role |
|---|---|---|
| Faker | [faker](faker/README.md) | synthetic test data |
| NumPy | [numpy](numpy/README.md) | typed arrays and numerical computation |
| Polars | [polars](polars/README.md) | typed eager and lazy dataframe transformations |
| DuckDB | [duckdb](duckdb/README.md) | embedded analytical SQL and Parquet access |

[INDEX.json](INDEX.json) is the machine entry point; [SOURCES.json](SOURCES.json) tracks official upstream URLs. Each library's `api.json` is a curated capability inventory. [TASKS.json](TASKS.json) and [RISKS.json](RISKS.json) support agents, while [docs/verification.md](docs/verification.md) and [fixtures](fixtures/README.md) establish a static independent oracle.

## Separate knowledge domains

- `references/rosetta-code/` contains preserved SAS source material.
- `kb/convert/` holds existing SAS conversion guides and stamped knowledge; do not duplicate or edit those sources here.
- SASchi-Go retains executable conversion and semantic gates.
- `catalog/resources.json` is the external discovery catalog. Our INDEX only inventories documents that belong to this shelf.
- No standalone executable Python programs, package installation, new CI jobs or MCP changes are part of this initial reference landing. Original software licensing remains a separate decision.

Start with [operating rules](OPERATING_BOUNDARIES.md), [managed environment](docs/environment.md) and [interoperability](docs/interoperability.md). The earlier standalone Faker and three-library reference kits provided candidate source material; only their documentation concepts and small static fixture are integrated.
