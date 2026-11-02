# R translation result

Status: engineering candidate with passing R-runtime checks, not live-SAS equivalence or a general translator. The principal may review and reuse it within the stated input contract; broader acceptance needs additional evidence.

## Contract and source

The supplied request specifies a base R `translate(df)` function, a UTF-8 CSV CLI, and columns `row_id,value,prev,prev2,change` in that order. Input is a character key with SAS width 8 and a numeric value. Ordinary SAS numeric missing maps to R `NA_real_` and blank numeric CSV cells. The interchange key stays unpadded and unchanged. Each invocation starts a fresh DATA step.

`packet/source.sas` has one SET statement, unconditional LAG and LAG2 calls, and subtraction. It contains no includes, macros, BY groups, filters, explicit OUTPUT statements, or external references. `work.have` is the supplied input and `work.want` is the returned table or output CSV.

Source SHA-256: `6860b2c29011ddb4e73b8bf24fd9212c1f9ce8ade703270a796adc6ccf0560ea`.

The exact source, request, four inputs, delivered program, and test script identities are recorded in `sha256.txt`. Inputs inspected were `main.csv` with 4 rows, `edge.csv` with 4 rows, `single.csv` with 1 row, and header-only `empty.csv`. No supplied expected outputs or sibling implementations were read.

## Comparison policy and implementation

The policy was fixed before implementation: exact numeric values for these bounded cases, exact missingness, character bytes, row multiplicity/order, column names/order, and column types. There is no approximate statistical calculation and no tolerance adjustment. Source descriptors are represented by R character/double columns; SAS descriptor metadata and physical character padding are outside the interchange contract.

SAS documents separate queues initialized with missing values for each LAG occurrence. Each queue advances whenever its function executes. [SAS LAG documentation](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm).

Inference from that documentation and the unconditional calls in this source: ordinary one-row and two-row shifts reproduce these two queues. Missing input values occupy queue positions. Subtraction propagates missingness, and overflow is converted to ordinary missing, consistent with the [SAS arithmetic documentation](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000989183.htm).

The function constructs a new data frame and holds no persistent state. CLI input reads keys as character, preserving numeric-looking keys and literal `NA`. It writes quoted text keys, blank numeric missing cells, and 17 significant digits for nonmissing numbers. CSV handling follows the R [input](https://www.stat.ethz.ch/R-manual/R-devel/library/utils/html/read.table.html) and [output](https://stat.ethz.ch/R-manual/R-devel/library/utils/help/write.table.html) documentation.

## Executed evidence

Observed verdict: all 38 final checks passed, with process exit status 0. `self_test.R` reproduces the checks; `test-results-final.txt` retains the output. The initial 35-check run is also retained in `test-results.txt`.

- The four supplied cases matched independently written hand expectations through both the API and CLI. The checks include nonmutation, repeated fresh invocation, typed empty output, and blank missing cells.
- An independently implemented scalar queue witness matched the vector implementation at lengths 0, 1, 2, 3, 7, and 1000, using fixed-seed values and missing entries.
- A deliberately wrong result that skips a missing queue value was rejected by the exact comparator.
- Eight additional text keys exercised leading zeros, literal `NA`, empty text, spaces, comma, UTF-8 accent, quote, and hash. Their decoded character bytes survived the CLI round trip.
- A separate source-only R process with CLI-like arguments produced no CSV, confirming that sourcing does not execute the CLI.
- Three precision-sensitive decimal inputs survived an exact numeric CSV round trip. A two-row overflow case returned missing change values.

Runtime: R 4.3.3, x86_64-pc-linux-gnu, Ubuntu 24.04.5 LTS, C.UTF-8 character locale, C numeric locale. Only base R packages were used. `sessionInfo()` produced a warning because its `timedatectl` probe could not connect to the system bus; all translation checks had passed and the R process exited 0. The raw warning remains in the log.

## Reproduction and limits

Run from `/tmp/roku-starter-20261101/lag-r`:

```sh
Rscript output/converted.R packet/main.csv output/main.csv
Rscript output/self_test.R
```

Or source `output/converted.R` and call `translate(df)` with the typed input data frame.

No SAS runtime was available, so no live SAS comparison or captured SAS baseline was executed. The oracle is hand derivation plus an independent R queue witness. Special SAS missing categories, descriptor metadata, SAS logs, invalid encodings, out-of-contract input types, and general SAS programs are unsupported. Width-8 validity is supplied by the contract; keys are not truncated or padded. Broader floating-point behavior across SAS host platforms remains unproved. New source control flow, new missing-value categories, or broader input descriptors would require a revised contract and new witnesses.
