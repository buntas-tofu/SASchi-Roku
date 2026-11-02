# ML-009: Macro arithmetic silently discards a fractional result

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: arithmetic. Search terms: %EVAL; %SYSEVALF; integer division; %IF.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

Macro arithmetic defaults differ from ordinary floating-point calculations. %EVAL performs integer arithmetic; %SYSEVALF provides floating-point evaluation. A translated expression must preserve the intended arithmetic domain.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%put INTEGER=%eval(7/2);
%put FRACTION=%sysevalf(7/2);
%put BOOLEAN=%sysevalf(0.25 > 0,boolean);
```

## Expected behavior, not observed output

Expected: INTEGER=3, FRACTION=3.5, and BOOLEAN=1.

## Corrective guidance

Use %SYSEVALF when fractions are intentional, with an explicit conversion when feeding an integer or Boolean consumer. Do not assume a decimal token is valid in %EVAL arithmetic.

## Migration recommendation (inference)

Declare numeric types and division semantics. Repairing an accidental truncation changes behavior and needs a stated decision.

## Sources

- [SAS 9.3 Macro Language Reference, Arithmetic Expressions](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/p17i177l3z4kzgn11m7pl8833ch7.htm). Consulted 2026-09-15.
- [Supporting reference](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a000206831.htm). Consulted 2026-09-15; cited edition is the version scope, not a content hash.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
