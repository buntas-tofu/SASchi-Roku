# Group boundaries, match merges and character widths

Status: bounded engineering evidence for maintainer review, recorded 2026-11-02.
All 89 parent machine checks and 12 artifact-review criteria passed. This is
target-runtime evidence against hand-derived expectations, not a live-SAS
comparison or a general conversion guarantee.

Three fresh evaluators used unchanged existing skills. Each produced both Python
and R, so there are three evaluations and six paired target implementations.
The parent froze source, inputs, contract, literal truth and comparison code
before dispatch. All 18 first-delivery files remain unchanged. No parent repair
or adjustment to expected values was required.

## Independent acceptance

| Check | Count | Result |
|---|---:|---|
| 16 cases, two languages, CLI and typed API | 64 | Exact ordered values, missing positions, text and schemas matched |
| Unsorted input refusals, both languages and interfaces | 12 | Rejected without input changes or new output |
| Original group-bug execution | 1 | Reproduced row 3 last_account as 0 instead of 1 |
| Deliberately wrong output controls | 12 | All rejected by the same comparator |

Each CLI check reopens the files, then confirms an existing destination is refused
without modification. Each API check enforces column types and call isolation,
including a populated call repeated after empty input. Character checks include
both intermediate and final tables and the width descriptor on empty data.
CPython 3.12.3 and native R 4.3.3 ran. The exact receipt is [receipt.json](receipt.json).

| Task | Distinguishing observation | Parent checks |
|---|---|---:|
| Nested groups | A region change also changes account boundary flags. LAG continues across groups while the source masks only its receiver. | 29 |
| Match MERGE | Main emits eight rows. Shared-column values depend on new reads, including missing overwrites and exhaustion, while unique fields persist within a group. | 36 |
| Width propagation | Stage truncation survives widening in the next step. Concatenation includes padding, tag width follows the first source assignment, and reopened fields preserve every space. | 24 |

The 12 rejected controls corrupt outputs to represent queue reset, flat subgroup
flags, unmasked receivers, invented sum resets, Cartesian multiplicity, reread
shared values, coalesced missings, cross-key carry, runtime-derived tag width,
recovered characters, trimmed transport and incorrect blank LENGTH. They are
comparator controls, not 12 generated implementations.

## Reproduce and audit

From the repository root:

```sh
python3 trials/state-boundaries/verify.py
```

The replay requires native Rscript and Python standard library. It refuses to
skip a missing R runtime. `--receipt NEW_PATH` can write a new receipt; preserve
the first recorded receipt when comparing later runs. CI runs this after all
previous skill replays.

- [CONTRACT.md](CONTRACT.md): accepted scope, interfaces and rubric.
- [DERIVATION.md](DERIVATION.md) and [oracle.json](oracle.json): independent parent truth and primary source basis.
- [freeze.json](freeze.json): 49 artifacts hashed before dispatch.
- [evaluation.json](evaluation.json): evaluator isolation and tool provenance.
- [delivery.json](delivery.json): all 18 first-delivery hashes, without exclusions.
- [review.json](review.json): 12 artifact criteria and reviewed file identities.
- `candidates/{groups,merge,widths}/`: unchanged targets, reports, histories and self-test sources.

The receipt was written before this explanatory README, so its file manifest
does not include this README. Packet snapshots include the exact skill and
principal contract. Isolation was by instructions and directories, not an OS
security boundary. Model revision and sampling settings were not exposed.

Evaluator self-tests are retained as separate self-reported evidence. They do
not inflate the 89 parent checks. The group evaluator recorded an additional
overflow assertion and repair before first delivery; the merge evaluator recorded
a failed version-probe command and correction. The parent has not independently
accepted their expanded generated corpora, precision or overflow behavior. Their
archived self-tests expect the original `packet/` and `output/` workspace layout;
the parent replay above works directly from this repository layout.

## Skill decisions and next evidence

All six skills retain initial-guidance status, with no instruction changes.
This successful small batch does not establish that a skill caused the result;
the planned with/without repeatability study has not run.

Candidate next vector, inferred from the evaluator's reported failure: numeric
range, overflow and recovery after a missing accumulator deserve their own frozen
witnesses. This is a proposal, not an independently verified semantic rule.

The width companion now runs through base R and reopened CSV under an explicit
printable-ASCII contract. Full labels/catalogs/special-missing interchange,
SAS-binary reading, Parquet round trips and live-SAS capture remain open. This
narrow contract does not close the earlier starter's NUL gap. No MCP server,
generic translator or skill installation is delivered by this trial.
