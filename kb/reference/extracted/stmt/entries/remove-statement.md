---
status: "generated"
entry: "REMOVE Statement"
docset: "stmt"
page: 312
physical_page: 324
category: "Action"
type: "Executable Use only with a MODIFY statement."
valid_in: "DATA step"
---

REMOVE Statement
Deletes an observation from a SAS data set.

Valid in:        DATA step
Category:        Action
Type:            Executable
Restrictions:    This statement is not supported in a DATA step that runs in CAS.
                 Use only with a MODIFY statement.




                 Syntax
                 REMOVE <data-set-name(s)>;


                 Without Arguments
                 If you specify no argument, the REMOVE statement deletes the current
                 observation from all data sets that are named in the DATA statement.
