# Toolkit roadmap

Status: engineering proposal implementing the principal's toolkit direction.
Maintainers may use this sequence for planning. It is not a delivery commitment
or a claim that the future capabilities already exist.

## 1. Foundation

Preserve the reference under a dedicated folder, retain compatibility paths,
record byte equality, and update governance. Seed the catalog from the gathered
sources, including the 22-repository Campaign census, sas-ref consolidation,
training modules, Go and Garage. Ship three initial skill entry points.

The foundation and reference-home layers have landed. The existing skill
instructions remain initial guidance; bounded trials record their observed
behavior without establishing general conversion reliability.

## 2. Prove the first workflows

The [first translation trial](../trials/sas-translate-sum-array/README.md) is
recorded: one complete source, one isolated generation, passing Python replay and
seven rejected negative controls. It preserves an unassigned missing value rather
than inventing the product suggested by the source title. This is an initial
observation; the broader workflow sequence below remains open.

The principal accepted the [phased evaluation plan](TEST_PLAN.md), starting with
four assessments plus LENGTH and unconditional LAG in Python and R. Review that
eight-task starter's [results](../trials/starter-batch/README.md), then the
[three accepted follow-on evaluations](../trials/skill-proposals/README.md).
The latter add dependency inventory, interchange contracts and stateful failure
diagnosis as separate initial skills. Seven dependency review criteria and
35 replay checks passed. Actual macro capture, SAS-binary/Parquet round trips,
and the remaining phases are still open.

The [state-filtering follow-up](../trials/state-filter-timing/README.md) now adds
WHERE/subsetting-IF timing with 31 parent checks and native Python/R execution.
This exercises the existing state skill; it does not add another overlapping
skill or establish live-SAS equivalence.

The [group, merge and width batch](../trials/state-boundaries/README.md) adds 89
bounded parent checks. The primary [dual-path interchange trial](../trials/parquet-dual-path/README.md)
records 56 checks over archival and analytical projections, selected SAS files,
and complete Python/R consumers. Its reader and live-SAS limitations remain explicit.

The supplemental [decoded Parquet trial](../trials/parquet-metadata/README.md)
exercises typed Parquet, exact byte/tag witnesses and a separate base R bridge.
Its first delivery has an observed CLI abort; a separate repaired attempt passes
68 checks. Frozen inputs, original deliveries, harness corrections and candidate
repairs stay distinct across both trials. Their counts are not a pooled score or
a controlled comparison of tools. Broader reader coverage and live SAS remain open.

Start with small examples whose behavior can be observed. Suggested order is
engineering judgment, not a measured ranking:

| Workflow | Trial | Acceptance |
|---|---|---|
| Assess a SAS program | Inputs, outputs, macros and state in a known example | Traceable inventory; unknown dependencies remain visible |
| Translate to Python or R | One bounded construct, then a composed program | Independent expected results, scoped comparisons, negative control |
| SAS dataset to Parquet | Numeric, text, date, label and special-missing cases | Reopened typed values and metadata checked against a declared policy |
| Explain a migration failure | Garage landmine plus a minimal witness | The failure is reproduced and the correction passes the same check |
| Teach with prompts | One training module, clean A/B attempts | Original responses and execution recorded separately; no leaked answers |

Keep program conversion separate from file conversion. Add SQL, DuckDB, Polars,
macro analysis and statistical-procedure workflows when actual requests justify
their own skill boundaries. A router can follow if discovery becomes difficult.

## 3. Grow a maintained catalog

Public catalog PR 6 added nine pinned resources on 2026-11-02, bringing the catalog
to 39 records. Its README inspections are discovery evidence, not executed
conversion results. Further additions should fill a demonstrated gap in the
existing catalog rather than create a parallel collection.

Resolve the collected `sas_migration` scaffold's upstream and rights before any
import. Review useful entries individually, recording a commit, relevant surface,
license evidence, local trial and last review date. Preserve unreviewed entries
as discovery leads. Do not infer current file counts from the September census.

Link training at its original commit and at its sas-ref consolidation location.
Keep those as two locations of one resource, not two independent bodies of proof.
Avoid importing the real-world program archive into the persona repository as a
side effect of indexing it.

## 4. Exercise the existing MCP interface

The advisory [MCP subproject](../mcp/README.md) landed with the reference-home
layers on 2026-11-02. Its current surface exposes knowledge lookup, reference
retrieval and workflow prompts, with a direct and in-memory protocol self-test
in governance. It is no longer an unimplemented roadmap item.

The next evaluation boundary is exact, ambiguous, stale, missing and conflicting
retrieval, hostile instruction-shaped content and tool failures. Provenance and
uncertainty must survive retrieval. The current self-test establishes its recorded
surface only; it does not establish every adversarial retrieval case.

Any future execution or conversion tools need a separate data boundary, bounded
inputs, dependency discovery, output isolation, cancellation and refusal behavior.
SASchi-Go remains the implementation home for its supported execution surface.

## Decisions for later

- License for new original executable tooling before a software release.
- Whether additional collected materials should be linked or imported, item by item.
- Which live-SAS task will provide the first captured reference execution.
- MCP deployment environment and whether it will ever execute user programs.
