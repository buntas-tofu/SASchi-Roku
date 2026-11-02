# Dual-path interchange contract

Status: approved archival and analytical direction for a bounded engineering
trial, 2026-11-02. Maintainers may review the executed evidence. This contract
does not establish general SAS fidelity or live-SAS execution.

## Inputs and retained source

Accept a supplied synthetic JSON envelope or SAS7BDAT file. An optional SAS7BCAT
catalog belongs to the SAS input. The JSON format supplies ordered descriptors
and rows: character cells contain lowercase hex of complete physical bytes;
numeric cells contain either finite `value` or `missing`, one of `.`, `._`,
`.A` through `.Z`. Descriptor widths are source bytes. Empty data retains all
descriptors. Source names do not control conversion behavior.

Retain the exact input bytes in `source/INPUT_BASENAME`. Retain a provided catalog
and a sibling LICENSE similarly. This retained source is part of archival output,
not replaceable by a claim that a reader decoded everything. Record every retained
file's role, relative path and SHA-256. Do not alter the inputs. The provided
upstream fixture license applies to its retained copies. No upstream binary is
imported into the repository; the pinned fetcher verifies its identity.

## Parquet projections

Both tables start with `__row_index`, physical int64, numbered zero through n-1
in source order. Duplicate business identifiers remain duplicates. Reserve this
name and the `__sas_missing` suffix; reject conflicting input names.

Archive columns follow source order. A character column is UTF-8 Parquet string
containing reversible lowercase hex. For an envelope, these are the exact supplied
physical bytes. For SAS, encode the reader's decoded character value as UTF-8;
label this `reader-utf8-reencoding`. Do not claim recovered SAS padding or raw
character bytes. The retained SAS file supplies the original-byte boundary.
Each numeric column is physical float64 with null for missing, immediately
followed by string `NAME__sas_missing`. Its tag is empty string for a finite value,
otherwise the exact canonical missing marker. Numeric dates retain SAS units.

Analysis columns follow source order without the tag columns. Numeric values use
float64; all numeric missing markers become null, with per-cell events recording
their tags. A declared date becomes date32, using the 1960-01-01 origin. A declared
datetime becomes timestamp in microseconds with no timezone, using the SAS 1960
origin. Time-of-day retains float64 seconds and its units in metadata. Envelopes
declare logical kinds. For the SAS reader profile, recognize the supplied date,
datetime and time formats explicitly, recording that interpretation. Other
formats do not authorize guessing a date. Value labels remain metadata rather
than replacing stored numeric codes.

Decode character envelope bytes strictly with the declared codec. Embedded NUL
maps to analysis null with `embedded-nul`; decode failure maps to null with
`decode-error`. Otherwise right-trim ASCII space only. All-blank becomes null
with `blank-to-null`; a nonempty trimmed value records `right-trim` when spaces
were removed. Preserve leading spaces, literal NA, quotes, commas, CR/LF and
valid Unicode. SAS reader values use the same analysis normalization after UTF-8
encoding. CP1252 undefined bytes must reject decoding, never become replacements.

## Metadata and association

Write `metadata.json` with these required fields, allowing additional explanatory
fields: `schema_version` (1), `source_format` (`envelope` or `sas7bdat`),
`row_count`, `source_files` (ordered data, catalog if supplied, LICENSE if present),
`source_encoding`, `character_fidelity` (`exact-envelope-bytes` or
`reader-utf8-reencoding`), `catalog_status` (`provided` or `absent`), `timezone`
(null for these inputs), `columns`, `events`, `files`, and `libraries`.

Each source_files entry has `role` (`data`, `catalog` or `license`), `path`
(`source/BASENAME`) and `sha256`. `files` maps archive.parquet and analysis.parquet
to their SHA-256 strings. `columns` follows source order and includes name, kind,
logical, width_bytes, label, format, informat, origin, units, timezone, value_labels.
Preserve known values; unavailable reader metadata is null, with gaps explained.
Do not infer storage widths or encodings from observed values. Canonicalize tagged
value-label keys to SAS spellings, for example `.A`, and preserve label text.

Events are in row-major, source-column order. Each contains zero-based `row`,
`column`, and `action`. Allowed actions for this profile are `embedded-nul`,
`decode-error`, `blank-to-null`, `right-trim`, `missing-to-null`, `date-to-date32`,
and `datetime-to-timestamp-us`. A missing event also has `tag`. Record one action
per affected cell. Finite declared date/datetime cells get their typed-conversion
event; unchanged finite numeric/time values and unchanged decoded text need none.
The descriptor and fidelity declaration record the standard hex/decode mapping.

Both Parquet schemas carry string metadata `saschi.source_sha256` for input data,
`saschi.catalog_sha256` (empty when absent), `saschi.mode` (`archive` or `analysis`)
and `saschi.schema_version` (`1`). Bind metadata, retained source and both outputs
together. Reader-imposed UTC display attributes do not establish a source timezone.

## Interface and validation

Implement `convert.py` or `convert.R` for the assigned language. CLI syntax:

```text
RUNTIME CONVERTER convert INPUT NEW_OUTPUT_DIRECTORY [--catalog CATALOG]
RUNTIME CONVERTER validate INPUT OUTPUT_DIRECTORY [--catalog CATALOG]
```

Conversion writes archive.parquet, analysis.parquet, metadata.json and source/.
Refuse existing destinations without modifying them. Validate admitted envelopes
before creating an output directory. Validate must reopen and compare complete
typed projections and metadata against the supplied source under this contract,
not merely trust stored hashes. It must reject corruption, stale/swapped metadata,
reordered or changed values even when file hashes were updated, missing-tag
collapse, wrong date mapping, modified source copies and a wrong external source.
Validation makes no output changes. No network operations in delivered code.

Use the task environment's libraries. Python may use pyarrow, pyreadstat and
pandas plus standard library. R may use arrow, haven, jsonlite and their installed
dependencies plus base R; sha256sum is available for hashing. The R converter must
perform its data work in R. No Python bridge or subprocess conversion is permitted.
Both readers use ReadStat internally, so agreement is not independent SAS proof.
No package installation, git operation or further delegation is allowed.
