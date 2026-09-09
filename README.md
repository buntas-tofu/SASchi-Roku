# Rosetta Code — SAS Solutions Corpus

A provenance-pinned snapshot of every SAS solution currently published on
[Rosetta Code](https://rosettacode.org/wiki/Category:SAS): **56 tasks, 100% of
the category**, retrieved **2026-09-08**.

This repository is a *data corpus*, not a software project. It holds the SAS
side of Rosetta Code's "same task, many languages" canon — community-written
SAS, from classroom classics (FizzBuzz, Fibonacci, N-queens, Sudoku) to
genuinely statistical material (Welch's t-test, QR decomposition, P-value
correction, cumulative standard deviation). It exists so that SAS work can be
searched, diffed, cited, and fed into tooling **without scraping the wiki**.

## Quick start

```sas
/* Run any single task's solution with SAS or SAS Studio: */
%include "corpus/fizzbuzz.sas";

/* Every solution is self-contained: read the provenance header, then the code. */
```

A browsable index of all 56 tasks lives in
[`TASKS.csv`](TASKS.csv) (task → file → source URL → page revision) and is
summarized in [`TASKS.md`](TASKS.md).

## Repository layout

| Path | Purpose |
|------|---------|
| `corpus/` | One `.sas` file per task. Filenames are slugified task titles. |
| `TASKS.csv` | Machine-readable index: file, task title, source URL, revision, retrieval time. |
| `LICENSE` | Corpus-wide license statement (GFDL 1.2, see below). |
| `NOTICE` | Provenance & attribution appendix. |

Every `.sas` file opens with a provenance header, e.g.:

```sas
/* Source: https://rosettacode.org/wiki/FizzBuzz
   Rosetta Code task 'FizzBuzz', page revision 410510.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:03Z. */
```

The **page revision ID** is the important part: it pins each file to the exact
revision of the wikitext it was extracted from, so any file is reproducible and
auditable against upstream.

## License and provenance

The SAS text in this corpus originates from [Rosetta Code](https://rosettacode.org),
which is published under the **GNU Free Documentation License 1.2**
(see [Rosetta_Code:Copyrights](https://rosettacode.org/wiki/Rosetta_Code:Copyrights)).
Individual contributors may have granted additional permissions; page history is
the authority. Accordingly:

- This collection, its headers, and this README are distributed under
  **GFDL 1.2** (see [`LICENSE`](LICENSE)) with attribution to the Rosetta Code
  project and the individual task authors.
- Each file preserves its own provenance so downstream reuse can attribute
  correctly. See [`NOTICE`](NOTICE).
- This is a **point-in-time snapshot** of a wiki; upstream content is licensed
  by its contributors, not by this repository.

If you redistribute, modify, or build on these files, keep the provenance
headers attached and reproduce this notice.

## Status and caveats

- **Community probe material, not verified gold.** Nothing here is a
  correctness claim until it has been executed and checked. Contributions may
  be partial, illustrative, or platform-specific (Base SAS vs. SAS/IML vs.
  SAS Studio).
- **Multiple examples per task are kept in one file**, separated by numbered
  comment banners (`/* --- task: example 1 of 2 --- */`).
- **Code-block language labels are not reliable upstream**; code inside a SAS
  section is captured regardless of its `lang=` label (PROC IML has shipped as
  `lang=text`, PROC SQL as `lang=sql`).

## Refresh

This snapshot is reproducible by re-running the harvest pipeline against the
MediaWiki API: enumerate the `Category:SAS` members, fetch each task's
wikitext, and extract the `{{header|SAS}}` sections. The upstream category
grows over time; refresh whenever a newer snapshot is wanted. Provenance
headers make each generation auditable. A refresh script is planned in a future
release (see [CONTRIBUTING](CONTRIBUTING.md)).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — briefly: prefer a PR per task,
keep provenance headers intact, and mark any additions that are *yours*
(not re-scraped) clearly.

---

*Mirrored snapshot of https://rosettacode.org/wiki/Category:SAS retrieved
2026-09-08. Rosetta Code and its content are © their respective contributors
and licensed under GFDL 1.2.*
