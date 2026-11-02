# ML-005: Data containing commas, ampersands, or operators becomes macro syntax

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: quoting. Search terms: %SUPERQ; %NRSTR; %BQUOTE; %NRBQUOTE; comma; ampersand.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

Macro quoting masks syntax rather than adding ordinary string quotes. Literal text and already stored values need different handling. %SUPERQ takes a variable name without an ampersand and protects its value from further resolution.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_payload=%nrstr(A&B,OR);
%macro ml_accept(value);
  %put PAYLOAD=%superq(value);
%mend;
%ml_accept(%superq(ml_payload))
```

## Expected behavior, not observed output

Expected: one parameter containing A&B,OR, with no attempted lookup of B. This example demonstrates protection; it is not evidence that every quoting context is covered.

## Corrective guidance

Use %NRSTR for suitable literal text and %SUPERQ for an existing variable value. Compilation-time quoting requires special handling of unmatched quotes or parentheses. Avoid automatic %UNQUOTE at boundaries.

## Migration recommendation (inference)

Keep data as data, with explicit parameter values instead of constructing executable text.

## Sources

- [SAS 9.3 Macro Language Reference, Macro Quoting](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/n0o0rjikrg6iezn1ltra79iamibr.htm). Consulted 2026-09-15.
- [Supporting reference](https://support.sas.com/resources/papers/387699_macro-programming-tools.pdf). Consulted 2026-09-15; cited edition is the version scope, not a content hash.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
