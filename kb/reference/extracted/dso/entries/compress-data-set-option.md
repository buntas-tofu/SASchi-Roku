---
status: "generated"
entry: "COMPRESS= Data Set Option"
docset: "dso"
page: 16
physical_page: 28
category: "Data Set Control CAS Use with output data sets only."
type: ""
valid_in: "DATA step and PROC steps"
---

COMPRESS= Data Set Option
Specifies how observations are compressed in a new output SAS data set.

Valid in:         DATA step and PROC steps
Categories:       Data Set Control
                  CAS
Restrictions:     When using this option with the CAS server, use YES and NO values only.
                  Use with output data sets only.




                  Syntax
                  COMPRESS=NO | YES | CHAR | BINARY


                  Syntax Description
                  NO
                    specifies that the observations in a newly created SAS data set are
                    uncompressed (maintaining fixed-length records).

                  YES | CHAR
                    specifies that the observations in a newly created SAS data set are compressed
                    (producing variable-length records) by using RLE (Run Length Encoding). RLE
                    compresses observations by reducing repeated runs of the same character
                    (including blanks) to 2-byte or 3-byte representations.

                      Alias   ON

                  BINARY
                     specifies that the observations in a newly created SAS data set are compressed
                     (producing variable-length records) by using RDC (Ross Data Compression).
                     RDC combines run-length encoding and sliding-window compression to
                     compress the file by representing repeated byte patterns more efficiently.


                      Note: This method is highly effective for compressing medium to large (several
                      hundred bytes or larger) blocks of binary data (character and numeric variables).
                      Because the compression function operates on a single record at a time, the
