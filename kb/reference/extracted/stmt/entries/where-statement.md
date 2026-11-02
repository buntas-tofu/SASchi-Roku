---
status: "generated"
entry: "WHERE Statement"
docset: "stmt"
page: 359
physical_page: 371
category: "Action CAS"
type: "Declarative"
valid_in: "DATA step or PROC step"
---

WHERE Statement
Selects observations from SAS data sets that meet a particular condition.

Valid in:        DATA step or PROC step
Categories:      Action
                 CAS
Type:            Declarative
Note:            Using a random number function in a WHERE statement might generate a different
                 result set from using a random number function in a subsetting IF statement. This
                 difference can be caused by how the criteria are optimized internally by SAS and is
                 expected behavior.
Tip:             The SAS Tutorial video Filtering a SAS Table in a DATA Step shows you how to
                 filter data using the WHERE statement.




                 Syntax
                 WHERE where-expression-1
                 < logical-operator where-expression-n>;


                 Arguments
                 where-expression
                   is an arithmetic or logical expression that generally consists of a sequence of
                   operands and operators.

                    Tips   The operands and operators described in the next several sections are
                           also valid for the WHERE= data set option.

                           You can specify multiple where-expressions.

                 logical-operator
                    can be AND, AND NOT, OR, or OR NOT.
