#!/usr/bin/env python3
"""sync_knowledge.py : pull the canonical knowledge copies into kb/ and stamp them.

sas-ref holds COPIES of the machine-readable knowledge, never the canonical
home. The canonical source is the SASchi-Go repository of the source lane;
this tool copies the routed files into kb/, writes a SOURCE.json stamp per
layer (source repo, pinned commit, version, copy time, per-file sha256), and
verifies on demand that the copies still match their stamps.

Contract (same shape as the harvest pipeline):
  --check         verify local copies against their SOURCE.json stamps;
                  exit 1 on drift; write nothing; no network
  --verify-source additionally re-fetch the pinned commit from the recorded
                  source and compare content (network)
  plain run       refresh the copies from the source, rewrite the stamps

Source resolution (operator ruling 2026-11-02, design question 2):
configurable, remote-preferred. --source accepts a git URL (default: the
canonical public repository) or a local path to a clone; --ref accepts any
commit-ish (default: the source's HEAD, resolved and stamped as a sha).

Routing table:
  kb/rulebook/    docs/sasconversionrulebook.json
  kb/capability/  docs/capability-manifest.json
  kb/semantics/   sas_semantics.py, kb01/sas_semantics_reference.txt
  kb/census/      docs/macro_surface_census.csv, docs/macro_surface_census.md
  kb/evidence/    the remaining docs/ files, minus the repository operations
                  docs (OPERATIONS.md, USER_GUIDE.md, STATEFUL_EXECUTION.md)
                  which describe the source repo, not the SAS surface

Editing a synced file under kb/ is a drift smell: the stamp check will fail,
and the fix is to re-sync, never to hand-edit. Pure standard library plus a
git subprocess for remote fetches.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"

DEFAULT_SOURCE = "https://github.com/buntas-tofu/SASchi-Go.git"

FIXED_LAYERS = {
    "rulebook": ["docs/sasconversionrulebook.json"],
    "capability": ["docs/capability-manifest.json"],
    "semantics": ["sas_semantics.py", "kb01/sas_semantics_reference.txt"],
    "census": ["docs/macro_surface_census.csv", "docs/macro_surface_census.md"],
}
EVIDENCE_EXCLUDE = {
    "sasconversionrulebook.json",
    "capability-manifest.json",
    "macro_surface_census.csv",
    "macro_surface_census.md",
    "OPERATIONS.md",
    "USER_GUIDE.md",
    "STATEFUL_EXECUTION.md",
}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def resolve_source(source: str, ref: str):
    """Return (tree_dir, source_commit, is_temp). tree_dir is a checkout of ref."""
    p = Path(source)
    if p.is_dir():
        out = subprocess.run(["git", "-C", str(p), "rev-parse", ref],
                             capture_output=True, text=True)
        if out.returncode != 0:
            sys.exit(f"error: local source {source} cannot resolve ref {ref}")
        return p, out.stdout.strip(), False
    tmp = Path(tempfile.mkdtemp(prefix="sync-knowledge-"))
    url = source
    want = ref
    if ref == "HEAD":
        ls = subprocess.run(["git", "ls-remote", url, "HEAD"],
                            capture_output=True, text=True, check=True)
        want = ls.stdout.split()[0]
    subprocess.run(["git", "init", "--quiet", str(tmp)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(tmp), "fetch", "--quiet", "--depth", "1",
                    url, want], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp), "checkout", "--quiet",
                    "FETCH_HEAD"], check=True, capture_output=True)
    return tmp, want, True


def layer_files(tree: Path) -> dict:
    """The routing table resolved against a source tree: layer -> {name: path}."""
    layers = {}
    for layer, rels in FIXED_LAYERS.items():
        files = {}
        for rel in rels:
            src = tree / rel
            if not src.is_file():
                sys.exit(f"error: source tree lacks {rel} (layer {layer})")
            files[Path(rel).name] = src
        layers[layer] = files
    docs = tree / "docs"
    evidence = {}
    for f in sorted(docs.iterdir()):
        if f.is_file() and f.name not in EVIDENCE_EXCLUDE:
            evidence[f.name] = f
    if not evidence:
        sys.exit("error: source tree produced an empty evidence layer")
    layers["evidence"] = evidence
    return layers


def source_version(tree: Path, layer: str, files: dict) -> str:
    if layer == "rulebook":
        data = json.loads(files["sasconversionrulebook.json"].read_bytes())
        return str(data.get("meta", {}).get("version", "unknown"))
    if layer == "capability":
        data = json.loads(files["capability-manifest.json"].read_bytes())
        v = data.get("version", data.get("meta", {}).get("version"))
        if v is not None:
            return str(v)
    try:
        manifest = json.loads((tree / "agent-manifest.json").read_bytes())
        return str(manifest.get("project", {}).get("version", "unknown"))
    except (OSError, json.JSONDecodeError):
        return "unknown"


def do_sync(source: str, ref: str) -> None:
    tree, commit, is_temp = resolve_source(source, ref)
    try:
        layers = layer_files(tree)
        copied_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for layer, files in layers.items():
            dest = KB / layer
            dest.mkdir(parents=True, exist_ok=True)
            hashes = {}
            for name, src in sorted(files.items()):
                raw = src.read_bytes()
                (dest / name).write_bytes(raw)
                hashes[name] = sha256_bytes(raw)
            stamp = {
                "layer": layer,
                "source_repo": source if not Path(source).is_dir() else str(Path(source).resolve()),
                "source_commit": commit,
                "version": source_version(tree, layer, files),
                "copied_at": copied_at,
                "files": hashes,
            }
            (dest / "SOURCE.json").write_text(json.dumps(stamp, indent=2) + "\n")
            print(f"synced {layer}: {len(hashes)} file(s) at {commit[:7]} (version {stamp['version']})")
    finally:
        if is_temp:
            shutil.rmtree(tree, ignore_errors=True)


def do_check(verify_source: bool) -> int:
    drift = 0
    for stamp_path in sorted(KB.glob("*/SOURCE.json")):
        dest = stamp_path.parent
        stamp = json.loads(stamp_path.read_bytes())
        layer = stamp["layer"]
        listed = stamp["files"]
        actual = {p.name for p in dest.iterdir() if p.is_file() and p.name != "SOURCE.json"}
        if actual != set(listed):
            extra = sorted(actual - set(listed))
            missing = sorted(set(listed) - actual)
            print(f"drift [{layer}]: file set differs (extra={extra}, missing={missing})")
            drift += 1
            continue
        bad = []
        for name, want in listed.items():
            got = sha256_bytes((dest / name).read_bytes())
            if got != want:
                bad.append(name)
        if bad:
            print(f"drift [{layer}]: hash mismatch in {bad}; re-sync, never hand-edit")
            drift += 1
        if verify_source and not bad and actual == set(listed):
            tree, commit, is_temp = resolve_source(stamp["source_repo"], stamp["source_commit"])
            try:
                if commit != stamp["source_commit"]:
                    print(f"drift [{layer}]: pinned commit {stamp['source_commit'][:7]} no longer resolves")
                    drift += 1
                    continue
                layers = layer_files(tree)
                for name in listed:
                    src = layers[layer].get(name)
                    if src is None or sha256_bytes(src.read_bytes()) != listed[name]:
                        print(f"drift [{layer}]: {name} differs from the pinned source commit")
                        drift += 1
            finally:
                if is_temp:
                    shutil.rmtree(tree, ignore_errors=True)
        if drift == 0:
            print(f"ok [{layer}]: {len(listed)} file(s) match the stamp at {stamp['source_commit'][:7]}")
    if drift:
        print(f"check: {drift} drifted layer(s); run without --check to re-sync")
        return 1
    print("check: every synced layer matches its SOURCE.json stamp")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Pull the canonical knowledge copies into kb/ and stamp them.")
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="git URL (default: the canonical public repo) or a local clone path")
    ap.add_argument("--ref", default="HEAD",
                    help="commit-ish to pin (default: source HEAD, resolved to a sha)")
    ap.add_argument("--check", action="store_true",
                    help="verify copies against stamps; write nothing; no network")
    ap.add_argument("--verify-source", action="store_true",
                    help="with --check: also re-fetch the pinned commit and compare content")
    args = ap.parse_args()
    if args.check:
        return do_check(args.verify_source)
    do_sync(args.source, args.ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())
