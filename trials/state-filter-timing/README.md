# WHERE and subsetting IF state timing

Status: bounded engineering evidence for maintainer review, recorded 2026-11-02.
This is one exploratory use of the existing sas-diagnose-state skill, not a
general conversion guarantee or live-SAS comparison. Both target repairs came
from the same fresh evaluator.

## Parent result

All 31 machine checks and six artifact-review criteria passed under CPython
3.12.3 and native R 4.3.3. The parent preserved the first delivered code and used
its own frozen literal expectations, not candidate helpers or cross-language
agreement as truth.

| Check | Count | Observed result |
|---|---:|---|
| Six cases, two languages, CLI and typed API | 24 | Both output tables match exact ordered values and missing positions |
| Original buggy Python execution | 1 | Reproduced the expected mismatch |
| Deliberately wrong output controls | 6 | All rejected by the same comparator |

Each CLI check also repeats against its existing destination and verifies refusal
without file changes. Typed API checks preserve inputs, require character IDs and
numeric/missing columns, and repeat calls around an empty call to detect leaked
state. Empty tables retain schema. The six cases cover the main sequence, a
leading excluded row, one selected row, all-missing values, no selected rows and
empty input. Identifiers include leading zeros and the literal `NA`.

The original bug filters both paths before LAG and accumulation. Its first
differing output cell is `if_path`, row 2 (`r8`), `prev`: actual 5, expected 100.
The earlier input row `r2` changes the IF queue and total before its output is
discarded. The main outputs have the same row identifiers and row counts, so
row-count agreement cannot establish preservation.

| r8 output | prev | total |
|---|---:|---:|
| WHERE path | 5 | 15 |
| IF path | 100 | 115 |

These expected values are source/document-derived inference, not captured SAS
output. WHERE is declarative even though it is written below the sum statement;
subsetting IF acts at its written execution position. Both DATA steps read the
same input independently. They are not a chained pipeline.

## Preserved evidence

- `CONTRACT.md`, `oracle.json`, `freeze.json`: contract, independent truth and
  input/skill hashes frozen before generation.
- `packet/`: synthetic source, original failing translation, six CSV inputs,
  request and the exact existing skill snapshot.
- `harness-freeze.json`: parent comparator and typed-driver hashes fixed before
  first candidate delivery, checked by the replay.
- `candidate/`, `delivery.json`: 163 unchanged regular files. Two temporary test
  symlinks are recorded as literal targets, not recreated as active links.
  Empty directories are inventoried; Python bytecode caches are excluded.
- `review.json`: six parent review findings bound to the inspected files.
- `verify.py`, `python_driver.py`, `r_driver.R`, `receipt.json`: independent
  execution and its first result. The receipt binds files present at execution;
  this explanatory README was added afterward.

The evaluator retained the original mismatch and a preparation failure caused by
an already existing empty output folder. That preparation failure did not modify
files. Its larger self-test corpus and overflow inference remain visible as
agent self-reports, separate from the parent's 31 checks and bounded verdict.
No parent repair, oracle adjustment or feedback-driven retry occurred.

## Replay and boundaries

From repository root, with native Rscript available:

```sh
python3 trials/state-filter-timing/verify.py
```

The replay verifies frozen hashes, runs candidates in temporary directories, and
fails if native R is absent. It binds the archived prose review rather than
automatically judging it again. CI replays saved code, not a new model invocation.

The evaluator received its packet, applicable skill and permission to consult
primary public documentation, without parent history or expected results.
Isolation was by instructions/directories, not an OS access boundary. Model
revision and sampling settings were unavailable and remain null.

No new skill or instruction change follows from this successful invocation.
The existing six skills remain initial guidance. BY groups, merge behavior,
general numeric edge behavior and arbitrary programs are not accepted by these
fixtures. SAS-binary reading, R metadata consumption, Parquet round trips and
live-SAS evidence remain separate milestones in [the test plan](../../docs/TEST_PLAN.md).
