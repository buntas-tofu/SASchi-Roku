# ML-001: A macro reference reads the old value inside its producing DATA step

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: timing. Search terms: CALL SYMPUTX; SYMGET; compile time; run time.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

An ampersand reference is resolved while the step is being prepared; CALL SYMPUTX updates the symbol table when the step executes. Statement order alone does not make the reference see the new value.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_value=before;
data _null_;
  length compiled runtime $ 12;
  call symputx('ml_value','after','G');
  compiled="&ml_value";
  runtime=symget('ml_value');
  put compiled= runtime=;
run;
%put AFTER_STEP=&ml_value;
```

## Expected behavior, not observed output

Expected: compiled=before, runtime=after, and AFTER_STEP=after. This is a prediction, not a captured log.

## Corrective guidance

Use the DATA step value directly, SYMGET for a deliberate runtime lookup, or a subsequent step. Do not substitute RESOLVE casually: it can execute further macro expressions.

## Migration recommendation (inference)

Model the dependency explicitly in Python/R. A string substituted before a loop is different from a lookup during that loop.

## Sources

- [SAS Macro Language Reference, SYMGET](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000210322.htm). Consulted 2026-09-15.
- [Supporting reference](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/n1rvuiao0okk6cn1afs9ckt2unh9.htm). Consulted 2026-09-15; cited edition is the version scope, not a content hash.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
