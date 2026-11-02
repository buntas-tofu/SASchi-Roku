---
status: "generated"
entry: "LINK Statement"
docset: "stmt"
page: 222
physical_page: 234
category: "CAS Control"
type: "Executable"
valid_in: "DATA step"
---

LINK Statement
Directs program execution immediately to the statement label that is specified and, if followed by a
RETURN statement, returns execution to the statement that follows the LINK statement.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable




                 Syntax
                 LINK label;


                 Arguments
                 label
                    specifies a statement label that identifies the LINK destination. You must
                    specify the label argument.




                 Details
                 The LINK statement tells SAS to jump immediately to the statement label that is
                 indicated in the LINK statement and to continue executing statements from that
                 point until a RETURN statement is executed. The RETURN statement sends
                 program control to the statement immediately following the LINK statement.

                 The LINK statement and the destination must be in the same DATA step. The
                 destination is identified by a statement label in the LINK statement.

                 The LINK statement can branch to a group of statements that contain another LINK
                 statement. This arrangement is known as nesting. To avoid infinite looping, SAS has
                 set a default number of nested LINK statements. You can have up to 10 LINK
                 statements with no intervening RETURN statements. When more than one LINK
                 statement has been executed, a RETURN statement tells SAS to return to the
                 statement that follows the last LINK statement that was executed. However, you
                 can use the /STACK option in the DATA statement to increase the number of
                 nested LINK statements.
