# ML-012: %SCAN collapses empty list positions unless instructed otherwise

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: lists. Search terms: %SCAN; %QSCAN; M modifier; empty token; delimiter.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

Consecutive delimiters normally behave as one delimiter. A positional list with an empty field can shift assignments silently. The M modifier retains zero-length positions; %QSCAN protects special characters in the result.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_list=alpha||gamma;
%put DEFAULT=[%scan(%superq(ml_list),2,|)];
%put POSITIONAL=[%qscan(%superq(ml_list),2,|,m)];
```

## Expected behavior, not observed output

Expected: DEFAULT=[gamma] and POSITIONAL=[].

## Corrective guidance

Specify delimiters and the empty-field policy. Add quoted-delimiter cases separately when needed; M is not a complete CSV parser.

## Migration recommendation (inference)

Choose split behavior explicitly and validate field counts. Do not discard empty fields merely because the target language makes that convenient.

## Sources

- [SAS Macro Language Reference, SCAN and QSCAN](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/z3514scan.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
