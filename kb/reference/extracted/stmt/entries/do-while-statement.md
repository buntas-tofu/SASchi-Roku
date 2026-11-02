---
status: "generated"
entry: "DO WHILE Statement"
docset: "stmt"
page: 78
physical_page: 90
category: "CAS Control"
type: "Executable"
valid_in: "DATA step"
---

DO WHILE Statement
Executes statements in a DO loop repetitively while a condition is true.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable




                 Syntax
                 DO WHILE (expression);
                 ...more SAS statements...

                 END;


                 Arguments
                 (expression)
                    is any SAS expression, enclosed in parentheses. You must specify at least one
                    expression.




                 Details
                 The expression is evaluated at the top of the loop before the statements in the DO
                 loop are executed. If the expression is true, the DO loop iterates. If the expression
                 is false the first time it is evaluated, the DO loop does not iterate even once.




                 Comparisons
                 There are three other forms of the DO statement:
                 n The DO statement, the simplest form of DO-group processing, designates a
                     group of statements to be executed as a unit, usually as a part of IF-THEN/ELSE
                     statements.
                 n The iterative DO statement executes statements between DO and END
                     statements repetitively based on the value of an index variable.
