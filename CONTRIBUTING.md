# Contributing

This repository is a **passive, provenance-pinned snapshot** of Rosetta Code's
SAS category. The primary workflow is *refresh*, not hand-editing.

## Refresh (recommended)
The corpus is generated from upstream by a reproducible harvest pipeline.
If upstream SAS solutions have changed or grown, re-run the refresh rather than
hand-editing `corpus/`. Keep the provenance headers: each run pins the exact
upstream revision each file was taken from. Refresh = regenerate + commit
`corpus/`, `TASKS.csv`, `TASKS.md`, and bump the snapshot date in `README.md`.

## Adding or fixing a solution (rare, deliberate)
1. Keep it scoped to one task; one PR per task.
2. Preserve the provenance header block. If you are adding **your own** new SAS
   (not re-scraped upstream), write your own header noting it is a new
   contribution rather than a Rosetta mirror.
3. Solutions here are community probes: clearly mark anything not yet executed
   and verified.
4. Follow the existing style: `data step`/`proc` SAS, numbered `/* --- ... --- */`
   banners when a task has multiple examples.
5. Re-run the index: `TASKS.csv`/`TASKS.md` must stay in sync with `corpus/`.

## Questions / licensing
See `LICENSE` and `NOTICE`. When in doubt about GFDL compliance of a reuse,
ask before copying code into other projects.
