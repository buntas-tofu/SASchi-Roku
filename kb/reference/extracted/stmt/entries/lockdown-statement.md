---
status: "generated"
entry: "LOCKDOWN Statement"
docset: "stmt"
page: 229
physical_page: 241
category: ""
type: ""
valid_in: ""
---

LOCKDOWN Statement
Secures the SAS Viya Workspace or SAS/CONNECT server on SAS Viya by restricting access from
within a server process to the host operating environment.

Notes:           The LOCKDOWN statement for SAS Viya has moved to SAS Viya Administration:
                 Programming Run-Time Servers. For more information, see SAS Viya LOCKDOWN
                 Statement.
                 For information about LOCKDOWN on SAS 9.4, see SAS 9.4 LOCKDOWN
                 Statement.




LOSTCARD Statement
Resynchronizes the input data when SAS encounters a missing or invalid record in data that has
multiple records per observation.

Valid in:        DATA step
Categories:      Action
                 CAS
Type:            Executable




                 Syntax
                 LOSTCARD;


                 Without Arguments
                 The LOSTCARD statement prevents SAS from reading a record from the next group
                 when the current group has a missing record.




                 Details

                 When to Use LOSTCARD
                 When SAS reads multiple records to create a single observation, it does not
                 discover that a record is missing until it reaches the end of the data. If there is a
                 missing record in your data, the values for subsequent observations in the SAS data
                 set might be incorrect. Using LOSTCARD prevents SAS from reading a record from
                 the next group when the current group has fewer records than SAS expected.
