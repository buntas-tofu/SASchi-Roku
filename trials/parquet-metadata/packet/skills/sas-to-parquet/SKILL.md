---
name: sas-to-parquet
description: Convert SAS datasets or transport files to Parquet with an explicit policy for types, labels, formats, dates, encodings and missing values. Use for data interchange, not translation of a SAS program into executable Python or R.
metadata:
  status: initial-guidance
---

# SAS dataset to Parquet

Status: initial interchange workflow for engineering use. No converter or universal
metadata-preservation guarantee is bundled with this skill.

Identify the actual source format, accompanying catalogs, encoding, size and
destination. Distinguish `.sas` program text from `.sas7bdat` data and transport
files. Inspect descriptors before conversion. Do not infer an identifier's type
from its first rows or turn formatted display text into stored values by accident.

Read [the preservation contract](references/preservation.md). Establish explicit
handling of column names/order, numeric and character types, widths, labels,
format/informat names, value labels, dates/times, tagged missing values and
source encoding. Mark unavailable metadata as unknown. Do not invent a timezone
from a date display or silently collapse distinct missing tags.

Use the user's Python or R environment where practical. Check the selected reader
and Parquet writer's current primary documentation and installed versions. Select
based on the actual input format and metadata needs. Avoid promising catalog or
special-missing support merely because a reader accepts the file extension.

Write into a new output location. Retain metadata that the chosen path cannot
round-trip in an explicit companion file or representation, with its association
to the source and output. A sidecar that merely lists tag names cannot restore
per-cell missing tags; the representation must identify their positions or stable
row/column keys. State any intentional loss and obtain agreement before applying
it when it changes the requested result. Keep source files intact.

Reopen the written Parquet and companion metadata. Compare row counts, ordered
schema, typed values, null/tag counts, date values and relevant metadata under the
declared policy. For large data, distinguish complete chunked validation from a
sample; a sample is not whole-file proof. Include edge cases for empty tables,
all-missing columns, leading-zero identifiers and multibyte text when applicable.

Deliver the data, companion metadata, source/output hashes, library versions,
preservation policy, validation scope and observed differences. A file that opens
successfully is not enough evidence for a claim of lossless conversion. If required
metadata cannot be recovered, explain the gap instead of calling the output exact.
