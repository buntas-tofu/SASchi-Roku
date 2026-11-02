---
status: "generated"
entry: "INFORMAT Statement"
docset: "stmt"
page: 161
physical_page: 173
category: "CAS Information"
type: "Declarative"
valid_in: "DATA step or PROC step"
---

INFORMAT Statement
Associates informats with variables.

Valid in:        DATA step or PROC step
Categories:      CAS
                 Information
Type:            Declarative




                 Syntax
                 INFORMAT variable-1 <...variable-n> <informat>;

                 INFORMAT <variable-1> <... variable-n> <DEFAULT=default-informat>;

                 INFORMAT variable-1 <...variable-n> informat <DEFAULT=default-informat>;


                 Arguments
                 variable
                    specifies one or more variables to associate with an informat. You must specify
                    at least one variable when specifying an informat or when including no other
                    arguments. Specifying a variable is optional when using a DEFAULT= informat
                    specification.

                    Tip   To disassociate an informat from a variable, use the variable's name in an
                          INFORMAT statement without specifying an informat. Place the
                          INFORMAT statement after the SET statement. See “Example 3: Removing
                          an Informat” on page 165.
