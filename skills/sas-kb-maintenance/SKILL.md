---
name: sas-kb-maintenance
description: "Maintain the SASchi-Roku kb: syncs, harvests, drift, and gates."
version: 0.1.0
status: active
author: Matthew Haubach (buntas-tofu), Hermes Agent
license: GFDL-1.2
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sas, kb, maintenance, sync, provenance]
    related_skills: [sas-conversion]
---

# SAS Knowledge Base Maintenance Skill

How to keep the SASchi-Roku `kb/` honest: the sync and harvest contracts, what
drift means, which gate catches what, and the ledger discipline for moves.
Pure standard library tooling plus git; no runtime dependencies beyond the
repository tools (the `mcp/` subproject's fastmcp dependency is only needed
to run the server, not to maintain the kb).

## When to Use

- A CI gate went red (stamps, corpus lockstep, linter, manifest, MCP
  self-test).
- The canonical source lane moved and the copies need a refresh.
- The Rosetta corpus needs its periodic drift check.
- Content is moving within the repository (a new namespace, a rename, a
  fold, a retirement).

Don't use for: converting SAS (that is `sas-conversion`), or for editing
synced knowledge (that is never done here; see the drift doctrine).

## The three copy classes

1. **Synced, stamp-controlled** (`kb/rulebook`, `kb/capability`,
   `kb/semantics`, `kb/census`, `kb/evidence`): byte-stable copies of the
   canonical source lane with a `SOURCE.json` stamp beside them (source
   repo, pinned commit, version, copy time, per-file sha256).
2. **Harvested** (the corpus directory beside its `TASKS.csv`, wherever
   the instance keeps it, plus `kb/reference`): the Rosetta Code snapshot
   with per-file provenance headers and generated indexes (`TASKS.csv`,
   `TASKS.md`), and the SAS 9.4 docsets: pinned PDFs under
   `kb/reference/pdfs/`, page-pinned entries under `extracted/`, reconciled
   against the capability manifest's universes (108 stmt, 40 dso).
3. **Imported, ledgered** (`kb/landmines`, `kb/research`, `kb/convert`,
   plus `training/`, `archive/`, `vendor/`): material consolidated from
   elsewhere, recorded in `consolidation/LEDGER.md` with per-move manifests.

## Drift doctrine

A synced file that differs from its stamp is drifted. The fix is always
`python3 tools/sync_knowledge.py` (re-sync from the source), never a hand
edit: hand edits break the stamp hash, de-sanitize the copy lane, and hide
the divergence the stamp exists to surface. If the copy is *wrong*, the
correction belongs upstream in the canonical repo, then re-sync. Editing a
synced file in this repository is a contract-level smell, not a shortcut.

## Quick reference

```
python3 tools/sync_knowledge.py --check              # stamps vs files, offline
python3 tools/sync_knowledge.py --check --verify-source   # also re-fetch the pin
python3 tools/sync_knowledge.py [--source S] [--ref R]    # refresh + re-stamp
python3 tools/fetch_sas_reference.py --check         # reference layer determinism
python3 tools/fetch_sas_reference.py [--refresh]     # (re-)harvest the 9.4 docsets
python3 tools/fetch_rosetta_sas.py --check           # corpus vs upstream (network)
python3 tools/fetch_rosetta_sas.py                   # refresh corpus + indexes
python3 scripts/check_corpus_index.py                # corpus/TASKS/headers agree
python3 scripts/dmf-lint . --ignore evidence         # the floor + pointers
(cd kb && python3 tools/check_catalog.py)            # landmine card catalog
python3 -m sas_ref.mcp.selftest                      # needs SAS_REF_KB + fastmcp
```

## The five CI jobs and what each proves

- **Invariant linter**: fences, pointers, status lines, style floor. Runs
  with `--ignore evidence`: that exemption is a declared assertion (synced
  copies stay byte-stable; their links resolve in the source repository).
  The style floor still applies to evidence files.
- **Manifest validation**: `agent-manifest.json` against its schema.
- **Synced-copy stamps**: `sync_knowledge.py --check`; a red stamp job
  means drift doctrine applies.
- **MCP self-test**: the server loads the live kb/ and answers at the
  protocol level; red usually means a tool and the kb shape diverged.
- **Corpus index lockstep**: corpus, `TASKS.csv`, `TASKS.md`, and the
  provenance headers agree; red after any corpus move means a script path
  or the index format changed without its partner.

## Procedure: refreshing the synced copies

1. Run `--check` first; a green result means nothing drifted locally and
   the only question is whether the source moved.
2. Refresh: plain run (default source is the canonical public repository,
   HEAD pinned at run time). Criterion: the run prints per-layer counts and
   the new `SOURCE.json` stamps carry one identical `source_commit`.
3. Re-run `--check` and the selftest. Criterion: both green.
4. Commit stamps and copies together; the changelog names the new source
   pin. Criterion: one commit contains the whole refresh.

## Procedure: moving content inside the repository

1. The move gets a ledger row BEFORE it lands: `consolidation/LEDGER.md`,
   internal-moves section (what, ruling reference, verification slot).
2. Prefer `git mv` (rename detection keeps history). Path strings in
   referencing files are updated mechanically; prose is not reworded as a
   side effect of a move.
3. Repoint every contract that resolves the path: scripts, checkers, the
   linter invocation, workflow steps, README layout rows, and the AGENTS
   identity paragraph.
4. Verification is a receipt, not a vibe: run the affected checkers and the
   linter, and for anything hash-manifested re-verify from a fresh clone.
   Record the receipts in the ledger row.
5. The ledger stays sanitization-neutral: repository names, commits, and
   hashes only; no host names, no estate paths (the tree is destined for a
   public sister).

## Pitfalls

- New evidence documents appear automatically: the sync globs the source
  `docs/` minus a small exclusion list, so an upstream family report lands
  in `kb/evidence/` on the next refresh with no code change. Read the
  per-layer count delta in the sync output; a surprise file is a surprise
  upstream doc, not a bug.
- `--check` is offline by design (CI-safe). To prove the pin still exists
  and matches upstream, use `--check --verify-source` (network).
- The corpus harvest `--check` hits the live wiki (56 throttled requests);
  it is not a CI job for that reason. Budget a couple of minutes. The
  reference `--check` is offline (it regenerates from the stored PDFs) and
  IS a CI job; it needs `pdftotext` (poppler-utils).
- The reference parser's entry detection is reconciled against the
  capability manifest at every harvest: a count mismatch exits non-zero.
  If upstream enumerates a new docset (fmt, func, opt...), add it to the
  harvester's DOCSETS table with its verified slug and terminator; slugs
  must be confirmed against documentation.sas.com before pinning (the
  design's guessed DSO slug 404s).
- A corpus move without repointing BOTH `tools/fetch_rosetta_sas.py` and
  `scripts/check_corpus_index.py` passes lint and fails the lockstep job;
  the generator and the checker are a pair.
- Version bumps: `agent-manifest.json` and the CHANGELOG header carry the
  same semver; a kb shape change is a minor bump, a content refresh is
  patch-level unless a contract changed.

## Verification

Maintenance is done when: `--check` is green, the corpus checker is green,
the linter is green with the declared exemption, the selftest is green, the
ledger row for any move carries its receipts, and the changelog names what
changed with the source pin where one applies.
