# Stateful DATA-step repair

Status: engineering validation for the principal's review. These are executed Python and base R results against independently derived source-semantics witnesses, not live-SAS equivalence evidence or release authorization. Validation covers the supplied inputs and the bounded tests described below. A SAS run or additional counterexample could change the conclusion.

## Evidence and first observed failure

The supplied request and `source.sas` define the slice and input contract. The expected outputs below are **inference** from that source and the primary SAS documentation, not supplied expected output and not captured SAS output. No macros, includes, or other missing source authority control this slice.

Before writing the repair, I copied the supplied packet unchanged to `evidence/frozen/`, recorded its SHA-256 hashes in `evidence/input_sha256.json`, executed the supplied `buggy.py` on `main.csv`, and retained its complete result and comparison in `evidence/first_observed_mismatch.json`. That receipt is preserved unchanged.

The first observed output mismatch, comparing `stage` before `want`, is output position 2, row `r8`, column `total`: the buggy result is missing (`None`), while the independent hand trace gives **115**. There are **22 differing cells** across the two tables. Both buggy tables contain six rows, so row counts alone miss the failure.

The earliest internal state divergence is one input iteration earlier: `r2` is silent but must add 100, bringing total from 15 to 115. The buggy code skips it entirely. On `r8`, it then turns the missing input value into a missing accumulator. These two separate errors combine in the first observed mismatch.

The comparison policy was fixed before repair: exact row count, input-relative row order, ordered columns, exact missing positions, string identifiers, numeric nonmissing columns, and exact numeric equality for these small integer or binary-fraction witnesses. Python `None` and R numeric `NA` represent ordinary missing. CSV quoting and numeric spelling are parsed before comparison; raw file bytes are not the acceptance criterion. No tolerance or comparison was weakened after failure.

## Why the original translation fails

1. **Output timing.** `if emit=1 then output` controls output only. Every input row reaches the earlier LAG branch and sum statement. Explicit OUTPUT also suppresses implicit output in the first step. The buggy early `continue` discards state-changing work on `r2` and `r4`. [SAS OUTPUT statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm).
2. **Queue timing.** This LAG occurrence begins with one missing queue entry and advances only when `take=1`. The buggy `prior` advances after every emitted row and never after silent rows. It therefore confuses input order, LAG-call order, and output order. In particular, `r4` queues 3 despite emitting nothing; `r6` must receive 3. Missing values also occupy queue entries. [SAS LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm).
3. **Receiver lifecycle.** `prev` is created in the step, absent from the input, and not retained. It resets to missing each input iteration, independently of queue memory. Thus `r1` and `r3`, where `take=0`, have missing `prev`. The buggy function retains the last assigned receiver. The SET-retention rule applies to variables read from the input, which does not include `prev`. [SAS DATA-step initialization](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm).
4. **Sum semantics.** `retain total 10` supplies the initial accumulator; `total + value` retains it and adds zero for a missing expression. The buggy ordinary arithmetic assignment makes the total missing permanently after `r8`. [SAS sum statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1dfiqj146yi2cn1maeju9wo7ijs.htm).

The second DATA step reads the actual six-row `stage`, in that order. It performs a fresh assignment of `delta=value-prev` on each row, propagating ordinary missing when either operand is missing. It does not reprocess the eight original input rows or reuse first-step execution state.

## Independent hand trace

Here `.` means ordinary missing. Each iteration starts with `prev=.`. `Q` is the one-entry LAG queue. The table is a derived diagnostic trace, not an additional production output.

| Input | row_id | value | take | emit | Q before | LAG call | prev after branch | Q after | total before | total after | stage position |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | r9 | 5 | 1 | 1 | . | 1 | . | 5 | 10 | 15 | 1 |
| 2 | r2 | 100 | 0 | 0 | 5 | none | . | 5 | 15 | 115 | none |
| 3 | r8 | . | 1 | 1 | 5 | 2 | 5 | . | 115 | 115 | 2 |
| 4 | r1 | 7 | 0 | 1 | . | none | . | . | 115 | 122 | 3 |
| 5 | r4 | 3 | 1 | 0 | . | 3 | . | 3 | 122 | 125 | none |
| 6 | r6 | 9 | 1 | 1 | 3 | 4 | 3 | 9 | 125 | 134 | 4 |
| 7 | r3 | 2 | 0 | 1 | 9 | none | . | 9 | 134 | 136 | 5 |
| 8 | r7 | -4 | 1 | 1 | 9 | 5 | 9 | -4 | 136 | 132 | 6 |

The repaired intermediate and final outputs agree with the following hand-derived table. `stage` contains the first four columns; `want` adds only `delta`.

| row_id | value | prev | total | delta |
|---|---:|---:|---:|---:|
| r9 | 5 | . | 15 | . |
| r8 | . | 5 | 115 | . |
| r1 | 7 | . | 122 | . |
| r6 | 9 | 3 | 134 | 6 |
| r3 | 2 | . | 136 | . |
| r7 | -4 | 9 | 132 | -13 |

## Repairs and interface

`converted.py` uses only the Python standard library. `translate(rows)` accepts typed dictionaries with string `row_id`, numeric or `None` `value`, and 0/1 flags. It returns `{"stage": [...], "want": [...]}`. `converted.R` uses base R. `translate(df)` accepts a typed data frame with character `row_id`, numeric `value` with ordinary numeric `NA`, and 0/1 flags, and returns `list(stage=..., want=...)`.

Both repairs allocate the total and queue inside each call, reset `prev` inside each input iteration, execute state updates before checking `emit`, and construct the second step from the materialized intermediate output. The caller is unchanged. Returned stage and want are independently editable. They keep the requested columns in order and omit the input flags. Empty R results retain character and numeric column types; both CLIs always write headers even for zero rows.

Importing or sourcing defines functions without running the CLI. From this task folder:

```sh
python output/converted.py packet/main.csv output/python-example
Rscript output/converted.R packet/main.csv output/r-example
```

Each command requires a new output directory and writes `stage.csv` and `want.csv`. These example destinations were not created during validation. CSV input preserves row identifiers as text, including leading zeros, the literal `NA`, embedded punctuation, and internal spaces. Missing numeric CSV fields become ordinary missing and serialize as blank fields. The functions assume the supplied valid-input contract; they do not implement SAS special missing codes or general input validation.

## Executed checks and receipts

The reproducible validation command was:

```sh
python output/selftest.py
```

It exited **0**, using Python **3.12.3** and R **4.3.3**. The retained run is `evidence/run-hfq434r5/validation_receipt.json`, with the actual CLI CSVs alongside it. The R self-test is also saved as `selftest.R`.

- **4,369 cases per language:** every sequence of length 0 through 3 over values `{missing, -2, 0, 3}`, `take` in `{0,1}`, and `emit` in `{0,1}`. This is `1 + 16 + 256 + 4096`. Each case is compared at both tables against a separate index-and-prefix-sum witness, called twice, checked for caller mutation, and followed by an empty call. The independent witness uses selected input positions for LAG and prefix sums over all input values, rather than the repaired execution loop.
- **Literal hand truth:** both languages separately match the six-row main table above. The preserved original buggy output is reproduced unchanged. Python/R agreement alone is not the oracle.
- **10 CLI successes:** both languages run the four supplied CSVs plus one seven-row key/fraction/missing-value witness. Both `stage` and `want`, schema order, missing positions, identifier strings, and numbers match. The extra witness includes an empty string key as an additional transport check, without asserting that such a key is required by the source descriptor.
- **10 expected rejection exits:** rerunning each CLI against its existing destination exits nonzero and leaves the output file hashes unchanged. These are intentional contract checks, not repair failures. Exact messages are retained in the receipt.
- **Import/source, isolation, and types:** importing Python and sourcing R produce no CLI output or invocation; R source occurs with only the self-test's single argument, so accidental CLI execution would fail the test. Editing returned `want` does not change `stage`, editing returned `stage` does not change the input, and a subsequent call still matches. Empty and silent cases retain the required output shape.
- **Five negative controls:** isolated wrong implementations are rejected under the same comparison. They respectively move the filter early, advance the queue unconditionally, retain the receiver, propagate missing through ordinary addition, and run step two over original input. The main-case first differences are captured in the validation receipt.

Small witnesses for those negative controls are retained in `evidence/minimal_witnesses.json`. Each triple below is `(value,take,emit)` in input order. These cases are also members of both languages' exhaustive corpus.

| Wrong variant | Small witness | Observed distinguishing failure |
|---|---|---|
| Early filter | `(3,1,0), (-2,1,1)` | Emitted row loses queued 3 and has total 8 instead of 11 |
| Unconditional queue | `(3,1,1), (0,0,1), (-2,1,1)` | Third row receives 0 instead of 3 |
| Retained receiver | `(3,1,1), (0,1,1), (-2,0,1)` | Third row retains 3 instead of missing |
| Ordinary addition | `(missing,0,1)` | Total becomes missing instead of 10 |
| Step two over original input | `(3,1,0)` | Want contains one row instead of zero |

No repair test failed. The original mismatch and intentional wrong-variant failures remain in the evidence. No later parent-feedback repair has been folded into this first delivery.

## Limits

There was no SAS runtime, and no SAS result was invented. The source-specific interpretation is supported by primary documentation and independent hand/indexed witnesses; live SAS comparison remains unperformed. The test count does not imply exhaustive coverage of all finite numbers, all input lengths, every ASCII key, floating-point edge cases, other missing classes, or other SAS programs. No sibling implementation, supplied expected output, package installation, or external mutation was used.
