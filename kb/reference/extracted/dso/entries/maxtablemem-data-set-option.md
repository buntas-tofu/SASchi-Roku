---
status: "generated"
entry: "MAXTABLEMEM= Data Set Option"
docset: "dso"
page: 49
physical_page: 61
category: "CAS Data Access"
type: ""
valid_in: "DATA step and PROC steps"
---

MAXTABLEMEM= Data Set Option
Specifies the maximum amount of memory in bytes that each thread should allocate for in-memory
blocks before converting to a memory-mapped file.

Valid in:       DATA step and PROC steps
Categories:     CAS
                Data Access

Default:        16M
Requirement:    You must have SAS Viya 3.3 or later.




                Syntax
                MAXTABLEMEM=integer | integerK | integerM | integerG


                Required Arguments
                integer
                    specifies the total number of bytes to allocate.

                integerK
                    specifies the total number of kilobytes to allocate.

                integerM
                    specifies the total number of megabytes to allocate.

                integerG
                    specifies the total number of gigabytes to allocate.




                Details
                Integer values are always converted to the nearest whole megabyte but not less
                than 1 megabyte. Specifying 0 indicates to use the value from the
                MAXTABLEMEM= session option.




                Comparisons
                n The MAXTABLEMEM= data set option overrides the MAXTABLEMEM=
                   LIBNAME statement option.
