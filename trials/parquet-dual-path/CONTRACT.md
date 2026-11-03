# Archival and analytical Parquet trial

Status: principal-approved dual-path direction, 2026-11-02. The exact eight cases,
interfaces and controls are implementation choices within that direction.
Maintainers may act on the recorded engineering evidence within its scope.

Start revision: `c6b8a41f77efaed8eb5c0c6346e447ae1a75416b`, PR 5, which remains
separately reviewable. The new branch is `codex/parquet-dual-path-trial`. Two fresh
evaluators receive the same input-only packet, one assigned Python and one R.
They do not receive parent expected tables, prior answers or one another's work.
The existing sas-to-parquet and sas-define-interchange instructions are snapshotted
unchanged. Isolation is by directory and instructions, not an OS security boundary.
Model revision and sampling settings are unavailable.

## Accepted meaning of both paths

The archive retains original source bytes and available descriptors, plus a typed
Parquet projection with reversible text bytes and per-cell missing tags. Reader
normalization stays explicit. The analytical table applies declared date/time,
text and null mappings and records affected cells. Its retained archive is the
route back to original representations. The precise contract given to evaluators
is [packet/CONTRACT.md](packet/CONTRACT.md).

Five original envelopes cover main data, zero rows, all missing, reordered duplicate
identifiers and UTF-8. They exercise CP1252, Unicode, invalid bytes, NUL, exact
widths, leading zeros, literal NA, quotes and CR/LF. Two pinned SAS files supply
eight total case invocations: the basic file once, and the special-missing file
with and without its catalog. Their original binary bytes are fetched into the
task environment, verified by SHA-256 and retained with the upstream license.
No upstream binary or private estate material is copied into this repository.

The fixture source is Roche/pyreadstat at
`e6e23bc0021875f35fccc3c2707c3e5151c130bb`. Its root license distributes the
package as a whole under Apache-2.0 and retains the bundled ReadStat MIT notice.
The original license accompanies the downloaded fixture set and every copied
fixture capsule. Source URLs and hashes are in [upstream.json](upstream.json).
This is a source-based reuse assessment, not a legal finding or a new license
for the project's original software.

## Fixed evidence method

Freeze the packet, source identities, parent oracle and both parent consumers
before dispatch. The oracle is independently derived from envelope bytes, explicit
upstream CSV date/time spellings and the upstream SAS missing-value source. It
is not candidate output or agreement between readers. Metadata observations are
identified separately where a reader supplies the only exposed descriptor.

Run eight cases through each writer. Each of 16 conversion checks reopens both
Parquet tables through independent parent Python and R readers, checks metadata
and retained bytes, then tests refusal of an existing destination. There are
32 consumer comparisons within those 16 named checks. Run 16 complete candidate
validations, 16 corruption/refusal checks and eight invalid-envelope refusals,
for 56 planned parent machine checks. Corruption controls include updated hashes
on incorrect values, missing tags, row order and date mappings. Never weaken
expected values or modify first-delivery code to obtain acceptance.

Five artifact-review criteria per writer, ten total: preservation boundaries;
descriptor and missing/byte policy; typed date/time and transformation treatment;
source/output association and licensing; and reproducible execution with failure
history and remaining limits. Expanded evaluator self-tests remain separate from
the parent's eight fixed cases. Preserve the entire first delivery unchanged.

Python and R readers both use ReadStat internally. Their agreement does not prove
independent source semantics. No live SAS run, general SAS-binary fidelity,
catalog coverage beyond this one fixture, streaming scalability or installed
MCP service is established by this trial.

## Environment

The task uses an isolated temporary environment with Python 3.12.16, PyArrow
25.0.1, pyreadstat 1.3.7, pandas 3.1.0, R 4.4.3, arrow 25.0.1, haven 2.5.5 and
jsonlite 2.0.0. [environment.yml](environment.yml) pins these direct dependencies.
Existing repository checks continue in their existing runtimes. No global
package environment was altered.

Setup history: a micromamba-run version probe initially tried its default cache
outside the writable workspace and failed before execution. Direct task-runtime
executables supplied the successful probes. A first fixture fetch without network
access failed before writing a file; the already downloaded, pinned bytes were
copied to the fixture cache and the fetcher's identity checks passed offline.
These setup failures did not involve a candidate or change an expected value.
