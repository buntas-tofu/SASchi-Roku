# Session handoff

Status: locally checked toolkit foundation prepared for maintainer review, dated
2026-11-02. The latest checkpoint is the PR 5 conflict resolution below. This
record is not a release or a live-SAS correctness claim.

## Current direction

Read [decision 0001](docs/decisions/0001-toolkit-scope.md). The principal requested
a toolkit home, preserving the existing reference in a subfolder, adding skills
and an index of gathered repositories, with MCP as a longer-term goal.

Sources explicitly identified by the principal: sas-ref, sas-campaign/docs and
sas-training-modules in the professional lane. Inspected commit pins are in
[the catalog](catalog/resources.json). The Campaign macro census supplies the
22-repository seed. The training source has also been consolidated into sas-ref;
both locations belong to one catalog resource. The principal also identified a
broader local reference archive. Its public acquisition inventory matches the
22 census repositories; a SAS lexer pointer was checked against public upstream
and added separately. No archive programs, data or private records were imported.

## Implemented locally

- Preserved the collection under `references/rosetta-code/`, retaining old paths
  as symlinks and retargeting the harvest/index commands.
- Recorded 60 matching preservation comparisons against the source commit.
- Added 33 catalog resources, three initial workflow skills, a roadmap, and
  repository checks. GLOBAL and license files remain unchanged.

## Validation

The corpus-index check and catalog check pass. All 10 regression tests pass,
including check-mode no-write behavior, refresh destination and idempotence,
index/header drift, missing provenance, duplicate records and unresolved origins.
The manifest validates against its unchanged schema. All three skills pass the
skill-creator validator. The invariant linter reports zero errors and three
documented skill-frontmatter status warnings; skill status is in supported
metadata and the body. Its shared implementation is unchanged.

Recomputed all 60 preservation records against both Git source and relocated
files. The GLOBAL block and root LICENSE are byte-identical to the source.
The 22 census repository URLs and five family source commit anchors resolve
through GitHub. None of these lookups executes or endorses the linked code.

The harvester's offline regression test exposed unclosed index readers; the
readers now close through context managers with newline handling preserved.
Hosted CI status belongs to the resulting PR, not this local check record.
No upstream refresh, SAS execution, MCP server or skill installation has occurred.

## First behavioral trial, 2026-11-01

The principal accepted a small real conversion as the next step. Used the
skill-creator independent-evaluation procedure with a fresh agent, the initial
`sas-translate` skill and the unchanged complete sum-and-product corpus source.
The evaluator received no parent history or expected answer. The parent already
knew the source and selected the task deliberately; no randomized or held-out
population claim is made.

The [trial package](trials/sas-translate-sum-array/README.md) preserves the candidate
and its original self-report. Parent execution independently produced `338350 .`
and rejected seven negative controls, including an executed product-inventing
rewrite. The source has no assignment to c, so preservation means missingness.
The oracle uses closed-form arithmetic and documented initialization semantics,
not candidate helpers. CPython 3.12.3 ran; SAS did not. Receipt hashes bind the
source, candidate, oracle and verifier. CI replays the archived code, not the model.

No change to the skill instructions was justified by this single successful
invocation. Their initial-guidance status remains. Draft PR 3 carries the
foundation and this trial; its hosted checks are the external CI record.

## Follow-up boundaries

Resolve the collected migration scaffold's upstream before importing it. Choose
a stateful or metadata-focused task for another behavioral skill trial. Decide the license for future
original software before release. Keep the professional lane independent.


## Starter batch, 2026-11-01

The principal accepted four assessments plus LENGTH and unconditional LAG in
Python and R as the representative starter. The accepted scope and later
proposed phases are in [TEST_PLAN](docs/TEST_PLAN.md). Eight fresh evaluations
used isolated input-only packets and exact skill snapshots, with no parent
history or expected answers. Raw first deliveries remain unchanged.

[Starter results](trials/starter-batch/README.md): all four assessments passed
parent artifact review, five criteria each. All four target conversions passed
32 parent checks across CLI and in-memory interfaces; 10 negative controls were
rejected. Native R 4.3.3 and CPython 3.12.3 actually ran. SAS did not. Agent
self-test counts and raw repair histories are separate from parent results.

The broad ASCII wording left an unresolved NUL boundary for R's character
interface. The original request was not narrowed after generation. Frozen
witnesses pass; full-domain signoff remains false. A custom R CSV parser also
exposed the need to separate semantic and transport testing. A self-test oracle
naming failure was retained by the R evaluator; the parent oracle did not change.

Candidate directions are dependency/macro inventory, character and metadata
interchange contracts, and stateful failure diagnosis. These are labeled
inferences and coverage-driven proposals, not new skills or established needs
across a population. No skill instruction changes or later-phase runs occurred.
Review this checkpoint before broadening tests. Model revision/settings were
not exposed. Eleven linter warnings are the three existing skill-frontmatter
warnings plus eight identical snapshots, with no linter changes.

## Three accepted follow-on skills, 2026-11-02

The principal approved all three proposed directions. See
[decision 0002](docs/decisions/0002-three-skill-proposals.md). Added separate skills
for dependency and macro capture inventory, character/metadata contracts, and
stateful failure diagnosis. All six skills remain initial guidance.

The [new trial package](trials/skill-proposals/README.md) contains three fresh
evaluations, 53 unmodified first-delivery files, frozen parent truth, manual
review and an independent replay. All seven dependency criteria passed. The
35 machine checks passed under CPython 3.12.3 and native R 4.3.3: 12 interchange
checks and 23 state checks, including 12 rejected corruption controls overall.
The original buggy translation ran and failed as expected. Its first differing
output cell is r8.total; the loss of state begins earlier at silent row r2.

The parent did not edit candidate outputs or change expected values after
generation. One evaluator supplied both state targets, so they are not two
independent model generations. Agent self-test counts remain separate from the
35 parent checks. Dependency analysis keeps the supplied trace synthetic, its
unresolved hook visible and native capture pending. The CSV witness preserves
raw byte fallbacks and missing tags without claiming a SAS-binary reader,
R character import or Parquet round trip. The prior starter's NUL gap remains.

Repository regression checks and previous trial replays pass. Manifest validation
and the six skill validations pass. The linter reports zero errors and 18 status
warnings across six skills and 12 exact snapshots, with its implementation
unchanged. CI adds the new replay after the starter in the same native-R job.
Hosted status must be read from the resulting PR revision.

The principal confirmed no live SAS runtime and separately requested help with
cloud onboarding. That work has not supplied execution evidence. Keep account,
billing and onboarding credentials outside the public repository. The immediate
evidence milestone remains a real SAS run with finalized source capture and raw
log, after resolving the complete input context. No MCP implementation or skill
installation has occurred.

## State-filtering follow-up, 2026-11-02

The principal asked to return to skill work. The agent selected the existing
phase 3 WHERE/subsetting-IF item as a bounded next test, recording that choice in
[its contract](trials/state-filter-timing/CONTRACT.md) before generation. One fresh
evaluator used the unchanged state-diagnosis skill and produced both target
repairs. The parent froze its independent oracle and harness before first delivery.

[Results](trials/state-filter-timing/README.md): all six artifact-review criteria
and 31 independent replay checks passed under CPython 3.12.3 and native R 4.3.3.
The original bug reproduced `if_path` row 2, r8.prev as 5 instead of 100. Both
paths emit the same row identifiers, so values and state timing distinguish them.
Six deliberately wrong outputs were rejected. Calls preserve inputs and fresh
state; existing CLI destinations are refused without changes.

The archive preserves 163 regular first-delivery files unchanged. Two temporary
test symlinks are recorded literally instead of made active, and empty directories
are inventoried. A setup failure from an already existing empty output folder is
retained in the agent history. Its broader self-test corpus remains separate from
the parent checks. No candidate repair or oracle change followed delivery.

The six initial skills remain unchanged. CI adds this replay after the earlier
three-proposal replay. The linter has zero errors and 20 status warnings across
the skills and exact snapshots; its implementation is unchanged. No SAS runtime,
SAS-binary reader, R metadata consumer or Parquet round trip has been verified.

## Reference-home layers landed (2026-11-02, Hermes session)

The principal cleared the re-cut after PR #3 merged. The professional-lane
reference home (its Phases 0-4: consolidation ledger, stamped syncs, the 9.4
reference harvest, the advisory MCP, the workflow skills, the sanitization
gate) was adapted to this repository's shape and landed on
`hermes/reference-home-layers`:

- The corpus stayed exactly where the toolkit put it
  (`references/rosetta-code/`, root compat symlinks untouched); the MCP
  server discovers it there via a location-independent resolution order, so
  one server codebase serves both instances.
- kb/ layers are additive; the catalog, trials, tests, and the six toolkit
  skills are untouched except for the remediation below.
- Remediation, disclosed: the sanitization gate (landing in the same PR)
  found 84 raw hits of the private professional account name in public
  files: ten trial-packet citation links, the decision record, the catalog
  (three entries describing private repositories), and README links. The
  citations in the live files (catalog, decision record, README, the live
  sas-translate reference) were re-voiced to neutral text pins (name, lane,
  private, the 40-hex commit pin kept); the three catalog entries for
  private repositories were removed (the record contract requires a public
  HTTPS URL for repository-kind entries, and the lane ruling forbids the
  account token in public trees); the catalog README was regenerated with
  `check_toolkit.py --write-index`. The FROZEN trial packets were first
  repaired as well, and the starter replay correctly rejected the edit as
  frozen-input drift: they were restored verbatim, because updating their
  hashes would misrepresent what the frozen candidates were generated
  against. Their citation tokens are allowlisted in the sanitization gate
  with the collision declared for the principal's ruling: keep verbatim
  (receipt integrity) or re-freeze with repaired citations and fresh
  evaluations. No trial results, evaluations, or receipts were altered.
- Receipts: both instances' corpora and harvested reference outputs are
  byte-identical; nine CI checks green on the branch; the professional
  instance runs the same server code against its own kb/corpus location.

## Accepted boundary batch, 2026-11-02

The principal merged PR 3 and deleted its remote branch. Local main was verified
at `27025665bb89e0b67c3f5f6fcf0f6113b9c54e10`, with the same tested tree and no
local changes. The principal then accepted the proposed next immediate batch:
group boundaries, merge behavior and character-width propagation.

Work starts on `codex/state-boundaries-trial`. The
[contract](trials/state-boundaries/CONTRACT.md) and literal oracle were frozen
before three independent evaluator dispatches under the skill-creator workflow.
Their packets contain existing skill snapshots, synthetic source and inputs,
and the interface contract. They do not contain parent truth or earlier answers.
Six target implementations are paired outputs of three evaluations. Native SAS,
general metadata interchange and Parquet remain outside this batch.

Completed [boundary results](trials/state-boundaries/README.md): 89 parent machine
checks and 12 artifact criteria passed. All 18 delivered files were preserved
byte-for-byte; the parent changed neither candidates nor frozen truth. The group
bug first differs at main row 3, last_account. Merge acceptance includes actual
read precedence after exhaustion and missing overwrites. Width acceptance covers
both DATA-step tables and the descriptor after reopening CSV, including empty data.

The evaluator's additional overflow failure and pre-delivery repair are retained
as self-reported evidence, not included in parent acceptance. Numeric range and
recovery after overflow are a candidate future vector, labeled as inference.
No new skill or skill edit was justified. Full metadata interchange and Parquet
are the next planned evidence boundary; live-SAS work still awaits onboarding.

All earlier replays, corpus/catalog checks, 10 repository tests and manifest
validation pass. The unchanged linter reports zero errors and 24 status warnings
across six skills and their exact snapshots. CI adds the new replay after existing
ones. Hosted checks must be read from the new PR revision, not inherited from PR 3.


## PR 5 conflict resolution, 2026-11-02

Status: conflict resolution and local validation for maintainer review, not a
merge approval or a live-SAS correctness result. Only
`codex/state-boundaries-trial` is updated; public catalog PR 6 stays unmerged.

Merged main at `33b337dd11e98022afa1161e2ca74a2a7aff31c7` into PR 5 at
`c6b8a41f77efaed8eb5c0c6346e447ae1a75416b`. Resolved the workflow by retaining
all nine main jobs, its documented linter evidence exemption and every existing
step, plus the state-boundaries replay after the earlier starter replays.
Resolved this journal by retaining both the reference-home and boundary-batch
handoffs. No frozen input, candidate, receipt, gate or allowlist was changed.

Local validation: actionlint 1.7.12 passes, and a parsed workflow comparison
confirms main differs only by the intended replay step. The corpus/index check,
30-record catalog check, all 10 regression tests, every trial replay (including
89 state-boundaries checks), manifest schema and instance validation, synced-copy
stamps, pinned reference regeneration and MCP self-test pass. Python 3.12.3 and
native R 4.3.3 ran. The invariant linter reports zero errors and 23 warnings.
The MCP protocol test stalled in the restricted local runner, then passed in the
normal local runner using a temporary isolated dependency environment.

The unchanged sanitization gate fails on two historical citation tokens in the
frozen merge and widths packets under `trials/state-boundaries/packets/`.
Changing the packets would invalidate their freeze; broadening the allowlist
would alter governance. Both remain unchanged for a separate maintainer ruling.
Hosted CI and mergeability must be read from the resulting PR revision.
