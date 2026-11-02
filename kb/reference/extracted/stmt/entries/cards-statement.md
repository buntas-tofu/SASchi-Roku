---
status: "generated"
entry: "CARDS Statement"
docset: "stmt"
page: 47
physical_page: 59
category: "File-Handling"
type: "Declarative"
valid_in: "DATA step"
---

CARDS Statement
Specifies that lines of data follow the statement.

Valid in:         DATA step
Category:         File-Handling
Type:             Declarative
Alias:            DATALINES, LINES
Restriction:      This statement is not supported in a DATA step that runs in CAS.
z/OS specifics:   The behavior of the CARDS statement is affected by the CARDIMAGE system
                  option. For more information, see “CARDIMAGE System Option: z/OS” in SAS
                  Companion for z/OS.
See:              “DATALINES Statement” on page 61




CARDS4 Statement
Specifies that the lines of data that follow the statement contain internal semicolons.

Valid in:         DATA step
Category:         File-Handling
Type:             Declarative
Alias:            DATALINES4, LINES4
Restriction:      This statement is not supported in a DATA step that runs in CAS.
See:              “DATALINES4 Statement” on page 63




CATNAME Statement
Logically combines two or more catalogs into one by associating them with a catref (a shortcut
name); clears one or all catrefs; lists the concatenated catalogs in one concatenation or in all
concatenations.

Note:             The CATNAME Statement has moved to SAS Global Statements.
