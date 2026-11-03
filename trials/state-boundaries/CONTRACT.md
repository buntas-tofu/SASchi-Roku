# Group, merge and width trial contract

Status: approved bounded engineering trial for maintainer review, 2026-11-02.
The principal accepted this immediate three-case batch. The exact fixtures,
interfaces and controls below are implementation choices within that scope.
This is not a live-SAS comparison, population study or general translator release.

Start revision: `27025665bb89e0b67c3f5f6fcf0f6113b9c54e10`, the merged PR 3.
Three fresh evaluators receive separate input-only packets, with unchanged skill
snapshots. Each evaluator supplies Python and base R, so the six targets are not
six independent generations. No parent history, oracle or sibling answers are
provided. Isolation is by directory and instructions, not an operating-system
security boundary. Model revision and sampling settings are not exposed.

## Fixed scope

| Packet | Skill use | Cases and observable boundary |
|---|---|---|
| groups | sas-diagnose-state | Five cases: ordered nested BY keys, hierarchical FIRST/LAST flags, global LAG versus receiver masking, region sum, missing keys, singleton and empty input |
| merge | sas-translate | Six cases: duplicate and ordinary-missing keys, unequal group sizes in both directions, shared numeric column, absent keys, one empty side and both empty |
| widths | sas-translate and sas-define-interchange | Five cases: two DATA steps, truncation/padding, first source assignment width, widening before SET, exact CSV text and width companion, blanks and empty input |

The source and packet request together define each interface. Numeric values are
finite or ordinary missing; special missing tags are out of scope. Sorting is a
precondition for group and merge tasks, with explicit rejection of unsorted input.
Width values admit printable ASCII only. They start as decoded, physically padded
synthetic values. No SAS reader, arbitrary Unicode, NUL, Parquet, label/catalog
interchange or generic program parsing is implied. The earlier NUL gap remains.

## Acceptance frozen before evaluation

`oracle.json` contains literal parent-derived values, including physical blanks.
`DERIVATION.md` records the reasoning and primary references. Neither is supplied
to evaluators. Freeze hashes bind the packets, this contract, oracle, derivation,
parent adapters and comparator before dispatch. First deliveries are archived
unchanged and separately hashed; self-test history and later repairs remain visible.

Run all 16 cases under both runtimes and both interfaces, 64 comparisons. Typed
API checks also enforce schemas, input preservation and repeated calls around
empty input. Every CLI comparison reopens the files and then verifies refusal
of the existing destination. Reject three unsorted input variants under both
interfaces and languages, 12 checks. Execute the supplied group bug once. Reject
12 deliberately corrupted outputs, four per task. These are comparator controls,
not 12 additional generated implementations. The planned machine total is 89.

Comparison is exact for column/table order, row multiplicity/order, strings and
missing positions. Numeric spellings may differ if their finite decimal values
match exactly; no floating tolerance is introduced for these integer fixtures.
The descriptor companion is compared even for empty input. Never change expected
results or edit candidates to manufacture a passing first delivery. Harness
defects, if discovered, must retain the original and a separately explained fix.

Artifact review has four criteria per task, 12 total: source/contract scope and
limits; independently reasoned mechanism trace; task-specific evidence (original
failure for groups, row/contribution/shared-column explanation for merge, physical
representation and descriptor for widths); and reproducible executed target
validation with failures retained. Review content, not phrasing or headings.

The skill-creator independent forward-testing workflow supplies the evaluation
method. No skill edit is required by a successful trial. Extract narrow changes
only if observed evidence justifies them. Future repeatability and MCP work remain
separate phases.
