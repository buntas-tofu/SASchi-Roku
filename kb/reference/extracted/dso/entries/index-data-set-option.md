---
status: "generated"
entry: "INDEX= Data Set Option"
docset: "dso"
page: 42
physical_page: 54
category: "Data Set Control Use with output data sets only."
type: ""
valid_in: "DATA step and PROC steps"
---

INDEX= Data Set Option
Defines an index for a new output SAS data set.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with output data sets only.




                  Syntax
                  INDEX=(index-specification <index-specification-2 ...> )


                  Syntax Description
                  index-specification
                     names and describes a simple or a composite index to be built. Index-
                     specification has this form:

                     index= (variable(s) </UNIQUE> </NOMISS> )

                  index
                     is the name of a variable that forms the index or the name that you choose for a
                     composite index.

                  variable(s)
                     is a list of variables to use in building a composite index.
