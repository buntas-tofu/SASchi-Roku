# First-delivery history

Status: candidate execution history for one bounded decoded-JSON interchange trial. Self-test evidence only; independent parent acceptance remains unobserved. Reviewers may use the included sources and receipts to reproduce these observations.

1. Read the supplied packet contract, request, both skill files, and both referenced representation/preservation documents. Enumerated and read the supplied valid and invalid fixtures. Applied the skills as initial guidance rather than treating their descriptions as an executed guarantee. The packet-only request governed the scope; no referenced repository decision, journal, parent artifact, or sibling answer was opened.

2. Queried the installed runtimes and PyArrow reader/writer docstrings. Observed CPython 3.12.3, PyArrow 26.0.0, and Rscript 4.3.3. Consulted current Apache Arrow reader/writer primary documentation and R primary documentation for character constants, CSV input, and binary decoding.

3. A setup attempt to create the designated candidate directory returned exit 1 because that directory already existed. No output was removed or overwritten by this command. Wrote the requested implementation and candidate self-test sources into the designated directory afterward. This setup error did not require an implementation change.

4. Implemented the fixed schema, strict byte decoding and width checks, numeric validation, source-epoch date handling, per-cell tags, complete descriptor retention, source/output hashes, and an embedded companion digest. Chose uncompressed Parquet with dictionary encoding disabled to keep floating-point zero signs in the stored value stream. This choice was subsequently verified by byte-level numeric round trips rather than assumed correct from the writer option alone.

5. Implemented the sourceable base R bridge consumer. Hex-decoded `text` remains raw, binary64 values use explicit little-endian decoding, and metadata/label tables remain character data.frames with automatic NA interpretation disabled. The requested `id` character representation cannot hold NUL; added an explicit rejection rather than truncating it.

6. First complete self-test command:

   ```sh
   /tmp/saschi-parquet-venv/bin/python selftest.py --packet /tmp/saschi-parquet-trial/packet --work /tmp/saschi-parquet-selftest-01
   ```

   Exit 0. Six valid cases passed complete Python restoration and R bridge checks: 44 rows, 308 cells, 169 missing tags. Seven invalid cases were rejected with no output destination. Thirty-three adversarial bundle scenarios were rejected through both public validation/restoration APIs. Five additional checks passed. No unexpected implementation test failure occurred, and no implementation repair was needed.

7. Preserved expected source rejection outcomes:

   | Fixture | Observed exception and reason |
   |---|---|
   | bad-tag | ValueError, invalid missing tag at row 0/value |
   | boolean-number | ValueError, expected JSON number at row 0/value |
   | duplicate-column | ValueError, wrong or duplicate column name/order |
   | fractional-date | ValueError, fractional source date at row 0/date |
   | invalid-utf8 | UnicodeDecodeError, byte 0xff invalid at position 0 |
   | over-width | ValueError, byte width mismatch at row 0/id |
   | unknown-encoding | ValueError, unsupported encoding |

   These are intended input failures, not repaired fixtures. The packet remained unchanged. `selftest_results.json` retains the actual exception names and messages.

8. Checked for the repository linter using `command -v inertia-drift-lint`. It returned exit 1 with no executable found. Added a clearly labeled local mechanical artifact check, without claiming that it substitutes for repository governance or CI.

9. Probed R's NUL representation directly. R reported `embedded nul in string: 'A\0B'` for a raw-to-character conversion containing NUL; the probe caught and printed the expected error. R also reported its platform, endian setting, and `C.UTF-8` locale. This confirmed the documented boundary rather than an issue in Parquet preservation.

10. Expanded self-tests, without changing the implementation, to convert and restore a NUL-bearing ID in Python, prove the R consumer rejects that unrepresentable character ID, and reject three malformed bridges: text tag, empty numeric payload without a tag, and wrong cell order. This was extra boundary coverage, not a repair following a hidden or independent test.

11. Second complete self-test command:

    ```sh
    /tmp/saschi-parquet-venv/bin/python selftest.py --packet /tmp/saschi-parquet-trial/packet --work /tmp/saschi-parquet-selftest-02
    ```

    Exit 0. Repeated all six valid, seven invalid, and 33 adversarial scenarios successfully; nine additional checks passed. The intentional R NUL-ID subprocess exited nonzero with the explicit embedded-NUL error. Each of the three malformed-bridge subprocesses also exited nonzero as required. Copied this run's structured results into the delivery directory.

12. Converted all six supplied valid cases into fresh delivered `bundles` subdirectories. Each conversion reopened and fully compared its own output before returning, then returned the validation receipt. Recorded source and Parquet hashes in `bundle_receipts.json`. Wrote the report and this history, then ran the supplied local mechanical style check and final receipt validation. No independent parent acceptance was run or consulted before delivery.

Pre-delivery repairs: none to the implementation after its first complete self-test. The history records the setup directory error, unavailable repository linter, expected invalid-input rejections, and observed R representation failure instead of erasing or reclassifying them as successful conversions. No commits, pull requests, delegated work, or messages to other chats were created.
