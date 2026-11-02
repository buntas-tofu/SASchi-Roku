# Python migration assessment

Status: static planning assessment for the program owner to use in scoping and evidence collection. This is not an execution result, equivalence proof, or translator support certification. No program execution or conversion was performed.

The supplied source establishes a small wrapper, but not its scoring behavior. The next useful step is to recover the include and macro dependency envelope. A faithful migration of the complete program cannot be specified from this packet alone.

## Evidence and source identity

Observed source: `/tmp/roku-starter-20261101/A2/packet/source.sas`, lines 1 through 6. No revision identifier was supplied. SHA-256:

`ae96e42c903b76e442249441cf5d538a5bca2517bf93ef0594dc48ca2f05799e`

The packet contains the request, source, skill, and skill source map. It contains no `settings.sas`, macro definition, datasets, schema descriptions, SAS logs, generated SAS, or reference results. “Missing” below means absent from this packet, not necessarily absent from the production environment.

## Observed sequence and its limits

| Location | Observed source | What remains unresolved |
| --- | --- | --- |
| Line 1 | `%include "settings.sas";` | The file contents, runtime path resolution, nested dependencies, session changes, and any executable work in that file. Its name does not prove that it contains only configuration. |
| Line 2 | `%score(in=work.have, out=work.scored);` | Macro definition, parameter contract, invocation environment, generated source, algorithm, and effects. |
| Lines 3 through 6 | A DATA step names `work.want`, reads `work.scored` with `SET`, and specifies `KEEP id score`. | Whether the input exists, whether both variables exist, their attributes, actual observations, and relevant session options. |

Inference: the macro's argument names suggest that `work.have` is a scoring input and `work.scored` is its output. The source does not establish that the macro actually reads or creates either dataset. It could use other inputs or produce other outputs. No definition of `work.have` is visible.

Observed: there are no visible procedures, macro definitions, calculations, `MERGE`, `BY`, `RETAIN`, `LAG`, explicit `OUTPUT`, filters, sorts, character-width declarations, or references to automatic variables. This observation applies only to the six supplied lines. The include and macro may introduce any of these constructs.

Documented interpretation of the final DATA step: `KEEP` selects output variables, not observations or score values. Without explicit `OUTPUT`, SAS ordinarily writes at the end of each DATA-step iteration. Thus, conditional on valid input and the actual execution context, the visible final step is an output projection, not a scoring calculation. Neither a successful run nor an exact row count was established. See SAS's [KEEP reference](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000202978.htm) and [OUTPUT reference](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/n1lltvbis7ye1an1eryo4leh2mck.htm).

## Missing evidence that changes the plan

1. Recover the exact `settings.sas` used by the job, its transitive includes, and the resolved `%score` definition and dependencies. Establish whether macro resolution depends on included source, an existing session, autocall configuration, or stored compiled material. These are possibilities, not observed mechanisms. Keep macro source and generated SAS as separate evidence; one expansion may cover only one invocation path.
2. Record the launch context: SAS version, working directory and include resolution, startup configuration, relevant options and macro variables, library assignments, and the producer of `work.have`. Capture only what affects the job, without retaining credentials.
3. Obtain representative schemas and permitted sample data for `work.have`, `work.scored`, and `work.want`, plus a successful reference log and outputs if available. Required attributes include types, lengths, column order, formats, labels, encoding, missing-value behavior, and row order. No row count, key uniqueness, score type, score range, or numeric tolerance can currently be asserted.
4. Inventory formats/catalogs, model artifacts, external files, reports, exports, services, and other effects after inspecting the missing code. None is declared in the wrapper beyond the include; their absence from the complete program is unproven.

## Bounded first slice and proposed checks

Recommendation: retain Python as the requested target, but defer engine and library selection until the scoring workload is known. Do not substitute a generic Python function for `%score` based on its name or treat this assessment as evidence that an installed translator supports it. No translator implementation was inspected.

The first bounded implementation candidate is lines 3 through 6, using an independently supplied `work.scored` fixture. That isolates the visible projection and leaves scoring outside the slice. Implementation is future work, not part of this delivery.

Proposed tests, all not run:

- Compare selected values, missing values, row count, duplicates, and observation order against the reference final step. Do not assume unique IDs or introduce sorting or deduplication.
- Check output variable membership, actual column order, types, lengths, labels, formats, and encoding under an agreed Python representation. Do not infer column order from the `KEEP` list alone.
- Cover empty input and representative boundary values after the schema is known. Establish expected diagnostics for absent input or variables.
- For the complete program, compare intermediate and final outputs, additional effects, and failure behavior. Inference: stale session datasets could matter if an upstream operation fails; test the intended behavior once the missing code is available. Choose score comparison tolerances only after the computation is understood.

With no additional files available now, this dependency checklist and the isolated projection boundary are the useful planning deliverables. Recovering `settings.sas` and the actual `%score` source is the highest-value next step.

## Actions performed

Listed the packet, read the request, supplied skill and source map, displayed the source with line numbers, and calculated its SHA-256. Searched for primary SAS documentation and read the KEEP and OUTPUT reference pages cited above. A macro reuse reference page could not be fetched; no conclusion relies on that failed lookup. The source map's repository links were not followed under the evaluation's access boundary.

No SAS source, include, macro, generated program, or Python translation was executed. No conversion, runtime tests, fixtures, or execution receipts were created. No repository implementation, sibling task, or expected answer was inspected. Only this report was written.
