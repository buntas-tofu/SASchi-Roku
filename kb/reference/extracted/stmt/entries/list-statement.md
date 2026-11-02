---
status: "generated"
entry: "LIST Statement"
docset: "stmt"
page: 224
physical_page: 236
category: "Action CAS"
type: "Executable"
valid_in: "DATA step"
---

LIST Statement
Writes to the SAS log the input data record for the observation that is being processed.

Valid in:        DATA step
Categories:      Action
                 CAS
Type:            Executable




                 Syntax
                 LIST;


                 Without Arguments
                 The LIST statement causes the input data record for the observation being
                 processed to be written to the SAS log.




                 Details
                 The LIST statement operates only on data that is read with an INPUT statement; it
                 has no effect on data that is read with a SET, MERGE, MODIFY, or UPDATE
                 statement.

                 In the SAS log, a ruler that indicates column positions appears before the first
                 record listed.

                 For variable-length records (RECFM=V), SAS writes the record length at the end of
                 the input line. SAS does not write the length for fixed-length records (RECFM=F),
                 unless the amount of data read does not equal the record length (LRECL).
