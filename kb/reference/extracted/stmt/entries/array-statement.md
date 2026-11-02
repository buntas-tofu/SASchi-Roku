---
status: "generated"
entry: "ARRAY Statement"
docset: "stmt"
page: 21
physical_page: 33
category: "CAS Information"
type: "Declarative"
valid_in: "DATA step"
---

ARRAY Statement
Defines the elements of an array.

Valid in:        DATA step
Categories:      CAS
                 Information
Type:            Declarative
Restriction:     Variables with a VARCHAR data type are supported when an array is initialized.
Requirement:     The CAS engine is required if you want to preserve a variable as a VARCHAR data
                 type when reading the variable in or writing it out using the DATA step.




                 Syntax
                 ARRAY array-name { subscript }
                 <$ length | length | VARCHAR(length) | VARCHAR(*)>
                 <array-elements> <(initial-value-list)>;


                 Arguments
                 array-name
                    specifies the name of the array.

                    Restrictions    array-name must be a SAS name that is not the name of a SAS
                                    variable in the same DATA step.

                                    The array-name argument cannot be one of these names: IF,
                                    SELECT, SUBSTR, INPUT, PUT, WHEN, WHILE, UNTIL, RETURN.

                    CAUTION         Using the name of a SAS function as an array name can cause
                                    unpredictable results. If you inadvertently use a function name as the
                                    name of the array, SAS treats parenthetical references that involve the
