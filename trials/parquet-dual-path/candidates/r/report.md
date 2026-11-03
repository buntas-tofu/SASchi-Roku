# Native R interchange trial

Status: executed engineering observation on five supplied synthetic envelopes and two pinned SAS files, exercised in three SAS configurations. Maintainers may review and rerun this evidence. This is not a universal SAS preservation claim, live SAS execution, or authorization to publish results as an official finding. Changes to inputs, readers, formats, or runtime require renewed validation.

`convert.R` performs conversion and validation in R with Arrow 25.0.1, Haven 2.5.5, jsonlite 2.0.0, and R 4.4.3. It invokes only `sha256sum` for hashing. The converter has no network operations, Python bridge, installation step, or dependency on the self-test consumer. Model revision and settings were not exposed.

## Interface

```text
/tmp/roku-interchange-runtime/bin/Rscript output/convert.R convert INPUT NEW_OUTPUT_DIRECTORY [--catalog CATALOG]
/tmp/roku-interchange-runtime/bin/Rscript output/convert.R validate INPUT OUTPUT_DIRECTORY [--catalog CATALOG]
```

SAS7BDAT is selected by its extension, case-insensitively; other inputs are parsed as JSON envelopes. Basenames and case identifiers do not choose policies or expected values. A destination must not already exist, including a dangling symlink. Envelopes, reserved names, descriptors, physical byte lengths and cells are checked before directory creation. A failed conversion removes its newly created output. Validation performs no output writes.

## Preservation boundaries

The source directory retains exact bytes of the input, the supplied catalog, and a sibling LICENSE when present. SHA-256 entries bind their roles and relative paths. The fixture LICENSE is copied unchanged with the SAS source. No upstream binaries are delivered in this source-code submission.

For envelopes, archival character hex is the complete supplied physical bytes, including padding, invalid byte sequences and NUL. This boundary is declared `exact-envelope-bytes`. For SAS, archival hex encodes Haven's decoded strings as UTF-8 and is declared `reader-utf8-reencoding`. It does not recover source padding, source bytes, or source codec identity. The retained SAS binary provides that original-byte boundary.

Archive numeric columns are float64 in SAS units. A string column immediately after each numeric holds either the canonical missing marker or an empty string. Missing numeric values are physical nulls. Stable int64 row positions, including rows sharing business identifiers, associate tags and events with cells.

Analysis decodes strictly and trims only trailing ASCII spaces. Leading spaces, literal NA, CR/LF, punctuation and Unicode remain text. NUL takes precedence and maps to null with `embedded-nul`; invalid decoding maps to null with `decode-error`; all-blank maps to null with `blank-to-null`; nonempty right-trimmed text records `right-trim`. Undefined CP1252 bytes are explicitly rejected as decoding errors instead of relying on platform replacement behavior. Events are in row-major source-column order, with one action per affected cell. Numeric null events contain their original marker, including ordinary `.` and `._`.

Finite declared dates become date32 after converting the SAS 1960 origin to the Unix epoch. Finite datetimes become timezone-free timestamp(us), rounded to the nearest microsecond; R's rounding determines ties. Time remains float64 seconds. Ordinary numeric values remain float64. Date and datetime events record these conversions. Values never become their catalog display labels. No source timezone is inferred from Haven's UTC display attribute.

## Descriptor availability

Envelopes retain the supplied ordered descriptor objects, including widths, labels, formats, informats, origin, units and value labels. Empty envelopes retain the same typed schema. SAS descriptors preserve available names, order, labels, `format.sas`, and catalog value labels. Tagged label keys are canonicalized, for example `.A`. Widths, source encoding and informats are unavailable through the selected Haven path and remain null. They are not estimated from values or format widths.

The SAS logical profile explicitly recognizes DATE and YYMMDD date formats, DATETIME datetime formats, and TIME time formats, with their supported width/precision suffixes. Other formats remain ordinary numeric; the converter does not guess from names. Haven's Date/POSIXct epoch adjustment is reversed for archive values. Metadata includes explanatory gaps and the format-profile interpretation. Unexposed descriptors and catalogs beyond the supplied fixture remain untested.

## Association and validation

Both schemas contain the required source hash, optional catalog hash, mode and schema version. The sidecar lists source identities, both output hashes, library versions, descriptors, normalization events and fidelity. Validation reads the external source again, reconstructs both complete typed projections, reopens the actual Parquet, checks complete ordered schema and schema metadata, compares every typed value and null position, checks retained source hashes, and compares the source-derived sidecar including fresh output hashes. Updating hashes after changing values does not satisfy the projection comparison.

## Executed evidence

The final R self-test regenerated and fully validated all eight configurations: five envelopes, the sample SAS file, and missing-value SAS with and without its catalog. Tests also covered a legal column name overlapping an Arrow API argument. No validation was sampled.

The mutation suite rejected changed values and reordered rows in each projection, wrong physical row-index type, collapsed missing tags, wrong date origin, altered descriptors, a swapped sidecar, changed retained source, wrong external source with the same basename, corrupt Parquet with refreshed hashes, existing output destinations, and seven invalid envelope variants. Value, row-order, missing-tag and date attacks preserved the expected schema metadata and refreshed the output hash, so their failures exercised source-derived data comparisons. Hashes before and after valid validation were unchanged.

A separate Python consumer using PyArrow 25.0.1 compared every archive and analysis value, all types, events and association fields for all five envelopes against independently constructed source-derived projections. PyReadStat 1.3.7 compared each SAS archive cell with reader output and checked the supplied catalog value label. This is a separate consumer and implementation path, but Haven and PyReadStat share ReadStat internally. Their agreement is not independent proof against live SAS.

The final self-test commands completed with `SELFTEST PASSED` and `INTEROPERABILITY PASSED`. The unchanged linter result is recorded in `history.md`.

## Bounds and reproduction

This is an in-memory bounded converter, not a streaming system. It supports the specified input representation and explicit format profile. Envelope dates must be integral and fit date32; envelope datetimes are restricted to the exact native integer-microsecond range. R double arithmetic limits extreme or sub-microsecond timestamps. The supplied pre-epoch SAS values were exercised, but arbitrary precision or every SAS temporal format is not established. Catalog labels other than the supplied tagged label, broader encodings, large files, alternate platforms, and hostile concurrent filesystem changes remain untested.

From this isolated workspace, with no existing `scratch/`, run:

```text
/tmp/roku-interchange-runtime/bin/Rscript output/selftest.R
/tmp/roku-interchange-runtime/bin/python output/interop_test.py
python3 inertia-drift-lint output
```

The R self-test creates its eight baseline outputs in temporary `scratch/`; the Python consumer reads them. Remove `scratch/` after review. All generated data were removed before delivery. `selftest.R` and `interop_test.py` are optional test sources, not production dependencies.

Primary documentation consulted: [Haven SAS reader](https://haven.tidyverse.org/reference/read_sas.html), [Haven conversion semantics](https://haven.tidyverse.org/articles/semantics.html), and [Arrow Parquet writer](https://arrow.apache.org/docs/r/reference/write_parquet.html). The public Arrow page reported version 26.0.0; installed 25.0.1 API probes and actual execution established the behavior used here. Attempts to fetch archived Arrow 25 documentation failed; no archived-document claim is made.
