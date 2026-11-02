---
status: "generated"
entry: "PUT Statement: Named"
docset: "stmt"
page: 302
physical_page: 314
category: "CAS File-Handling"
type: "Executable"
valid_in: "DATA step"
---

PUT Statement: Named
Writes variable values after the variable name and an equal sign.

Valid in:        DATA step
Categories:      CAS
                 File-Handling
Type:            Executable




                 Syntax
                 PUT <pointer-control> variable= <format.> <@ | @@>;

                 PUT variable= start-column <-end-column> <.decimal-places> <@ | @@>;


                 Arguments
                 pointer-control
                    moves the output pointer to a specified line or column in the output buffer.

                     See   “Column Pointer Controls ” on page 268

                           “Line Pointer Controls ” on page 270

                 variable=
                    specifies the variable whose value is written by the PUT statement in the form
                     variable=value

                 format.
                    specifies a format to use when the variable values are written.

                     Tip         Ensure that the format width provides enough space to write the
                                 value and any commas, dollar signs, decimal points, or other special
                                 characters that the format includes.

                     See         “Formatting Named Output” on page 303

                     Examples    This PUT statement uses the format DOLLAR7.2 to write the value of
                                 X:
