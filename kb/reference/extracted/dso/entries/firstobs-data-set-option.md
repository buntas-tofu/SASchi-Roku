---
status: "generated"
entry: "FIRSTOBS= Data Set Option"
docset: "dso"
page: 33
physical_page: 45
category: "Observation Control Valid for input (read) processing only. Cannot use with PROC SQL views."
type: ""
valid_in: "DATA step and PROC steps"
---

FIRSTOBS= Data Set Option
Specifies the first observation that SAS processes in a SAS data set.

Valid in:        DATA step and PROC steps
Category:        Observation Control
Restrictions:    Use in the Compute Server, but not in CAS.
                 Valid for input (read) processing only.
                 Cannot use with PROC SQL views.




                 Syntax
                 FIRSTOBS=n | nK | nM | nG | hexX | MIN | MAX


                 Syntax Description
                 n | nK | nM | nG
                     specifies the number of the first observation to process in multiples of 1 (bytes);
                     1,024 (kilobytes); 1,048,576 (megabytes); or 1,073,741,824 (gigabytes). For
                     example, a value of 8 specifies the eighth observation, and a value of 3k
                     specifies 3,072.


                    Note: You can also use the KB, MB, and GB syntax notations.


                 hexX
                    specifies the number of the first observation to process as a hexadecimal value.
                    You must specify the value beginning with a number (0–9), followed by an X.
                    For example, the value 2dx sets the 45th observation as the first observation to
                    process.
                 MIN
                   sets the number of the first observation to process to 1. This is the default.

                 MAX
                   sets the number of the first observation to process to the maximum number of
                   observations in the data set. This number can be up to the largest eight-byte,
                   signed integer, which is 263–1, or approximately 9.2 quintillion observations.
