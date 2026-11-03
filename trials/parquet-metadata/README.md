# Parquet, metadata and base R bridge trial

Status: bounded engineering evaluation for maintainer review. The first delivery
has an observed CLI process-abort failure; a separate repaired attempt passes
68 parent checks. Synthetic decoded inputs exercise real Parquet transport and
an explicit base R bridge. This is
not a live-SAS comparison, a SAS-binary reader, direct R Parquet reading, or a
universal preservation guarantee.

The principal approved continuing after the public catalog addition. This trial
uses the unchanged `sas-to-parquet` and `sas-define-interchange` skills. One fresh
evaluator supplies paired Python and R code. The parent freezes expectations,
adapters and acceptance before dispatch; the evaluator receives inputs only.
First-delivery files are archived unchanged. Targets are paired outputs of one
evaluation, not independently generated implementations.

## Results and separate repair

The initial independent replay passed 67 of 68 checks. One CLI process aborted
with `terminate called without an active exception`. A normal-runner replay
passed 66 of 68, with two CLI aborts. Ten targeted original CLI runs observed
four aborts. Limiting Arrow CPU and IO pools to one worker produced one passing
68-check replay but still three aborts in ten targeted CLI runs. Both failed
receipts and the passing-but-unreliable worker-limited result are retained.

The parent preserved the evaluator's 21 delivered files byte-for-byte, including
six Parquet/companion pairs. A separately recorded one-line repair uses
`ParquetFile(...).read(use_threads=False)` on the same checked byte snapshot.
The repaired attempt passes the unchanged 68-check comparator and 20 targeted
CLI repetitions without an observed abort. This supports the chosen reader-path
repair in this environment; an upstream root cause has not been established.
All six archived delivered bundles also pass independent semantic comparison.
See [the repair record](REPAIR.md) for manifests, receipts and exact boundaries.

First-delivery acceptance is false. The repaired witness result does not imply
full-domain acceptance: R still rejects NUL-bearing character identifiers and
its ISO-date bridge admits four-digit years. NUL in the raw text column is
exercised successfully. The evaluator's larger self-test corpus and counts
remain self-reported evidence, separate from the 68 parent checks.

## Executed boundary

The six valid envelopes contain 44 rows altogether. They cover all 28 admitted
missing tags at numeric/date cell positions, duplicate and leading-zero IDs,
fixed source byte widths and padding, UTF-8 and Latin-1, empty and all-missing
tables, embedded NUL and control bytes, Unicode normalization, signed zero,
date origins, labels/value mappings and unknown timezone metadata. Seven invalid
envelopes exercise strict refusal before output creation.

The writer emits actual Parquet with an explicit seven-column schema and a JSON
companion bound to source/output hashes. The parent reopens both and compares
all cells, ordered types, raw bytes/binary64 bits, tag positions and descriptor
properties. It calls the candidate's restoration API separately. Negative
controls include rewritten files with repaired hashes, so matching hashes alone
cannot satisfy the semantic comparator. These hashes associate artifacts; they
do not authenticate a publisher.

A frozen parent adapter exports values from reopened Parquet plus the companion
into three normalized CSV tables. Native base R consumes typed doubles and Date
values, exact character identifiers, raw text vectors, tags and descriptor/value
label tables. Text raw vectors deliberately support NUL and are not ordinary R
character strings. This does not retroactively close the earlier R text/NUL gap.

## Reproduce

From the repository root, with native Rscript available and a task-specific
Python environment:

```sh
python -m pip install -r trials/parquet-metadata/requirements.txt
python trials/parquet-metadata/parent_selftest.py
python trials/parquet-metadata/verify_repair.py --receipt /tmp/parquet-replay.json
```

PyArrow is pinned to 26.0.0. The replay records the Python and R versions it
actually executes. CI installs this dependency in the existing native-R replay
job after all prior trial steps and executes the separately repaired attempt.
The wrapper verifies the original delivery hashes before constructing an isolated
repair workspace. Original replay remains available as `verify.py` and can abort
intermittently. No expectation or frozen comparator was edited.

## Evidence files

- [Contract](CONTRACT.md), [derivation](DERIVATION.md), [literal oracle](oracle.json)
  and [freeze hashes](freeze.json) define the pre-dispatch parent acceptance.
- `packet/` holds the actual supplied request, descriptors, fixtures and exact
  skill snapshots. It contains no parent answers or comparator.
- `candidate/` holds the original implementation, report, history and self-tests.
  Candidate self-test counts remain separate from parent acceptance.
- `repair/` holds the separate repaired implementation and its delivery manifest.
  `verify_repair.py` assembles that attempt without modifying the first delivery.
- `bridge.py`, `r_driver.R` and `verify.py` are parent-owned adapters and replay.
  `parent_selftest.py` checks six positive witnesses and one negative witness.

The next boundaries remain actual SAS-binary reader behavior, real SAS reference
capture, direct R Parquet consumption, broader repeatability, and adversarial MCP
retrieval. No skill instruction or catalog resource is promoted by this trial.
