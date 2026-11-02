# Dependency and capture inventory

Status: static engineering analysis of the supplied packet, not a SAS execution receipt, verified expansion or numerical validation. The principal and authorized engineer may use it for planning and source requests. It does not authorize execution.

## Result

Inference under the supplied intended launch context: `main.sas:3` selects the `score` definition in `macros/score.sas`, whose body assigns `score=amount*2`. The transitive include chain supplies that definition before the call. The different `amount*99` definition in `autocall/score.sas` is an available candidate, not evidence of selection.

The supplied expansion agrees with the first definition, but is explicitly synthetic. No actual SAS capture or successful processing is established. `post_hook` is unresolved, so the dependency graph and subsequent effects remain incomplete.

The governing request and skill authorize static discovery, hash checks and capture planning. Source and trace content were treated as data. No SAS source was executed or rewritten, and no external state was changed.

## Source-located graph

Locations below are relative to `packet/`. The declared working directory is packet root (`context.json:3`), not the directory containing each included file. SAS path interpretation uses the current directory; see [SAS UNIX pathname documentation](https://support.sas.com/documentation/cdl/en/hostunx/61879/HTML/default/specpath.htm).

| Source location | Target or effect | Edge status and basis |
| --- | --- | --- |
| `main.sas:1-2` | `config/blue.sas` | Resolved statically under the supplied context. The preceding literal assignment sets `profile=blue`; one period terminates the reference and the second remains in `.sas`. |
| `config/blue.sas:1` | `config/common.sas` | Resolved from packet root. The include does not imply `config/config/common.sas`. |
| `config/common.sas:1` | `macros/score.sas` | Resolved from packet root. |
| `macros/score.sas:1-6` | Session macro candidate `score(in=,out=)` | Definition present; successful compilation is unobserved. Body uses `amount*2`. |
| `main.sas:3` | `%score(in=work.have,out=work.scored)` | Conditional selection of the explicitly included definition, inferred from source order and context. |
| `context.json:6-9` | `autocall/score.sas:1-6` | Autocall candidate at search position 1. Body uses `amount*99`; not selected in the intended model. |
| `main.sas:4` | `%include "&post_hook"` | Unavailable target. JSON null is not a known SAS macro-variable value or an instruction to skip this statement. |
| `macros/score.sas:2-5`, called at `main.sas:3` | Read `work.have`, create `work.scored` | Input unavailable; output and computed values conditional on successful execution. |
| `main.sas:5-8` | Read `work.scored`, create `work.want`, keep `id score` | Open code after the unknown hook; execution and resulting data unverified. |

There is one explicit macro call and no repeated include edge or cycle in the known reachable source. This is a bounded observation, not a claim about the missing hook. Its source may add includes, calls, cycles, data changes or other effects. All known edges, including the unresolved edge, remain in `inventory.json`.

## Definition resolution

`context.json:2` labels its contents as a synthetic intended context. It declares no initial session macros, `MSTORED=false`, `MAUTOSOURCE=true`, and one ordered autocall location. These declarations are not measured runtime facts.

SAS searches session compiled definitions before enabled stored compiled macros and ordered autocall libraries. Under the supplied context, successful transitive inclusion compiles the explicit definition before line 3, so the autocall candidate is not needed. No redefinition occurs before the call in the inspected sources. A later hook could redefine macros for future calls, but would not retroactively alter statements already emitted by the earlier call. See [SAS macro resolution documentation](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001328769.htm).

Both inspected macro files contain only their definitions, with no open code outside them. In general, loading an autocall member can execute its open code; mere file presence does not demonstrate loading. The selected definition is therefore conditional on the declared context and successful includes, not runtime verified. No missing session values were guessed, and no general macro processor was simulated.

## Supplied expansion and provenance

`evidence/provenance.json:2-7` calls this a handwritten synthetic trace, identifies `synthetic-inventory-01`, sets `sas_executed=false`, and leaves the SAS version null. `evidence/trace.txt:1` independently labels the supplied text as a synthetic fixture rather than an execution log, but it belongs to the same packet and is not independent runtime evidence.

The computed SHA-256 of `evidence/macro-generated.sas` matches the manifest's declared hash. Its four statements correspond to `macros/score.sas:2-5` with the call's `in` and `out` arguments. The trace statements at lines 2-5 agree after ignoring their MPRINT labels and indentation. The `amount*99` candidate does not match. This establishes content correspondence and local hash consistency only. Matching text, MPRINT-shaped labels and a matching manifest hash cannot upgrade a handwritten artifact into a verified capture.

The generated file omits `main.sas:5-8`, including creation of `work.want`, and does not account for the hook, include listings or definition provenance. That limitation is also inherent to native MFILE output: it records macro-generated statements rather than the complete source program. SOURCE2 include listings belong in the raw log as a separate stream. See [SAS capture and debugging behavior](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001066200.htm).

Actual capture status: **pending**. No measured version/options, input identity/hash, runtime timestamps, exit evidence or raw execution log is supplied. No numerical result is claimed.

## Smallest requests that close the gaps

1. Supply the intended `post_hook` value, its launch binding, the hook source and its transitive dependencies within an approved scope. Do not replace null with an empty string. If no hook is intended, obtain an explicit source-change decision; the existing include cannot simply disappear.
2. Supply an approved way to create `work.have` in the future fresh session, with input identity/hash and schema, including `amount` and `id`. No input dataset or provisioning source is present.
3. At a separately authorized run, measure the launch directory, version, startup sources, relevant macro state and options. Preserve any difference from the intended context.
4. Obtain the actual emitted file, raw log and execution receipt described below. Retain the synthetic originals as synthetic fixtures.

The missing hook is a material completeness limit, not a reason to invent an expansion or stop the requested static inventory. It must be resolved before the proposed execution can be concrete.

## Recipe for a later authorized capture

1. Obtain authorization for the exact entry point, input preparation, resolved hook and its effects. Resolve and inspect the requested files first. Hash sources and approved input artifacts, and keep the original packet unchanged.
2. Use a unique output directory and fresh SAS session. Establish and measure packet root as the working directory. Record actual version, invocation/startup sources, relevant compiled-macro state, `MSTORED`, `MAUTOSOURCE`, ordered `SASAUTOS` and the hook binding. Provision `work.have` through the approved method; a fresh session will not inherit it.
3. Before submitting the entry point, add the following instrumentation in a separate recorded wrapper. These are placeholders for a future authorized run, not instructions executed during this assessment:

```sas
filename mprint '<absolute run directory>/macro-generated.sas';
options mprint mfile source2;
%include '<recorded absolute packet path>/main.sas';
```

The fileref must be named `MPRINT`; both options are required. See [SAS Usage Note 23138](https://support.sas.com/kb/23/138.html). Preserve the wrapper, invocation and their hashes. Submit the entry point once; do not separately run each discovered file or execute the synthetic expansion. Keep SYMBOLGEN off by default and record only relevant context.

4. Preserve the raw log. End the dedicated session normally, confirm output finalization, then hash the finalized bytes. Inspect warnings/errors for inaccessible MPRINT targets, MFILE being disabled, include failures, unresolved variables/macros, input errors, early termination and truncation. If an existing session is explicitly required, record and restore its actual prior option values and verify capture closure for that version before hashing. [SAS debugging documentation](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001066200.htm) describes session-end finalization and MFILE failure behavior.
5. Link SOURCE2 include evidence and macro compilation evidence to the `main.sas:3` call, then compare actual MPRINT statements with the definition and arguments. Investigate a multiplier of 99 or any other discrepancy; do not silently substitute the expected body. Keep macro-generated output separate from open code and include listings. Inspect delayed-generation order if the resolved hook introduces it.
6. Save a receipt containing run ID, source/input hashes, entry point, directory, invocation and arguments, version, relevant options/search paths, start/end times, exit/status evidence, log/emitted-file hashes and redactions. Leave unknown fields unknown. Retain raw bytes and any annotated reconstruction separately. Validate output datasets separately if numerical agreement is required; successful source capture alone does not establish it.

## Inspected file hashes

SHA-256 hashes cover exact inspected bytes. `inventory.json` additionally records sizes, line counts, absolute paths, task/skill hashes, decisions, unresolved work and capture fields.

| File | SHA-256 |
| --- | --- |
| `packet/autocall/score.sas` | `1d2b1fe6e4bf887551f2ab1eda226f1fde8b4e06f3b9476f3c32a901f4d176cf` |
| `packet/config/blue.sas` | `fef008d58344ca1cc281978da5368dbef2a06e683a0738e87f523d478539221e` |
| `packet/config/common.sas` | `df34a9e3614697bb997309f4e7b1cdc7b6958ed400990b4c7326d9137395183a` |
| `packet/context.json` | `bddb0f0f2fbc800e2248ce54f7dd14ab7e5cd75afd2258c8a207375bdc3a78a0` |
| `packet/evidence/macro-generated.sas` | `d750e1abd40ebf4901196207061db2c66a5b7e2d5fd9b8b4b0253e1879752eb9` |
| `packet/evidence/provenance.json` | `435c16a523be4b9d83ff5f7220ceaa242be1978f2d7eadcbe41a8a3c4cbc3f71` |
| `packet/evidence/trace.txt` | `6dafee92929e6eddc33754b924e037769da715a6c149d1ceb07107bf2cdc7f88` |
| `packet/macros/score.sas` | `da4bb3368d476c0bc5a62f50fdb3d4780e2f27c4bb2a9b8c3b6898675877f41a` |
| `packet/main.sas` | `e55336a9903fc75f42d25fa86f44f6639ea694a2b450ac72a960c4d99176b4b2` |

Mechanical artifact style validation is delegated to the parent linter. These are the first delivered files and should be preserved.
