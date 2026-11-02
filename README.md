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
| Trace includes, macro selection and capture evidence | [Dependency inventory](skills/sas-trace-dependencies/SKILL.md) |
| Define byte, character and metadata preservation | [Interchange contracts](skills/sas-define-interchange/SKILL.md) |
| Diagnose conditional queues and retained state | [Stateful failure diagnosis](skills/sas-diagnose-state/SKILL.md) |
| Find repositories and already gathered material | [Resource catalog](catalog/README.md) |
| See the build sequence and future MCP work | [Roadmap](docs/ROADMAP.md) |
| Review staged tests and starter observations | [Test plan](docs/TEST_PLAN.md), [starter results](trials/starter-batch/README.md) |

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

The [first translation trial](trials/sas-translate-sum-array/README.md) records
one isolated skill invocation, the unchanged-source Python candidate, an
independent oracle and seven rejected negative controls. It is a bounded example,
not a general skill validation. CI replays its archived candidate.

The [eight-task starter batch](trials/starter-batch/README.md) records four static
assessments and LENGTH/LAG conversions in Python and native R. Its 32 runtime
checks and 10 rejected controls are bounded evidence; an explicit character-byte
domain gap remains. Full-domain and live-SAS acceptance are not claimed.

The [three follow-on evaluations](trials/skill-proposals/README.md) add dependency
inventory, character/metadata contracts and stateful diagnosis skills. Seven
dependency review criteria and 35 independent replay checks passed. Conditional
LAG repairs ran in Python and native R; the CSV witness preserves raw fallback
bytes and missing tags. Actual macro capture, SAS-binary reading and Parquet
round trips remain unperformed. All six skills retain initial-guidance status.

The [filter-timing trial](trials/state-filter-timing/README.md) extends state
diagnosis to WHERE versus subsetting IF. One fresh paired Python/R delivery passes
31 parent checks, including the reproduced original failure and six rejected
controls. The two outputs have identical row counts but different queue values
and totals. The skill instructions remain unchanged.

The [group, merge and width batch](trials/state-boundaries/README.md) adds 89
parent checks across Python and native R, plus 12 artifact-review criteria.
Three fresh paired deliveries cover nested group flags and queue state, duplicate
and missing-key match merges, and physical character widths through two DATA
steps and reopened CSV. First deliveries and frozen expectations are preserved.
The six skill instructions remain unchanged; live-SAS validation is pending.

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
python3 trials/sas-translate-sum-array/verify.py
```

With native Rscript available, also run `python3 trials/starter-batch/verify.py`,
`python3 trials/skill-proposals/verify.py`,
`python3 trials/state-filter-timing/verify.py` and
`python3 trials/state-boundaries/verify.py`.

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
