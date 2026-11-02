# ML-002: CALL EXECUTE mixes immediate macro execution with queued SAS statements

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: timing. Search terms: CALL EXECUTE; generated code; step boundary.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

A macro invocation encountered by CALL EXECUTE can run immediately, while generated SAS statements wait for a step boundary. A macro can therefore inspect state before the SAS statements meant to create that state have run.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_status=before;
%macro ml_report;
  %put MACRO_SEES=&ml_status;
%mend;
data _null_;
  call execute('data _null_; call symputx("ml_status","after","G"); run;');
  call execute('%ml_report');
run;
%put AFTER_QUEUE=&ml_status;
```

## Expected behavior, not observed output

Expected: MACRO_SEES=before, then AFTER_QUEUE=after. The example deliberately exposes the ordering defect.

## Corrective guidance

Separate data production from macro consumption with an explicit completed step. Quoting-based deferral needs its own expansion trace; changing quote marks alone is not a general repair.

## Migration recommendation (inference)

Keep dynamic program construction under human review (MC-004). Translate the dependency graph before replacing it with function dispatch.

## Sources

- [SAS Macro Language Reference, CALL EXECUTE](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000543697.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
