# R conversion report

Status: candidate engineering conversion for principal review and bounded use. Target execution passed 45 checks, including 8 supplied rows, 491 additional byte witnesses and 5 constructed CSV rows. This is not live-SAS equivalence evidence or approval for other programs. A SAS run against these inputs could confirm or change the semantic verdict.

The supplied request and source define the authority for this task. The source reads `work.have`, computes `len = length(text)`, and implicitly outputs each row. There are no includes, macros, retained values, filters or other source dependencies. The supplied descriptor is `row_id` width 8 and `text` width 10. The requested interchange retains `row_id` without padding.

`converted.R` provides `translate(df)` and the requested CLI. It uses only standard R facilities. It returns a new data frame with character columns `row_id,text` and a double column `len`. It pads each decoded text value with literal spaces to 10 bytes, retains that stored text, and computes the last non-space byte position with a minimum of 1. All state is local to each invocation.

The [SAS LENGTH reference](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0f6jve4kdxnh1n1m7c82fhosgih.htm) specifies byte length excluding trailing blanks and a result of 1 for blank strings. The [SAS TRIM reference](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n1io938ofitwnzn18e1hzel3u9ut.htm) documents padding when assigning a shorter value to a fixed-width character variable. These are candidate external documentation evidence, not an executed SAS result. Interpretation for the ASCII contract: a blank is byte 32; a tab is a significant byte. SAS distinguishes blanks from horizontal tabs in its [FINDC documentation](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n1mdh2gvd5potjn14jipysvzn4o7.htm).

Comparison policy was fixed before implementation: exact schema and numeric values, exact decoded character bytes including padding, row count and order, stable unpadded keys, and no caller mutation. No numeric tolerance was used. CSV quoting and line-ending syntax may differ from input, but decoded field bytes must match.

Actual execution used R 4.3.3, x86_64-pc-linux-gnu, Ubuntu 24.04.5 LTS, with `LC_CTYPE=C.UTF-8`. No packages were installed. Only base and standard R packages were loaded. Full environment output is in `self_test.log`. Its environment inspection emitted a `timedatectl` bus-access warning; the test process exited 0.

Run from this task folder:

```sh
Rscript output/converted.R packet/main.csv output/main.csv
Rscript output/self_test.R
```

Sourcing `converted.R` defines functions without running the CLI, as exercised by the test script. The normal R CSV reader normalized an embedded CRLF to LF in an initial probe, so the CLI uses a byte-preserving CSV parser. Output uses [R write.table](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/write.table.html) with UTF-8, quoted character fields, doubled quotes, and empty numeric missing cells. [R nchar](https://stat.ethz.ch/R-manual/R-devel/library/base/html/nchar.html) supplies byte counts.

Executed checks:

- All four supplied examples ran through both `translate` and the CLI. Separately derived hand lengths were main `[4,10,1]`, edge `[3,3,1,1]`, singleton `[2]`, and header-only `[]`. Standard R CSV reading independently checked their emitted results.
- Each example checked schema, row keys/order, exact input and padded output bytes, caller immutability, and repeated invocation behavior.
- An independent oracle scanned raw bytes to find the last non-space position. It agreed for 364 strings over `A`, space and tab of lengths 0 through 5, plus 127 strings containing each nonzero ASCII byte between spaces.
- A deliberately wrong `nchar(trimws(text))` variant disagreed on 428 of those 491 rows, demonstrating detection of the blank, leading-space and tab traps.
- A hand-built five-row CSV checked embedded CRLF, doubled quotes, commas, literal `NA`, and tabs. CLI output matched separately specified bytes exactly.
- The writer independently emitted a blank numeric missing cell. This source never produces missing `len`, including for blank text.
- Overwidth and non-ASCII text were rejected.

The first test run failed because the oracle's R vector acquired names from its string inputs while the output numeric vector had no names. The original log remains in `self_test.first_failure.log`. The oracle was corrected to produce an unnamed numeric vector; the comparison still uses exact identity and the conversion code did not change. The final log records 45 passing checks. Reproducible tests and CSV receipts remain under `output`.

Limits: no SAS runtime or captured SAS outputs were available, so hand truth and independent R witnesses do not prove SAS equivalence. The implementation covers this source and descriptor only. It rejects R `NA`, wrong column types or order, invalid UTF-8 keys, overwidth values and non-ASCII text rather than inventing unspecified conversion rules. Empty text represents SAS character missingness and is stored as ten spaces. R character strings cannot contain NUL, so CSV NUL bytes are explicitly rejected; this is an interface representation limit if ASCII is interpreted to include NUL. The CSV reader holds the input in memory; large-file performance was not measured. Metadata such as SAS labels, formats and physical dataset encoding is outside the requested interchange.

Source and input identities, SHA-256 of original bytes:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `packet/request.txt` | 1341 | `10185774f0c1e61a30112672fd1a4628a950ee7cbf851d4d6d846d7495eb3c6f` |
| `packet/source.sas` | 60 | `7d885ba79a895afa2efa52282ce71ba39430bcb6ff9ea6d3ddc3ca6aa4c58880` |
| `packet/main.csv` | 44 | `483076b6bee43147cccd0dd46a5c5bdee6ac1d53daae5a04ff3d4248d522c3eb` |
| `packet/edge.csv` | 44 | `bfa6fddb9a13dc93b55e13085549d9904514cda641da1ce74552039338548236` |
| `packet/single.csv` | 20 | `706575c77a29a86218f73be74bb574cd9ed15d5865e0190b09b136574b8df501` |
| `packet/empty.csv` | 13 | `2bcb01b44abe67c45803a909e9b3df30c306e0be2cb294bcdb0a256413031867` |
| `packet/skill/SKILL.md` | 2841 | `6cdb948823b5fb1caccfee7c3c4754892bdb617a0b7da526272bbd21220ac91c` |
| `packet/skill/references/evidence.md` | 1727 | `da999e1e82759c319fa51ca39c221c72e0bf3637bfacf303e2043abb861e949e` |
| `output/converted.R` | 4097 | `e10ee67efadd7ecf5ac900c1719d441872a76222a7b6dc293a53198bdb15b14b` |

Only this task's packet/output and primary public SAS/R documentation were consulted. No sibling implementation or expected-output file was read.
