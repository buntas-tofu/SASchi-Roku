# Interchange preservation contract

Status: proposed checklist for a specific conversion, not an executed round trip.

Record the source format and hashes, reader/writer versions, chosen encoding,
output files and hashes, row count, column order, and the policy for each field.
A useful per-column record distinguishes stored values from display metadata:

| Property | Decision to record |
|---|---|
| Name, order and type | Original descriptor and target physical/logical type |
| Character width | Source byte width, padding policy and decoding errors |
| Label and format | Original names/text, catalog availability, preserved or unknown |
| Missing values | Ordinary versus tagged; reversible per-cell representation or declared loss |
| Date, time, datetime | Source unit/origin and target interpretation; timezone only if known |
| Value labels | Preserve raw values and the mapping separately when both matter |

The companion metadata and data are one deliverable. Reopen both. Check their
association so a sidecar from a different conversion cannot silently be reused.
Record which properties were checked completely, sampled, or not recoverable.

Sources to inspect when choosing an implementation:

- [Garage SL-020](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/corpora/sas-conversion-landmines/sl-020-metadata-roundtrip.md): candidate metadata-roundtrip witness design; not live-SAS evidence.
- [Haven SAS reader](https://haven.tidyverse.org/reference/read_sas.html) and [conversion semantics](https://haven.tidyverse.org/articles/semantics.html): current reader/catalog and R representation contracts; recheck against the installed release.
- [Apache Parquet format](https://github.com/apache/parquet-format): the storage specification, not an execution engine or a SAS converter.

These are navigation references. The workflow must still demonstrate the chosen
reader-to-writer path on the actual source and declared contract.
