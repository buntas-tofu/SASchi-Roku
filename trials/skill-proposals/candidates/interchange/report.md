# Executed interchange evaluation

Status: local synthetic-envelope adapter evidence for the task owner's engineering
review. This is not a SAS binary reader result, a Parquet preservation result or
an executed base R import. The test suite passed 53 of 53 checks; fixture coverage
is full, not sampled. Changes to the adapter, sources or consumer require renewed
validation.

## Delivered result

`bundle.py` implements both requested commands using Python standard-library
modules. `contract.md` defines the supported input, byte policy, fallback
associations, numeric and date meanings, identity checks and reversal procedure.
The demonstration bundles are `main-bundle/` and `empty-bundle/`. Each contains
data.csv, metadata.json and an exact original-envelope archive source.json.

The main fixture produces these results. Escaped control notation below is only
for reading this report; the actual CSV contains the original CR/LF characters.

| row_no | id | Text mode | Text or raw bytes | Amount | Raw event_day |
|---|---|---|---|---|---|
| 1 | `0012` | decoded | `A\r\nB` followed by two spaces | 1.25 | 0 |
| 2 | `0012` | raw | `410042202020` | missing `.A` | 1 |
| 3 | `0003` | decoded | `é` followed by five spaces | missing `.` | -1 |
| 4 | `0004` | raw | `812020202020` | 0 | 2 |

Both raw-mode CSV text cells are empty, and both missing amount cells are empty.
Every metadata row retains source text hex, mode and original amount tag or null.
Duplicate id `0012` survives; unique row_no values carry the associations. All
four event-day counts remain unchanged in days since 1960-01-01. The null timezone,
labels, formats, informats, unavailable catalog and null value-label information
remain in the descriptor without invented contents. The empty fixture produces
only the CSV header and an empty metadata row list with the complete descriptor.

## Commands actually executed

```sh
python3 output/test_bundle.py
python3 output/bundle.py build packet/main.json output/main-bundle
python3 output/bundle.py build packet/empty.json output/empty-bundle
python3 output/bundle.py check packet/main.json output/main-bundle
python3 output/bundle.py check packet/empty.json output/empty-bundle
```

All five commands exited 0. Build itself reopens and checks its written bundle.
The self-test also invokes independent `check` CLI commands. It uses a temporary
folder under output, makes only local synthetic fixture copies, and removes its
own trial data afterward. Its timestamped receipt is retained.

Executed runtime: Python 3.12.3, GCC 13.3.0, Linux x86_64 with glibc 2.39. Reader
and writer are the csv and json modules bundled with that exact Python runtime;
Decimal handles finite fractional numeric values. No packages were installed.
Test completion time: 2026-11-02T05:38:16.968580+00:00.

Evidence: `test-results-20261102T053816969817Z.json` records every test name,
outcome and rejection message, runtime details and the writer/test-runner hashes.
The executable test source is `test_bundle.py`.

## Executed coverage

| Checks | Count | Evidence |
|---|---:|---|
| Build/check main and empty | 4 | Both CLI modes pass on both inputs |
| Independent literal main/empty assertions | 2 | All fields, metadata, hashes and archived bytes compared |
| Exhaustive single-byte domain | 1 | 256 rows, all 256 byte values, six raw fallback cases, all-missing amounts, nonascending row_no order |
| Text sequences and missing tags | 1 | Nine text patterns; all 28 supported missing tags; duplicate ids; extra nested descriptor property |
| Exact numeric transport | 1 | Long decimal amount and fractional negative raw day count retained |
| Invalid source rejection | 17 | Unsupported/unknown encodings, widths, duplicate/boolean positions, invalid identifiers/hex/tags/numbers, missing units, duplicate JSON property, NaN |
| Existing destination rejection | 1 | Existing directory, file and dangling symlink retained unchanged |
| Metadata corruption rejection | 15 | Byte/mode/tag associations, positions, order, row counts, descriptor labels/units/timezone/catalog and hashes |
| CSV corruption with refreshed hash | 7 | Identifier, decoded text, numeric amount, raw date, populated fallback, populated missing value and extra reordered row |
| Cross-file/source corruption | 4 | Swapped empty companion, byte-different equivalent source, corrupted source archive, duplicate metadata property |
| Total | 53 | All passed |

The text patterns include quote/comma, standalone CR, standalone LF, CRLF, `NA`,
empty text, spaces, a tab/CRLF sequence and a literal backslash-n. Each is
reopened with newline translation disabled and compared exactly. The 256-byte
test independently expects raw fallback for 00, 81, 8d, 8f, 90 and 9d; the other
250 values remain decoded. Invalid-source tests assert that the rejected
destination does not exist. Corruption tests expect a failing CLI exit rather
than relying only on exception behavior in imported functions.

## File identity

| Item | SHA-256 |
|---|---|
| main source envelope | `e26071328bde64b7f4fdf1ffb9a672f9e0bd1cc6a41391193a3d07152c34c43b` |
| main data.csv | `9aa5179a3b043731b358450391d689c81c4579f35114757c88bb10d17cc64914` |
| empty source envelope | `d0fe0ee8e0ba24eef2f5ee4ce6e1cafbe0b441a027970fb59f545264409e21fd` |
| empty data.csv | `0fbf785c5cb9497448f80e76eee1608283497035fd333a6e15f996cfcbfac351` |
| bundle.py | `5569c90930377b5622baa7fb7cd4f117079a3e50ace6d7a09b8fcd7c8519c78d` |
| test_bundle.py | `d6712f31d8baaf19edeeb7656b87c16bf62cc99fc412634f9a6fab235f017c8d` |

## Limits and source basis

Only the supplied packet, this task's output and the primary R/Python references
were consulted. No SAS reader, binary dataset, Parquet implementation or R process
was used. The original envelope claims remain synthetic input claims, not verified
SAS provenance. The reported preservation is established for the declared adapter
and executed fixtures, not every future consumer. Python 3.11 compatibility is
the implementation target; the actual executed version was 3.12.3.

The supported encoding set is intentionally narrow. The byte-domain test is
exhaustive for individual Windows-1252 bytes, not all possible sequences. The
adapter retains exact numeric decimal text; this does not prove arbitrary-precision
numeric import in base R. No performance, concurrent filesystem, process-crash,
hostile-input resource-limit or cross-platform test was executed.

The NUL fallback follows the supplied skill reference and [R's primary character
literal documentation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html).
CSV reopening follows [Python's primary CSV documentation](https://docs.python.org/3/library/csv.html).
Those references support the representation decisions. The local files and
receipt support the executed results. CSV evidence does not demonstrate Parquet
preservation.
