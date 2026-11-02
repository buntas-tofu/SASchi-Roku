---
status: "generated"
entry: "SET Statement"
docset: "stmt"
page: 331
physical_page: 343
category: "CAS File-Handling"
type: "Executable"
valid_in: "DATA step"
---

SET Statement
Reads an observation from one or more SAS data sets.

Valid in:       DATA step
Categories:     CAS
                File-Handling
Type:           Executable
Note:           The variables read using the SET statement are retained in the PDV. For more
                information, see “How the DATA Step Processes Data” in SAS Programmer’s Guide:
                Essentials and “RETAIN Statement” on page 319.




                Syntax
                SET<SAS-data-set(s) <(data-set-options(s) )> >
                   <options>;


                Without Arguments
                When you do not specify an argument, the SET statement reads an observation
                from the most recently created data set.


                Arguments
                SAS-data-set (s)
                  specifies a one-level name, a two-level name, or one of the special SAS data set
                  names.

                   Tips      You can specify data set lists. For more information, see “Using Data
                             Set Lists with SET” on page 338.

                             Instead of using a data set name, you can specify the physical
                             pathname to the file, using syntax that your operating system
                             understands. The pathname must be enclosed in single or double
                             quotation marks.

                   See       See “SAS Data Sets” in SAS Language Reference: Concepts for a
                             description of the levels of SAS data set names and when to use each
                             level.

                   Example   “Example 13: Using Data Set Lists” on page 343
