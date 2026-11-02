---
status: "generated"
entry: "REDIRECT Statement"
docset: "stmt"
page: 310
physical_page: 322
category: "Action"
type: "Executable"
valid_in: "DATA step"
---

REDIRECT Statement
Points to different input or output SAS data sets when you execute a stored program.

Valid in:        DATA step
Category:        Action
Type:            Executable
Restriction:     This statement is not supported in a DATA step that runs in CAS.
Requirement:     You must specify the PGM= option in the DATA statement.




                 Syntax
                 REDIRECT INPUT | OUTPUT old-name-1=new-name-1 <...old-name-n=new-name-
                 n>;
