---
status: "generated"
entry: "WRITE= Data Set Option"
docset: "dso"
page: 98
physical_page: 110
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

WRITE= Data Set Option
Assigns a WRITE= password to a SAS file that prevents users from writing to a file, unless the users
enter the password.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Restriction:      Use in the Compute Server, but not in CAS.
Note:             Check your log after this operation to ensure password security. For more
                  information, see “Blotting Passwords and Encryption Key Values” in SAS
                  Programmer’s Guide: Essentials.




                  Syntax
                  WRITE=write-password


                  Syntax Description
                  write-password
                     must be a valid SAS name.




                  Details

                  Overview of the WRITE= Option
                  The WRITE= option applies to all types of SAS files except catalogs. You can use
                  this option to assign a password to a SAS file or to access a write-protected SAS
                  file.
