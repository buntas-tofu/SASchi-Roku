# Three follow-on skill evaluations

Status: bounded engineering evidence for maintainer review, recorded 2026-11-02.
This is not a release, live-SAS equivalence claim or estimate of general skill
effectiveness. One fresh invocation per new skill produced the first deliveries.

## Results

| Task | Parent observation | Scope |
|---|---|---|
| Dependency inventory | All seven frozen review criteria passed | Transitive includes, conditional macro selection and provenance of synthetic emission |
| Character/metadata contract | All 12 replay checks passed | Two build/reopen/check cases, four refusal checks and six corruption controls |
| Stateful diagnosis | All 23 replay checks passed | 16 target/case/interface comparisons, reproduced original failure and six incorrect-output controls |

The 35 machine checks ran under CPython 3.12.3 and native R 4.3.3. All 12
corruption controls were rejected. State comparisons inspect both intermediate
stage and final want, with exact ordered fields, missing positions and values.
In-memory calls preserve inputs and start fresh. Python/R agreement alone is not
the oracle. The dependency assessment has no runtime result to replay.

The original state translation skips silent rows, mishandles the LAG queue and
receiver, and poisons the accumulator on missing input. Its first differing
output cell is r8.total: missing instead of 115. The earlier r2 iteration loses
100 from retained state before that output appears. The first delivered repairs
passed the frozen comparison without parent edits or feedback repairs.

The interchange witness preserves CRLF and trailing spaces, duplicate business
identifiers, original missing tags, descriptor unknowns and exact text bytes.
NUL and undefined Windows-1252 bytes use a row-associated raw fallback. This is
a declared new representation, not a retroactive change to the starter's ASCII
contract or evidence that an R character column accepts NUL.

## Evidence and replay

- `CONTRACT.md`, `oracle.json`, `freeze.json`: rubric, literal expected values and
  packet hashes fixed before generation.
- `packets/`: original synthetic requests, source/input files and skill snapshots.
- `candidates/`, `delivery.json`: all 53 unmodified first-delivery files and their
  hashes. Agent self-test reports and receipts are retained as self-reports.
- `review.json`: parent review with artifact hashes, seven dependency criteria,
  two interchange-contract criteria and two state-diagnosis criteria.
- `drivers/`, `verify.py`, `receipt.json`: independent execution, comparison and
  the first parent replay receipt. The receipt binds files present at execution;
  this explanatory README was added afterward.

Run from repository root with native Rscript available:

```sh
python3 trials/skill-proposals/verify.py
```

The replay verifies frozen inputs and first-delivery hashes before running saved
code in temporary directories. It requires native R and fails if it is absent.
It binds the archived artifact review; it does not automatically rejudge prose
or invoke a model. CI runs the same command after the earlier starter replay.

Each evaluator saw only its packet, applicable skill and primary public sources,
with no parent history, sibling implementation or expected answers. Isolation was
by instructions and directories, not an operating-system access boundary. One
state evaluator produced both Python and R. Model revision and sampling settings
were not exposed and remain null. No causal with/without-skill comparison ran.

## Remaining work

Actual SAS execution is absent. The dependency evidence deliberately remains
synthetic, and the unresolved post_hook and missing work.have prevent a complete
program run. Its capture recipe records how to collect finalized MPRINT/MFILE
bytes and a raw log after resolving those dependencies in a later authorized
case. No emitted source was invented as a live capture.

The CSV witness starts from a decoded synthetic envelope. It does not test a
SAS-binary reader, R consumer or Parquet writer. The state slice covers ordinary
numeric missingness and the declared two-step source, not BY groups, WHERE,
merge behavior or arbitrary programs. More cases, repeatability and live-SAS
comparisons remain in [the phased plan](../../docs/TEST_PLAN.md).

All six repository skills retain initial-guidance status. This successful batch
did not justify changing their instructions or treating the bounded witnesses
as production converters.
