---
status: "generated"
entry: "MODIFY Statement"
docset: "stmt"
page: 240
physical_page: 252
category: "File-Handling"
type: "Executable This statement cannot modify the descriptor portion of a SAS data set, such as adding a variable."
valid_in: "DATA step"
---

MODIFY Statement
Replaces, deletes, and appends observations in an existing SAS data set in place but does not create
an additional copy.

Valid in:          DATA step
Category:          File-Handling
Type:              Executable
Restrictions:      This statement is not supported in a DATA step that runs in CAS.
                   This statement cannot modify the descriptor portion of a SAS data set, such as
                   adding a variable.
Notes:             If you modify a password-protected data set, specify the password with the
                   appropriate data set option (ALTER= or PW=) in the MODIFY statement, and not in
                   the DATA statement.
                   The variables read using the MODIFY statement are retained in the PDV. For more
                   information, see “Overview of DATA Step Processing” in SAS Language Reference:
                   Concepts and the “RETAIN Statement” on page 319.
See:               “Updating Data Using the MODIFY Statement and the KEY= Option” in SAS
                   Programmer’s Guide: Essentials
CAUTION:           Damage to the SAS data set can occur if the system terminates abnormally during
                   a DATA step that contains the MODIFY statement. Observations in native SAS data
                   files might have incorrect data values, or the data file might become unreadable. DBMS
                   tables that are referenced by views are not affected.




                   Syntax
         Form 1:   MODIFY master-data-set <(data-set-options)> transaction-data-set <(data-set-
                   options)>
                   <CUROBS=variable> <NOBS=variable> <END=variable>
                   <UPDATEMODE=MISSINGCHECK | NOMISSINGCHECK>;
                   BY by-variable;
         Form 2:   MODIFY master-data-set <(data-set-options)> KEY=index </ UNIQUE>
                   <KEYRESET=variable> <NOBS=variable> <END=variable>;
         Form 3:   MODIFY master-data-set <(data-set-options)> <NOBS=variable> POINT=variable;
