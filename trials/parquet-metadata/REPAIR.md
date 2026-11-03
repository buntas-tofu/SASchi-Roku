# Separate Parquet reader repair

Status: parent-authored repair after independent execution exposed a CLI process
abort. Maintainers may review the bounded result; first-delivery acceptance is
false. This is not an upstream Arrow root-cause finding or general safety claim.

The evaluator delivered 21 files. `delivery.json` binds their original bytes;
`freeze.json` binds the pre-dispatch packet, oracle, comparator and adapters.
Both remain unchanged. The evaluator was stopped after first delivery and did
not receive parent acceptance results or make the repair.

## Observed evidence

| Run | Result | Record |
|---|---|---|
| Initial parent replay | 67/68, one CLI abort | `receipt.initial.json` |
| Normal local runner | 66/68, two CLI aborts | `receipt.normal-runner.json` |
| Original CLI, all-missing case | Four aborts in ten repetitions | `diagnostic.cli-default.json` |
| CPU/IO pools limited to one | 68/68 in one replay | `receipt.single-worker.json` |
| Worker-limited original CLI | Three aborts in ten repetitions | `diagnostic.cli-single-worker.json` |
| Separate repaired attempt | 68/68 | `receipt.repaired.json` |
| Repaired CLI, ten all-missing and ten all-tags | No observed abort in 20 repetitions | `diagnostic.cli-repaired.json` |
| Archived original bundles | Six independent comparisons passed | `delivery_review.json` |

Every abort reported `terminate called without an active exception`. Targeted
original failures left both output files present. The failures occurred in both
local runners, so the evidence does not support blaming runner restrictions.
Thread-pool limits did not reliably fix them. The counts above describe these
specific observations, not an estimated population failure probability.

## One-line implementation difference

The checked Parquet byte snapshot is unchanged. Only its reader call differs:

```python
# Original first delivery, preserved in candidate/converted.py
table = pq.read_table(pa.BufferReader(raw))
# Separate parent repair in repair/converted.py
table = pq.ParquetFile(pa.BufferReader(raw)).read(use_threads=False)
```

[Arrow's ParquetFile API](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetFile.html)
documents the selected reader and thread option. The observed successful replay
supports this repair for the recorded environment; the experiment changes both
the reader path and its threading option and does not isolate a C++ root cause.

`repair/delivery.json` binds the repaired Python file and all unchanged original
artifacts, and records the original delivery manifest hash. `verify_repair.py`
first verifies the original delivery, then creates a temporary workspace with
the same frozen parent inputs and comparator, substituting only the repaired
Python file and the explicitly separate repair manifest. It runs all 68 checks.
No process failure is converted to success, and no failed original receipt is
overwritten. The R implementation remains the original first delivery.

The original contract admits character byte cases whose general domain exceeds
the requested R character identifier representation. Its supplied identifiers
are representable. The evaluator explicitly rejects NUL-bearing identifiers and
limits its R date bridge to four-digit ISO years. These are retained limits;
passing supplied witnesses does not retroactively narrow the original request
or establish full-domain acceptance. No existing skill instruction changed.
