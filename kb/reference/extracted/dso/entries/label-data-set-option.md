---
status: "generated"
entry: "LABEL= Data Set Option"
docset: "dso"
page: 47
physical_page: 59
category: "Data Set Control CAS"
type: ""
valid_in: "DATA step and PROC steps"
---

LABEL= Data Set Option
Specifies a label for a SAS data set.

Valid in:         DATA step and PROC steps
Categories:       Data Set Control
                  CAS




                  Syntax
                  LABEL='label'


                  Syntax Description
                  'label'
                      specifies a text string of up to 256 bytes. If the label text contains single
                      quotation marks, enclose the label in double quotation marks. To remove a label
                      from a data set, assign a blank space that is enclosed in quotation marks to the
                      label.

                     You can also use two single quotation marks in the label text and enclose the
                     string in single quotation marks.




                  Details
                  You can use the LABEL= option on input and output data sets. When you specify
                  LABEL= on input data sets, it assigns a file label for the duration of that DATA step
                  or PROC step. When you specify LABEL= for an output data set, the label becomes
                  a permanent part of that file. The file can be printed using the CONTENTS or
                  DATASETS procedure, and modified using PROC DATASETS.

                  A label that is assigned to a data set remains associated with that data set when
                  you update a data set by using the APPEND procedure or the MODIFY statement.
                  However, a label is lost if you use a data set with a previously assigned label to
                  create a new data set in the DATA step. For example:
