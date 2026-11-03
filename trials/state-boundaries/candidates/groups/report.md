# Stateful conversion diagnosis

Status: bounded engineering evidence for the supplied DATA step. This is not a live SAS execution receipt or a general equivalence certification. The requesting maintainer may inspect and test this delivery; independent acceptance remains separate.

## Evidence and comparison

The immutable packet supplies the source program, buggy target, schema, five ordered input tables, and initial diagnostic guidance. Those are the task's source material. SAS documentation is candidate-tier semantic evidence. The expected rows below are explicitly an independently derived trace, not captured SAS output. Target execution results are observations from Python 3.12.3 and R 4.3.3. Model revision and settings were not exposed.

Comparison policy was fixed before the repair: table and column names/order, row count/order, identifier text, every numeric cell, and every missing position must agree. Tests compare parsed numeric values exactly, with no tolerance; they do not compare alternative valid CSV quoting or numeric spellings. Python missing values are `None`; R missing values are numeric `NA`. The API is `translate(tables)` in both targets. Importing or sourcing the files does not invoke the CLI.

## Reproduced original failure

Run `python3 -B output/selftest.py --baseline` from the isolated workspace to execute the unchanged packet target against independent hand fixtures. In row-major order and the schema's column order, the original first differences are:

| Input | First differing cell | Original target | Independent trace |
| --- | --- | --- | --- |
| main | row 3, `last_account` | 0 | 1 |
| hierarchy | row 1, `last_account` | 0 | 1 |
| missing-keys | row 2, `raw_prev` | missing | 2 |
| single | none | one matching row | one hand-derived row |
| empty | none | zero rows | zero rows |

The main case contains seven rows. Its complete differing cells are row 3 `last_account` (0 to 1), row 4 `raw_prev` (missing to 20) and `first_account` (0 to 1), row 6 `raw_prev` (missing to -2) and `last_account` (0 to 1), and row 7 `raw_prev` (missing to 0) and `first_account` (0 to 1). All other main cells match the hand trace below. The hierarchy case additionally differs at row 2 `raw_prev` (missing to 4) and `first_account` (0 to 1). The missing-key case additionally differs at row 2 `last_account` (0 to 1), and row 3 `raw_prev` (missing to 3) and `first_account` (0 to 1). These observations preserve the original failure without copying or modifying the packet.

The two-row hierarchy input is a minimal supplied witness for hierarchical boundaries: both account values are 9, but the region changes from 1 to 2. It distinguishes nested BY semantics from independent account comparisons. Missing-keys row 2 also distinguishes a continuous queue from a reset queue because its predecessor has a nonmissing value.

## Source state transitions

The source has one unconditional LAG occurrence and one retained sum accumulator. Every input row reaches the LAG, the two conditional assignments, the sum statement, and one implicit output event. There is no filter, explicit output, macro, include, or second DATA step in this slice.

The queue initially contains one missing value. Each `raw_prev=lag(value)` removes the prior queued value, returns it as `raw_prev`, and enqueues the current value, including missing. Neither `FIRST.account` nor `FIRST.region` resets that queue. `prev=raw_prev` assigns the current result; `FIRST.account` masks only `prev` to missing.

`BY region account` is hierarchical. A region change also starts a new account group, even when the account number is unchanged. Similarly, a following region change ends the current account group. Thus the first row has both FIRST flags, the final row has both LAST flags, and the account boundary comparison uses the pair `(region, account)`. Ordinary missing equals ordinary missing for grouping, and sorts before any finite number under the packet contract.

`total` begins at zero because it is a sum-statement accumulator. Each first-region row assigns 100 before adding its current value. A missing current value contributes nothing to a nonmissing total. Account-only changes do not reset `total`.

The derived main output follows. `.` denotes ordinary numeric missing in this report only; delivered CSV uses blank numeric fields.

| row_id | region | account | value | raw_prev | prev | total | first_region | last_region | first_account | last_account |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0007 | 1 | 7 | 5 | . | . | 105 | 1 | 0 | 1 | 0 |
| NA | 1 | 7 | . | 5 | 5 | 105 | 0 | 0 | 0 | 1 |
| g3 | 1 | 8 | 20 | . | . | 125 | 0 | 1 | 1 | 1 |
| g4 | 2 | 8 | 100 | 20 | . | 200 | 1 | 0 | 1 | 0 |
| g5 | 2 | 8 | -2 | 100 | 100 | 198 | 0 | 0 | 0 | 1 |
| g6 | 2 | 9 | 0 | -2 | . | 198 | 0 | 1 | 1 | 1 |
| g7 | 3 | 9 | . | 0 | . | 100 | 1 | 1 | 1 | 1 |

For rows 1 through 7, the queue before execution is respectively `[., 5, ., 20, 100, -2, 0]`; after execution it is `[5, ., 20, 100, -2, 0, .]`. The retained total before each row is `[0, 105, 105, 125, 200, 198, 198]`. The first-region assignment changes the working total to 100 on rows 1, 4, and 7. Output positions equal input positions. Row 3's missing predecessor happens to conceal the buggy queue reset, but its incorrect LAST flag still exposes the first divergence.

The missing-keys hand trace has raw predecessors `[., 2, 3]`, all `prev` values missing, totals `[102, 105, 104]`, FIRST-region flags `[1, 0, 1]`, LAST-region flags `[0, 1, 1]`, and both account flag sequences `[1, 1, 1]`. The single missing-value row emits total 100 with all four flags equal to 1. Empty input executes no rows and produces an empty output with the specified schema.

## Repair and executed checks

Both targets retain the LAG queue across all rows and propagate region changes into account flags. They retain source order, validate ascending missing-first keys, and reject unsorted inputs before creating the destination. The API preserves inputs, allocates output independently, and has fresh state on every call. The CLI reads identifiers as text, keeps numeric missing distinct from literal text `NA`, emits schema headers for empty tables, and refuses existing file or directory destinations without altering them.

Observed final validation: 47 datasets passed the Python API checks, comprising the five supplied cases, 40 deterministically generated datasets, one precision case, and one overflow case. The generated oracle scans contiguous region and account runs, separately from the target's adjacent-row algorithm. Both CLIs passed all 47 datasets, for 94 successful CLI executions. Direct R API checks passed a three-row hand trace, integer input, empty numeric schemas, repeated calls surrounding empty input, and input preservation. Six invalid Python API cases, three invalid R API cases, twelve invalid-input CLI executions, and four existing-destination checks behaved as required. The original buggy target remains a negative control and still fails the three distinguishing supplied cases.

The additional overflow witness exposed a pre-delivery error after an overflowing accumulator was followed by missing input. The final implementation maps an overflow to ordinary missing and preserves missing when both SUM operands are missing; a subsequent finite operand restarts the sum. This behavior is a documentation-derived inference from the sum statement's equivalence to retained `SUM`, tested against explicit hand expectations and pending live SAS execution. See history for the failed assertion and repair.

## References and limitations

Primary SAS documentation consulted:

- [LAG function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm): each occurrence owns a queue advanced when executed.
- [BY-group identification](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm): FIRST and LAST changes propagate to following BY variables.
- [Sum statement](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1dfiqj146yi2cn1maeju9wo7ijs.htm): retention, initialization, missing-expression behavior, and SUM equivalence.
- [SUM function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0zxive1z1ctqin12w06c85jfigd.htm): nonmissing operands and all-missing results.
- [Generated missing values](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000989183.htm): overflow yields missing. The search result was available; a direct fetch timed out. This is a narrower retrieval basis than the other successfully opened references.

No SAS runtime or SAS-produced expected output was available. No general translator, conditional LAG, special missing tags, SAS logging, metadata, formats, macros, or includes were tested. Numeric operations use ordinary binary64 values; arbitrary-precision mathematical integers are not a cross-language numeric representation claim. The tested numeric precision and overflow cases do not establish every SAS platform's numeric edge behavior. A differing captured SAS result would require a new comparison and a separately recorded repair attempt. No later edits to this first delivered code are implied.
