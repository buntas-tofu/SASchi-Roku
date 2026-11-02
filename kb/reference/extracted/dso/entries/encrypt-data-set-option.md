---
status: "generated"
entry: "ENCRYPT= Data Set Option"
docset: "dso"
page: 22
physical_page: 34
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

ENCRYPT= Data Set Option
Specifies whether to encrypt an output SAS data set.

Valid in:         DATA step and PROC steps
Category:         Data Set Control

Default:          ENCRYPT=NO
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with output data sets only.
                  If you copy an AES2 data set to an SPD Engine data set, the encryption is changed
                  to AES.
                  SAS 9.4M5 or later software is required to use AES2 encryption.




                  Syntax
                  ENCRYPT=AES | AES2 | NO | YES
