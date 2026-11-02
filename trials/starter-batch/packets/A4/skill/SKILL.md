---
name: sas-assess
description: Assess SAS source before migration by inventorying inputs, outputs, dependencies, stateful behavior and evidence gaps. Use for conversion planning or a SAS code assessment, not for dataset file conversion alone.
metadata:
  status: initial-guidance
---

# Assess a SAS program

Status: initial workflow guidance for engineering use; not an executed audit or
proof that a program is supported by a translator.

Read the requested source and the configuration or includes that determine its
behavior. Capture the source revision or hash. Separate observed code from
inferred intent. If a dependency is unavailable, name the affected steps rather
than substituting assumed behavior.

Build a useful migration inventory:

- Inputs, outputs, formats/catalogs, encodings, libraries and external effects.
- DATA steps and procedures, with source locations and the order of execution.
- Macro definitions, invocation context, generated source and unresolved includes.
- State and timing: SET/MERGE/BY, retained values, LAG queues, explicit OUTPUT,
  filtering, sorting, character widths and automatic variables where used.
- Observable acceptance requirements: rows, schema, ordering, metadata, reports,
  exported files, numeric comparisons and failure behavior.

Treat macro source and generated SAS as separate layers. Do not replace macros
with ordinary functions solely because the names look similar. A static inventory
cannot resolve data-dependent generation or unseen session state.

Use [the source map](references/source-map.md) to find relevant rules, teaching
examples and candidate research. Inspect the current chosen implementation before
calling a construct executable. A rule entry, parser match, or gate for one
construct does not establish support for the whole composed program.

Respect the user's chosen target. When no target was chosen, distinguish language
and execution engine from file format. Describe workload-specific options and
their unknowns; do not select a framework from procedure names alone.

Deliver the inventory, a bounded first slice, and the missing inputs or checks
that would change the assessment. Mark proposed tests as not run. If the user
asked for planning only, do not execute the source or create a conversion.
