# Changelog

All notable changes to SASchi-Roku are recorded here. Versioning is semver per
`agent-manifest.json`, and the current version is `0.2.0`.

The repository carries no release tags yet, so a version named in this file
describes a state of `main` rather than a published artifact. This file was added
on 2026-09-14, and the entries below were reconstructed from the commit history of
`main`, which was the only record before it existed. Short hashes are given so
every line can be traced to its commit.

## 0.2.0 - 2026-11-02

### Added

- The reference-home layers, cut from the professional-lane instance at its
  post-Phase-4 state and adapted to this repository's shape: `kb/` (stamp-synced
  copies of the canonical rulebook (115 rules), capability manifest (148
  entries), semantics, census, and 23 evidence documents at source pin
  `3491504`; the harvested SAS 9.4 reference, 148 page-pinned dictionary
  entries reconciled 108/108 and 40/40 against the capability manifest and
  page-pin matched 148/148; the 49 landmine cards; conversion guides; field-guide
  research), `mcp/` (the advisory MCP server: twelve tools, nine resources,
  three prompts, stdio with the HTTP transport flag ready, installable via
  `pip install ./mcp` or the git subdirectory URL), the two knowledge-base
  skills (`sas-conversion`, `sas-kb-maintenance`), and `vendor/` (the
  parquet-format reference pair under pinned provenance).
- Four new CI checks (nine total): synced-copy stamps, reference determinism
  (harvest from the pinned public URLs, committed output reproduces
  byte-identical; the PDFs themselves are gitignored, the sha256 pins and
  URLs are the provenance), the MCP self-test, and the sanitization token
  gate under this instance's profile with declared exemptions and an
  adjudicated allowlist.

- Toolkit scope decision, roadmap, session handoff and relocation receipt.
- Initial assessment, translation and Parquet interchange skills.
- Source-backed resource catalog seeded from the Campaign census, sas-ref,
  training modules, Go and Garage, including unresolved upstream provenance.
- Toolkit checks and relocation regression tests alongside existing CI gates.
- First isolated translation skill trial: archived candidate, independent
  arithmetic/missingness oracle, seven rejected negative controls and CI replay.

- Accepted phased test plan and eight independent starter deliveries: four
  reviewed assessments, four Python/native-R conversions, 32 parent runtime
  checks, 10 rejected controls, immutable packets and separate CI replay.
- Parent findings preserve the open ASCII/NUL interface boundary and distinguish
  agent self-test repair from independent verification.
- Three accepted follow-on skills: dependency and macro capture inventory,
  character/metadata interchange contracts, and stateful failure diagnosis.
- Three isolated first deliveries, seven dependency review criteria, a CSV/raw
  companion witness, conditional-state repairs in Python and native R, and
  35 independent replay checks including 12 rejected corruption controls.
- An executed original failure remains archived; actual SAS capture is pending.
- WHERE versus subsetting IF state trial: one fresh paired Python/R delivery,
  frozen parent harness, 31 passing checks, six rejected output controls and
  the reproduced original failure. CI replays the bounded result.

### Changed

- Preserve the Rosetta Code corpus, indexes and attribution under
  `references/rosetta-code/`; retain old paths as compatibility symlinks.
- Retarget the harvest and corpus-index checks to the nested collection.
- Close harvest index readers explicitly while preserving newline handling.
- Expand the LOCAL contract and root documentation to the toolkit scope.
- Preserve all 56 SAS files and both indexes byte for byte. Keep license terms
  unchanged. No upstream refresh or live-SAS execution is part of this move.

## 0.1.0 - 2026-09-14

### Added

- The corpus: every SAS solution published on Rosetta Code at the time of
  retrieval, 56 tasks, one file each, each carrying a provenance header with its
  source URL, page revision, licence, and retrieval timestamp (`6c18a02`).
- `LICENSE` (GFDL 1.2) and `NOTICE.md`, which records that the content is licensed
  by its Rosetta Code contributors and not by this repository (`661eef6`).
- `TASKS.csv` and `TASKS.md`, the machine-readable and human indexes of the corpus
  (`661eef6`).
- `CONTRIBUTING.md` and the README reshape (`661eef6`).
- `tools/fetch_rosetta_sas.py`, the MediaWiki harvest pipeline, which can check the
  corpus against the upstream category or refresh it (`3773dc7`).
- DMF governance: the `AGENTS.md` contract, `agent-manifest.json` and its schema,
  the vendored drift linter, and the governance workflow (`92315e5`).

### Changed

- Re-vendored `scripts/inertia-drift-lint` at 2.1.0, whose floor covers all text
  artifact formats (`6cd6af4`).
- Index titles and timestamps normalized (`c56a2a6`).

### Fixed

- A faithful resync of `palindrome_detection` against upstream (`c56a2a6`), and the
  earlier palindrome fix that came with the public-ready pass (`661eef6`).

### Notes

- Nothing in this repository is a correctness claim until it has been executed and
  checked. The corpus records what upstream published, not what has been verified
  here.
