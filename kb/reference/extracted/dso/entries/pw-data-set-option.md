---
status: "generated"
entry: "PW= Data Set Option"
docset: "dso"
page: 66
physical_page: 78
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

PW= Data Set Option
Assigns a READ, WRITE, and ALTER password to a SAS file, and enables access to a password-
protected SAS file.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Restriction:      Use in the Compute Server, but not in CAS.
Note:             Check your log after this operation to ensure password security. For more
                  information, see “Blotting Passwords and Encryption Key Values” in SAS
                  Programmer’s Guide: Essentials.




                  Syntax
                  PW=password


                  Syntax Description
                  password
                     must be a valid SAS name, which limits the password to eight characters and is
                     case-insensitive.




                  Details

                  Overview of the PW= Option
                  The PW= option applies to all types of SAS files except catalogs. Use this option to
                  assign a password to a SAS file or to access a password-protected SAS file.

                  When you replace a SAS data set that is protected by an ALTER password, the new
                  data set inherits the ALTER password. To change the ALTER password for the new
                  data set, use the MODIFY statement in the DATASETS procedure.
                  Operating Environment Information: For more information about using passwords,
                  see the appropriate sections of the SAS documentation.
