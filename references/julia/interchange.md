# SAS files, Julia tables, and reversible metadata

Status: interoperability design, not a measured round trip.

## Reader boundary

ReadStatTables.jl supports `.sas7bdat` and `.xpt`, returning a Tables-compatible result and selected metadata. Its published limitations include incomplete SAS value-label reading, collapsing all original missing representations to `missing`, and experimental SAS writing. Its `writestat` docs warn that SAS might reject generated `.sas7bdat` files. None of those caveats is waived here.

For archives requiring faithful provenance, keep the original source bytes and optional catalog, with hash, license, source encoding and descriptor metadata. A sidecar for tagged missings must record each cell's tag position or stable row/column identity, not merely a list of tag names.

## Analytical boundary

- `CSV.jl` and `Tables.jl` support tabular transfer, but only under explicit field types, string IDs, encoding, missing and date conventions.
- `Arrow.jl` can support typed columnar exchange; it is not proof that SAS labels, special missing tags, formats or raw text bytes survived.
- A separately selected Parquet reader may be appropriate, but its version and metadata fidelity must be inspected before use.
- Julia's `DataFrame` is an analytical view. It does not replace the archival representation when full source fidelity matters.

The existing [Roku dual-path trial](../../trials/parquet-dual-path/README.md) illustrates archival/analytical separation, but only for its executed Python/R cases. No Julia writer or reader has been exercised by this PR.
