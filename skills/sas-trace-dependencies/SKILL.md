---
name: sas-trace-dependencies
description: Trace SAS includes, macro resolution and generated-source provenance before migration or when an expansion differs from expectations. Use for dependency discovery and capture analysis, not as a general macro evaluator.
metadata:
  status: initial-guidance
---

# Trace dependencies and expansion evidence

Status: initial guidance for engineering use. Static discovery, a supplied trace
and a verified SAS execution are different evidence levels.

Start from the entry point, launch directory, session settings and permitted
source roots. Hash the inspected files. Build a source-located graph of includes,
macro definitions, calls and generated artifacts. Record each edge as resolved,
conditional, ambiguous or unavailable. Follow transitive includes only within the
provided scope; retain cycles and repeated calls rather than hiding them.

Resolve a path using its actual invocation context. A relative include does not
become relative to the including file merely because it is adjacent on disk.
Macro variables, filerefs, autocall search paths and generated paths may require
runtime evidence. Do not guess missing variable values or simulate a general
macro processor with string replacement.

Distinguish candidate definitions from the definition used at a call. Session
compiled macros, stored compiled macros and ordered autocall locations can differ.
An autocall source file may contain open code as well as definitions. A file's
presence alone does not prove that it was selected or executed. Explain how each
resolution is established, including redefinitions and unknown session state.

For expansion work, read [capture evidence](references/capture.md). Associate
source, invocation arguments, runtime/options, input identities, log and emitted
source by run and hash. Keep macro-generated statements separate from open code
and include listings. Match the observed expansion back to its call and source;
flag discrepancies instead of silently replacing source with a convenient trace.
A synthetic trace or handwritten expansion remains synthetic even if it parses.

Deliver the graph, resolution decisions with locations, unresolved effects, and
the smallest capture or source request that closes each material gap. Planning
or trace inspection alone does not authorize running the program. For authorized
execution, retain the actual emitted bytes and execution receipt; missing SAS
access means capture is pending, not that an inferred expansion is verified.
