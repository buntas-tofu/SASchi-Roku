---
status: "generated"
entry: "GENMAX= Data Set Option"
docset: "dso"
page: 35
physical_page: 47
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

GENMAX= Data Set Option
Requests generations for a new data set, modifies the number of generations for an existing data set,
and specifies the maximum number of versions.

Valid in:        DATA step and PROC steps
Category:        Data Set Control

Default:         0
Restrictions:    Use in the Compute Server, but not in CAS.
                 Use with output data sets only.




                 Syntax
                 GENMAX=number-of-generations


                 Syntax Description
                 number-of-generations
                   requests generations for a data set and specifies the maximum number of
                   versions to maintain. The value can be from 0 to 1,000. The default is
                   GENMAX=0, which means that no generation data sets are requested.




                 Details
                 You use GENMAX= to request generations for a new data set and to modify the
                 number of generations for an existing data set. The first time the data set is
                 replaced, SAS keeps the replaced version and appends a 4-character version
