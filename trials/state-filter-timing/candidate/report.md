# Filter timing repair

Status: local engineering repair and execution evidence for the supplied program. This is not live-SAS validation or a general translator certification. The principal and evaluator may inspect and rerun these artifacts; acceptance remains with the principal.

The supplied `buggy.py` applies an early filter to both output tables. That matches the declared `where_path`, but changes the declared `if_path`. The repaired Python and base R implementations preserve the two filter timings and passed the local comparisons described below.

## Evidence and authority

The packet request and source define this task's contract. The original packet is preserved byte for byte under `evidence/frozen_packet/`, with SHA-256 hashes in `evidence/input_manifest.json`. No source or supplied input was edited. The final self-test checked all 11 original files and their frozen copies against those hashes.

SAS documentation is secondary evidence. Every expected SAS result below is a document-based inference derived from the source, not a captured SAS execution. The hand expectations were written before either repaired implementation. Both targets were compared against those expectations separately; Python/R agreement was not the oracle.

## Reproduced original mismatch

The frozen original implementation was executed on all six supplied CSVs. Comparison order was table order `where_path`, `if_path`; row order within each table; then columns `row_id`, `value`, `prev`, `total`. It required exact cell equality and missing positions, with no numeric tolerance or row sorting.

The first differing output cell for `main.csv` is:

| Table | Output row | row_id | Column | Original actual | Hand expected |
| --- | ---: | --- | --- | ---: | ---: |
| if_path | 2 | r8 | prev | 5 | 100 |

The same row's `total` is also wrong: original `15`, expected `115`. All `where_path` cells match the hand expectations. In `if_path`, later rows retain the consequences of the prematurely discarded observations.

The first internal state divergence precedes that output: physical input row 2, `r2`, has `value=100`, `eligible=0`. The source's `if_path` executes its LAG call and sum statement, making the queue `100` and total `115`, before rejecting output. The original skips this row entirely, leaving queue `5` and total `15`.

The supplied two-row `leading.csv` is a smaller witness. The excluded `0007` row has value `100`; the next row has identifier `NA`, value `8`, and is eligible. Expected `where_path` is `(NA, 8, missing, 18)`. Expected `if_path` is `(NA, 8, 100, 118)`. The original produces the former for both. Inference: two input rows are the smallest shape that can expose an excluded row's effect on a later emitted row here.

`main` and `leading` reproduce mismatches. `single`, `empty`, `silent`, and `all-missing` match the original because their values and selection patterns do not distinguish this defect. Their filenames were not used to infer semantics.

Preserved receipts:

- `evidence/original_run/*.json`: actual original outputs and first differences.
- `evidence/original_execution.json`: the executed command and exit code `1`.
- `evidence/original_stdout.txt` and `evidence/original_stderr.txt`: captured output. Exit `1` deliberately records the reproduced mismatch.

## Independently derived source trace

Both DATA steps read `work.have` independently. They are not chained. Each starts its own one-element LAG queue at missing and its own retained total at `10`.

The WHERE expression acts before an observation enters DATA-step processing, regardless of its textual placement after the sum statement. The subsetting IF executes at its written position, after the LAG and sum statements. A false IF suppresses that iteration's output, but does not undo state already changed. These timings follow the primary [WHERE/IF comparison](https://support.sas.com/documentation/cdl/en/lrcon/65287/HTML/default/p04fy20d8il3nfn1ssywe4f25k27.htm) and [subsetting IF reference](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p1cxl8ifdt8u0gn12wqbji8o5fq1.htm).

Each reached LAG call returns the queue's prior entry and then enqueues the current value, including ordinary missing. `prev` is assigned on every reached iteration; its value is distinct from queue storage. See the [LAG reference](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm).

`retain total 10` supplies the initial value. The sum statement retains the accumulator and ignores a missing input expression. See the [sum statement reference](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1dfiqj146yi2cn1maeju9wo7ijs.htm). There is no explicit OUTPUT in this source; iterations reaching the end emit implicitly, as described in the [OUTPUT reference](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm).

The following compact hand trace shows states after each physical input position. A dash means that WHERE excluded the row before a DATA-step iteration, so `prev` was not assigned. `missing` denotes an ordinary numeric missing value.

| Input | value | eligible | WHERE prev | WHERE total | WHERE emits | IF prev | IF total | IF emits |
| --- | ---: | ---: | --- | ---: | --- | --- | ---: | --- |
| r9 | 5 | 1 | missing | 15 | yes | missing | 15 | yes |
| r2 | 100 | 0 | - | 15 | no | 5 | 115 | no |
| r8 | missing | 1 | 5 | 15 | yes | 100 | 115 | yes |
| r1 | 7 | 0 | - | 15 | no | missing | 122 | no |
| r4 | 3 | 1 | missing | 18 | yes | 7 | 125 | yes |
| r6 | 9 | 1 | 3 | 27 | yes | 3 | 134 | yes |
| r3 | 2 | 0 | - | 27 | no | 9 | 136 | no |
| r7 | -4 | 1 | 9 | 23 | yes | 2 | 132 | yes |

The full trace, including queue-before/after, total-before/after, statement reachability, and output position, is `evidence/main_hand_trace.csv`. It includes excluded physical rows as explanatory entries, not as invented WHERE iterations.

The hand-derived main expected tables are:

| Table | row_id | value | prev | total |
| --- | --- | ---: | ---: | ---: |
| where_path | r9 | 5 | missing | 15 |
| where_path | r8 | missing | 5 | 15 |
| where_path | r4 | 3 | missing | 18 |
| where_path | r6 | 9 | 3 | 27 |
| where_path | r7 | -4 | 9 | 23 |
| if_path | r9 | 5 | missing | 15 |
| if_path | r8 | missing | 100 | 115 |
| if_path | r4 | 3 | 7 | 125 |
| if_path | r6 | 9 | 3 | 134 |
| if_path | r7 | -4 | 2 | 132 |

For the remaining fixtures, `single` produces `(s1, 8, missing, 18)` in both tables. `all-missing` emits `m1` then `m3`, each with missing value and prev and total `10`, in both tables. `empty` and `silent` produce zero rows in both tables. Each empty CSV still has its four-column header. Complete expected outputs for every supplied fixture are preserved as JSON and CSV under `evidence/hand_expected/`.

## Repair and interfaces

`converted.py` and `converted.R` each execute two fresh, independent passes. The WHERE pass tests eligibility before updating the queue and total. The IF pass updates them before deciding whether to append an output row. Both preserve input order, advance the queue on missing values, and leave the input unchanged.

The Python function returns an `OrderedDict` containing `where_path` then `if_path`. Each row has exactly the four requested columns in order and uses `None` for missing. The R function returns a named list in the same order; each table has character `row_id` and double `value`, `prev`, and `total`, including when empty. Missing numeric values are `NA_real_`. Importing or sourcing defines functions without starting the CLI.

Both command lines accept the requested two arguments:

```text
python3 converted.py INPUT_CSV NEW_OUTPUT_DIRECTORY
Rscript converted.R INPUT_CSV NEW_OUTPUT_DIRECTORY
```

Each writes `where_path.csv` and `if_path.csv`. CSV ingestion keeps identifiers as strings before converting only numeric fields. Literal `NA`, leading zeros, punctuation, spaces, commas, and quotes are preserved. R writes numeric fields with 17 significant digits for binary64 transport. Missing numeric cells are blank. Existing files, directories, and symlinks are refused with a nonzero exit, before any changes to them.

Both implementations use native binary64 arithmetic. As a document-based inference for finite inputs whose accumulation overflows, the code maps overflow to ordinary missing and permits subsequent sum-statement recovery. This follows the [overflow reference](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000989183.htm) and [SUM missing rules](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0zxive1z1ctqin12w06c85jfigd.htm). It is separately labeled in the test data and is not a SAS execution observation. SAS log messages and automatic error variables are outside the requested output schema.

## Executed validation

Local runtimes: Python 3.12.3 and native base R 4.3.3. No packages were installed. Delivered code uses only the Python standard library and base R, and makes no network calls.

One implementation self-test attempt ran, from `2026-11-02T06:10:18.250996+00:00` through `2026-11-02T06:10:21.962070+00:00`, and passed. The unchanged comparison policy requires table/column order, exact row/identifier order, row counts, exact numeric cells, missing patterns, and API types. No tolerance was loosened after failure.

| Check | Executed result |
| --- | --- |
| Supplied fixtures | All 6 passed in each API and each CLI |
| API cases | 1,564 per language |
| R API assertions | 54,373 passed |
| Successful CLI runs | 18, nine input cases per language |
| Existing destination refusal checks | 10, all nonzero and contents unchanged |
| Deliberately wrong variants | 3 rejected at their expected first differing cells |
| Original packet preservation | All 11 files and frozen copies matched initial hashes |

The API cases contain the six supplied fixtures, all 1,555 sequences of length zero through four over values `{missing, -2, 3}` and eligibility `{0, 1}`, plus text transport, precision, and overflow-recovery cases. The bounded sequence expectations use an independently written index/prefix definition, not target outputs. These small integer sums are exact. The three additional cases use a prefix witness or literal expectations as identified in `suite_case_index.csv`.

For each API case, tests check fresh repeated calls, an interleaved empty call, input preservation, output-table independence, and schema/missing/value agreement. The CLI cases are the six supplied inputs and the three additional cases. Existing-destination checks cover a populated directory, a regular file, an empty directory, a directory symlink, and a dangling symlink for each runtime.

Wrong-variant checks retained in `wrong_variants.json` reject:

- Early filtering for both paths: `if_path`, row `r8`, `prev=5` instead of `100`.
- Late filtering for both paths: `where_path`, row `r8`, `prev=100` instead of `5`.
- Skipping missing queue entries: `where_path`, row `r4`, `prev=5` instead of missing.

Detailed command arguments, exits, runtime durations, stdout, stderr, test inputs, expected rows, per-case statuses, and the tested implementation snapshots are in `evidence/self_tests/attempt_01/`. Run `python3 self_test.py` from this output directory to create another numbered attempt without overwriting this one.

## Failures, history, and limits

The initial directory-preparation call failed because the supplied output directory already existed. It was inspected and found empty, then used. This failure made no file changes. One public WHERE documentation fetch timed out; other primary WHERE/IF references were available. Both events are recorded in `evidence/history.txt`. Original mismatch receipts and intentional overwrite-refusal failures remain preserved. The repaired implementation had no observed failing self-test and no post-test code repair.

There was no SAS runtime and no live-SAS receipt. The source trace is hand-derived, and the independent witness remains a model of the documented semantics. Floating-point edge behavior across other SAS hosts, logs, metadata, malformed-input diagnostics, and constructs absent from this source have not been certified. This work supports inspection of this bounded repair. A live-SAS comparison on the same ordered inputs would strengthen or overturn the inference and should be recorded as separate evidence.
