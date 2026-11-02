---
status: "generated"
entry: "PUT Statement"
docset: "stmt"
page: 265
physical_page: 277
category: "CAS File-Handling"
type: "Executable write to the SAS log, PRINT, or an external file, missing values might be suppressed in the output. Missing values can be displayed if an explicit line break (/) is included in the PUT statement."
valid_in: "DATA step"
---

PUT Statement
Writes lines to the SAS log, to the SAS output window, or to an external location that is specified in
the most recent FILE statement.

Valid in:        DATA step
Categories:      CAS
                 File-Handling
Type:            Executable
Interaction:     When using the DSD option in the FILE statement and using the PUT statement to
                 write to the SAS log, PRINT, or an external file, missing values might be suppressed
                 in the output. Missing values can be displayed if an explicit line break (/) is included
                 in the PUT statement.




                 Syntax
                 PUT <specification(s)> <_ODS_> <@ | @@>;

                 PUT 'ERROR: text' | 'NOTE: text' | 'WARNING: text';

                 PUT 'ERROR- text' | 'NOTE- text' | 'WARNING- text';


                 Without Arguments
                 The PUT statement without arguments is called a null PUT statement. The null PUT
                 statement can be used to perform these tasks:
                 n write the current output line to the current location, even if the current output
                     line is blank.
