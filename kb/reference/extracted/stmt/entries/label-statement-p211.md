---
status: "generated"
entry: "Label: Statement"
docset: "stmt"
page: 211
physical_page: 223
category: "CAS Control"
type: "Declarative"
valid_in: "DATA step"
---

Label: Statement
Identifies a statement that is referred to by another statement.

Valid in:        DATA step
Categories:      CAS
                 Control
Type:            Declarative




                 Syntax
                 label: statement;


                 Required Arguments
                 label
                    specifies any SAS name. Follow the SAS name with a colon (:).

                     Requirement     The name that you choose for your label must be followed by a
                                     colon (:).

                     Example         data mydata2;
                                        type="new"; num=0;
                                        if type ="new" then
                                     /* LINK to label calculate */
                                        link calculate;
                                     /* define destination (statement) for label calculate */
                                        calculate: if num=0
                                           then order="yes";
                                        num=num+1;
                                     run;

                 statement
                    specifies any executable statement, including a null statement (;).

                     Restrictions    No two statements in a DATA step can have the same label.

                                     If a statement in a DATA step is labeled, it should be referenced by
                                     a statement or option in the same step.

                     Requirement     Both the label and statement arguments are required and they
                                     must be separated by a colon (:).

                     Tip             A null statement can have a label:
                                     ABC:;

                     Example         data test;
                                        <other-sas-DATA-step-statements>
