# ML-010: SELECT INTO leaves an old value when the result has no rows

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: state. Search terms: PROC SQL; SELECT INTO; SQLOBS; stale value; empty result.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

An empty SELECT result does not clear an existing target macro variable. A later step can reuse yesterday's or the previous iteration's value while the query itself completed normally.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_choice=previous;
data work.ml_empty;
  length item $ 12;
  stop;
run;
proc sql noprint;
  select item into :ml_choice trimmed from work.ml_empty;
  %let ml_rows=&sqlobs;
quit;
%put ROWS=&ml_rows CHOICE=&ml_choice;
```

## Expected behavior, not observed output

Expected: ROWS=0 and CHOICE=previous.

## Corrective guidance

Initialize the target before the query and capture SQLOBS immediately afterward. Decide explicitly whether zero rows means skip, stop, or a permitted empty value. Also check query errors; zero rows is not an error verdict.

## Migration recommendation (inference)

Use an explicit empty-result branch instead of retaining the last loop value. Treat this as a correction when the legacy program relied on retained state.

## Sources

- [SAS 9.2 SQL Procedure User's Guide, Using PROC SQL with the Macro Facility](https://support.sas.com/documentation/cdl/en/sqlproc/62086/HTML/default/a001360983.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
