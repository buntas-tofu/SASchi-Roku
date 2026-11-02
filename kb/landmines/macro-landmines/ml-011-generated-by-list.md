# ML-011: A BY list is not a single FIRST. variable

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: generated-code. Search terms: FIRST.; LAST.; BY list; conditional BY; semicolon.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

Macro substitution does not parse a variable list. With two names, first.&ml_by expands to first.region visit, not a combined group-boundary test. A prematurely emitted semicolon can also leave a grouping key outside the BY statement.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_by=region visit;
%put GENERATED_TEST=first.&ml_by;

data work.ml_groups;
  input region visit;
  datalines;
1 1
1 1
1 2
2 1
;
run;
data work.ml_first;
  set work.ml_groups;
  by &ml_by;
  if first.visit;
run;
```

## Expected behavior, not observed output

Expected expansion: first.region visit (invalid as the intended single test). The explicit corrected example keeps rows (1,1), (1,2), and (2,1).

## Corrective guidance

Choose the intended grouping grain, preserve BY order, and name the corresponding FIRST./LAST. variable. The last key is appropriate for the full ordered key tuple in this example, not universally for every business rule.

## Migration recommendation (inference)

Review generated structure under MC-004. A list parser must account for DESCENDING and name literals; splitting blindly on blanks is not a general solution.

## Sources

- [SAS Language Reference Concepts, How the DATA Step Identifies BY Groups](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
