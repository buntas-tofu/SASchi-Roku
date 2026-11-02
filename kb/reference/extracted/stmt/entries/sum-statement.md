---
status: "generated"
entry: "Sum Statement"
docset: "stmt"
page: 348
physical_page: 360
category: "Action CAS"
type: "Executable set Table1; total + x; run;"
valid_in: "DATA step"
---

Sum Statement
Adds the result of an expression to an accumulator variable.

Valid in:        DATA step
Categories:      Action
                 CAS
Type:            Executable
Example:         data Table2;
                    set Table1;
                    total + x;
                 run;




                 Syntax
                 variable+expression;


                 Arguments
                 variable
                    specifies the name of the accumulator variable, which contains a numeric value.
