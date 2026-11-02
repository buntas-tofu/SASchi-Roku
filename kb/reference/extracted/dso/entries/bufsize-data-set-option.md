---
status: "generated"
entry: "BUFSIZE= Data Set Option"
docset: "dso"
page: 13
physical_page: 25
category: "Data Set Control This data set option is not supported in a DATA step that runs in CAS."
type: ""
valid_in: "DATA step and PROC steps"
---

BUFSIZE= Data Set Option
Specifies the size of a permanent buffer page for an output SAS data set.

Valid in:        DATA step and PROC steps
Category:        Data Set Control
Restrictions:    Use with output data sets only.
                 This data set option is not supported in a DATA step that runs in CAS.
See:             BUFSIZE= Data Set Option under UNIX, z/OS, or OpenVMS in the documentation
                 for your operating environment.




                 Syntax
                 BUFSIZE=n | nK | nM | nG | hexX | MAX


                 Syntax Description
                 n | nK | nM | nG
                     specifies the page size in multiples of 1 (bytes); 1,024 (kilobytes); 1,048,576
                     (megabytes); or 1,073,741,824 (gigabytes). For example, a value of 8 specifies a
                     page size of 8 bytes, and a value of 4k specifies a page size of 4,096 bytes.


                    Note: You can also use the KB, MB, and GB syntax notations.



                    Note: If the system option and the data set option are not set, the default is 0.
                    As a result, SAS uses the minimum optimal page size for the operating
                    environment. The BUFSIZE= system option is used in either of the following
                    scenarios:
                 n if the BUFSIZE= data set option is not set

                 n if the BUFSIZE= data set option is set to zero

                    Use BUFSIZE=0 to reset the buffer page size to the default value in your
                    operating environment.


                 hexX
                    specifies the page size as a hexadecimal value. You must specify the value
                    beginning with a number (0–9), followed by an X. For example, the value 2dx
                    sets the page size to 45 bytes.

                 MAX
                   sets the page size to the maximum possible number in your operating
                   environment, up to the largest 4-byte, signed integer, which is 2 31–1, or
                   approximately 2 billion bytes.
