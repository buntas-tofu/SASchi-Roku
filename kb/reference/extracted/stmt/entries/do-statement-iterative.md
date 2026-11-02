---
status: "generated"
entry: "DO Statement: Iterative"
docset: "stmt"
page: 72
physical_page: 84
category: "CAS Control"
type: "Executable"
valid_in: "DATA step"
---

DO Statement: Iterative
Executes statements between the DO and END statements repetitively, based on the value of an
index variable.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Executable




                 Syntax
                 DO index-variable=specification-1 <, ...specification-n>;
                 ...more SAS statements...

                 END;


                 Arguments
                 index-variable
                    names a variable whose value governs execution of the DO group.

                     Tip          Unless you specify to drop it, the index variable is included in the
                                  data set that is being created.

                     CAUTION      Changing the index variable within the iterative DO group might
                                  cause infinite looping.

                 specification
                    denotes an expression or a series of expressions in this form:

                     start <TO stop> <BY increment> <WHILE(expression) | UNTIL(expression)>

                     The DO group is executed first with index-variable equal to start. The value of
                     start is evaluated before the first execution of the loop.

                     start
                        specifies the initial value of the index variable.

                           When it is used without TO stop or BY increment, the value of start can be a
                           series of items expressed in this form:
                           item-1 <, ...item-n>;

                           The items can be either all numeric or all character constants, or they can be
                           variables. Enclose character constants in quotation marks. The DO group is
                           executed once for each value in the list. If a WHILE condition is added, it
                           applies only to the item that it immediately follows.
