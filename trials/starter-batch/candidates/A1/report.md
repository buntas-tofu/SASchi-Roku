# SAS to Python assessment

Status: static engineering plan for the requesting project owner and migration engineer. This is not an executed audit, proof of translator support, or approval to deploy. Input observations inspected: n = 0. A supplied schema, representative data, SAS reference results, or session configuration could change this assessment.

The complete supplied program has one DATA step and one arithmetic assignment. The first slice can cover that entire step, initially under an explicit numeric-input contract. The missing input dataset prevents confirming its actual schema, results, or runtime behavior.

## Evidence and source identity

- Request: `/tmp/roku-starter-20261101/A1/packet/request.txt`, specifying Python, planning only, no execution or translation, and no input data supplied.
- Program: `/tmp/roku-starter-20261101/A1/packet/source.sas`, lines 1 through 4, all inspected.
- Program SHA-256: `e393ee79d148975747a8121c03900124e5ed9ccea19ccb3da2ec7fed39782137`.
- Workflow: supplied `packet/skill/SKILL.md` and `packet/skill/references/source-map.md`. No repository revision was supplied. The hash identifies the inspected bytes.

Below, **Observed** means visible in the supplied source; **documented behavior** means primary SAS reference material, not a result observed on this program; **inference** and **proposal** are explicitly labeled.

## Inventory and execution order

| Location | Observed source | Assessment |
|---|---|---|
| Line 1 | `data work.want;` | Declares the sole output dataset, `work.want`. |
| Line 2 | `set work.have;` | Reads the sole named input, `work.have`, with no dataset options in the source. Its creation and contents are not supplied. |
| Line 3 | `doubled = amount * 2;` | Assigns an arithmetic result to `doubled`; reads `amount`. Neither variable's existing attributes are shown. |
| Line 4 | `run;` | Ends the single DATA step. There are no subsequent steps. |

**Observed:** no procedures, macro definitions or invocations, macro variables, generated-source mechanisms, includes, library assignments, explicit formats, format catalogs, encoding declarations, export statements, reports, or operating-system/network operations appear in these four lines. No `MERGE`, `BY`, explicit `RETAIN`, `LAG`, explicit `OUTPUT`, filtering, sorting, `KEEP`/`DROP`, character-width declaration, or automatic-variable reference appears.

**Documented behavior:** a DATA step normally writes a row automatically at the end of an iteration when explicit output has not replaced that behavior. [SAS OUTPUT statement documentation](https://www2.sas.com/onlinetutor/linklib/outputst.htm).

**Inference:** with an available ordinary input dataset and normal processing settings, this is a row-preserving transformation in input order: carry input columns forward and create or overwrite `doubled`. No code suggests a cross-row calculation. This is not a measured row-count or ordering result. Upstream data, input views, and session options remain uninspected.

The output dataset and SAS diagnostic log are relevant observable effects. No external deliverable is declared. The Python output location, persistence format, and consumer expectations are not specified.

## Unknowns that matter

1. **Input availability and schema:** obtain `work.have`, or a representative extract plus its descriptor. Confirm whether `amount` exists and is numeric or character; whether `doubled` already exists; and variable order, lengths, labels, formats, missing encodings, and text encoding. Do not assume that `doubled` is necessarily a new numeric column merely from its assignment.
2. **Value behavior:** profile missing values, negative values, fractions, extremes, and any character content in `amount`. SAS can convert a character operand temporarily for arithmetic while retaining its original character value, so string multiplication in Python would not be an equivalent interpretation. [SAS automatic character-to-numeric conversion](https://www2.sas.com/onlinetutor/wbt105/m30d2.htm).
3. **Missing and invalid arithmetic:** documented SAS behavior propagates numeric missing values through arithmetic; special numeric missings become ordinary missing in expression results. Invalid conversion and overflow also need comparison of results and diagnostics. These are candidate rules for testing against the actual SAS version, not executed findings. [SAS 9.3 Language Reference: Concepts, printed pages 59 and 60](https://support.sas.com/documentation/cdl/en/lrcon/65287/PDF/default/lrcon.pdf).
4. **Runtime context and delivery:** obtain the SAS version, relevant options such as observation limits, any input-view definition, actual row/byte scale, expected Python runtime, and downstream metadata/order requirements. These determine ingestion, memory strategy, and output representation. No specific Python framework is justified by the four lines alone.

## Practical first slice

**Proposal, not implemented:** migrate the entire four-line transformation after agreeing on a narrow initial contract: a supplied table with an existing numeric `amount`, no pre-existing `doubled`, known column attributes, and an explicit representation for missing values. Preserve all input rows, their sequence, duplicates, and other columns; add the calculated field. Select a Python tabular representation and storage boundary after inspecting the data size and consumer requirements.

First obtain a small, non-sensitive fixture with the real schema, an empty fixture, and SAS-produced expected outputs plus logs under recorded settings. Include ordinary numeric values and missing cases. Compare a later Python implementation against those references. Character `amount`, existing `doubled`, and extreme-value behavior require additional cases before broadening the accepted input contract. This staged contract is a proposed scope limit, not a claim that the supplied data meets it.

## Acceptance checks, all proposed and not run

- **Rows and order:** compare input and output counts to the SAS baseline; match each output row by input position, preserving duplicates. Verify the empty-table result and schema.
- **Schema and metadata:** compare column names/order, types, and required labels, formats, lengths, and encodings. Confirm all non-target columns and their missing distinctions survive unchanged; decide how SAS metadata is represented in Python outputs.
- **Values:** compare every `doubled` result for zero, positive, negative, fractional, ordinary missing, special missing, and large numeric inputs. Use exact agreement where achievable; define and justify any tolerance before acceptance. Do not accept mismatches hidden by display rounding.
- **Schema variants:** separately test existing numeric or character `doubled`, character `amount` with valid and invalid numeric text, and absent `amount`. Record SAS behavior before deciding whether Python reproduces it or explicitly rejects an out-of-contract input.
- **Failures and diagnostics:** compare behavior for unavailable input, conversion problems, overflow, and output-write failure. Record whether SAS continues or stops and whether partial output exists; agree on Python diagnostics and failure handling.
- **Delivery:** verify the agreed output artifact and downstream reader, including replacement behavior and reproducibility under recorded runtime settings. No report/export parity is required by the supplied source itself.

Acceptance requires recorded SAS/Python comparison results for the agreed contract. Static simplicity alone is not acceptance evidence.

## Actions actually taken

Listed this task's packet/output files; read the request, skill, source map, and complete source as text; computed the source SHA-256; consulted primary SAS documentation; and authored this report. One direct SAS documentation page fetch timed out; an official SAS manual and other primary pages were available. Source-map repository links were not followed because this assessment's access boundary excludes them.

No SAS program, translated program, translator, parser, fixture, or test suite was executed. No input data, generated SAS, logs, output datasets, or implementation was available for inspection. No translation was created. No external system was modified. The only deliverable created is this planning report.
