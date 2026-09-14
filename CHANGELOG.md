# Changelog

All notable changes to SASchi-Roku are recorded here. Versioning is semver per
`agent-manifest.json`, and the current version is `0.1.0`.

The repository carries no release tags yet, so a version named in this file
describes a state of `main` rather than a published artifact. This file was added
on 2026-09-14, and the entries below were reconstructed from the commit history of
`main`, which was the only record before it existed. Short hashes are given so
every line can be traced to its commit.

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
