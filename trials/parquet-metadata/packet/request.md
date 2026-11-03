# Preserve this decoded dataset through Parquet and a base R bridge

Status: bounded engineering evaluation of existing interchange skills. This is
synthetic decoded input, not a SAS binary or live-SAS reference result.

Use both supplied skills. Deliver `converted.py`, `consume.R`, `report.md`,
`history.md` and any self-tests in the designated output folder. Preserve first
failures and repairs in the history. No new skill or generic converter is requested.

## Source and policy

The JSON cases contain an ordered descriptor and row arrays. The two character
columns carry exact source bytes as `{ "hex": "..." }`. Their byte lengths must
equal the declared widths, including padding. Decode strictly with the named
source encoding. Preserve Unicode normalization, NUL, controls and all blanks.
Encode/decode reversibly: no trimming, replacement, inferred identifier types or
format-to-value conversion. The scope admits utf-8 and latin-1 encodings only.

The numeric columns carry finite binary64-compatible JSON numbers or
`{"missing":"tag"}` with one of `.`, `._`, `.A` through `.Z`. Booleans are
invalid numbers. The date column carries integral source days since 1960-01-01
or the same missing objects. No timezone is asserted for `stamp`; preserve its
numeric source seconds and descriptor. Retain signed zero. Preserve every
descriptor property exactly, including null versus empty string, labels,
format/informat names and the status value-label mapping. Duplicate business IDs
are intentional; cell identity is zero-based row position plus column name.

The ordered Parquet schema is `id: string`, `text: string`, `value: double`,
`date: date32[day]`, `stamp: double`, `all_missing: double`, `status: double`.
Apply that schema to empty and all-missing cases too. Represent numeric/date
missing cells as Parquet null plus a per-cell tag in the companion. No numeric
value or character payload may be duplicated into the companion as a substitute
for reading the actual Parquet file.

Write `data.parquet` and `metadata.json` into a new directory. Metadata requires
`version` = 1, `policy` = `preserve-v1`, `source_format`, `encoding`, `columns`
(the exact descriptor), `row_count`, `source_sha256` (the exact input JSON bytes),
`parquet_sha256`, `missing_tags` (ordered row-major objects with `row`, `column`,
`tag`), and `versions` identifying Python and PyArrow. Other fields are allowed
only when they do not copy row values. Unknown metadata remains null.

## Python interface

`convert(source_path, destination_dir)` writes the bundle. CLI usage is
`python converted.py SOURCE_JSON DESTINATION_DIR`. Refuse an existing destination
without changing it. Invalid inputs must fail before creating the destination.

`validate(bundle_dir, expected_source_sha256)` raises on a wrong source identity,
a changed Parquet hash, absent or malformed required metadata, wrong ordered
schema, row count mismatch, duplicate/out-of-range/unknown tags, or a tag on a
non-null cell. Every numeric/date null must have exactly one valid tag.

`restore(bundle_dir, expected_source_sha256)` validates first, reopens actual
Parquet bytes and returns the original source object: source_format, encoding,
columns and rows. Restore dates to original day counts, text to original encoded
hex bytes and missing objects to original cell positions. It may not read the
source JSON or depend on the original path. Both API functions accept Path or
string arguments. `convert` and validation may return None or useful evidence.

## R interface and boundary

Base R has no Parquet dependency in this environment. A frozen parent adapter
will reopen the actual Parquet and companion, then export three CSV tables.
Your `consume(bridge_dir)` function in `consume.R` consumes these tables. Do not
claim direct R Parquet or SAS-binary reading.

`cells.csv` has columns `row,column,kind,value,tag`. Each row is one cell, in
row-major order. `row` is zero-based. Kinds are `text_hex` (UTF-8 bytes from the
reopened string), `float64_hex` (eight little-endian IEEE bytes), and `date_iso`
(YYYY-MM-DD). Null numeric/date cells have empty value and a missing tag. Text
never has a tag. Empty data has a header and zero cell records.

`columns.csv` has `column,property,type,value`, for every descriptor property
except name and value_labels, plus the source encoding per column. Null has type
`null` and empty value; numbers are decimal with type `number`; strings have type
`string` and UTF-8 hex value. `labels.csv` has `column,value_hex,label_hex` using
binary64 little-endian hex for raw values and UTF-8 hex for labels. All CSVs use
ordinary RFC-style quotes, UTF-8, no implicit NA spellings, and include headers.

Return a list with `data`, `tags`, `metadata`, `labels`. `data` is a named list in
schema order. `id` is a character vector (keep zeros and padding); `text` is a
list of raw vectors (including NUL); `date` is a Date vector; every other column
is double. Tags are a data.frame with row, column, tag; metadata and labels are
the corresponding CSV tables as character data.frames, preserving values.
For empty data return all seven correctly typed zero-length vectors. `consume.R`
must be sourceable without automatically running a CLI. No packages beyond base
R are available. Raw `text` is a deliberate representation, not ordinary R text.

## Deliver and report

Exercise supplied valid and invalid cases. Include runtime versions, primary
reader/writer documentation, commands and observed results. Distinguish your
self-tests from the independent parent acceptance. Do not browse any parent
oracle, comparator or files outside the packet except installed dependencies
and primary documentation. Write only to the designated output and temporary
self-test directories. Do not modify this packet or access the repository.
