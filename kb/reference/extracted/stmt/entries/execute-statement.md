---
status: "generated"
entry: "EXECUTE Statement"
docset: "stmt"
page: 84
physical_page: 96
category: "Action"
type: "Executable Use EXECUTE with stored compiled DATA step programs only."
valid_in: "DATA step"
---

EXECUTE Statement
Executes a stored compiled DATA step program.

Valid in:        DATA step
Category:        Action
Type:            Executable
Restrictions:    This statement is not supported in a DATA step that runs in CAS.
                 Use EXECUTE with stored compiled DATA step programs only.
Requirement:     You must specify the PGM= option in the DATA step.




                 Syntax
                 EXECUTE;


                 Without Arguments
                 The EXECUTE statement executes a stored compiled DATA step program.




                 Details
                 Use the DESCRIBE statement with the EXECUTE statement in the same DATA step
                 to retrieve the source code and execute a stored compiled DATA step program. If
                 you do not specify either statement, EXECUTE is assumed. The order in which you
                 use the statements is interchangeable. The DATA step program executes when it
                 reaches a step boundary. For information about how to use these statements with
                 the DATA statement, see “DATA Statement” on page 49.




                 See Also
                 Statements:
                 n “DATA Statement” on page 49
                 n “DESCRIBE Statement” on page 66
