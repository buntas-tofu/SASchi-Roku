# 0004: Separate Python dependency references from SAS sources

Status: principal-confirmed direction, proposed implementation for maintainer review, 2026-11-03.

The principal affirmed that SAS content and dependency documentation must remain separate, then authorized integration of Faker, NumPy, Polars and DuckDB references.

Implementation: add `references/python-libraries/` for independent API cards, machine-readable inventories, official source links and a frozen synthetic fixture. Keep preserved `references/rosetta-code/`, `kb/` stamps and conversion guides, `catalog/resources.json` external discovery records, existing trials, CI gates and MCP interfaces unchanged.

No executable original Python software is included while the repository's separate software licensing decision remains unresolved. No live-SAS or enterprise package execution is claimed. Hosted governance tests belong to the resulting PR.
