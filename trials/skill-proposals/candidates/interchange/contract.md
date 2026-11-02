# Synthetic envelope interchange contract, version 1

Status: local engineering contract for the supplied synthetic decoded envelopes.
It is not a SAS binary reader contract or Parquet preservation result. The task
owner may use the implementation and evidence to evaluate this CSV adapter.

## Source boundary and authority

The supplied request, skill, reference, `main.json` and `empty.json` ground this
contract. The envelopes already contain an identifier string, hexadecimal text
bytes, numeric values or explicit missing tags, and a descriptor. Their bytes
are not evidence of any SAS file reader's behavior.

The implementation accepts UTF-8 JSON envelopes with a descriptor and row list.
Supported source text encodings are `windows-1252` and its `cp1252` alias, matched
case-insensitively. Other encodings are rejected, including recognized encodings
outside this deliberately bounded adapter. JSON property names must be unique;
nonfinite constants are rejected. Supplied descriptors have four ordered
columns: id, text, amount and event_day, with character, character, numeric and
numeric source types respectively. Character widths must be nonnegative integer
byte counts. The event_day descriptor must supply a nonempty unit string.

All descriptor properties are carried unchanged as JSON values, including
unknown additional properties. Null remains null. In these fixtures the id
width is 4 bytes and text width is 6 bytes. Labels, formats, informats, the raw
day unit, null timezone, unavailable catalog and null value-label mapping are
retained. `VALUEFMT.` is a format name, not available catalog content. No label
mapping or timezone is inferred.

## Bundle and physical representation

The new destination contains three files:

* `data.csv`: UTF-8 without BOM, comma delimiter, double-quote quoting with
  doubled interior quotes, minimal quoting, and CRLF record terminators.
* `metadata.json`: UTF-8 JSON containing exactly source_sha256, data_sha256,
  descriptor and rows. Descriptor properties are retained, not reconstructed
  from a subset of fields.
* `source.json`: an exact byte-for-byte copy of the input envelope. This retains
  the full original envelope, including lexical spelling, whitespace and any
  additional envelope or row properties outside the CSV projection.

The CSV column order is always `row_no,id,text,amount,event_day`, including on
empty input. The source row-list order is the output order. `row_no` is the
supplied integer position key, not a generated sequence or a sorting request.
It must be unique. Negative or noncontiguous integer positions are admissible;
booleans are not positions. Duplicate business identifiers are admissible.

| Column | CSV representation | Meaning and restoration |
|---|---|---|
| row_no | Integer decimal text | Position key; never identified by id |
| id | Text | Leading zeros and spaces retained; import as character |
| text | Decoded Unicode text or empty fallback cell | Companion decides the representation; every cell retains source hex |
| amount | Finite JSON numeric value rendered as decimal text, or empty | Nonmissing stays numeric logically; companion restores each missing tag |
| event_day | Finite JSON numeric value rendered as decimal text | Raw count in supplied units; no calendar or timezone conversion |

CSV has no intrinsic schema. Consumers must apply these column meanings rather
than infer identifier types or missingness from displayed values. Numeric values
are parsed with Python integers and Decimal, without an intermediate binary
float. Empty numeric amount cells denote tagged missing values. An untagged JSON
null or string amount is rejected. Supported original tags are `.`, `._` and
`.A` through `.Z`. The ordinary missing tag `.` remains distinct from the special
tags. This adapter requires nonmissing numeric event_day values because the
provided envelope has no companion field for event-day missing tags.

## Byte and text policy

All byte values 0x00 through 0xFF are admitted within `text_hex`, subject to the
descriptor byte width. Hex must be contiguous complete pairs. Width counts
source bytes before decoding. Values shorter than the descriptor are retained
as supplied, with no invented padding. Values longer than the descriptor are
rejected. Whitespace is never trimmed, normalized or replaced.

Decode strictly using Windows-1252. A successfully decoded string without NUL
uses `text_mode: "decoded"`; all representable controls remain decoded,
including CR, LF, CRLF, tab, other non-NUL controls and trailing spaces. CSV
quoting protects separators, quotes and line breaks. No Unicode normalization,
newline normalization, replacement decoding or backslash interpretation occurs.

A NUL-containing value or a value that cannot decode strictly uses
`text_mode: "raw"`; its CSV text cell is empty. The complete original bytes remain
in `text_raw_hex`, using lowercase pairs with no prefix. Undefined Windows-1252
bytes are 81, 8d, 8f, 90 and 9d. In a multi-byte value, one such byte makes the
entire cell raw. NUL similarly makes the entire cell raw. No row is dropped.

For every row, including decoded text and empty text, the metadata row contains:

```json
{"row_no": 1, "text_mode": "decoded", "text_raw_hex": "410d0a422020", "amount_missing": null}
```

`amount_missing` is JSON null for nonmissing amounts and the exact supplied tag
otherwise. Empty decoded text is distinguishable from raw fallback by text_mode;
empty numeric cells are interpreted using amount_missing. Missing-like literal
strings such as `NA` remain text. A raw fallback is a transport representation,
not a missing text value.

Base R character strings cannot contain embedded NUL, so a raw cell must remain
an associated raw vector or hex payload rather than being forced into a character
column. This boundary is documented by [R's character literal reference](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html).
For id, which has no requested raw fallback companion, NUL, unencodable text and
descriptor-width violations are rejected. Identifier strings stay strings.

## Identity, validation and reversal

Hashes are lowercase hexadecimal SHA-256 digests over the exact source-envelope
bytes and exact CSV bytes, respectively. Metadata row order matches CSV order,
and each row_no binds text mode, raw bytes and the amount tag to its source row.
The original source remains untouched.

`build` first checks that the destination does not exist, parses and validates
the entire source, and constructs the expected projection in memory. Unsupported
encoding, excessive text width and duplicate positions fail before output
creation. Existing files, directories and symlinks at the destination are
rejected. The parent directory must already exist. An exclusive directory
creation prevents overwriting an existing destination. Build writes the bundle,
then invokes the same full check on the reopened files. A caught build failure
removes its newly created incomplete destination.

`check` is read-only. It independently derives the required projection from the
supplied source, verifies both hashes, compares every descriptor property and
metadata row with types and associations intact, compares the archived source
bytes, reparses the actual CSV, compares every field in order, and verifies the
canonical CSV bytes. Linked bundle files and a linked bundle directory are
rejected. Hashes alone are insufficient: data and metadata must agree with the
supplied source. Equivalent CSV spellings outside the specified canonical writer
output are deliberately rejected.

To restore the text bytes, decode text_raw_hex into bytes for every position.
For decoded cells, strict encoding of the CSV string must agree with those bytes;
for raw cells, keep the hex or bytes outside ordinary character storage. Restore
each amount either from its numeric CSV cell or from its amount_missing tag.
Keep id as text and event_day as a raw number with the descriptor units. The
original source envelope itself is restored exactly by copying source.json after
validation. The archive is additional evidence, not a replacement for checking
the CSV and metadata projection.

Use a CSV reader that retains embedded newlines and spaces. Python's reader is
opened with newline translation disabled, following the [official CSV documentation](https://docs.python.org/3/library/csv.html).
In base R, explicitly import identifiers and ordinary text as character, retain
raw fallbacks separately, and avoid automatic missing-string conversions. This
delivery does not include or certify an R importer.

## Commands and limits

From the evaluation folder:

```sh
python3 output/bundle.py build packet/main.json NEW_DIRECTORY
python3 output/bundle.py check packet/main.json NEW_DIRECTORY
python3 output/bundle.py build packet/empty.json ANOTHER_NEW_DIRECTORY
python3 output/bundle.py check packet/empty.json ANOTHER_NEW_DIRECTORY
python3 output/test_bundle.py
```

Python 3.11+ and the standard library are required. The executed runtime is
recorded separately in the test receipt. A successful command emits a JSON
summary; validation errors return a nonzero exit code and an error message.

This implementation is an in-memory fixture adapter. It does not establish
streaming behavior, crash-atomic publication, resistance to concurrent hostile
filesystem changes, SAS binary reading, catalog recovery or Parquet preservation.
The hashes bind supplied bytes; they do not authenticate the source's origin.
Automatic conversion to base R doubles could round numeric values beyond that
runtime's precision, so the CSV decimal representation and source archive remain
the exact transport evidence. No arbitrary-precision base R importer is supplied.
