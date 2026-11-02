---
status: "generated"
entry: "EXTENDOBSCOUNTER= Data Set Option"
docset: "dso"
page: 30
physical_page: 42
category: "Data Set Control"
type: ""
valid_in: "DATA step and PROC steps"
---

EXTENDOBSCOUNTER= Data Set Option
Specifies whether to extend the maximum observation count in a new output SAS data file.

Valid in:         DATA step and PROC steps
Category:         Data Set Control
Alias:            EOC=

Defaults:         For Windows and z/OS, the default is YES.
                  For UNIX, the default is not set.
Restrictions:     Use in the Compute Server, but not in CAS.
                  Use with output data files only.
                  Use with the V9 engine only.
                  If you copy a file, the extended observation count attribute is not inherited.
