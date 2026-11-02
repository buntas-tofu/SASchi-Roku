---
status: "generated"
entry: "REPLACE= Data Set Option"
docset: "dso"
page: 76
physical_page: 88
category: "Data Set Control CAS This option is valid only when creating a SAS data set."
type: ""
valid_in: "DATA step and PROC steps"
---

REPLACE= Data Set Option
Specifies whether a new SAS data set that contains data can overwrite an existing data set.

Valid in:         DATA step and PROC steps
Categories:       Data Set Control
                  CAS
Restrictions:     Use with output data sets only.
                  This option is valid only when creating a SAS data set.
Note:             When you use the OUT2= PermanentLibrary._ALL_ option within PROC CONTENTS
                  or PROC DATASETS with the CONTENTS statement, you must also set the
                  REPLACE=YES data set option or the REPLACE system option.




                  Syntax
                  REPLACE=NO | YES


                  Syntax Description
                  NO
                    specifies that a new data set does not replace an existing data set.

                  YES
                    specifies that a new data set replaces an existing data set.




                  Details
                  n The REPLACE= data set option overrides the REPLACE system option for the
                      individual data set.
                  n The REPLACE system option applies only to permanent SAS data sets.

                  Use REPLACE=YES and REPEMPTY=NO for the convenience of replacing existing
                  data sets with new ones that contain data.




                  Example
                  Using the REPLACE= data set option in this DATA statement prevents SAS from
                  replacing a SAS data set named ONE in a library referenced by MYLIB:
