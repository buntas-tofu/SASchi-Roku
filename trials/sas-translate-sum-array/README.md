# First translation skill trial

Status: one exploratory skill invocation and bounded Python replay for maintainer
review, recorded 2026-11-01. No live-SAS execution, general conversion guarantee,
or population success rate is claimed. CI replays the archived code; it does not
generate a new model response.

## Result

The unchanged [source](../../references/rosetta-code/corpus/sum_and_product_of_an_array.sas)
fills an array with the squares of 1 through 100, sums it into `b`, and prints
`b c`. The source never assigns `c` or computes a product. The candidate preserved
that behavior instead of repairing the program to match its task title.

Observed Python stdout was `338350 .` followed by a newline, with exit status 0
and empty stderr. The parent independently derived the sum through
`100 * 101 * 201 / 6` and checked the missing field separately. The missing-value
interpretation is supported by [SAS DATA-step initialization documentation](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm)
and [list PUT documentation](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p0jcwhe1ofmb49n1xf1q2kc44b0v.htm).
This is a documented-language interpretation plus Python evidence, not captured
SAS output. The source's SUM uses the documented [nonmissing argument sum](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0zxive1z1ctqin12w06c85jfigd.htm);
every array element is assigned in this particular program.

All seven negative controls were rejected: replacing missing with zero, inventing
a product value, excluding the final square, dropping the missing field, adding
a second record, hiding a tiny numeric difference through float rounding, and
executing an actual Python rewrite that computes a product.

## Evidence and replay

| Artifact | Role |
|---|---|
| [CONTRACT.md](CONTRACT.md) | Source pin, scope and parent acceptance policy |
| [request.txt](request.txt) | Neutral conversion request used for the isolated trial |
| [converted.py](converted.py) | Candidate preserved exactly as produced |
| [report.md](report.md) | Candidate agent's original self-report, not the parent verdict |
| [oracle.json](oracle.json) | Independently derived expectation and wrong-output controls |
| [verify.py](verify.py) | Parent subprocess execution and comparison, standard library only |
| [receipt.json](receipt.json) | Parent's first recorded replay, with artifact hashes and environment |

From the repository root:

```sh
python3 trials/sas-translate-sum-array/verify.py
```

The runner prints a new replay result without changing the recorded receipt.
Use `--receipt` with a new path to save another result; existing receipts refuse
overwrite. The initial parent replay used CPython 3.12.3 on Linux x86_64.
The exact tested source, candidate, oracle and verifier are hash-bound in the
receipt. The source and skills are pinned to Roku commit
`03fc5b3916b7423619b5e4308604215feb6b2c96` for the generation event.
The model revision and sampling controls were not captured. The replay command
reproduces execution of the saved candidate, not the original generation event.

The evaluator got the source and skill bundle in a separate temporary directory,
with no parent conversation or oracle. It was allowed primary language references
and prohibited sibling implementations, prior expected outputs and tests. The
report retains those original temporary paths as part of its unedited record;
use this directory's files and the replay command above now. The parent inspected
the resulting code and ran its own comparator rather than accepting the agent's
self-report. The parent's comparator allows equivalent numeric spellings and
spacing; the agent independently chose a stricter canonical output check.

## Skill assessment

Observed: the invocation kept source behavior, inspected the missing assignment,
derived an independent arithmetic witness, ran Python, and stated the missing SAS
baseline. This is evidence for this one instruction-following outcome.

Engineering inference: the skill's existing separation of source behavior from
algorithm redesign worked for this example. No skill edit is justified by this
successful trial alone. The skill remains initial guidance. A useful next trial
would exercise state or metadata instead of repeating this arithmetic example.

Keep this source, report and oracle out of the inputs for any future evaluation
that claims to hold this answer out. Once exposed, this is a regression example.
