---
status: "generated"
entry: "PUT Statement: Formatted"
docset: "stmt"
page: 292
physical_page: 304
category: "CAS File-Handling"
type: "Executable"
valid_in: "DATA step"
---

PUT Statement: Formatted
Writes variable values with the specified format in the output line.

Valid in:        DATA step
Categories:      CAS
                 File-Handling
Type:            Executable




                 Syntax
                 PUT <pointer-control> variable format. <@ | @@>;

                 PUT <pointer-control> (variable-list) (format-list) <@ | @@>;


                 Arguments
                 pointer-control
                    moves the output pointer to a specified line or column.

                     See       “Column Pointer Controls ” on page 268

                               “Line Pointer Controls ” on page 270

                     Example   “Example 1: Writing a Character between Formatted Values” on page
                               295

                 variable
                    specifies the variable whose value is written.

                 (variable-list)
                    specifies a list of variables whose values are written.

                     Requirement   The (format-list) must follow the (variable-list).

                     See           “How to Group Variables and Formats” on page 294
