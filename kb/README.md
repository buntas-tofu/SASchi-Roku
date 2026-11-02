# sas-kb

The SAS migration field guide: semantics, landmines, and evidence.

Status: candidate engineering reference, not an agency finding or proof of
cross-language equivalence. The examples and proposed tests have not been newly
executed against SAS as part of this collection.

sas-campaign and SASchi-Roku hold the implementations; sas-kb holds the research notes.

## Start here

| Collection | Cards | What it covers |
|---|---:|---|
| [Macro landmines](landmines/macro-landmines/README.md) | 12 | Timing, scope, quoting, rescanning, and generated code |
| [LLM migration quirks](landmines/llm-migration-quirks/README.md) | 12 | Invented APIs, incomplete conversions, evidence mistakes, and evaluation design |
| [SAS conversion landmines](landmines/sas-conversion-landmines/README.md) | 25 | Row counts, DATA step state, metadata, statistics, and engine contracts |

Read the [SAS research synthesis](research/SAS_REBUILD_RESEARCH_20260915.md),
[LLM evidence review](research/LLM_MIGRATION_QUIRKS_20260915.md), or
[25 proposed validation cases](research/SAS_FIXTURE_QUEUE_20260915.csv).
The [research source register](research/SOURCES_20260915.json) records 43 sources;
the macro collection has its own [source register](landmines/macro-landmines/SOURCES.md).

## The family

- [SASchi-Go](https://github.com/buntas-tofu/SASchi-Go) owns the translator,
  executable semantic rules, fixtures, and verification receipts.
- this repository (SASchi-Roku) preserves the community
  SAS program corpus and its upstream provenance.
- **sas-kb** owns the authored teaching cards, research, citations, and
  proposed tests. AWS packaging and deployment remain in a separate consumer.

A research card can describe a known behavior before Go supports it. A citation
is not an execution receipt. Stable IDs (ML-001, LQ-001, SL-001) connect research
to implementation without duplicating either repository's source of truth.

## Consume and check

`collections.json` lists all 49 cards, their source references, and evidence
metadata without coupling them to a retrieval provider. Use the explicit lists;
do not recursively ingest the repository. Research and proposed test answers
are not held-out evaluation material.

```sh
python3 tools/check_catalog.py
```

The validator uses Python 3.11+ and the standard library. It checks inventory,
IDs, evidence metadata, local links, and import records. It does not execute SAS
or certify the factual accuracy of a cited claim.

Pin a full Git commit when building a retrieval corpus. Keep each card whole and
preserve its status and references. All current cards are asserted/unreviewed.
Promotion requires independent review and appropriately scoped runtime evidence.

## Contributing and provenance

Add a named mechanism, a scoped source, an observable failure, and a proposed
witness. Distinguish documented contracts, local observations, and inference.
Keep raw internal records, credentials, deployment configuration, and held-out
answers outside this repository.

[PROVENANCE.md](PROVENANCE.md) explains the initial extraction and
[IMPORT_MANIFEST.json](IMPORT_MANIFEST.json) records the original file hashes.
[NOTICE.md](NOTICE.md) states the current rights boundary.
