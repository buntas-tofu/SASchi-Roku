# Expected projections and evidence boundaries

Status: parent reference truth prepared before evaluation. Maintainers may audit
these projections against raw source and recorded runtime observations. They are
not a captured SAS execution or a validation of every reader behavior.

The five synthetic envelopes are original fixtures. Archive expected strings are
their literal hex cells, including padding, NUL and invalid sequences. Numeric
values and canonical tags remain separate in adjacent columns. Analysis truth
decodes the declared codec strictly, trims only ASCII space on the right and
records explicit null/fallback decisions. The two duplicate `0007` identifiers
retain separate ordinal positions and different missing/byte events. The main
amount column is 1.5, .A, ._, ordinary missing, -7.25. Its analytical values are
1.5, null, null, null, -7.25. The all-missing numeric column remains float64.

Main notes distinguish cafe with an accented e, quoted CR/LF text, embedded NUL,
undefined CP1252 byte 0x81 and all blanks. The UTF-8 witness includes valid snow
text and invalid 0xff. Archive truth is always the original supplied bytes;
analysis maps the unrepresentable cases to null with per-cell reasons. The empty
case retains both complete schemas and descriptor arrays.

Date calculations use Python standard-library calendar arithmetic. SAS day zero
is 1960-01-01, which is -3653 Unix days; 21310 SAS days is 2018-05-06. Datetime
seconds use the same 1960 origin. Raw seconds 0, 1.25 and -1 therefore become
-315619200000000, -315619198750000 and -315619201000000 Unix microseconds.
No source timezone is supplied, so the timestamp type has no timezone. Time-of-day
seconds remain numeric and explicitly carry their units in the descriptor.

The basic SAS fixture has a separately published human-readable CSV. Its five
numeric values are 1.1, 1.2, -1000.3, -1.4 and 1000.3; characters are a through e.
Its dates include 2018-05-06, 1880-05-06, 1960-01-01 and 1583-01-01, followed by
missing. The datetime and time spellings in that CSV supply calendar truth without
using either converter. The old date requires deliberate timestamp units rather
than an unexamined nanosecond default. CSV identity is pinned in upstream.json.

The upstream special-missing SAS source explicitly assigns .A, .B, .C, .X, .Y,
.Z, ._, ordinary missing and 1 to var1 through var9. It declares format A on
var1 and a catalog label mapping .A to missing. This provides literal expectations
for per-cell tags and the known label. One invocation omits the catalog to expose
that unavailable value-label context. Source and CSV identities are recorded in
upstream.json; only the binary inputs and license are supplied to evaluators.

Descriptor formats, storage widths and encoding for the actual SAS files were
inspected with the installed reader before dispatch. These are reader observations,
not independently decoded binary descriptors. Python exposes UTF-8 and widths;
haven does not expose all those attributes. Null values with explicit gaps are
accepted where that R reader lacks a field. Both share ReadStat, so cross-reader
agreement cannot independently establish source metadata. The byte-identical
retained source remains the archival evidence for unavailable information.

Before dispatch, both parent consumers reopened tables built from the expected
projections for all eight cases, including zero rows and old dates. That checked
the adapters and exact comparator, independently of candidate implementations.
The parent oracle, adapters and this derivation are withheld from evaluators.

Primary implementation references:

- [PyArrow Parquet I/O](https://arrow.apache.org/docs/25.0/python/parquet.html).
- [Arrow R Parquet reader](https://arrow.apache.org/docs/25.0/r/reference/read_parquet.html).
- [haven SAS reader and labels](https://haven.tidyverse.org/reference/read_sas.html).
- [pyreadstat pinned reader documentation](https://github.com/Roche/pyreadstat/blob/e6e23bc0021875f35fccc3c2707c3e5151c130bb/README.md).
- [upstream license](https://github.com/Roche/pyreadstat/blob/e6e23bc0021875f35fccc3c2707c3e5151c130bb/LICENSE).
