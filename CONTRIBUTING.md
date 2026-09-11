# Contributing

This repository is a **passive, provenance-pinned snapshot** of Rosetta Code's
SAS category. The primary workflow is *refresh*, not hand-editing.

## Refresh (recommended)
The corpus is generated from upstream by the harvest pipeline bundled at
`tools/fetch_rosetta_sas.py` (standard library only). Check first, then
refresh:

```sh
python3 tools/fetch_rosetta_sas.py --check   # report drift; writes nothing
python3 tools/fetch_rosetta_sas.py           # regenerate + report
```

`--check` exits non-zero when the repository is not current, so it doubles
as a drift alarm. A refresh is faithful and minimal: unchanged files keep
their original retrieval stamps, and anything that moved is restored to
byte-faithful upstream extraction, so local touch-ups to generated files are
overwritten by design. If you need a deliberate local edit, keep it out of
generated files or mark it in the file header as your own contribution.
Refresh = regenerate + commit `corpus/`, `TASKS.csv`, `TASKS.md`, and update
the snapshot dates in `README.md`.

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
