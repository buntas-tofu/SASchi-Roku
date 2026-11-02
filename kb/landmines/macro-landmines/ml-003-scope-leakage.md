# ML-003: A helper macro overwrites a caller or session variable

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: scope. Search terms: %LOCAL; %GLOBAL; %LET; nested macros.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

A %LET assignment can update an already visible variable instead of creating a fresh local one. Helper names and loop counters can leak changes into a caller or the session.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_counter=outside;
%macro ml_bad;
  %let ml_counter=inside;
%mend;
%ml_bad
%put LEAKED=&ml_counter;

%let ml_counter=outside;
%macro ml_good;
  %local ml_counter;
  %let ml_counter=inside;
%mend;
%ml_good
%put PRESERVED=&ml_counter;
```

## Expected behavior, not observed output

Expected: LEAKED=inside and PRESERVED=outside. Repeat under a nested caller as a later validation variant.

## Corrective guidance

Declare scratch variables and loop counters local before assigning them. Specify intended outputs separately; declaring everything global spreads the problem.

## Migration recommendation (inference)

Pass inputs and return outputs explicitly. Preserve a documented side effect only when it is part of the required behavior.

## Sources

- [SAS Macro Language Reference, Examples of Macro Variable Scopes](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001072111.htm). Consulted 2026-09-15.
- [Supporting reference](https://support.sas.com/resources/papers/387699_macro-programming-tools.pdf). Consulted 2026-09-15; cited edition is the version scope, not a content hash.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
