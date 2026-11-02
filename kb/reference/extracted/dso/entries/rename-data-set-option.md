---
status: "generated"
entry: "RENAME= Data Set Option"
docset: "dso"
page: 70
physical_page: 82
category: "Variable Control CAS"
type: ""
valid_in: "DATA step and PROC steps"
---

RENAME= Data Set Option
Changes the name of a variable.

Valid in:         DATA step and PROC steps
Categories:       Variable Control
                  CAS




                  Syntax
                  RENAME=(old-variable-name-1=new-variable-name-1 <old-variable-name-2=new-
                  variable-name-2 ...> )


                  Syntax Description
                  old-name
                     is the variable that you want to rename.

                  new-name
                     is the new name of the variable. It must be a valid SAS name.




                  Details
                  If you use the RENAME= data set option when you create a data set, the new
                  variable name is included in the output data set. If you use RENAME= on an input
                  data set, the new name is used in DATA step programming statements.

                  If you use RENAME= on an input data set that is used in a SAS procedure, SAS
                  changes the name of the variable in that procedure. If you use RENAME= with
                  WHERE processing such as a WHERE statement or a WHERE= data set option, the
                  new name is applied before the data is processed. You must use the new name in
                  the WHERE expression.

                  Use RENAME= in the same DATA step with either the DROP= data set option or the
                  KEEP= data set option. The DROP= and KEEP= data set options are applied before
                  RENAME=. You must use the old name in the DROP= and KEEP= data set options.
                  You cannot drop and rename the same variable in the same statement.


                  Note: The RENAME= data set option has an effect only on data sets that are
                  opened in output mode.


                  Use the RENAME statement or the RENAME= data set option when program logic
                  requires that you rename variables. An example is two input data sets that have
