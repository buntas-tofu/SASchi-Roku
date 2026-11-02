---
status: "generated"
entry: "BUFNO= Data Set Option"
docset: "dso"
page: 11
physical_page: 23
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

BUFNO= Data Set Option
Specifies the number of buffers to be allocated for processing a SAS data set.

Valid in:        DATA step and PROC steps
Category:        Data Set Control
Restriction:     Use in the Compute Server, but not in CAS.
See:             BUFNO= Data Set Option in the documentation for your operating environment.




                 Syntax
                 BUFNO= n | nK | nM | nG | hexX | MIN | MAX


                 Optional Arguments
                 n | nK | nM | nG
                     specifies the number of buffers in multiples of 1 (bytes); 1,024 (kilobytes). For
                     example, a value of 8 specifies 8 buffers, and a value of 1k specifies 1,024
                     buffers.

                    Note: You can also use the KB, MB, and GB syntax notations.


                 hexX
                    specifies the number of buffers as a hexadecimal value. You must specify the
                    value beginning with a number (0–9), followed by an X. For example, the value
                    2dx sets the number of buffers to 45.

                 MIN
                   sets the minimum number of buffers to 0, which causes SAS to use the
                   minimum optimal value for the operating environment. This is the default.

                 MAX
                   sets the number of buffers to the maximum possible number in your operating
                   environment, up to the largest 4-byte, signed integer, which is 2 31–1, or
                   approximately 2 billion.
