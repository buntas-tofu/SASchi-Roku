---
status: "generated"
entry: "ROLE= Data Set Option"
docset: "dso"
page: 78
physical_page: 90
category: "Data Set Control Use with input data sets only."
type: ""
valid_in: "PROC SQL"
---

ROLE= Data Set Option
Identifies the fact table for a star schema join.

Valid in:         PROC SQL
Category:         Data Set Control
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with input data sets only.




                  Syntax
                      ROLE=FACT | DIMENSION | DIM


                  Syntax Description
                  FACT
                    identifies the SAS data set as the fact table for a star schema.
