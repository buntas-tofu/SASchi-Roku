# Bounded SAS-to-Python translation

Status: candidate conversion with passing Python self-tests, for the principal's engineering review and further testing. This is not a live-SAS equivalence receipt or a claim of general SAS translation support.

## Source and interpretation

The supplied `packet/source.sas` reads `work.have`, calls `lag(value)` and `lag2(value)` unconditionally, calculates `value - prev`, and implicitly outputs each observation to `work.want`. There are no includes, macros, BY groups, conditional lag calls, or additional external dependencies in this source. The supplied input descriptor is `row_id` character width 8 and `value` numeric. The requested interchange keeps `row_id` unchanged and unpadded.

Inference from the source and documented SAS behavior: each row advances two separate queues, including rows whose value is missing. The queues begin with one and two missing entries respectively. A missing operand makes `change` missing. Fresh queue instances inside `translate` implement the supplied requirement that every call represents a new DATA step.

Primary documentation consulted:

- [SAS LAG function reference](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm): independent queues, initial missing entries, and advancement on execution.
- [SAS missing-value calculations](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000989183.htm): missing operands propagate through arithmetic; arithmetic overflow yields missing.

Only this task packet, generated task outputs, and primary public documentation were consulted. No sibling implementation, provided expected output, or captured SAS result was read.

## Comparison policy

The policy was established before implementation: exact comparison of output schema and column order (`row_id,value,prev,prev2,change`), row count and sequence, character keys, numeric values, and numeric missingness. Independent literal expected tables were derived by hand from the supplied source and documented queue rules. These are derived expectations, not measured SAS outputs. No comparison tolerance was used because the supplied values are small integers and the additional fractional witness uses exactly representable binary fractions.

API results use `float` for nonmissing numerics and `None` for ordinary missing. The API accepts numeric strings from CSV readers, Python integers/floats, blank numeric text, and `None`; floating NaN also maps to ordinary missing. Booleans, nonnumeric objects, infinite values, and textual nonfinite numbers are rejected. Each output row is new and has exactly the requested columns.

CSV comparison checks parsed typed numeric values rather than numeric text formatting: `12.0` and `12` represent the same numeric value. Missing output cells must be empty. Character field UTF-8 bytes are compared exactly after CSV decoding; CSV quoting and record delimiters are transport formatting, not character field contents. No padding, stripping, truncation, or normalization is applied to `row_id`.

## Executed evidence

Environment: CPython 3.12.3, GCC 13.3.0, Linux 7.0.0-28-generic x86_64, glibc 2.39. The implementation and tests use only the Python standard library. No package installation or SAS execution occurred.

Executed `python3 output/selftest.py` successfully with exit code 0. The reproducible test script is `output/selftest.py`; its recorded output is `output/test-results.txt`.

- All four supplied CSV files passed API and separate-process CLI comparisons against literal hand-derived tables: `main` 4 rows, `edge` 4 rows, `single` 1 row, `empty` 0 rows. This is 9 supplied input rows, including the header-only case.
- These checks also verified unchanged caller inputs, distinct output list and row objects, repeated-call freshness, exact output key order and numeric result types, and blank numeric CSV missing cells.
- A 5-row typed API witness passed for leading missing, consecutive missing, and exact binary fractions.
- A separate 5-row CLI witness preserved UTF-8 character field bytes for surrounding spaces, non-ASCII text, quotes, commas, LF and CRLF within quoted fields. Its keys fit the supplied 8-byte width.
- Importing the module succeeded without invoking the CLI or producing output.
- The same exact comparator rejected a deliberately wrong implementation that omits missing inputs from lag history. At `e7`, it produced `prev=5` and `change=-7`, where the hand-derived expectation has both missing. The rejected mismatch is retained in `output/evidence/negative-control.txt`; it is not an accepted translation output.

Accepted CLI outputs are in `output/evidence/main.csv`, `edge.csv`, `single.csv`, and `empty.csv`. Character-round-trip input/output files are in the same directory.

Observed verdict: all listed Python self-tests passed. Syntax was exercised by successful import and execution. SAS equivalence remains unproved at the runtime boundary.

## Reproduction

From `/tmp/roku-starter-20261101/lag-python`:

```sh
python3 output/converted.py packet/main.csv output/main.csv
python3 output/selftest.py
```

Import `translate` from `output/converted.py` and call it with a list of dictionaries containing `row_id` and `value`. Import does not run the CLI. CLI input must have exactly the `row_id,value` header and two cells per observation, encoded in UTF-8.

## Source and input identities

SHA-256 hashes are over the original file bytes, including line endings.

| Packet file | SHA-256 |
| --- | --- |
| source.sas | `6860b2c29011ddb4e73b8bf24fd9212c1f9ce8ade703270a796adc6ccf0560ea` |
| request.txt | `54b93739cbbcaa179a9ee8cd3691a02d0599a8d0a242ecda690978d1d221a812` |
| main.csv | `8d5ba1d91b049d62a5230a07df383ef52230548f3b6765e2ebc57876a381c8e0` |
| edge.csv | `89d406226bc33a4b25d3c429361797f8d4d33151d94f2a4e44dc90f087b48a00` |
| single.csv | `0a9f21b50eadad89863881bd3199ad2536fa8f80b2f3a113f14430a5a825d85d` |
| empty.csv | `ec2c174b782ade3be97f33c9464bce85068315ad6e293045f47da57600b21083` |

## Limits

This implements the supplied program, not a parser or a general SAS runtime. It does not reproduce SAS dataset files, descriptor metadata, logs, formats, labels, special missing categories, or behavior of a different source containing conditional calls or BY processing. Character width is supplied as an input contract, not enforced by truncating the interchange key. The CLI loads the input into memory.

Python floating-point numeric parsing and subtraction were tested only on the stated values. Platform-specific SAS numeric representation, arbitrary decimal rounding, extreme ranges, and SAS diagnostic side effects were not compared. The overflow-to-missing branch and floating-NaN input convenience are implemented but not separately witnessed by these tests. A live SAS run with the same data and descriptor, plus additional numeric boundary witnesses, would be needed to strengthen the parity claim.
