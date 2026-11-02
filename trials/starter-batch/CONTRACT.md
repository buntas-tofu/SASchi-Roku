---
title: Starter evaluation contract
status: active
---

# Starter evaluation contract

Status: engineering evaluation contract frozen before generation, 2026-11-01.
Maintainers may use the results to improve the workflow. Eight selected tasks do
not estimate model reliability or establish live-SAS equivalence.

## Method

Four independent assessment tasks use sas-assess. Four independent translations
use sas-translate: LENGTH/Python, LENGTH/R, unconditional LAG/Python and LAG/R.
Each fresh evaluator receives one task, a copy of the applicable skill and its
references, raw synthetic inputs and the neutral request. No parent history,
oracle, reference implementation, sibling code or other candidate is allowed.
Isolation is instructional and directory based, not an OS access-control boundary.
Agents may consult primary SAS and target-language documentation. Record tool use
and any limitation reported by the evaluator. Preserve first delivered artifacts;
agent self-checks before delivery are allowed, but no parent-oracle repair feedback.

The parent freezes an independently hand-derived oracle and this rubric before
generation, then reads actual files and runs the delivered code. All cases are
original, deliberately chosen examples inspired by the scope of training modules
03 and 10 at 4be913210dcf3c1befc3367420c4ac9032bac39d. No training reference code,
expected CSV columns or archive programs/data are copied. No random-sample or
training-set novelty claim is made. Model revision and sampling parameters are
unavailable to the parent; run IDs, timestamps and file hashes are captured.

## Assessment rubric

Evaluate each report manually against the supplied source and scope. Automated
replay verifies archived review/file identity; it does not re-judge prose.

- A1: identify work.have as input and work.want as output; observe ordinary
  derived-column arithmetic; chosen target stays Python; acceptance includes
  row/schema/order/missing-value behavior; source data is absent, so execution
  and full equivalence cannot be claimed. A bounded first slice is proposed.
- A2: name the missing settings.sas include and unresolved %score invocation;
  distinguish known source from unknown macro expansion, generated inputs and
  side effects; ask for include/macro/session dependencies; do not invent them.
- A3: compare to the supplied synthetic engine capability profile; PROC GLM is
  outside that profile; do not equate parsing with translation or substitute
  regression defaults; propose an unsupported ticket or separately validated
  manual slice. Do not claim that R/Python generally cannot implement GLM.
- A4: distinguish source text from a SAS dataset and Parquet from a programming
  language; ask for actual dataset paths/schema/metadata/access and a loss policy;
  identify the source's input/output; do not fabricate a converted dataset or
  claim that translating the program is itself a dataset export.

All four require source identity/locations, observed-versus-inferred distinction,
useful next checks and honest execution status. Scores are per criterion with
supporting artifact locations, not keyword counts. One material unsupported
claim fails the case. A schema or report omission is retained visibly.

## Translation comparison

Scope: decoded ordinary data, finite small numeric values, ordinary numeric
missingness, ASCII text of at most width 10, source row order. LENGTH is the SAS
function; retained character storage has width 10. No Unicode or coercion claim.
LAG and LAG2 each run once per row, with independent queues, and each transform
invocation starts a fresh DATA step. No conditional calls or BY resets.

The interface supplies CSV and an in-memory translate function. Python uses the
standard library; R uses base R. Compare exact logical rows, column order, numeric
values, missing positions and character bytes against oracle.json. Equivalent
numeric CSV spellings are accepted; nonfinite or nonnumeric values are rejected.
Test caller-object preservation and two calls in one process, in addition to CLI
execution on main, edge, singleton and empty data. No output reordering or
trimming is permitted. CLI physical quoting/newlines are not compared.

Parent expected rows are written by hand from rightmost non-space positions and
prior-call histories, before seeing candidate code. The verifier never calls a
candidate to derive its expected answer. Primary definitions:

- https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0f6jve4kdxnh1n1m7c82fhosgih.htm
- https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm

Negative controls cover blank length zero, leading-space trimming, tab trimming,
wrong storage width, reordered rows, missing lag history replaced with zero,
missing inputs skipped in queues and lag direction. They exercise the same
comparator used for real candidates. Separate caller-mutation and state-leak
controls exercise the in-memory contract harness. Failures remain failures.

Saved replay tests archived candidates, not new generations. No SAS runtime is
invoked. No skill effectiveness or causal advantage is inferred from this batch;
that question belongs to phase 5's controlled attempts.
