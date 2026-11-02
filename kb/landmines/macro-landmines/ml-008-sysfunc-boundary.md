# ML-008: DATA step function syntax does not transfer unchanged into %SYSFUNC

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: functions. Search terms: %SYSFUNC; %QSYSFUNC; nested functions; quotes.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

%SYSFUNC bridges macro arguments to supported SAS functions. Character arguments do not use DATA step quoting conventions, and nesting ordinary functions inside one %SYSFUNC call is not equivalent to nesting separate %SYSFUNC calls.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%put NESTED=%sysfunc(abs(%sysfunc(mod(17,5))));
%put LETTERS=%sysfunc(compress(a-b,-));
```

## Expected behavior, not observed output

Expected: NESTED=2 and LETTERS=ab. The invalid counterpart abs(mod(17,5)) inside a single %SYSFUNC is intentionally not executed here.

## Corrective guidance

Use one %SYSFUNC boundary per nested function and check the supported-function list. %QSYSFUNC masks special characters in the returned value; it does not repair arbitrary malformed inputs.

## Migration recommendation (inference)

Map the actual function and formatting contract, not just the function spelling.

## Sources

- [SAS 9.3 Macro Language Reference, SYSFUNC and QSYSFUNC](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/p1o13d7wb2zfcnn19s5ssl2zdxvi.htm). Consulted 2026-09-15.
- [Supporting reference](https://support.sas.com/resources/papers/proceedings12/190-2012.pdf). Consulted 2026-09-15; cited edition is the version scope, not a content hash.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
