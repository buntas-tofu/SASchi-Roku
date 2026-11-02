# ML-006: A suffix changes the variable name or consumes the dataset separator

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: resolution. Search terms: period delimiter; two-level dataset; suffix.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

The scanner takes following name characters as part of a macro variable name. A delimiter period ends the reference and is consumed; a literal period after the reference needs a second period.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_stem=panel;
%let ml_lib=work;
%put SUFFIX=&ml_stem._2024;
%put DATASET=&ml_lib..panel;
```

## Expected behavior, not observed output

Expected: SUFFIX=panel_2024 and DATASET=work.panel. Without the delimiter before the underscore, a different macro variable name is requested.

## Corrective guidance

Separate name termination from literal punctuation. Inspect fully expanded dataset and file names before running generated code.

## Migration recommendation (inference)

Represent library and member names as separate validated fields rather than reproducing textual delimiter rules.

## Sources

- [SAS Macro Language Reference, Using Macro Variables](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001071889.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
