# vendor/

Status: active. Foreign content, declared and pinned. Not governed by the DMF
style floor or pointer checks; this file is the declaration that makes that
exemption deliberate rather than silent.

Trees under `vendor/` are kept verbatim. They are exempt from `dmf-lint`
because both of its ignore lists name `vendor`. The exemption is a claim about
each entry below: it is foreign, unedited since vendoring, and pinned to a
provenance anchor. Estate-authored content never lives here.

## parquet-format-README.md and parquet.thrift

- What: the README and the Thrift IDL from the Apache `parquet-format`
  project, Apache-2.0. The ASF license header is preserved inside the README.
- In-repo anchor: both files added in commit `229997d` (2026-10-16).
- Upstream revision: not recorded at vendoring time. Inference, labeled:
  taken from the upstream default branch around the anchor date.
- Why here: the README's relative links (`src/main/thrift/parquet.thrift`,
  `PageIndex.md`, `BinaryProtocolExtensions.md`) resolve in the upstream
  repository layout, not in this one. The files are reference material for the
  corpus's Parquet outputs.

## sas_migration-main/ (never shipped to this instance)

A conversion starter scaffold lived in the professional instance's vendor/
and was retired there before this sister was cut (its conversion guides
were folded into `kb/convert/`, which ships here). The scaffold itself is
not part of this tree; its provenance record lives in the professional
instance.

## Rule for additions

Every new entry in this directory needs a section above it: what it is, the
commit that brought it in, the upstream it came from (or an explicit note that
none was recorded), and why the floor does not apply.
