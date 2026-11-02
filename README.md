# SASchi-Roku

The SAS toolkit shelf: reference programs, migration skills, and an indexed map
of the tools and lessons gathered across the SASchi projects.

Status: toolkit foundation for maintainer review. The preserved corpus is
community probe material. The skills are initial workflow guidance, not a
universal converter or a claim of live-SAS equivalence. MCP is planned.

## Start here

| Need | Entry point |
|---|---|
| Read the existing 56 Rosetta Code SAS programs | [Preserved reference collection](references/rosetta-code/README.md) |
| Assess a SAS program before migration | [SAS program assessment](skills/sas-assess/SKILL.md) |
| Translate a bounded program to Python or R | [Translation with evidence](skills/sas-translate/SKILL.md) |
| Move SAS datasets into Parquet | [Dataset interchange](skills/sas-to-parquet/SKILL.md) |
| Find repositories and already gathered material | [Resource catalog](catalog/README.md) |
| See the build sequence and future MCP work | [Roadmap](docs/ROADMAP.md) |

## Repository shape

| Path | Owns |
|---|---|
| `references/rosetta-code/` | SAS files, task indexes, collection documentation and attribution |
| `skills/` | Individually usable agent workflow instructions and focused references |
| `catalog/resources.json` | Source-backed resource records; generates `catalog/README.md` |
| `docs/` | Scope decision, migration receipt and roadmap |
| `tools/` and `scripts/` | Harvesting and repository checks |
| `JOURNAL.md` | Current session handoff |

The old `corpus/`, `TASKS.csv`, and `TASKS.md` paths are compatibility symlinks.
They resolve to the nested collection, including for existing SASchi-Go checks.
Use the nested paths for new integrations. Checkouts without symlink support
should use those paths directly.

## Skills

Each folder under `skills/` is a self-contained skill. Read or explicitly invoke
its `SKILL.md` in a compatible agent, or install that folder through the agent's
normal skill installation mechanism. A clone alone does not install skills.
The skills link to pinned source material and state what evidence a result needs.
They do not install a translator, SAS runtime, or Parquet library.

Program translation and dataset interchange are separate jobs. Python and R are
execution targets; Parquet is a storage format. A readable output table does not
by itself prove that the program or its metadata survived conversion.

## Check and maintain

Run from the repository root:

```sh
python3 scripts/inertia-drift-lint .
python3 scripts/check_corpus_index.py
python3 scripts/check_toolkit.py
python3 -m unittest discover -s tests -v
```

CI also validates `agent-manifest.json` against its existing JSON schema.
These checks cover repository integrity, not execution of the SAS corpus.
The [contribution guide](CONTRIBUTING.md) explains catalog regeneration and
upstream refresh. No upstream refresh is needed for a directory move.

## The family

[SASchi-Go](https://github.com/buntas-tofu/SASchi-Go) owns executable translation
and semantic gates. [SASchi-Garage](https://github.com/buntas-tofu/SASchi-Garage)
owns its authored field guide and research. Roku brings references, workflows,
and discovery together without duplicating those implementation sources.

The professional lane has [sas-campaign](https://github.com/the-pgh-cid/sas-campaign),
[sas-ref](https://github.com/the-pgh-cid/sas-ref), and the collected
[training modules](https://github.com/the-pgh-cid/sas-training-modules).
Catalog records identify the inspected commits. Shared ancestry does not imply
matching versions, gates, or results.

## Governance and provenance

The [scope decision](docs/decisions/0001-toolkit-scope.md) records the principal's
2026-11-01 direction. [AGENTS.md](AGENTS.md) retains the DMF GLOBAL contract.
[The relocation receipt](docs/migrations/2026-11-01-reference-move.json) records
60 matching byte comparisons: 56 SAS files, two indexes, LICENSE and NOTICE.
Collection navigation was adapted separately.

The existing [GFDL 1.2 license](LICENSE) and
[attribution notice](references/rosetta-code/NOTICE.md) remain in place.
Linked repositories retain their own terms. Inclusion in the catalog is not
permission to copy their contents or a claim that their code has been tested.
