# SL-019: Equal seeds do not establish equal random streams across languages

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P2, an engineering judgment, not an observed frequency.
Related rulebook entries: ST-016, SV-006; stochastic tolerance tier.
Coverage assessment: Existing stochastic policy; per-generator validation required. An entry's existence is not an equivalence proof.

## Failure mechanism

The cited SAS RAND implementation and NumPy's RNG interfaces have distinct stream contracts. A seed alone does not specify initialization, generator, distribution transform, call order, or parallel stream allocation.

## Witness to build (not executed here)

Generate normals and uniforms from equal integer seeds in the chosen runtimes. Treat unequal draws as expected unless an exact shared algorithm contract has been implemented.

## Preservation contract and mitigation (recommendation)

For stochastic equivalence, predeclare distributional diagnostics and tolerances. For exact replay, capture or specify the complete stream and transformation contract. Do not tune tests until unrelated streams happen to match.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S20: [RAND function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p0fpeei0opypg8n1b06qe4r040lv.htm). Scope: SAS 9.3; not a claim about every later RNG implementation. Consulted 2026-09-15.
- T02: [NumPy RNG compatibility](https://numpy.org/doc/stable/reference/random/compatibility.html). Scope: NumPy 2.5 manual as served; stable URL is mutable. Consulted 2026-09-15.
