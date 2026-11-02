# Character and metadata representation choices

Status: design guidance to apply to an explicit source/consumer contract.

| Boundary | Decision and witness |
|---|---|
| Encoding | Named source codec and strict decode; invalid sequences must reject or retain original bytes |
| Width | Count source bytes where the descriptor does; distinguish padding from meaningful trailing spaces |
| NUL/control bytes | Specify each admitted class; prove the destination can represent it or use an agreed raw encoding |
| CSV | Exercise quotes, separators, CR, LF, CRLF, empty fields, literal missing-like strings and exact decoded bytes |
| Metadata | Keep known labels/formats/catalogs separately from unknown or unavailable properties |
| Missing tags | Preserve raw tags at unique row/column positions; an inventory of tag names is insufficient |
| Companion association | Bind to source/output hashes and row identity; reject stale or swapped companions |
| Dates | Preserve raw units/origin or explicitly convert; a display format supplies no timezone |

Base R character strings cannot hold embedded NUL. Raw vectors are a possible
representation, but they are not ordinary text columns. A lossless fallback must
retain original bytes and mark which cells use it; blank CSV cells alone cannot
distinguish missing text from an encoded binary fallback. Hex/base64 is reversible
only with its decoding rule and cell association. Do not declare a universally
safe ASCII contract while leaving byte zero unspecified.

For SAS datasets, a reader's success opening a file is not proof of preservation
of catalogs, tags, labels or encodings. Check the installed reader and writer,
then compare a reopened artifact. A CSV test cannot establish a Parquet schema.

Primary references:

- [R character literals and NUL limits](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html).
- [R raw-byte alternative](https://stat.ethz.ch/R-manual/R-devel/library/base/html/readChar.html).
- [Haven SAS reading](https://haven.tidyverse.org/reference/read_sas.html).
- [Apache Parquet format](https://github.com/apache/parquet-format).
