# Parquet and metadata trial contract

Status: bounded engineering trial authorized by the principal's 2026-11-02
continuation instruction. Exact fixtures and interfaces are engineering choices
within the accepted plan. This is not a live-SAS comparison or a generic reader.

One fresh evaluator receives only `packet/`, the existing sanitized skill
snapshots, the request and a temporary environment with PyArrow 26.0.0. It supplies
paired Python and base R code. These are one evaluation, not two independent
model generations. Isolation is by instructions and directory; no operating-system
security boundary or hidden-task claim is made. Model revision and sampling
settings are unavailable. The original first delivery and history remain intact.

## Scope

Six valid decoded envelopes cover ordinary and tagged missing values (all 28
codes), leading-zero and duplicate identifiers, source padding, UTF-8 and Latin-1,
NUL/control bytes, combining versus composed Unicode, empty and all-missing data,
signed zero, declared date origins, unknown timezone, labels and value mappings.
Seven invalid envelopes cover invalid UTF-8, over-width bytes, malformed tags,
fractional dates, duplicate columns, unknown encoding and boolean numeric input.

The expected ordered schema and literal expected cell bytes, binary64 bits,
dates, metadata properties and tag positions are frozen in `oracle.json` before
dispatch. Numeric/date nulls require one positional companion tag; text is strict
source decoding without trimming or normalization. Unknown metadata remains null.
All intentionally preserved fields are in the packet's explicit contract.

Python writes actual Parquet plus a bound JSON companion, validates them, and
restores source envelopes by reading the written Parquet. The parent imports no
candidate helpers when comparing output. An independent parent adapter reopens
those files and exports an explicit normalized CSV bridge. Base R consumes that
bridge as typed numeric/Date values, exact identifier strings, raw text byte
vectors, positional tags and descriptor/value-label tables. Direct R Parquet
reading and SAS-binary input remain outside this trial. The old R text/NUL gap
is not closed: this consumer deliberately uses raw vectors for text.

## Planned independent acceptance

For each of six valid cases, check CLI conversion, API conversion, refusal of
both existing destinations, restoration, and the base R consumer: 36 checks.
Seven invalid cases must fail under both interfaces before creating an output:
14 checks. Twelve corruptions must fail the independent comparator; six also
must be rejected by the candidate's bundle validator: 18 checks. Total: 68.

The controls cover swapped/stale companions, lost or displaced tags, schema drift,
trimmed identifiers, date-origin error, signed-zero loss, changed labels and Unicode
normalization. Controls that repair the Parquet hash test semantic comparison,
not authentication. A matching unkeyed hash does not authenticate a publisher.

Before dispatch, parent self-tests construct separate witness files from the
literal expectations and demonstrate comparator/bridge agreement, with a
negative signed-zero witness. Expected values and candidate files may not be
edited to manufacture success. Harness defects require a preserved original,
explicit correction and replay. Self-test and parent counts are separate.

Manual review checks four observable criteria: source/representation boundaries,
reproducible executed self-tests, preserved failures/repairs, and an honest
explanation of losses or remaining limits. Skill instructions stay initial
guidance unless a demonstrated failure justifies a narrow change. The broader
repeatability study and adversarial MCP retrieval tests are later phases.
