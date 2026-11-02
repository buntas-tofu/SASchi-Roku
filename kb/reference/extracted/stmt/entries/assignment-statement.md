---
status: "generated"
entry: "Assignment Statement"
docset: "stmt"
page: 32
physical_page: 44
category: "Action CAS"
type: "Executable"
valid_in: "DATA step"
---

Assignment Statement
Evaluates an expression and stores the result in a variable.

Valid in:        DATA step
Categories:      Action
                 CAS
Type:            Executable




                 Syntax
                 variable=expression;


                 Arguments
                 variable
                    names a new or existing variable.

                     Range   variable can be a variable name, array reference, or SUBSTR function.

                     Tip     Variables that are created by the Assignment statement are not
                             automatically retained.

                 expression
                    is any SAS expression.

                     Tip   expression can contain the variable that is used on the left side of the equal
                           sign. When a variable appears on both sides of a statement, the original
                           value on the right side is used to evaluate the expression. The result is
                           stored in the variable on the left side of the equal sign. For more
                           information, see “Expressions” in SAS Language Reference: Concepts.
