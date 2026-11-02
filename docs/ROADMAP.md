# Toolkit roadmap

Status: engineering proposal implementing the principal's toolkit direction.
Maintainers may use this sequence for planning. It is not a delivery commitment
or a claim that the future capabilities already exist.

## 1. Foundation

Preserve the reference under a dedicated folder, retain compatibility paths,
record byte equality, and update governance. Seed the catalog from the gathered
sources, including the 22-repository Campaign census, sas-ref consolidation,
training modules, Go and Garage. Ship three initial skill entry points.

Completion requires passing repository checks and a reviewable change. The skill
instructions remain initial guidance until realistic use establishes their value.

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

Resolve the collected `sas_migration` scaffold's upstream and rights before any
import. Review useful entries individually, recording a commit, relevant surface,
license evidence, local trial and last review date. Preserve unreviewed entries
as discovery leads. Do not infer current file counts from the September census.

Link training at its original commit and at its sas-ref consolidation location.
Keep those as two locations of one resource, not two independent bodies of proof.
Avoid importing the real-world program archive into the persona repository as a
side effect of indexing it.

## 4. Build the MCP interface

Candidate first surface: search catalog records, retrieve a reference with its
provenance, look up a semantic rule, and report the scope of a verification
receipt. Stable resource IDs and explicit evidence fields can serve this layer.

Before implementation, choose transport, deployment, authentication and the
allowed data boundary. Start with read-only retrieval. Execution or conversion
tools need bounded inputs, dependency discovery, output isolation, cancellation
and refusal behavior, plus tests against the same contracts used outside MCP.
An MCP response must preserve source revision and evidence status.

The server should call shared tooling rather than invent a second translator.
SASchi-Go remains the implementation home for its supported execution surface.
Do not describe a skill instruction as an MCP tool or a planned tool as installed.

## Decisions for later

- License for new original executable tooling before a software release.
- Whether additional collected materials should be linked or imported, item by item.
- Which live-SAS task will provide the first captured reference execution.
- MCP deployment environment and whether it will ever execute user programs.
