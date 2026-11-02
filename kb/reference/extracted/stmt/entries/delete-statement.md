---
status: "generated"
entry: "DELETE Statement"
docset: "stmt"
page: 65
physical_page: 77
category: "Action CAS"
type: "Executable"
valid_in: "DATA step"
---

DELETE Statement
Stops processing the current observation.

Valid in:       DATA step
Categories:     Action
                CAS
Type:           Executable




                Syntax
                DELETE;


                Without Arguments
                When DELETE executes, the current observation is not written to a data set, and
                SAS returns immediately to the beginning of the DATA step for the next iteration.




                Details
                The DELETE statement is often used in a THEN clause of an IF-THEN statement or
                as part of a conditionally executed DO group.




                Comparisons
                n Use the DELETE statement when it is easier to specify a condition that excludes
                    observations from the data set or when there is no need to continue processing
                    the DATA step statements for the current observation.
                n Use the subsetting IF statement when it is easier to specify a condition for
                    including observations.
                n Do not confuse the DROP statement with the DELETE statement. The DROP
                    statement excludes variables from an output data set; the DELETE statement
                    excludes observations.
