---
status: "generated"
entry: "TYPE= Data Set Option"
docset: "dso"
page: 91
physical_page: 103
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

TYPE= Data Set Option
Specifies the data set type for a specially structured SAS data set.

Valid in:        DATA step and PROC steps
Category:        Data Set Control
Restriction:     Use in the Compute Server, but not in CAS.




                 Syntax
                 TYPE=data-set-type


                 Syntax Description
                 data-set-type
                    specifies the special type of data set.




                 Details
                 Use the TYPE= data set option in a DATA step to perform these tasks:
                 n to create a special SAS data set in the proper format

                 n to identify the special type of SAS data set in a procedure statement

                 You can use the CONTENTS procedure to determine the type of data set.

                 Most SAS data sets do not have a specified type. However, there are several
                 specially structured SAS data sets that are used by some SAS/STAT procedures.
                 These SAS data sets contain special variables and observations, and they are
                 usually created by SAS statistical procedures. Because most of the special SAS
                 data sets are used with SAS/STAT software, they are described in the SAS/STAT
                 User's Guide. Some of the special data sets are CORR, COV, SSPC, EST, and
                 FACTOR.

                 Additional values are available in other SAS software products and are described in
                 the appropriate documentation.


                 Note: If you use a DATA step with a SET statement to modify a special SAS data
                 set, you must specify the TYPE= option in the DATA statement. The data-set-type
                 is not automatically copied to the data set that is created.
