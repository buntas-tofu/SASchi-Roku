---
status: "generated"
entry: "INPUT Statement: Named"
docset: "stmt"
page: 200
physical_page: 212
category: "File-Handling"
type: "Executable"
valid_in: "DATA step"
---

INPUT Statement: Named
Reads data values that appear after a variable name that is followed by an equal sign and assigns the
values to corresponding SAS variables.

Valid in:        DATA step
Category:        File-Handling
Type:            Executable
Restriction:     This statement is not supported in a DATA step that runs in CAS.




                 Syntax
                 INPUT <pointer-control> variable= <$> <@ | @@>;

                 INPUT variable= <$> start-column<–end-column>
                 <@ | @@>;


                 Arguments
                 pointer-control
                    moves the input pointer to a specified line or column in the input buffer.

                    See   “Column Pointer Controls” on page 168 and “Line Pointer Controls” on page
                          170

                 variable=
                    specifies a variable whose value is read by the INPUT statement. In the input
                    data record, the field has this form:
                    variable=value

                    Tip        Use the INFORMAT statement to associate an informat with a
                               variable.

                    See        SAS Informats in SAS Formats and Informats: Reference

                    Example    “Example 3: Using Named Input with Another Input Style” on page 203
