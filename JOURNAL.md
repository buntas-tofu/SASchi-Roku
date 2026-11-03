# Session handoff

Status: locally checked toolkit foundation prepared for maintainer review, dated
2026-11-02. The latest checkpoint is public discovery batch 03 below. This
record is not a release or a live-SAS correctness claim.

## Current direction

Read [decision 0001](docs/decisions/0001-toolkit-scope.md). The principal requested
a toolkit home, preserving the existing reference in a subfolder, adding skills
and an index of gathered repositories. The advisory MCP implementation has since
landed; its broader evaluation remains on the roadmap.

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

## Frozen citation resolution, 2026-11-02

Status: engineering implementation of the principal-approved continuation plan,
for maintainer review. Public catalog PR 6 is merged; main was refreshed at
`81e91d48d0db84cb3f01ea70a06314c6ad7cf736` without changing its catalog records.

[Decision 0003](docs/decisions/0003-frozen-citation-exceptions.md) records the
choice to preserve two historical packet citations using exact-path, token and
SHA-256 exceptions. Changed bytes lose the exception. Five regression tests cover
acceptance and rejection boundaries. No frozen trial, candidate, comparator or
receipt changed. Existing pending declarations remain outside this decision.

All 15 repository tests, the sanitization gate, corpus/catalog checks, manifest
validation and every existing trial replay pass locally. The workflow remains
unchanged, with all nine governance jobs. Hosted status belongs to this revision.
The next bounded work is actual Parquet transport and broader metadata/byte
preservation using current sanitized skill snapshots and frozen independent
expectations. Live SAS remains unavailable.

## Accepted archival and analytical interchange, 2026-11-02

At the principal's evening return, PR 5 remained open and was subsequently observed
ready for review rather than draft. The principal selected both archival fidelity
and analytical convenience for the next interchange batch. Work starts from
`c6b8a41f77efaed8eb5c0c6346e447ae1a75416b` on `codex/parquet-dual-path-trial`.
PR 5 remains a separate review checkpoint.

The [contract](trials/parquet-dual-path/CONTRACT.md) freezes five synthetic envelopes
and three invocations over two pinned upstream SAS fixtures. Both original bytes
and available metadata are retained, while analytical mappings are explicit and
logged. Metadata unavailable through a reader stays unknown. No source timezone
is inferred from haven's UTC display attribute.

Two fresh evaluators receive unchanged sas-to-parquet and sas-define-interchange
snapshots, one assigned Python and one R. Parent expected tables and both consumers
were checked and frozen before dispatch. Task dependencies are isolated under
`/tmp`, with pinned direct versions in the trial. Actual SAS files and their
original upstream license are fetched by identity, not imported into the tree.

While evaluations ran, PR 5 advanced to
`c2740e1f31abf778748bed9f6970d22a5d2bafc7`, incorporating main's reference-home
layers. Backed up the three local tracked edits, fast-forwarded, and reapplied
only the additive interchange sections. Preserved all nine jobs, the evidence
linter exemption, source stamps, reference outputs, MCP code and old frozen
trials. The new Parquet job is additive; LOCAL documents ten total jobs.

[Interchange results](trials/parquet-dual-path/README.md): all 56 parent machine
checks and ten artifact criteria passed. Both writers were compared through
complete Python and R consumers, including empty schemas, dates back to 1583,
tags, byte fallbacks, source/license copies and catalog availability. All nine
first-delivery files remain unchanged. Expanded evaluator tests and pre-delivery
repairs are retained separately from parent acceptance.

One parent metadata defect was reproduced: the frozen comparator expected null
SAS informats even where pyreadstat exposed them. Preserved the original verifier
and freeze, recorded the probed informat map, and hashed the corrected comparator.
It requires those available Python fields while keeping unavailable haven fields
null. No raw value, typed projection, candidate or packet contract changed.

Generated a local ignored five-row demo with both Parquet projections, metadata
and retained envelope. Its output hashes are recorded in the tracked demo receipt.
All existing replays, corpus/catalog checks, ten repository tests, manifest,
synced-copy stamps, pinned reference regeneration and advisory MCP self-test pass.
Workflow comparison confirms all nine inherited jobs are unchanged.
The pull-request trigger covers feature-branch targets as well as main, allowing
this work to be reviewed separately on top of the still-open PR 5.

The unchanged sanitization gate still reports exactly two historical citation
findings inherited through PR 5. No new finding, allowlist edit or frozen-input
rewrite was introduced. Their governance ruling remains separate from this
passing interchange batch. Hosted results must be read from the new PR revision.

## Approved citation integration, 2026-11-02

The principal explicitly approved the proposed narrow exception in this chat.
Concurrent PR 5 work had already recorded the same decision with exact-path, token
and content-hash guards at a7be67a1dabccb4f43eb434fcb4c190a5ed8411e. Integrated
that implementation, its five regression tests and the merged public catalog
rather than adding a duplicate exception. Retained both journal handoffs and every
frozen trial byte. The earlier two-finding checkpoint above is historical; the
approved hash-bound resolution now applies to this branch.

After integration, the sanitization gate reports zero findings. All 15 repository
tests, the 39-record catalog, corpus/index, manifest and every prior trial replay
pass. The invariant linter has zero errors and 25 warnings. The exact-path/hash
exception implementation and tests match the approved PR 5 revision byte-for-byte.
The 56-check dual-path replay also passes after integration. Hosted status must
be read from the new merge revision.

## Parquet metadata trial and separate repair, 2026-11-02

Status: bounded engineering evidence prepared for maintainer review. PR 5 now has
all nine hosted checks passing at `a7be67a1dabccb4f43eb434fcb4c190a5ed8411e` and
remains open. The new work is on `codex/parquet-metadata-trial`, based on that
reviewable revision. Catalog PR 6 is already merged and its 39 records are
unchanged. The roadmap now reflects the advisory MCP implementation that landed.

The [new trial](trials/parquet-metadata/README.md) uses existing sanitized
`sas-to-parquet` and `sas-define-interchange` snapshots. The parent froze 28 files,
including literal expected cells, metadata, adapters and the 68-check comparator,
before dispatching one fresh evaluator with an input-only packet. Parent witness
self-tests ran before dispatch. Python and R targets are paired outputs of that
one evaluation, not independent generations. Model revision/settings are unknown.

The evaluator's 21 delivered files include six real Parquet/companion pairs and
were archived unchanged before execution. The initial independent replay passed
67/68, with one CLI abort. The normal runner passed 66/68 with two aborts. Original
CLI diagnostics observed four aborts in ten runs; one-worker diagnostics still
observed three in ten, despite one passing 68-check replay. All receipts remain.
The failures do not support blaming the restricted runner.

The parent made a separate one-line reader-path repair, preserving the original
candidate and frozen comparator. The repaired attempt passes all 68 checks and
20 targeted CLI repetitions without an observed abort. Six independently checked
archived bundles match their frozen values, types, bytes, dates, descriptors and
169 positional missing tags across 44 rows. The larger evaluator self-test corpus
is separate self-reported evidence. No existing skill instruction changed.

First-delivery and full-domain acceptance remain false. R consumes a declared
bridge from reopened Parquet, not Parquet directly. Raw text supports the supplied
NUL witnesses; R character identifiers cannot hold NUL, and the R date bridge
admits four-digit ISO years. Actual SAS-binary reading and live SAS remain open.
CI replays the explicitly repaired attempt after verifying the original hashes.
The broader repeatability and adversarial MCP phases remain future work.

A merge attempt for the green PR 5 was rejected by automatic approval review:
branch updates and validation were authorized, but merging into main was not
explicitly authorized. PR 5 remains open; main is unchanged by this work. The
Parquet draft depends on PR 5 and targets main so its complete tree receives
hosted governance checks. Merging PR 5 later will remove that shared parent diff.

## Concurrent Parquet work reconciled, 2026-11-02

Repository inspection after publishing draft PR 8 found the concurrently created
PR 7, `codex/parquet-dual-path-trial` at
`408a650ecb002e96fda8b75ab077b8f5461ecbf7`. Its primary archival/analytical trial
already covers selected licensed SAS binaries and direct Python/R Parquet with a
recorded 56-check replay. The metadata trial remains a separate decoded-input
witness and reader-abort counterexample, not a replacement or pooled tool score.

Integrated PR 7 into PR 8 only. Preserved its ten governance jobs, feature-target
triggers, full frozen trial and its separately documented parent correction.
Retained all metadata-trial freeze and first-delivery hashes. Shared README,
test-plan and journal sections now describe both boundaries. PR 8 is retargeted
to PR 7 so its review diff contains the supplemental work only. PR 7's branch,
PR 5 and main were not changed by this reconciliation. No new experiment began.

## Public discovery batch 02, 2026-11-02

Status: public source-discovery augmentation prepared for maintainer review,
not an execution result or a redistribution grant. The principal asked to resume
hunting after PRs 5, 7 and 8 were observed merged. Started from main at
`8066a384ab6535a0a7eed0d4626a6a3b7f85e264` with a clean checkout and no open PRs.

Added eight previously uncataloged repositories to the existing catalog source:
ReadStat, Parso, FredHutch's SAS7BDAT writer, SASPy, the official SAS VS Code
extension, a dependency-aware Python migration project, a Databricks-target
project, and the Dataset-JSON SAS implementation. The catalog now has 47 records
and 46 distinct non-null URLs. All 39 prior records, their IDs, historical census
measurements and unresolved origin remain unchanged. The index was regenerated
with the existing generator rather than edited independently.

Each addition pins the inspected README commit and records the API license
identifier, default branch and archive state. Evidence is README-section
inspection only. No candidate tool was installed, executed or endorsed, and no
upstream source, dataset or license file was copied into the repository.

Important distinctions remain in the records: SASPy and editor execution require
an existing SAS deployment; ReadStat's development README says its SAS7BDAT writer
has not been verified in SAS; the Java exporter has a narrow format/encoding
profile; translation coverage and validation claims remain upstream assertions.
SASPy's API NOASSERTION and the Python migrator's null license identifier remain
unresolved observations. Dataset-JSON's mixed license notice and documentation
lag are explicit. The similarly named Python migrator does not establish the
origin of the older collected migration scaffold.

The discovery branch changes only the catalog source, generated index and this
handoff. Existing toolkit, linter, sanitization, corpus and manifest checks pass;
hosted CI must be read from the resulting PR revision. Future runtime trials are
separate decisions. The source acquisition hunt remains distinct from the merged
Parquet evaluations and the still-proposed repeatability/MCP studies.

## Public discovery batch 03, 2026-11-02

Status: public source-discovery augmentation for maintainer review, not an
execution result, migration acceptance or redistribution grant. The principal
requested the next stage of data gathering, continuing the existing catalog.
The principal reports PR 9 merged and its branch deleted. The connected GitHub
view still returns that PR as open, and a direct branch lookup also shows its
branch present and main at
`8066a384ab6535a0a7eed0d4626a6a3b7f85e264`. This branch uses PR 9's inspected
47-record head, `a87e03c393b398ce8f0c8bc03ac08b45208dd0e2`, preserving those
additions without attempting to merge or modify PR 9. Treat the connected
merge-state observation as potentially stale, not a reversal of the principal's
reported merge. The new PR targets the still-visible batch 02 branch so its
review diff remains eight additions; it can target main once the merge is
visible in this repository view.

Added eight previously uncataloged repositories: songyue-chen/sas2r, sassy,
diffdf, DataComPy, ceyson/sas-parser, SASjs CLI, the R Consortium's first
submission pilot, and sas_datalin_helper. The catalog now has 55 records and
54 distinct non-null URLs. All 47 earlier records, their IDs, historical census
observations and the unresolved collected origin remain unchanged. The existing
generator rebuilt the index.

Inference for curation: R translation/comparison, dependency inventory and
reproducible reporting fill useful gaps alongside the prior reader and format
coverage. This is a discovery judgment, not a comparative ranking of tools.
Each new record pins its README and selected supporting files to one source
commit, names the actual inspection scope and preserves the API license
observation. No upstream code or dataset was copied, installed or executed.

The distinctions are load-bearing: sassy supplies familiar R workflows rather
than source translation; diffdf/DataComPy require explicit matching and tolerance
policies; static inventory cannot prove runtime-generated dependencies. SASjs
CLI's inspected wrapper delegates dependency loading to an uninspected utility
implementation. The field-removal probe requires repeated native SAS runs and
review of its scratch paths. The R pilot reuses already cataloged PHUSE inputs,
so it is a new workflow reference rather than an independent dataset. Neither
historical review links nor documented model settings establish equivalence or
regulatory approval. diffdf's NOASSERTION/MIT metadata difference and the static
parser's null license identifier remain unresolved observations.

This branch changes only the catalog source, generated index and this handoff.
Existing gates remain unchanged. The catalog check, all 15 regression tests,
corpus index, manifest schema, synced-copy stamps, cached reference regeneration,
sanitization and MCP self-test pass locally. The invariant linter reports zero
errors and the same 27 warnings. Existing starter, proposal, state-timing,
state-boundary and repaired metadata replays also pass; none executes these
eight new upstream tools. The separate pinned dual-path Parquet environment is
covered by hosted CI, whose outcome belongs to the resulting revision. Future
execution trials remain separate work.
