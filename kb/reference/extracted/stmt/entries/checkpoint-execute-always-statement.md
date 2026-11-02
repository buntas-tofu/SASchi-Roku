---
status: "generated"
entry: "CHECKPOINT EXECUTE_ALWAYS Statement"
docset: "stmt"
page: 48
physical_page: 60
category: ""
type: ""
valid_in: ""
---

CHECKPOINT EXECUTE_ALWAYS Statement
Indicates to execute the DATA step or PROC step that immediately follows the statement without
considering the checkpoint-restart data.

Note:            The CHECKPOINT EXECUTE_ALWAYS Statement has moved to SAS Global
                 Statements.




Comment Statement
Specifies the purpose of the statement or program.

Note:            The Comment Statement has moved to SAS Global Statements.




CONTINUE Statement
Stops processing the current DO-loop iteration and resumes processing the next iteration.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable
Restriction:     Can be used only in a DO loop




                 Syntax
                 CONTINUE;


                 Without Arguments
                 The CONTINUE statement has no arguments. It stops processing statements within
                 the current DO-loop iteration based on a condition. Processing resumes with the
                 next iteration of the DO loop.
