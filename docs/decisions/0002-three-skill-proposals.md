---
title: Three follow-on skill proposals
status: accepted
---

# Three follow-on skill proposals

Status: principal-authorized scope recorded 2026-11-02. Maintainers may develop
and test these three workflows. This is not a release or proof of SAS equivalence.

The principal approved dependency and macro expansion inventory, character and
metadata interchange contracts, and stateful conversion failure diagnosis. The
principal also confirmed that no live SAS runtime is currently available.

Implementation choices, labeled engineering decisions:

- Add three individually scoped skills with focused references, retaining the
  existing assessment, translation and Parquet entry points.
- Test each new skill with a fresh independent task. Dependency analysis uses a
  transitive include package, competing macro source and explicitly synthetic
  expansion evidence. It must not promote that evidence to actual SAS capture.
- Character/metadata tests use a synthetic decoded source envelope and an
  executable CSV-plus-metadata witness. They do not claim SAS-binary reading or
  Parquet support. Preserve NUL and undecodable bytes through an explicit raw
  representation rather than narrowing the prior frozen starter request.
- State diagnosis uses conditional queues, retained accumulation, explicit output
  and two DATA steps. A failing Python candidate and hand-derived expected values
  support Python and native R repairs; one evaluator supplies both target repairs.
- Freeze inputs, skill bytes, parent rubric and expectations before generation.
  Preserve first deliveries and original failures. Review actual artifacts and
  execute candidates independently. Later fixes remain separate attempts.

Actual SAS-generated source capture stays pending until a runtime is available.
Prepare its procedure and required provenance now; do not create a synthetic
receipt that says SAS executed. Cloud onboarding is a separate workstream requested
later by the principal, not an evaluation result or a prerequisite for completing
these local trials. No account specifics or credentials belong in this public
package. Raw archive use, skill installation and MCP implementation are outside
this evaluation scope.

See [the evaluation contract](../../trials/skill-proposals/CONTRACT.md).
