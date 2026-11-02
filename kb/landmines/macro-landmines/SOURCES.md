# Public source register

Status: reference register for candidate corpus review, not a runtime receipt.
Consulted 2026-09-15. URLs are mutable; edition labels are scope markers, not
archived content hashes. Excluded from ingestion by the pack's explicit source list.

| Card | Primary source | Additional source |
|---|---|---|
| ML-001 | [SAS Macro Language Reference, SYMGET](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000210322.htm) | [Supporting source](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/n1rvuiao0okk6cn1afs9ckt2unh9.htm) |
| ML-002 | [SAS Macro Language Reference, CALL EXECUTE](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000543697.htm) | None required |
| ML-003 | [SAS Macro Language Reference, Examples of Macro Variable Scopes](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001072111.htm) | [Supporting source](https://support.sas.com/resources/papers/387699_macro-programming-tools.pdf) |
| ML-004 | [SAS 9.3 Functions and CALL Routines Reference, CALL SYMPUTX](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n1nexcs36ctqk5n11uao7k9myz7y.htm) | None required |
| ML-005 | [SAS 9.3 Macro Language Reference, Macro Quoting](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/n0o0rjikrg6iezn1ltra79iamibr.htm) | [Supporting source](https://support.sas.com/resources/papers/387699_macro-programming-tools.pdf) |
| ML-006 | [SAS Macro Language Reference, Using Macro Variables](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001071889.htm) | None required |
| ML-007 | [SAS Macro Language Reference, Referencing Macro Variables Indirectly](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001071915.htm) | None required |
| ML-008 | [SAS 9.3 Macro Language Reference, SYSFUNC and QSYSFUNC](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/p1o13d7wb2zfcnn19s5ssl2zdxvi.htm) | [Supporting source](https://support.sas.com/resources/papers/proceedings12/190-2012.pdf) |
| ML-009 | [SAS 9.3 Macro Language Reference, Arithmetic Expressions](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/p17i177l3z4kzgn11m7pl8833ch7.htm) | [Supporting source](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000206831.htm) |
| ML-010 | [SAS 9.2 SQL Procedure User's Guide, Using PROC SQL with the Macro Facility](https://support.sas.com/documentation/cdl/en/sqlproc/62086/HTML/default/a001360983.htm) | None required |
| ML-011 | [SAS Language Reference Concepts, How the DATA Step Identifies BY Groups](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm) | None required |
| ML-012 | [SAS Macro Language Reference, SCAN and QSCAN](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/z3514scan.htm) | None required |

Community-facing source: Kevin Russell, SAS Institute, *Surviving the SAS Macro
Jungle by Using Your Own Programming Toolkit*, PharmaSUG 2016, paper BB11.
It supplies a practitioner-facing bridge for scope and quoting; its presence is
not a measured claim about prevalence across the community.

The SYSFUNC card also points to SAS Global Forum 2012 paper 190-2012, whose
indexed examples describe quotation and nesting mistakes. That PDF's full body
could not be fetched during this pass; the card's technical claims are supported
by the separately consulted SYSFUNC reference, not by an assumed full-paper review.

Cards paraphrase the relevant mechanisms and use original small examples.
Source rights remain with their owners. No blanket vendor documentation license
or permission to redistribute vendor manuals is asserted.
