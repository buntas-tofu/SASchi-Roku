# ML-004: CALL SYMPUTX can write a different symbol table than intended

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: scope. Search terms: CALL SYMPUTX; G; L; F; symbol table.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

The third argument selects scope: G targets the global table, L the most local available table, and F searches for an existing variable before choosing where to create it. Omitting a deliberate scope decision makes behavior depend on calling context.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_result=outer;
%macro ml_scope;
  %local ml_result;
  %let ml_result=local_before;
  data _null_;
    call symputx('ml_result','local_after','L');
  run;
  %put INNER=&ml_result;
%mend;
%ml_scope
%put OUTER=&ml_result;
```

## Expected behavior, not observed output

Expected: INNER=local_after and OUTER=outer.

## Corrective guidance

Choose L for local scratch work and G for an explicitly global output. L outside a macro has only the global table available. SYMPUTX also trims surrounding blanks; do not treat it as a byte-preserving text assignment.

## Migration recommendation (inference)

Use explicit ownership of state and preserve any required whitespace in a separate data value.

## Sources

- [SAS 9.3 Functions and CALL Routines Reference, CALL SYMPUTX](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n1nexcs36ctqk5n11uao7k9myz7y.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
