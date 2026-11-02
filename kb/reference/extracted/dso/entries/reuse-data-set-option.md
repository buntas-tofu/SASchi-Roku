---
status: "generated"
entry: "REUSE= Data Set Option"
docset: "dso"
page: 77
physical_page: 89
category: "Data Set Control Use with output data sets only."
type: ""
valid_in: "DATA step and PROC steps"
---

REUSE= Data Set Option
Specifies whether new observations can be written to available space in compressed SAS data sets.

Valid in:       DATA step and PROC steps
Category:       Data Set Control
Restrictions:   Use in the Compute Server, but not in CAS.
                Use with output data sets only.




                Syntax
                REUSE=NO | YES


                Syntax Description
                NO
                  does not track and reuse space in compressed data sets. New observations are
                  appended to the existing data set. Specifying the NO argument results in less
                  efficient data storage if you delete or update many observations in the SAS data
                  set.

                    You can use procedures such as APPEND and FSEDIT that add observations to
                    the end of SAS data sets with compressed data sets.

                YES
                  tracks and reuses space in compressed SAS data sets. New observations are
                  inserted in the space that is available when other observations are updated or
                  deleted.

                    REUSE=YES causes new observations to be added wherever there is space in
                    the file, not necessarily at the end of the file.
