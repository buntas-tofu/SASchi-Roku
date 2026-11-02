---
status: "generated"
entry: "OBSBUF= Data Set Option"
docset: "dso"
page: 50
physical_page: 62
category: "Data Set Control Valid only for a DATA step view"
type: ""
valid_in: "DATA step and PROC steps"
---

OBSBUF= Data Set Option
Determines the size of the view buffer for processing a DATA step view.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Restrictions:     Use in the Compute Server, but not in CAS.
                  Valid only for a DATA step view




                  Syntax
                  OBSBUF=n


                  Syntax Description
                  n
                      specifies the number of observations that are read into the view buffer at a
                      time.

                      Default    32K bytes of memory are allocated for the default view buffer, which
                                 means the default number of observations that can be read into the
                                 view buffer at one time depends on the observation length.
                                 Therefore, the default is the number of observations that can fit into
                                 32K bytes. If the observation length is larger than 32K bytes, then
                                 only one observation can be read into the buffer at a time.

                      Tip        To determine the observation length in bytes, use PROC CONTENTS
                                 for the DATA step view.

                      CAUTION    The maximum value for the OBSBUF= option depends on the
                                 amount of available memory. If you specify a value so large that the
                                 memory allocation of the view buffer fails, an out-of-memory error results.




                  Details
                  The OBSBUF= data set option specifies the number of observations that can be
                  read into the view buffer at a time. The view buffer is a segment of memory that is
                  allocated to hold output observations that are generated from a DATA step view.
