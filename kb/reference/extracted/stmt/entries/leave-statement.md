---
status: "generated"
entry: "LEAVE Statement"
docset: "stmt"
page: 214
physical_page: 226
category: "CAS Control"
type: "Executable"
valid_in: "DATA step"
---

LEAVE Statement
Stops processing the current loop and resumes with the next statement in the sequence.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable




                 Syntax
                 LEAVE;


                 Without Arguments
                 The LEAVE statement stops the processing of the current DO loop or SELECT
                 group and continues DATA step processing with the next statement following the
                 DO loop or SELECT group.




                 Details
                 You can use the LEAVE statement to exit a DO loop or SELECT group prematurely
                 based on a condition.
