---
status: "generated"
entry: "TOBSNO= Data Set Option"
docset: "dso"
page: 90
physical_page: 102
category: "Data Set Control The TOBSNO= option is valid only for data sets that are accessed through a SAS server by using the REMOTE engine."
type: ""
valid_in: "DATA step and PROC steps"
---

TOBSNO= Data Set Option
Specifies the number of observations to send in a client/server transfer.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Restrictions:     Use in the Compute Server, but not in CAS.
                  The TOBSNO= option is valid only for data sets that are accessed through a SAS
                  server by using the REMOTE engine.




                  Syntax
                  TOBSNO=n


                  Syntax Description
                  n
                      specifies the number of observations to be transmitted.




                  Details
                  If the TOBSNO= option is not specified, its value is calculated based on the
                  observation length and the size of the server's transmission buffers. This action is
                  specified by the PROC SERVER statement TBUFSIZE= option.

                  The TOBSNO= option is valid only for data sets that are accessed through a SAS
                  server via the REMOTE engine. If this option is specified for a data set that is
                  opened for update or accessed via another engine, it is ignored.




                  See Also
                  “FOPEN Function” in SAS Functions and CALL Routines: Reference
