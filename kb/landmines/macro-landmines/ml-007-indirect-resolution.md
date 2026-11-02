# ML-007: An indirect reference needs another scan

Status: candidate teaching reference for migration practitioners; not an agency finding or a live-SAS verification receipt.
Evidence: source-backed description plus an original illustrative example. Example not executed in SAS.
Family: resolution. Search terms: double ampersand; indirect reference; rescan; numbered variables.
Source scope: cited Base SAS 9.x documentation; behavior on other releases requires confirmation.

## Failure mechanism

Concatenating &prefix and &index does not mean looking up the variable named by their concatenation. Multiple ampersands introduce rescanning; intermediate names and final values are different objects.

## Minimal illustration

Run in an isolated SAS session. These examples may create WORK datasets or session macro variables.

```sas
%let ml_slot3=ready;
%let ml_index=3;
%put INDIRECT=&&ml_slot&ml_index;
```

## Expected behavior, not observed output

Expected: INDIRECT=ready. The intermediate reference is &ml_slot3 after the first scan.

## Corrective guidance

Trace each scan before adding ampersands. Values containing macro triggers also need quoting; a successful indirect lookup does not make the resulting text safe in every context.

## Migration recommendation (inference)

Replace numbered symbol names with an indexed list or dictionary after confirming ordering and missing-key behavior.

## Sources

- [SAS Macro Language Reference, Referencing Macro Variables Indirectly](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001071915.htm). Consulted 2026-09-15.

Receipt status: no live runtime receipt. The teaching example is ingested content and must not be used as a held-out retrieval evaluation question.
