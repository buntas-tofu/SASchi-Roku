---
status: "generated"
entry: "DM Statement"
docset: "stmt"
page: 70
physical_page: 82
category: ""
type: ""
valid_in: ""
---

DM Statement
Submits SAS Program Editor, Log, Procedure Output, or text editor commands as SAS statements.

Note:            The DM Statement has moved to SAS Global Statements.




DO Statement
Specifies a group of statements to be executed as a unit.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable
See:             DOLIST syntax (definition)
                 “Forms of the Iterative DO Loop” in SAS Programmer’s Guide: Essentials




                 Syntax
                 DO;
                 ...more SAS statements...

                 END;


                 Without Arguments
                 Use the DO statement for simple DO group processing.




                 Details
                 The DO statement is the simplest form of DO group processing. The statements
                 between the DO and END statements are called a DO group. You can nest DO
                 statements within DO groups.

                 You can also use DOLIST syntax to iterate over a list of values. For more
                 information, see “DOLIST syntax” in SAS Programmer’s Guide: Essentials.


                 Note: The memory capabilities of your system can limit the number of nested DO
                 statements that you can use. For more information, see the SAS documentation
