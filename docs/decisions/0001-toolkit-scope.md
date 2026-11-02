# 0001: SASchi-Roku becomes the SAS toolkit home

Status: principal direction recorded on 2026-11-01; implementation choices below
are labeled engineering decisions for maintainer review. This is a repository
scope record, not proof of conversion correctness.

## Confirmed direction

The principal requested that SASchi-Roku grow from a derived reference into a
toolkit repository. Preserve the existing content in a subfolder. Develop skills
for interaction with SAS and conversion to Python, R, Parquet and further targets,
using lessons from the SASchi projects. Add an indexed list of known repositories,
starting with the already gathered collection. An MCP build is a longer-term goal.
The principal identified `the-pgh-cid/sas-ref` as an existing collection and a
useful base of operations. Its separate reconfiguration remains in that lane.

This direction supersedes the former LOCAL data-corpus-only scope. The four DMF
invariants and the GLOBAL contract remain unchanged. Older sibling descriptions
of Roku as only a data repository describe the previous scope.

## Implementation decisions (engineering inference)

- `references/rosetta-code/` owns the existing corpus, indexes and attribution.
  Preserve every SAS file and both indexes byte for byte during relocation.
- Keep root `corpus/`, `TASKS.csv` and `TASKS.md` as compatibility symlinks for
  existing Go consumers. There is one physical copy of the collection.
- Keep the harvest and index-check commands at their existing paths; retarget
  their defaults to the nested collection. Do not refresh upstream during a move.
- `skills/` contains portable, individually usable workflow skills. Initial skills
  cover program assessment, evidence-based translation, and dataset interchange.
  Instructions are initial guidance, not a tested universal converter.
- `catalog/resources.json` is the source of the generated human index. Record
  source locations, evidence, review state and unresolved provenance explicitly.
  Link to the gathered materials; do not consolidate the sibling trees here.
- Keep current license files and GFDL declaration unchanged. A different license
  for future original software needs a separate explicit decision before release.
- MCP starts as a roadmap item. No service, tool registration or installed runtime
  is implied by this foundation.

## Acceptance

The existing index gate and manifest validation must still pass. Record SHA-256
preservation for the moved corpus and indexes. Exercise the relocated harvester
without contacting or modifying upstream. Check compatibility paths, catalog
structure and generated index consistency. Validate new skill metadata and links.
Run the unchanged invariant linter. A local check is not hosted CI or live SAS.

## Record

The source snapshot is `00b8b8879292309ef67d8351a05d333a0d66b9ae`.
The relocation inventory is [the migration record](../migrations/2026-11-01-reference-move.json).
The next-session entry point is [JOURNAL.md](../../JOURNAL.md).
