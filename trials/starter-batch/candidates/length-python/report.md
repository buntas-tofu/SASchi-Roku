# Python translation report

Status: bounded engineering conversion with passing Python execution checks. This is not a live-SAS equivalence finding or a general SAS translator. The task owner may use the code for the supplied input contract; broader acceptance requires additional evidence.

The implementation is `converted.py`. It applies the supplied text descriptor, retains text at exactly 10 ASCII bytes by adding trailing spaces, and computes the position of the last character other than a space. All-space text has LENGTH 1. Each call returns a fresh list and fresh dictionaries in input order, with columns `row_id,text,len`. The interchange key is preserved without padding. There is no state between calls.

## Authority and comparison policy

The source and bounded input contract come from `packet/source.sas` and `packet/request.txt`. The supplied skill guided the evidence workflow. There are no includes, macros, statistical settings, or external effects in the supplied source. No sibling code, previous outputs, or supplied expected-output files were used.

Comparisons were specified before implementation: exact row count and order, exact column order, exact text including spaces and control characters, unchanged row keys, and integer LENGTH values. No numeric tolerance applies. Character missingness is represented by all-space storage, with LENGTH 1 rather than numeric missing. The source does not produce missing numeric results; the standard CSV writer's empty-cell behavior for `None` was tested separately.

Primary SAS documentation is candidate supporting evidence, not an executed oracle. [SAS LENGTH documentation](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0f6jve4kdxnh1n1m7c82fhosgih.htm) describes trailing-blank exclusion and the all-blank result of 1. [SAS character assignment documentation](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000695113.htm) describes padding to the variable width. Inference: for this ASCII contract, a blank is the space byte; tabs remain significant. This interpretation is exercised explicitly but has not been verified in a SAS runtime.

The implementation uses an explicit space argument to `rstrip`, because [Python string methods](https://docs.python.org/3.11/library/stdtypes.html#str.rstrip) otherwise remove whitespace more broadly. [Python CSV documentation](https://docs.python.org/3.11/library/csv.html) supports the chosen newline handling, ordered fields, and empty numeric-missing serialization.

## Execution and evidence

Actual runtime: CPython 3.12.3, `/usr/bin/python3`, Linux x86_64, glibc 2.39. Only the standard library was used. No installation or SAS execution occurred.

`python3 output/selftest.py` exited 0. The expected results are separately hand-derived literal witnesses in `selftest.py`, not values obtained from the conversion helper.

| Supplied input | Rows | Expected LENGTH sequence | Observation |
| --- | ---: | --- | --- |
| main.csv | 3 | 4, 10, 1 | Exact API and CLI comparisons passed |
| edge.csv | 4 | 3, 3, 1, 1 | Exact API and CLI comparisons passed |
| single.csv | 1 | 2 | Exact API and CLI comparisons passed |
| empty.csv | 0 | Empty | Header-only output passed |

Twelve additional literal cases passed both API and CLI checks: empty and full-width blank text, tabs, leading spaces, internal spaces, a final character at position 10, CSV commas and quotes, and embedded LF/CR. Checks also passed for input nonmutation, fresh returned objects, repeated invocation, exact 10-byte output text, numeric result type, and silent import without CLI arguments.

The comparator rejected a deliberate mutation that used generic whitespace trimming: `AB\t` produced 2 instead of the expected 3. That failed comparison is retained as a rejected control in `evidence.json`; it is not an accepted output.

`evidence.json` records exact SHA-256 identities for the source, request, skill, four input CSVs, conversion, and test script, along with the runtime and observations. Generated `*.actual.csv` files preserve the observed target results. The source SHA-256 is `7d885ba79a895afa2efa52282ce71ba39430bcb6ff9ea6d3ddc3ca6aa4c58880`.

## Reproduction and limits

From the task directory:

```sh
python3 output/converted.py packet/main.csv output/reproduced.csv
python3 output/selftest.py
```

The function is importable as `translate(rows)`. The CLI requires header `row_id,text` and writes `row_id,text,len` in UTF-8 CSV. Malformed records and text outside the ASCII width-10 contract are rejected. Character strings remain decoded values; CSV quoting and record delimiters may differ from the input while field bytes are preserved with the required padding.

Acceptance is limited to these 20 tested rows plus the empty input and the supplied bounded semantics. A SAS run on the same descriptor and witnesses could strengthen or overturn the cross-runtime interpretation. Wider character encodings, other SAS programs, numeric-to-character coercion, SAS dataset metadata serialization, and oversized text are outside this conversion's scope.
