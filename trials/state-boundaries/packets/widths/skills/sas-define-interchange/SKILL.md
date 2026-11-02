---
name: sas-define-interchange
description: Define and test character, missing-value and metadata preservation contracts for SAS data interchange into Python, R, CSV or Parquet. Use when byte domains, decoding, padding, tags or companion metadata determine whether a conversion is acceptable.
metadata:
  status: initial-guidance
---

# Define an interchange contract

Status: initial guidance for engineering use. An agreed mapping is not evidence
that a source reader or destination writer implements it correctly.

Identify the actual data and descriptor, source encoding and byte widths, target
consumer, and required outputs. Distinguish raw source bytes, decoded values,
in-memory representation and transport. Do not infer storage types from names,
formatted displays or a sample of values. Unknown metadata remains unknown.

Read [representation choices](references/representations.md) for character and
metadata boundaries. Define the admitted byte alphabet, decoding errors, NUL and
control-character policy, width/padding, and normalization explicitly. Check the
consumer's representation before promising losslessness. Preserve otherwise
unrepresentable bytes in an agreed binary/escaped representation or reject them;
never silently trim, replace, truncate or drop observations.

Keep identifiers, ordinary nulls, special SAS missing tags and display labels
distinct. A reversible companion needs per-cell positions or stable unique keys,
plus source/output identity. Duplicate business identifiers cannot identify a
unique cell. Record ordering rules and verify the data and companion together.

Define per-column physical/logical type, labels, format/informat, value mappings,
source units/origin, timezone evidence and catalog availability. Retaining raw
SAS day counts can be an explicit choice; converting dates requires a declared
interpretation. Do not fabricate timezones or catalog contents.

Validate semantic values separately from CSV/Parquet transport. Reopen the actual
written bytes and companion, compare exact fields/types/missing positions under
the policy, and test corruption or mismatched companions. Include empty input,
all-missing columns, duplicate identifiers and admitted control bytes when they
matter. Compare full contents or label sampling honestly. Bind a receipt to
reader/writer versions and the files checked.

Deliver the contract, chosen representations, rejected or unresolved cases and
executed evidence. If only a decoded fixture or CSV adapter was tested, name that
boundary; it does not establish SAS-binary reading or Parquet preservation. Keep
source intact and use a new output location for a conversion trial.
