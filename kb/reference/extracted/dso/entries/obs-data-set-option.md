---
status: "generated"
entry: "OBS= Data Set Option"
docset: "dso"
page: 52
physical_page: 64
category: "Observation Control"
type: ""
valid_in: "DATA step and PROC steps"
---

OBS= Data Set Option
Specifies the last observation that SAS processes in a data set.

Valid in:         DATA step and PROC steps
Category:         Observation Control

Default:          MAX
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with input data sets only.
                  Cannot use with PROC SQL views




                  Syntax
                  OBS= n | nK | nM | nG | nT | hexX | MIN | MAX


                  Syntax Description
                  n | nK | nM | nG | nT
                      specifies a number to indicate when to stop processing observations, with n as
                      an integer. Using one of the letter notations results in multiplying the integer by
                      a specific value. That is, specifying K (kilo) multiplies the integer by 1,024; M
                      (mega) multiplies by 1,048,576; G (giga) multiplies by 1,073,741,824; or T (tera)
                      multiplies by 1,099,511,627,776. For example, a value of 20 specifies 20
                      observations, and a value of 3m specifies 3,145,728 observations.


                      Note: You can also use the KB, MB, and GB syntax notations.
