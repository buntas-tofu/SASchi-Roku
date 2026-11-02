---
title: Three skill proposal evaluation contract
status: frozen
---

# Three skill proposal evaluation contract

Status: parent contract and independent expectations fixed before generation on
2026-11-02. Maintainers may use these bounded results for engineering review.
They are not live-SAS evidence, broad support claims or causal skill evaluation.

## Isolation and evidence

Each of three fresh agents receives one input-only packet, the applicable new
skill, and no parent history, sibling implementation, expected results or prior
answer. Primary public documentation is allowed. Agents may self-test before
first delivery. Scope is directory/instruction isolation, not OS enforcement.
Retain the actual first delivered files, source/skill hashes and tool task names.
Model revision/settings unavailable to the parent remain null.

The parent reviews files and runs its independently written comparator. Frozen
oracle.json is hand truth, derived before generation. Parent comparison failures
remain visible; any subsequent candidate repair is a separate attempt. Compare
logical fields and finite numeric values exactly, allowing equivalent numeric
CSV spelling. Preserve character bytes and row/column order. No tolerance changes.
A saved-code replay is not a new generation or a re-review of prose.

## Dependency inventory rubric

Parent reviews source locations and factual claims, not headings/keyword matches:

1. Resolve main -> config/blue.sas -> config/common.sas -> macros/score.sas using
   the stated packet-root launch directory and the profile macro value.
2. Identify SCORE's included definition and distinguish autocall/score.sas as a
   candidate not selected in this stated fresh-session/include sequence. Mark
   the context as intended synthetic settings rather than an observed session.
3. Keep post_hook and its included file/effects unresolved. Do not claim a full
   dependency closure, final output result or ready-to-run whole program.
4. Match the synthetic expansion's work.have/work.scored and factor 2 to SCORE;
   distinguish emitted macro statements from the later open-code work.want step.
5. Inspect trace provenance and its hash. Explicitly reject promotion to actual
   SAS execution or complete-program generated source.
6. Give a feasible native capture procedure and evidence checklist including
   MPRINT/MFILE, launch/session context, raw log, emitted bytes and limitations.
7. Preserve static-only authority: no source execution, fabricated expansion or
   broad SAS support claim. Deliver report.md and inventory.json.

## Character and metadata interchange

One evaluator defines the contract and implements a Python standard-library
bundle witness. The agreed raw fallback preserves NUL and undecodable bytes with
per-row hex plus text_mode. No source bytes are silently replaced or dropped.
The duplicate business id is not the cell key. Descriptor unknowns remain null.

For main and empty inputs, build and reopen data.csv and metadata.json. Parent
compares all fields against the literal oracle, descriptor equality, source/output
hashes and metadata row association. Invoke candidate check against the source.
Require refusal before creating outputs for unknown encoding, width overflow,
duplicate row_no, and an already existing destination. Preserve caller input.

Corruption controls: changed text, collapsed special tag, wrong raw fallback,
wrong row association, stale source identity and stale output identity. Feed
mutants through the same parent comparator and candidate check; both must reject
for the declared validation contract. Keep data hash internally consistent in
semantic mutants so a hash-only check cannot pass as content validation.

This is decoded-source-to-CSV/companion evidence. No SAS file reader, R data-frame
round trip or Parquet writer is tested. The raw representation is an explicit
alternative for values an ordinary R character column cannot contain.

## Stateful failure diagnosis

The two-step source contains conditional LAG, a nonretained receiving variable,
an initialized retained sum, missing numeric input and explicit OUTPUT. State
updates on non-emitted rows still affect later emitted rows. Compare stage and
want independently. Input order is not sorted. No BY or WHERE scope is claimed.

Execute the supplied buggy.py against main and require a mismatch. Manually
review the first-divergence explanation and repair rationale. Python and native
R candidates each run main, singleton, no-output and empty inputs through CLI
and in-memory APIs. The APIs must preserve caller inputs and start fresh on two
successive invocations. Numeric fields must stay numeric or ordinary missing;
row_id stays character; column order and intermediate/final records are exact.

Negative controls cover an unconditional queue, retained prev on a skipped call,
wrong retained initial value, missing-poisoned accumulation, state discarded on
non-emitted rows and a wrong downstream delta. Exercise the same comparator with
these incorrect outputs. The original buggy execution is an additional real
failure witness. Parent truth uses documented queue, initialization, sum-statement
and output behavior, not candidate helpers. No live SAS ran.

The paired Python/R outputs come from one state-task evaluator, not independent
model generations. Each skill has one exploratory invocation. Further cases,
repeatability, live-SAS comparison and with/without-skill controls remain open.
