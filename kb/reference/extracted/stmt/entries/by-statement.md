---
status: "generated"
entry: "BY Statement"
docset: "stmt"
page: 39
physical_page: 51
category: "CAS File-Handling"
type: "Declarative"
valid_in: "DATA step or PROC step"
---

BY Statement
Controls the operation of a SET, MERGE, MODIFY, or UPDATE statement in the DATA step and sets
up special grouping variables.

Valid in:       DATA step or PROC step
Categories:     CAS
                File-Handling
Type:           Declarative
See:            SAS Cloud Analytic Services: DATA Step Programming
Example:        data ShoesByRegion;
                   set sashelp.shoes;
                   by descending Region
                      descending Subsidiary;
                run;


Example:        “Group and Sort Variables in Descending Order” in SAS Cloud Analytic Services:
                DATA Step Programming




                Syntax
                BY <DESCENDING> variable-1 <...<DESCENDING> variable-n>
                <NOTSORTED> <GROUPFORMAT>;
