# First-delivery history

Status: observed execution record for principal and independent acceptance review. This is not SAS-runtime evidence. No production equivalence or benchmark conclusion is asserted.

Working directory for every shell command: `/tmp/roku-state-boundaries-9ku9xsi3/merge`.

1. Read `packet/AGENTS.md`, `packet/request.txt`, `packet/source.sas`, `packet/schema.csv`, the supplied sas-translate skill and evidence map, and all six raw input pairs. Packet files were not changed. No parent repository, sibling task, prior trial, or evaluator output was read.
2. Consulted four primary SAS pages, identified by exact URLs in `report.md`, for match-MERGE multiplicity, actual-read overwrites, IN= retention, and group reset. No reference code was copied into the conversion.
3. Established exact typed-cell, schema, row-order, multiplicity, missingness, and call-state comparisons before writing the translation. Wrote the two implementations and two self-test files through shell heredocs. The self-test's expected tables are independently derived witnesses, not captured SAS output.
4. Environment command `python3 --version` succeeded: `Python 3.12.3`.
5. Environment command `Rscript --vanilla --version` failed with exit 1 and `file name is missing`. This was a command-interface failure, not a target comparison. Corrected with `Rscript --vanilla -e 'cat(R.version.string, "\n")'`, exit 0: `R version 4.3.3 (2024-02-29)`.
6. Executed `PYTHONDONTWRITEBYTECODE=1 python3 output/selftest.py`, exit 0 on the first run. It creates a temporary directory under the isolated workspace and removes it automatically. It performs the exact child commands below for each of the six packet cases and 80 generated cases. It also runs the R API witness with `Rscript --vanilla output/selftest.R TEMP_DIRECTORY`; the actual harness uses absolute paths resolved from its own location.

```sh
python3 output/converted.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY
Rscript --vanilla output/converted.R INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY
```

Observed self-test output:

```text
PASS: 86 R API cases; empty-call isolation; numeric schemas; 6 unsorted API refusals
PASS: 6 packet cases (16 rows); 80 generated cases; 86 Python API cases
PASS: 172 successful CLI runs; 172 existing-destination refusals; 12 unsorted CLI refusals
PASS: exact values/order/schema, blank missing CSV, fresh calls, input preservation, 3 wrong variants rejected
converted.py sha256 9beb2d98b0c32a459a5a2506d97cd197d41dd11e6a47b0356f338263fc91e597
converted.R sha256 730665e2ef6d0b88a978214d2e0c225ea9058e7881cea01307eabd31bc07fe4c
```

There were no failed target comparisons or target-code repairs before first delivery. The three wrong variants intentionally fail comparison and are counted as comparator checks, not accepted outputs. No post-delivery changes have occurred in this record.

7. Wrote the report with source/input identities, full main-case hand trace, documentary basis, observed checks, and the pending SAS boundary. The parent then provided the unchanged repository linter in this isolated workspace; it is a verification tool, not an output artifact.

8. Executed `python3 inertia-drift-lint output`, exit 0: `clean: no drift caught`. Repeated after adding this history entry, with the same exit 0 result.
9. Final inventory check confirmed exactly six regular files in `output/`: `converted.py`, `converted.R`, `report.md`, `history.md`, `selftest.py`, and `selftest.R`. No packet copy, generated results, symlink, or cache directory is retained in output. No temporary self-test directory remains. Implementation hashes remain those printed above. Model revision and settings are unavailable.
