---
status: "generated"
entry: "CALL Statement"
docset: "stmt"
page: 46
physical_page: 58
category: "Action CAS"
type: "Executable"
valid_in: "DATA step"
---

CALL Statement
Invokes a SAS CALL routine.

Valid in:        DATA step
Categories:      Action
                 CAS
Type:            Executable




                 Syntax
                 CALL routine(parameter-1 <, ...parameter-n>);


                 Arguments
                 routine
                    specifies the name of the SAS CALL routine that you want to invoke.

                     See   For information about available routines, see SAS Functions and CALL
                           Routines: Reference

                 (parameter)
                    is a piece of information to be passed to or returned from the routine.

                     Requirement   Enclose this information, which depends on the specific routine, in
                                   parentheses.

                     Tip           You can specify additional parameters, separated by commas.




                 Details
                 SAS CALL routines can assign variable values and perform other system functions.




                 See Also
                 SAS Functions and CALL Routines: Reference
