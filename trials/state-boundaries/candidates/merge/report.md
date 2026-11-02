# Match-MERGE conversion report

Status: candidate engineering conversion and target-runtime observations for the principal's review. This is not a live-SAS comparison or a general SAS-equivalence finding. SAS execution remains pending. The principal may use these files for independent acceptance testing; these observations do not authorize broader production claims.

## Scope and comparison contract

The supplied `source.sas` merges `work.left` followed by `work.right`, grouped by numeric `key`, and emits `want`. This implementation is specific to that program and the supplied schema. No macros, includes, formats, special missing tags, text columns, statistical procedures, or external resources are required. The Python implementation uses its standard library; R uses base R.

Before implementing the target, the comparison was set to exact numeric values, missingness, output columns and their order, row order and multiplicity, contribution flags, input preservation, and call isolation. This program performs no numerical approximation. Comparisons did not use a tolerance. CSV byte spelling of an equivalent number, such as `1` and `1.0`, is not part of numeric equality. CSV missing fields must be blank. Headers must exist for empty outputs.

The request provides the admitted input domain: individually ascending tables, missing key before numeric keys, integer keys, and finite numeric payloads or ordinary missing. Both APIs check ordering and reject an inversion; neither sorts source rows. All input columns are numeric, so the request's character-preservation examples are outside this schema. The delivered code does not pretend that numeric `0007` is a character identifier or that text `NA` is numeric missing. Blank is the only accepted CSV missing representation.

## Documentary basis and inference boundary

The following are Tier 2 documentary sources, read from primary SAS documentation. They are behavior references, not executed receipts:

- [SAS MERGE statement](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000202970.htm): each key group emits the maximum of its input counts. Duplicate keys are processed by position, not as a Cartesian product.
- [SAS Usage Note 48705](https://support.sas.com/kb/48/705.html): common variables are overwritten by the inputs actually read in an iteration. An exhausted shorter input is not reread. Missing values overwrite in the same way as nonmissing values.
- [SAS IN= option](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000131134.htm): once an input contributes to a BY group, its indicator remains set through that group unless program logic resets it.
- [SAS automatic missing-value initialization](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm): input variables retain values within a BY group and reset on group change.

Inference: applying these rules to this bounded numeric source yields the trace below. It was derived separately from target execution and is not captured SAS output. The packet's evidence map was read, but its sibling and prior-result links were not followed, respecting isolation.

For group counts `L` and `R`, row count is `max(L, R)`. While both inputs have another row, left writes first and right writes second. After one input runs out within the group, only the other input writes. Unique variables retain the shorter input's last value, including missing, until the next group. Flags describe group contribution, not whether that input read a new row on this particular iteration.

`key` and `shared` appear in both descriptors. They occupy one column each, not suffixed join columns. New reads of `shared` overwrite the current value, including overwrites with missing. In particular, right has precedence only when right actually reads. The same-key value written into `key` by either input identifies the current group. At a new group, all input values and flags reset so absent-source columns cannot leak from the preceding group. Two missing keys belong to the same group.

## Independently derived trace

`.` denotes ordinary numeric missing in this report; CSV uses a blank field. The two read columns identify new input reads using their sequence values. A blank read means that input supplies no new row in that iteration.

| Output row | Key | New left read | New right read | left_seq | right_seq | a | b | shared | from_left | from_right |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | . | 1 | 11 | 1 | 11 | 10 | 100 | 101 | 1 | 1 |
| 2 | . | 2 | | 2 | 11 | 20 | 100 | 2 | 1 | 1 |
| 3 | 1 | 3 | 12 | 3 | 12 | 30 | 200 | 102 | 1 | 1 |
| 4 | 1 | 4 | 13 | 4 | 13 | 40 | 300 | . | 1 | 1 |
| 5 | 1 | 5 | | 5 | 13 | 50 | 300 | 5 | 1 | 1 |
| 6 | 2 | 6 | | 6 | . | 60 | . | 6 | 1 | 0 |
| 7 | 3 | | 14 | . | 14 | . | 400 | 104 | 0 | 1 |
| 8 | 4 | 7 | 15 | 7 | 15 | 70 | 500 | . | 1 | 1 |

The main case has group count pairs `(2,1)`, `(3,2)`, `(1,0)`, `(0,1)`, and `(1,1)`, producing `2 + 3 + 1 + 1 + 1 = 8` rows. A Cartesian join would produce 11 rows. On rows 2 and 5, the new left read replaces `shared`, while right's unique fields and contribution flag remain retained. Row 8 demonstrates a missing right value overwriting nonmissing left `shared=7`.

| Supplied case | Left rows | Right rows | Expected and observed output rows | Distinguishing observation |
|---|---:|---:|---:|---|
| main | 7 | 5 | 8 | Left continues after right, and groups reset |
| right-long | 1 | 3 | 3 | Shared sequence is 100, missing, 300; left flag remains 1 |
| missing-only | 1 | 1 | 1 | Missing keys match; right missing replaces left shared 5 |
| left-empty | 0 | 2 | 2 | Left columns missing and left flag 0 |
| right-empty | 2 | 0 | 2 | Right columns missing and right flag 0 |
| empty | 0 | 0 | 0 | Both APIs empty; R and CSV retain columns |

## Executed observations

Environment observed: Python 3.12.3 and R 4.3.3 (2024-02-29). Model revision and model settings were not exposed. No SAS runtime was available or invoked.

`selftest.py` stores the six hand-derived packet expectations, independently reads input CSV, and implements a separate closed-form group-position witness. The witness selects unique fields at `min(position,last)` and selects shared from a current right row if present, otherwise a current left row. It does not use the conversion's row-buffer implementation. Eighty generated cases use seed `20261102`, five possible keys including missing and negative values, per-input group sizes from zero to four, and missing, zero, negative, fractional, and small finite payloads.

Observed pass results:

- Six supplied cases, 16 total expected output rows, in both languages.
- Eighty generated cases checked in both languages against the separate position witness.
- Eighty-six API cases per language, including repeated calls around empty inputs, unchanged caller inputs, and mutation of returned results followed by a fresh call.
- 172 successful CLI executions with exact parsed numeric values, missingness, columns, and row order.
- 172 reruns against an existing destination refused, with its output bytes and file inventory unchanged.
- Six unsorted API cases per language and 12 unsorted CLI cases refused. The CLI checks confirmed that a destination was not created on those failures.
- Three deliberately wrong outputs were rejected by the exact comparator: retained right `shared` after exhaustion, a per-read contribution flag, and Cartesian multiplicity.

No target-code repairs were needed after the first test run. One version-introspection command failed and was corrected; the exact record is in `history.md`.

## Reproduction and interface

Run commands from this isolated workspace. Use a fresh destination each time:

```sh
python3 output/converted.py packet/cases/main scratch-python
Rscript --vanilla output/converted.R packet/cases/main scratch-r
PYTHONDONTWRITEBYTECODE=1 python3 output/selftest.py
python3 inertia-drift-lint output
```

Python: import `converted.py` and call `translate({"left": left_rows, "right": right_rows})`. Missing numeric values are `None`; output is `{"want": rows}`. Empty input tables are `[]`.

R: source `converted.R` and call `translate(list(left = left_frame, right = right_frame))`. Supply numeric columns, including numeric `NA`; output is `list(want = frame)`. Empty inputs require the full numeric schema. Importing or sourcing does not run the CLI.

Both CLIs read `left.csv` and `right.csv`, and write `want.csv` in exactly the supplied output-column order. They reject an existing destination before reading or writing data. All merge state belongs to the call and current group.

## Remaining limitations

Live-SAS output agreement, SAS dataset descriptors beyond the requested numeric schema, labels, formats, storage lengths, and special missing tags remain untested. These programs are a manual translation of the supplied source, not a SAS parser or a translator for other programs. Numeric CSV is parsed to each runtime's floating-point representation. The tested decimal samples round-trip exactly; this is not a proof for every extreme numeric spelling or cross-platform floating-point boundary. No character behavior is claimed because this schema has no character columns.

Generated witnesses and hand traces supply independent target checks, but cannot substitute for running the source in SAS. Acceptance would change if independently captured SAS output disagrees with the trace or if the admitted input contract changes.

## Source and input identity

SHA-256 of the immutable source artifacts:

| Artifact | SHA-256 |
|---|---|
| source.sas | c6a1640eb1600a02e185ef81831ce7f1647f397e429c4c0a1099f649ad474fc9 |
| schema.csv | 12491f36d345afd1523d66caa666ac82af7b5dd4d2bc2bdb5e8a26ea0f18e028 |
| request.txt | 3d11db6ad10e4f12810dec601ab5e854614a4c3ea96777355f1f6c7b7cd92fc4 |
| AGENTS.md | 184dcc3afd7252fef7688bf97ee4d4266f92a5d5d8d58cb0c00505a27bf2d199 |
| skills/sas-translate/SKILL.md | 6cdb948823b5fb1caccfee7c3c4754892bdb617a0b7da526272bbd21220ac91c |
| skills/sas-translate/references/evidence.md | da999e1e82759c319fa51ca39c221c72e0bf3637bfacf303e2043abb861e949e |

Each case digest below hashes its files in sorted filename order, adding UTF-8 filename, one NUL byte, then the file's original bytes for each file.

| Input case | SHA-256 |
|---|---|
| empty | 4f582f45b1819cd07284fe71aa22d7a29edc6eef22b591e01bfb3699f0ed8452 |
| left-empty | da899e74771f53fe86ed2678c1f293990afb532b9c25ccd2dfbf3e28f1333151 |
| main | 952f944460a5d438e85c4aeb023749bdd43d282d489091572465555060f9275d |
| missing-only | b66cdc9349aa8fd8f8be1bd83eaa716742ae520c4e9d1f88dc09eef0cd5b5828 |
| right-empty | f871589ff625822475924f3a7d12a23b12398aed696523b0cbbe4b2b123da1c2 |
| right-long | 12d6afad8d2e41c5d05dcd27d19f382bf12aa9aefaa53125d55e52107e26bc81 |

Delivered implementation hashes:

- `converted.py`: `9beb2d98b0c32a459a5a2506d97cd197d41dd11e6a47b0356f338263fc91e597`
- `converted.R`: `730665e2ef6d0b88a978214d2e0c225ea9058e7881cea01307eabd31bc07fe4c`
