# Archival and analytical Parquet interchange

Status: bounded actual-file engineering evidence for maintainer review,
2026-11-02. All 56 parent checks and ten artifact-review criteria passed.
Python and native R wrote actual Parquet and both parent consumers compared
complete reopened tables. Live-SAS execution remains pending.

The principal selected both preservation and analytical convenience. Two fresh
evaluators used unchanged sas-to-parquet and sas-define-interchange snapshots,
one assigned each writer language. All nine first-delivery files remain
byte-for-byte unchanged. Source and expected data projections were fixed before
dispatch. One parent descriptor-comparison defect was corrected transparently,
as recorded below; no candidate repair followed delivery.

## The two outputs

| Boundary | Archive bundle | Analytical table |
|---|---|---|
| Source | Exact original data, optional catalog and original LICENSE retained | Associated by source/catalog hashes and ordinal row identity |
| Text | Exact envelope bytes as hex; SAS reader strings explicitly UTF-8 re-encoded | Strict decoding and ASCII-space right trimming, with null/fallback reasons |
| Numbers and missing | Float64 source units with adjacent per-cell canonical missing markers | Float64 values and nulls, with original missing tags in the event log |
| Date/time | Raw SAS day/second values | date32 and timezone-free microsecond timestamps; time-of-day seconds retained |
| Metadata | Known descriptors retained; unavailable reader fields stay null | Descriptors, explicit mappings and ordered per-cell events in metadata.json |

Original SAS character storage and padding are not recovered from decoded reader
strings. The retained binary is the original-byte boundary. Python exposes source
widths, encoding and informats in these fixtures; the chosen haven path leaves
those properties null. Neither reader's successful parse establishes universal
metadata preservation. Both readers share ReadStat internally.

## Independent parent results

| Named parent check | Count | Result |
|---|---:|---|
| Eight cases through two writers, with Python and R consumers | 16 | 32 complete consumer comparisons passed; existing outputs refused unchanged |
| Complete source-derived candidate validation | 16 | Both projections, metadata and retained copies matched; validation made no writes |
| Corruption and stale-source controls | 16 | Both candidate validators and the independent parent rejected every control |
| Invalid envelope refusals | 8 | Rejected before output creation; source unchanged |

The five original envelope cases cover main data, zero rows, all missing, reordered
duplicate identifiers and UTF-8. They include leading zeros, literal NA, CP1252,
Unicode, NUL, invalid bytes, quotes and CR/LF. The two upstream SAS fixtures are
exercised as three configurations: basic data with dates back to 1583, and tagged
missings with and without its catalog. Every row, type, descriptor field admitted
by the reader contract, event and source/output association is checked.

Wrong-value, row-order, missing-tag and date controls refresh the output hash,
so hash checks alone cannot pass them. Other controls corrupt a Parquet file,
swap metadata, alter the retained source, and supply a wrong external source.
These are corruption controls, not additional generated converters.

Runtime: Python 3.12.16, PyArrow 25.0.1, pyreadstat 1.3.7, R 4.4.3, arrow 25.0.1,
haven 2.5.5 and jsonlite 2.0.0. Direct dependencies are pinned in environment.yml.
The prior trial jobs retain their existing runtimes. Exact machine evidence is
in [receipt.json](receipt.json); artifact criteria are in [review.json](review.json).

## Parent correction and retained histories

The initial parent oracle used null for all SAS informats. A correct Python
candidate retained informats exposed by pyreadstat. Running the original
comparator reproduced `mychar: descriptor differs at informat`. The independently
probed reader map is now required for that Python fixture; R unavailable informats
remain null. Source identities, raw values, typed projections, controls and the
original packet contract were unchanged.

[harness-correction.json](harness-correction.json) binds the correction and original
verifier. [parent-original/verify.py](parent-original/verify.py) retains its exact
pre-dispatch bytes and still matches the original freeze. The corrected verifier
checks both that original and its own correction hashes. The first complete
parent replay after this repair passed all 56 checks. This is a parent adapter
repair, not a candidate failure hidden by editing acceptance data.

Evaluator reports, self-test source and failure histories remain in candidates/.
The R writer's pre-delivery repairs include reader class handling and an Arrow
argument-name collision. Both evaluators discovered that catalog application in
a checker could replace stored tags with display labels. Their expanded tests
remain self-reported evidence outside the 56 parent checks.
The Python history retains nine literal trailing-space log lines; the whitespace
checker reports those preserved lines. Newly authored files pass that check.

## Reproduce

Use the pinned environment, then fetch the four raw fixtures into a cache:

```sh
python trials/parquet-dual-path/fetch_fixtures.py /tmp/roku-parquet-fixtures
python trials/parquet-dual-path/verify.py --fixtures /tmp/roku-parquet-fixtures
```

The fetcher checks byte length and SHA-256 and retains the exact original license.
Cached bytes need no network. Replay uses Python plus native Rscript from the
environment; `--rscript PATH` selects it explicitly. `--receipt NEW_PATH` writes a
new receipt. Keep the first recorded receipt when comparing later environments.
The installed package binaries are task dependencies, not repository-wide installs.

A local five-row example is generated in the ignored demo/ directory. It contains
archive.parquet, analysis.parquet, metadata.json and source/main.json. Its observed
identities are in [demo-receipt.json](demo-receipt.json). To regenerate when demo/
does not exist:

```sh
python trials/parquet-dual-path/candidates/python/convert.py convert \
  trials/parquet-dual-path/packet/synthetic/main.json \
  trials/parquet-dual-path/demo
```

## Provenance and limits

[upstream.json](upstream.json) pins the Roche/pyreadstat source at
e6e23bc0021875f35fccc3c2707c3e5151c130bb, with exact source and license identities.
The upstream package-wide Apache-2.0 license and bundled ReadStat MIT notice
accompany downloaded and copied fixtures. No upstream binary enters this tree.
No original-project software license was changed or release license selected.

The packet and parent truth were frozen before evaluator dispatch. The receipt
was written before this README and the local demo receipt, so its file inventory
does not include those later explanatory artifacts. Isolation was by instructions
and directories, not an OS boundary. Model revision and sampling parameters were
not exposed. Optional evaluator self-tests expect their original isolated layout;
the parent replay command works from this repository layout.

The trial is an in-memory bounded workflow. Broader SAS formats/catalogs, unknown
encodings, numeric/temporal precision boundaries, streaming scale and live-SAS
validation remain open. The explicit NUL fallback does not retroactively close
the earlier starter's R-character gap. Existing skill instructions remain initial
guidance and unchanged; the with/without repeatability study has not run.

During the trial, concurrent reference-home work was integrated from PR 5 at
c2740e1f31abf778748bed9f6970d22a5d2bafc7. Its nine governance jobs and all frozen
trial bytes were preserved; the Parquet replay is an additive tenth job. The
pull-request trigger also covers feature-branch targets so this work can be
reviewed as a separate stacked PR while PR 5 remains open. The
existing advisory MCP is separate from these file converters. The principal
subsequently approved preserving the two historical frozen citation files.
PR 5's [hash-bound resolution](../../docs/decisions/0003-frozen-citation-exceptions.md)
was integrated with its regression tests. It checks exact paths, the classified
token and original file hashes; no frozen byte changed. The initial two-finding
checkpoint is historical, and the approved resolution now applies here.
