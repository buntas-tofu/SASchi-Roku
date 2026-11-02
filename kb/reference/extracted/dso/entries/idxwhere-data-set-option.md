---
status: "generated"
entry: "IDXWHERE= Data Set Option"
docset: "dso"
page: 40
physical_page: 52
category: "User Control of SAS Index Usage Use with input data sets only. Mutually exclusive with IDXNAME= data set option"
type: ""
valid_in: "DATA step and PROC steps"
---

IDXWHERE= Data Set Option
Specifies whether SAS uses an index search or a sequential search to match the conditions of a
WHERE expression.

Valid in:         DATA step and PROC steps
Category:         User Control of SAS Index Usage
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with input data sets only.
                  Mutually exclusive with IDXNAME= data set option




                  Syntax
                  IDXWHERE=YES | NO


                  Syntax Description
                  YES
                    tells SAS to choose the best index to optimize a WHERE expression, and to
                    disregard the possibility that a sequential search of the data set might be more
                    resource efficient.
                  NO
                    tells SAS to ignore all indexes and satisfy the conditions of a WHERE
                    expression with a sequential search of the data set.


                     Note: You cannot use IDXWHERE= to override the use of an index to process a
                     BY statement.
