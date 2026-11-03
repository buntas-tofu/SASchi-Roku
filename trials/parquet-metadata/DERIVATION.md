# Parent expectations and boundaries

Status: pre-dispatch engineering derivation. The synthetic descriptor and explicit
request define the source contract; no actual SAS reader or runtime supplied it.

The oracle decodes each supplied source hex string with its declared encoding
and then records exact UTF-8 bytes. It preserves padding, NUL, CR/LF, tabs, quotes,
commas and Unicode normalization. The numeric oracle records the IEEE binary64
little-endian bytes, including the sign bit of zero. Missing objects generate
null values and one row/column tag, never a business-ID lookup. All 28 admitted
codes are enumerated. The date oracle adds the declared integral day counts to
1960-01-01: -1 is 1959-12-31, zero is 1960-01-01, 3653 is 1970-01-01 and 21915 is
2020-01-01. The timestamp column keeps raw seconds with timezone unknown.

Descriptor comparison checks the complete source list before projecting it into
the portable R bridge. This prevents the bridge's own projection from concealing
lost metadata. The R driver checks native numeric and Date types, character IDs,
raw text vectors and lengths before re-encoding values for comparison. It does
not call a candidate comparison routine. Empty data must retain the full schema.

The parent positive witnesses are built from expected cells, not from candidate
conversion helpers. A negative signed-zero witness must be rejected even after
its Parquet association hash is repaired. These checks exercise the comparator
before it sees an evaluator's output; they do not add generated implementations.

Primary documentation inspected 2026-11-02:

- [Arrow Parquet writer](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html)
  and [reader](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.read_table.html):
  actual typed file transport and reopening; not SAS preservation guarantees.
- [Arrow date32](https://arrow.apache.org/docs/python/generated/pyarrow.date32.html):
  the selected date type; source day interpretation is separately explicit.
- [Arrow string](https://arrow.apache.org/docs/python/generated/pyarrow.string.html):
  the chosen UTF-8 logical representation.
- [R character constants](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html):
  R character strings cannot contain embedded NUL; raw vectors are deliberate here.

No catalog product has been promoted to a validated SAS reader by these lookups.
This trial starts after decoding and ends at actual Parquet plus a declared R
bridge. Whole-file equality is scoped to the supplied fixtures and policy.
