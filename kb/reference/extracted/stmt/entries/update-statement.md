---
status: "generated"
entry: "UPDATE Statement"
docset: "stmt"
page: 350
physical_page: 362
category: "File-Handling"
type: "Executable"
valid_in: "DATA step"
---

UPDATE Statement
Updates a master file by applying transactions.

Valid in:         DATA step
Category:         File-Handling
Type:             Executable
Restriction:      This statement is not supported in a DATA step that runs in CAS.
Note:             The variables read using the MERGE statement are retained in the PDV. The data
                  types of the variables that are read are also retained. For more information, see
                  “DATA Step Processing” in SAS Programmer’s Guide: Essentials and the “RETAIN
                  Statement” on page 319.
CAUTION:          If you add an OUTPUT statement when using an UPDATE statement, the results
                  that are generated are predictable but can be undesired.
