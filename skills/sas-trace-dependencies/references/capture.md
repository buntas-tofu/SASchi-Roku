# Capture evidence for macro analysis

Status: capture procedure and evidence contract. This file is not an execution
receipt or a complete SAS preprocessor implementation.

Use a fresh, authorized SAS session and an output directory specific to one run.
Macro expansion can execute open code, access data and cause external effects.
Resolve required dependencies first. Capture only relevant context, not a dump
of all macro variables or credentials. Do not enable SYMBOLGEN by default.

The native mechanism is a fileref named MPRINT plus the MPRINT and MFILE options:

```sas
filename mprint '/chosen/run/macro-generated.sas';
options mprint mfile source2;
/* Submit the authorized entry point in its recorded launch context. */
```

This is instrumentation, not an execution command to run every discovered file.
Record previous option values if using an existing session; restore those values
rather than assuming their defaults. Finalize the capture and retain the raw log;
check for missing/inaccessible MPRINT files, disabled MFILE, errors and truncation.
Hash finalized bytes, not an output file still being written.

MFILE captures macro-generated SAS statements, not all open code, source comments,
or an exhaustive dependency history. SOURCE2 can expose include listings in the
log; it is a different evidence stream. A trace covers only its observed branch,
inputs and invocation. CALL EXECUTE and other delayed generation require an
execution-order analysis before reconstructing a whole program.

A useful capture record names source/input hashes, entry point, working directory,
macro arguments, SAS version, relevant options/search paths, run identifier,
start/end times, exit/status evidence, raw log and emitted-file hashes, and known
redactions. Missing fields stay unknown. A manifest's assertion of provenance is
not independent proof: inspect its associated artifacts and trust boundary.
Keep the unmodified trace and any annotated/reconstructed view separately.

Primary references:

- [Native MPRINT/MFILE capture](https://support.sas.com/kb/23/138.html).
- [MFILE requirements and failure behavior](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/p0j3zpinabl49ln13q5f5r1t46mg.htm).
- [Macro resolution and autocall open code](https://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/a001328769.htm).

These references describe mechanisms. The current job still needs its own capture.
