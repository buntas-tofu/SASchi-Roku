# Width translation report

Status: bounded candidate translation and target-runtime observations, not live-SAS equivalence or a SAS-binary reader. The parent evaluator and principal may use this delivery for independent acceptance. No production acceptance is asserted. Observed scope: 10 supplied input rows across five cases, plus two supplemental rows. A SAS execution receipt or a counterexample could change this assessment.

## Scope and authority

The immutable request, schema and source in `packet/` define the task. The two supplied skills are initial workflow guidance. Public SAS documentation is candidate supporting evidence for the source interpretation; the trace below is explicitly an inference from source and documented language rules. No prior trials, acceptance truth, sibling repositories or corpus answers were inspected.

The delivered implementations specialize the two supplied DATA steps. They do not parse arbitrary SAS. `descriptor` is the requested companion table, not an invented third DATA step. Both `stage` and `want` are returned as independent output tables. Modifying `want` cannot retroactively change the stage values.

## Derived compiled attributes

The following widths are source-derived inferences, encoded once per implementation as compiled program attributes. They do not depend on input values, branch execution, case names or row count.

| Table | Column | Bytes | Source derivation |
| --- | --- | ---: | --- |
| stage | short | 3 | Explicit LENGTH before SET |
| stage | joined | 6 | Explicit LENGTH before SET |
| stage | tag | 1 | First lexical assignment has literal `Y` |
| want | short | 5 | Explicit LENGTH before SET overrides incoming width 3 |
| want | copy | 2 | Explicit LENGTH before SET |
| want | wrapped | 8 | Explicit LENGTH before SET |
| want | joined | 6 | Inherited from stage |
| want | tag | 1 | Inherited from stage |

This is exactly the descriptor row order: character columns in source KEEP order, stage then want, excluding `row_id`. Eight rows remain for empty input. Metadata fields `table` and `column` are variable-length companion labels, not SAS DATA-step character variables requiring their own recursive descriptor rows. `bytes` is numeric.

SAS establishes character attributes from the first occurrence and pads or truncates assignments on the right. A branch does not defer this compile-time decision. The first physical row may therefore take the false branch and still produce one byte `L` from `LONG`. [SAS: Ways to Create Variables](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000695113.htm)

The declared character length applies to both the program data vector and stored output. [SAS: LENGTH Statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p1hgqgmxm3dpqcn1d4w5za5qbz0d.htm)

## Independent source trace

Inference, established before target execution: `short=raw` retains the first three bytes, including blanks. `short || suffix` concatenates all three and two bytes, then the six-byte target supplies one final blank. Concatenation does not trim either argument. [SAS: Concatenation Operator](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000780367.htm)

At the second SET, the three-byte stage short is padded to five bytes. `copy=short` keeps the first two. `short=short || '!'` constructs six bytes and loses the final exclamation mark on assignment to five bytes. The three bytes already lost from raw are never recovered. Brackets around all five short bytes occupy seven bytes; wrapped adds one final blank to reach eight.

`n` is the rightmost nonblank position, with a minimum of one. `z` is the same position, with zero for an all-blank value. These are numeric values, not physical descriptor widths. [SAS: LENGTHN Function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p0z9e0q6e8snidn1t9m5pysmkl79.htm)

In these trace tables only, `·` denotes one ASCII space. It is never written as a replacement character in target data.

| row_id | stage.short | stage.joined | stage.tag |
| --- | --- | --- | --- |
| 0007 | ABC | ABCZ·· | L |
| NA | ·A· | ·A·Q?· | Y |
| x3 | ··· | ······ | L |
| x4 | A"B | A"B·!· | L |
| x5 | XY· | XY·R·· | Y |

| row_id | want.short | want.copy | want.wrapped | n | z |
| --- | --- | --- | --- | ---: | ---: |
| 0007 | ABC·· | AB | [ABC··]· | 3 | 3 |
| NA | ·A··· | ·A | [·A···]· | 2 | 2 |
| x3 | ····· | ·· | [·····]· | 1 | 0 |
| x4 | A"B·· | A" | [A"B··]· | 3 | 3 |
| x5 | XY··· | XY | [XY···]· | 2 | 2 |

Want inherits each row's joined and tag unchanged. Boundary rows independently give short `AB·`, `ABC`, `ABC` in stage, and `AB···`, `ABC··`, `ABC··` in want. The single false-branch row gives stage tag `L` and want n=z=1. The blank case gives n=1 and z=0. Empty input produces zero stage and want rows plus all eight descriptor rows. Literal hand-trace values for every supplied row are in `selftest.py`; the converters never import them.

## Interchange contract

Input is decoded synthetic data, not bytes extracted from a SAS file. Raw is exactly six physical bytes and suffix exactly two, with supplied padding already present. Values are printable ASCII 0x20 through 0x7e only; byte count equals character count in both implementations. No decoding replacement, normalization or trimming is performed. Invalid widths, NUL, controls, non-ASCII text, missing identifiers and flags outside numeric 0 or 1 are rejected. Base R strings cannot represent embedded NUL; the CLI rejects NUL bytes before parsing.

`row_id` is opaque nonempty text. Its complete spelling, including `0007`, `NA`, quotes, commas and surrounding spaces, survives unchanged. Identifiers need not be unique, and are not used as row keys. Input row order determines both output row orders. All other DATA-step text values physically include their full declared width in Python `str`, R character columns and reopened CSV fields. An all-blank character value is a sequence of spaces, not a null or an empty string.

Python returns an insertion-ordered dictionary with `stage`, `want`, `descriptor`; table values are lists of new dictionaries in schema order. Empty data tables are `[]`. R returns a named list of data.frames in the same order, with character text columns and numeric n, z and bytes columns. Empty R tables retain all column types. Inputs are not mutated and every call has fresh output and descriptor objects.

CSV is ASCII with a header, comma delimiter, doubled quote escaping and LF record endings on output. Quoting strategies differ between writers, so comparison is on exact reopened fields and types, not whole CSV byte equality. Numeric outputs use ordinary decimal fields. Numeric missing would use a blank field, represented by Python None or R numeric NA, but the admitted program has no numeric missing inputs or outputs; no special missing-tag preservation is claimed. Text `NA` remains text. Readers disable text missing-value inference and whitespace stripping.

The three output files form one companion set. Descriptor rows identify table and column, not business identifiers. Tests check the complete table schemas, exact values, row order, numeric values, widths and descriptor contents together. There is no persisted cryptographic pairing field in the requested descriptor schema, and standalone consumers do not automatically detect a swapped descriptor. The receipt hashes identify source and code for this bounded test; downstream consumers must keep the three outputs together and validate the expected descriptor before use.

CLI destinations must not exist. Existing files and directories are rejected without changes. Imports and R source calls do not run the CLI. Input validation precedes output directory creation. A filesystem failure during writing may leave a newly created partial directory; no transactional commit behavior is promised.

## Execution evidence

Observed environment: Python 3.12.3, standard-library csv reader/writer; R 4.3.3 (2024-02-29), base R and utils CSV functions. No added packages. The model revision, model sampling settings and SAS runtime version were not exposed and are not asserted.

Exact comparisons are appropriate because all operations are bounded ASCII copying, padding, truncation, branch selection and integer lengths. No approximate tolerance was used. The independent oracle is the source-derived literal hand trace, not captured SAS output. Python and R agreeing alone is not treated as sufficient evidence.

The first self-test run passed:

- All five supplied cases, 10 source rows, matched the literal trace through Python API, R API and both CLIs.
- Both Python and R consumers reopened every successful CLI output and checked all contents, headers, types and widths.
- Two supplemental rows used a duplicated identifier containing every printable ASCII character plus a trailing space. Quote/comma escaping and literal NA text survived.
- Empty calls around populated calls retained empty schemas, descriptor rows and fresh state. Input objects remained unchanged.
- All 10 existing-directory and all 10 existing-file refusal checks preserved destination bytes.
- Seven invalid-input cases failed before directory creation in each CLI; seven Python API and six R API invalid-input cases also rejected.
- Eight deliberately wrong result mutations were detected: tag widening, joined padding loss, retained exclamation mark, recovered raw characters, copy widening, trimmed wrapping, and incorrect blank n and z.

No target comparison failed and no converter repair was made before first delivery. Linter result and exact invocation history are recorded separately in `history.md`.

## Run

From this isolated workspace, using new output paths:

```sh
python3 -B output/converted.py packet/cases/main scratch/example-python
Rscript --vanilla output/converted.R packet/cases/main scratch/example-r
python3 -B output/selftest.py
```

The self-test creates temporary directories under `scratch/`, removes them, and does not retain caches. The first two example commands are documented invocations, not additional executed tests.

## Remaining limits

No SAS runtime was available; compile-time interpretation, descriptor choices and source-to-target behavior remain pending direct SAS validation. There is no SAS binary reader, Parquet path, encoding discovery, arbitrary Unicode support, special numeric missing tagging, labels, formats, informats or catalogs. Numeric precision beyond this binary flag and small length domain is untested. Physical column order follows the explicit task schema and KEEP-order requirement, rather than an assertion about SAS internal descriptor ordering. This is a translation of the supplied bounded source, not a general SAS translator.

## Receipt identities

SHA-256 of the exact files inspected or executed:

```text
184dcc3afd7252fef7688bf97ee4d4266f92a5d5d8d58cb0c00505a27bf2d199  packet/AGENTS.md
cdc61b0e401ed710bb2bfd86823d02ccbbabc31c723843f56ebd354429c7a4b3  packet/cases/blank/have.csv
aee4571d6a06e913055826086ad1fea93ecc52b6824ae5f8861ee1b8a763909e  packet/cases/boundary/have.csv
c59ac22f89ff62f74a88602c09aa083c28489dbb358f56e4622957b8a8ca7ff4  packet/cases/empty/have.csv
6084dfae62b50e79c47fff420991e16fc33335ff9a63fabc75ee455281d03c22  packet/cases/main/have.csv
8527d0e098c401b27b46fd02c89b7b7e1098e4d8a096612e658b4addd7aaf9ac  packet/cases/single-false/have.csv
86bf6b0a1232e9bdf801bcd89962756a4d8f7c173be1197094a098dc9ce78a7e  packet/request.txt
6e10565bf4ad0de0f661319218d16ca1b6e4b0752376bab5a21db2669b9ce4e1  packet/schema.csv
6c64545c5d511723c3c64c118afaefa7466f24c4961a2e012065fe27a0806b76  packet/skills/sas-define-interchange/SKILL.md
a33bb7bab10e506c5822a1bc7b9554f346811ff2b114f0ddf2aeb3b9afa49580  packet/skills/sas-define-interchange/references/representations.md
6cdb948823b5fb1caccfee7c3c4754892bdb617a0b7da526272bbd21220ac91c  packet/skills/sas-translate/SKILL.md
da999e1e82759c319fa51ca39c221c72e0bf3637bfacf303e2043abb861e949e  packet/skills/sas-translate/references/evidence.md
1707c2d50610cb28583731c1c275689c46ee6759f54414ec3b25541ecb60c64e  packet/source.sas
37144f568a20a7aad8ee12edb0c320188088cb701f549ca168afda175ea2520c  output/converted.py
a65a2d287fa409229943ae63492ebd650dcc1dcfb42bd97f2af3596d19753581  output/converted.R
09d56e6bf2713aae85d4f3ea1567f1be7761d90ac1c8d37c5d751e31c5673a7a  output/selftest.py
797f9a0f53cc48ca9658aa1e0ec6bdace4e7182f58748925dae5caf189d859dd  output/selftest.R
```
