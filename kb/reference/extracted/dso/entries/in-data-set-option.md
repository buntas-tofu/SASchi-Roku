---
status: "generated"
entry: "IN= Data Set Option"
docset: "dso"
page: 44
physical_page: 56
category: "Observation Control CAS"
type: ""
valid_in: "DATA step"
---

IN= Data Set Option
Creates a Boolean variable that indicates whether the data set contributed data to the current
observation.

Valid in:         DATA step
Categories:       Observation Control
                  CAS
Restriction:      Use with the SET, MERGE, MODIFY, and UPDATE statements only.




                  Syntax
                  IN=variable


                  Syntax Description
                  variable
                     names the new variable whose value indicates whether the input data set
                     contributed data to the current observation. Within the DATA step, the value of
                     the variable is 1 if the data set contributed to the current observation.
                     Otherwise, the value is 0.
