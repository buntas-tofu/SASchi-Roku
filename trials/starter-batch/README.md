---
title: Starter skill evaluation results
status: recorded
---

# Starter skill evaluation results

Status: bounded engineering observations for maintainer review, recorded
2026-11-01 local time (2026-11-02 UTC). Four static assessments passed parent
review; four delivered conversions passed 32 parent runtime checks. This is not
full-domain acceptance, live-SAS equivalence or a model reliability estimate.

## Result

| Task | Parent evidence | Result |
|---|---|---|
| A1, complete program | Input/output inventory, Python slice, unknown data, comparison scope | 5 rubric criteria pass |
| A2, absent include and macro | Unresolved expansion and effects remain unknown; bounded projection proposed | 5 rubric criteria pass |
| A3, excluded procedure | PROC GLM rejected under the supplied synthetic engine profile; no invented support | 5 rubric criteria pass |
| A4, source attached for Parquet | Source distinguished from data; dataset, metadata and mapping policy requested | 5 rubric criteria pass |
| LENGTH, Python | Main, edge, singleton and empty input through CLI and in-memory interface | 8 checks pass |
| LENGTH, native R | Same independent expected rows and interfaces | 8 checks pass; byte-domain gap remains |
| Unconditional LAG, Python | Same four shapes, missing queue inputs, fresh calls and nonmutation | 8 checks pass |
| Unconditional LAG, native R | Same independent expected rows and interfaces | 8 checks pass |

Python was CPython 3.12.3 and native R was 4.3.3 on Linux. Ten negative controls
were rejected: blank length zero, leading-space trim, tab trim, wrong storage
width, reordered rows, zero lag initialization, skipped missing queue inputs,
wrong lag direction, caller mutation and queue state leaking between calls.

The assessment decisions were reviewed against actual report text and source
hashes. Automated replay verifies their archived identity; it does not repeat a
semantic review of prose. Runtime checks execute saved conversion code against
hand-derived expectations. Agent self-tests and their additional counts are
retained separately and are not included in the 32 parent checks.

## What the process established

- Eight fresh agents received one task each, no parent conversation and no
  expected output, reference implementation or prior answer. They could inspect
  their packet and primary public documentation. Directory isolation was an
  instruction boundary, not a security boundary or proof of training novelty.
- Source, request, input, skill and parent oracle bytes were frozen before
  generation. First delivered outputs remain unchanged; self-checks before
  delivery were allowed. No parent feedback repair was needed.
- Each conversion was inspected and executed independently. The parent checked
  rows, order, schema, numeric missingness, exact text, caller preservation and
  fresh invocation state. Both CLI and in-memory interfaces were exercised.
- Receipt hashes bind the candidate files, oracle and verifier. Replaying this
  package reproduces target execution, not model generation. Model revision and
  sampling parameters were not exposed and remain null in the record.

## Findings and next skill directions

The request said ASCII without defining its full byte alphabet. The R LENGTH
candidate explicitly rejects NUL, which its character representation cannot
store. The supplied witnesses contain ordinary text, spaces and tabs, not NUL.
Their passing result does not close this request/interface mismatch. The frozen
request was not narrowed after seeing the result; full-domain signoff is false.

The R LENGTH delivery also includes a custom CSV parser to address character
transport. The parent inspected that code, but its broader transport claims are
outside this batch's frozen witnesses. Future tests should separate semantic
functions from independently validated input/output adapters and specify allowed
bytes, encoding and rejection behavior before generation.

The R agent preserved an initial extra self-test failure involving names on its
oracle vector, then corrected that self-test. Its original failure and final logs
remain in the archive. The parent oracle and comparison policy were unchanged.
This illustrates why evaluator failures, conversion failures and later repairs
need separate records.

Candidate skill directions, inferred from the observations and coverage gaps:

1. Dependency and macro expansion inventory, extending A2 to transitive includes,
   macro resolution and actual generated source.
2. Character and metadata interchange contracts, joining A4's metadata questions
   with the observed byte-domain and CSV boundary.
3. Stateful conversion failure diagnosis, moving from unconditional queues to
   conditional calls, retained values and composed DATA steps in a later phase.

These are proposals, not newly implemented skills. The existing instructions
remain initial guidance. This batch supplies no with/without-skill comparison,
so it cannot establish the skill's causal contribution. Review these findings
before expanding the [phased plan](../../docs/TEST_PLAN.md).

## Evidence and replay

- [Frozen contract and rubric](CONTRACT.md), [input/skill hashes](freeze.json),
  [independent expected rows](oracle.json).
- `packets/<task>/` preserves the exact inputs and skill snapshot.
- `candidates/<task>/` preserves each first delivery, including optional raw
  self-test artifacts; [delivery.json](delivery.json) binds their bytes and agent
  task names. Reports retain their original temporary paths and self-reported
  reproduction commands. They are raw evidence, not portable root commands.
- [Assessment review](assessment-review.json), [parent findings](findings.json),
  [parent execution receipt](receipt.json), and [replay verifier](verify.py).

From the repository root, with Python 3.11+ and native Rscript available:

```sh
python3 trials/starter-batch/verify.py
```

The verifier requires both runtimes and fails if either is unavailable; it does
not silently skip a target. It writes outputs only to a temporary directory.
Use `--receipt /path/to/new.json` to save a new execution receipt; existing files
are never overwritten. CI uses Python 3.12 and R 4.3.3 in a separate replay job.

For a raw agent self-test, reconstruct its original relative layout by copying
`packets/<task>/` to a scratch `packet/` and `candidates/<task>/` to a sibling
`output/`, then run the report's command from that scratch directory. Do not
replace the independent parent oracle with an agent self-test result.

## Provenance and limits

Sources and fixture rows are original synthetic examples inspired by the scoped
LENGTH and LAG teaching topics in sas-training-modules commit
`4be913210dcf3c1befc3367420c4ac9032bac39d`. No sibling implementation, expected
training CSV, raw archive program or dataset was imported. Skill snapshots come
from Roku `304a8ccd0a60cfefa73e4256f0b6fb571628ff12`. Primary SAS definitions are
linked in the contract. The synthetic engine profile is not a description of
SASchi-Go or a real product.

No SAS execution, conditional LAG, macro execution, statistical conversion,
Parquet writing, skill installation or MCP implementation occurred. Linter output
contains 11 documented status-frontmatter warnings: three existing skills plus
eight exact skill snapshots. Status is in supported skill metadata/body; the
shared linter and skill bytes are unchanged.
