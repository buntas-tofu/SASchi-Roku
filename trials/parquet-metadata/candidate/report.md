# Decoded dataset interchange report

Status: bounded candidate engineering self-test, 6 supplied valid cases and 7 supplied invalid cases. This is synthetic decoded JSON evidence, not a SAS-binary or live-SAS result. The independent parent acceptance has not been observed. Reviewers may rerun these artifacts; this report does not authorize production use.

## Delivery and runtime

`converted.py` implements `convert`, `validate`, `restore`, and the requested two-argument conversion CLI. `consume.R` defines a sourceable `consume(bridge_dir)` function. The `bundles` directory contains six actual Parquet and metadata pairs, one per supplied valid case. `bundle_receipts.json` records their source and output hashes. `selftest.py`, `consume_selftest.R`, `lint_artifacts.py`, and `selftest_results.json` make candidate validation inspectable. `history.md` preserves the execution sequence and observed failures.

Observed runtime: CPython 3.12.3, PyArrow 26.0.0, and native R 4.3.3 dated 2024-02-29. R reported `x86_64-pc-linux-gnu`, little-endian storage, and `C.UTF-8` character locale. No additional R packages were used. The installed PyArrow writer/reader docstrings and current Apache Arrow primary reference both identified the actual API used.

## Preservation contract implemented

The schema is always ordered `id:string`, `text:string`, `value:double`, `date:date32[day]`, `stamp:double`, `all_missing:double`, `status:double`. Empty input and entirely null numeric/date columns retain these types. Source characters are strictly decoded from their exact declared byte widths using only the admitted `utf-8` or `latin-1` encoding. No normalization, trimming, replacement, padding removal, identifier inference, or display-format conversion occurs. Restoration produces canonical lowercase hex for the original encoded bytes; it does not preserve the lexical casing of input hex spellings or original JSON whitespace.

Numeric/date missing cells become Parquet nulls. The companion records each tag in row-major order using zero-based position and column name, independent of duplicate business IDs. Dates use source day counts plus the constant offset -3653 to reach Parquet's 1970 epoch. Restoration uses integer day counts, including the full date32 endpoints, without converting through Python calendar-date objects. Numeric `stamp` remains double source seconds with its original descriptor and unknown timezone. Finite binary64 bits, including the sign of numeric zero, are compared after reopening. JSON integers that would lose precision when represented as binary64 are rejected. Dates have integral day-count semantics.

The exact descriptor is retained, including all properties, descriptor extensions, null versus empty strings, and the status raw-value label mapping. No character payload or numeric cell value is copied into the companion. It contains descriptor metadata, source/output SHA-256 identities, runtime versions, row count, policy, and per-cell tags.

The Parquet schema metadata additionally stores a SHA-256 digest of canonical companion content excluding `parquet_sha256`, binding descriptor and tag content to that Parquet file without a circular hash. Validation reopens a byte snapshot whose hash was checked, verifies schema and row count, and enforces exactly one valid tag per numeric/date null and no tag on a non-null cell. Restoration validates, reopens actual Parquet bytes again, and reconstructs cells without reading the source file. Hashes provide association and corruption detection, not authenticity against an adversary who can rewrite the entire bundle and its identities.

The R boundary is the specified three CSV tables. The candidate self-test adapter reopens actual Parquet and metadata to produce these tables; it is not the frozen parent adapter. The consumer returns UTF-8 bridge bytes as raw vectors for `text`, character `id`, a Date vector, double numerics, positional tags, and unchanged character data.frames for metadata and labels. For Latin-1 source text, these R raw vectors are the bridge's decoded UTF-8 representation; Python restoration recovers the original Latin-1 bytes. Empty input returns all seven required zero-length representations.

Base R cannot represent an embedded NUL inside the required character-vector `id`. The consumer rejects such IDs visibly. This limit was explicitly exercised with an additional fixture; Python preserved the same ID correctly. NUL in `text` is supported and tested. The supplied six cases contain representable IDs. The R date bridge is limited to its specified four-digit `YYYY-MM-DD` format; only Python restoration was tested at date32 extremes. No direct R Parquet reading, SAS-binary reading, catalog recovery, timezone inference, or live-SAS execution is claimed.

## Observed validation

| Supplied valid case | Rows | Preserved missing tags | Python round trip | R bridge check |
|---|---:|---:|---|---|
| all-missing | 2 | 10 | Pass | Pass |
| all-tags | 28 | 140 | Pass | Pass |
| controls | 8 | 8 | Pass | Pass |
| empty | 0 | 0 | Pass | Pass |
| latin1 | 2 | 2 | Pass | Pass |
| main | 4 | 9 | Pass | Pass |

Complete checks covered 44 rows, 308 cells, and 169 tagged nulls. All 28 allowed tag names were exercised in every numeric/date column. Exact character bytes, Unicode normalization distinctions, NUL, controls, blanks, leading zeros, duplicate IDs, numeric bits, dates, descriptors, and value labels were checked on reopened artifacts. None of these checks was sampled.

All seven supplied invalid cases failed before creating a destination: bad tag, boolean number, duplicate column, fractional date, invalid UTF-8, over-width bytes, and unknown encoding. The final self-test also passed 33 adversarial bundle rejection scenarios, each tested through both `validate` and `restore`. These included wrong identities and hashes, missing/malformed metadata, wrong schema and row counts, missing/duplicate/unknown/out-of-range/unordered tags, tags on valid cells, and corrupted bytes. Twelve scenarios were also deliberately rebound to exercise structural checks beyond companion binding.

Nine additional checks passed: existing destination unchanged; relocation and restoration after source deletion; descriptor extensions and binary64 endpoints; Python date32 endpoints; the explicit NUL-ID boundary; three malformed R bridge rejections; and the CLI. No unexpected implementation failure occurred in either complete self-test run. Expected rejection details are retained in `selftest_results.json` and the history.

## Reproduction

These are the complete self-test commands executed before delivery. Each uses a separate new directory outside the delivery tree:

```sh
/tmp/saschi-parquet-venv/bin/python selftest.py --packet /tmp/saschi-parquet-trial/packet --work /tmp/saschi-parquet-selftest-01
/tmp/saschi-parquet-venv/bin/python selftest.py --packet /tmp/saschi-parquet-trial/packet --work /tmp/saschi-parquet-selftest-02
```

Run them from the delivery folder. For a new rerun, select another nonexistent `--work` directory. The first run included five additional checks; the second added the explicit R boundary and three malformed-bridge checks. Both exited 0. Conversion CLI usage is:

```sh
/tmp/saschi-parquet-venv/bin/python converted.py SOURCE_JSON NEW_BUNDLE_DIRECTORY
```

For each valid case, the self-test internally executed the equivalent R command below against its own reopened-Parquet bridge:

```sh
Rscript consume_selftest.R consume.R BRIDGE_DIRECTORY
```

The repository's `inertia-drift-lint` executable was not installed on PATH and was not available in the permitted packet. A separate local mechanical artifact style check was supplied and run. No repository CI or independent acceptance claim follows from it.

## Primary documentation consulted

- [Apache Arrow 26.0.0 Parquet writer](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html): explicit writer version, compression, and dictionary options.
- [Apache Arrow 26.0.0 Parquet reader](https://arrow.apache.org/docs/python/generated/pyarrow.parquet.read_table.html): actual Parquet reopening, including byte-buffer input.
- [R binary input/output](https://stat.ethz.ch/R-manual/R-devel/library/base/html/readBin.html): raw-vector input and explicit eight-byte little-endian double decoding.
- [R table and CSV input](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/read.table.html): character column classes, disabled implicit NA spellings, and CSV quoting.
- [R character constants](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html): embedded NUL is unavailable in ordinary R character strings.

Both supplied skills and their preservation/representation references were applied as guidance. The source request defines the bounded policy. No parent oracle, comparator, repository, sibling answer, or external project authority file was inspected.
