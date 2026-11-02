#!/usr/bin/env python3
"""Check toolkit records and generate their human index. Standard library only."""

import argparse
import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog/resources.json"
INDEX = ROOT / "catalog/README.md"


def https_url(value):
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    return (parts.scheme == "https" and bool(parts.hostname)
            and not parts.username and not parts.password
            and not any(c.isspace() for c in value))


def date_ok(value):
    try:
        return datetime.date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def validate(data):
    """Return all structural findings; evidence remains an explicit source claim."""
    out = []
    if not isinstance(data, dict):
        return ["catalog must be an object"]
    if data.get("schema_version") != 1 or isinstance(data.get("schema_version"), bool):
        out.append("unsupported schema_version")
    if not date_ok(data.get("updated_on")):
        out.append("updated_on must be an ISO date")
    if not isinstance(data.get("status"), str) or not data["status"].strip():
        out.append("catalog needs an evidence status")
    records = data.get("resources")
    if not isinstance(records, list) or not records:
        return out + ["resources must be a nonempty list"]
    seen, urls = set(), set()
    required = {"id", "name", "kind", "category", "url", "description", "tags",
                "locations", "evidence", "github_snapshot", "historical_census"}
    for i, item in enumerate(records):
        at = f"resource {i + 1}"
        if not isinstance(item, dict) or set(item) != required:
            out.append(f"{at}: fields differ from the version 1 record contract")
            continue
        for field in ("id", "name", "category", "description"):
            value = item[field]
            if not isinstance(value, str) or not value.strip():
                out.append(f"{at}: {field} must be nonempty text")
        ident = item["id"]
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident):
            out.append(f"{at}: invalid stable ID")
        elif ident in seen:
            out.append(f"{at}: duplicate ID {ident}")
        else:
            seen.add(ident)
        if item["kind"] not in ("repository", "collected-material"):
            out.append(f"{at}: unknown resource kind")
        url = item["url"]
        if url is not None:
            if not https_url(url):
                out.append(f"{at}: invalid resource URL")
            elif url.lower().rstrip("/") in urls:
                out.append(f"{at}: duplicate resource URL")
            else:
                urls.add(url.lower().rstrip("/"))
        elif item["kind"] != "collected-material":
            out.append(f"{at}: repository must have a URL")
        tags = item["tags"]
        if (not isinstance(tags, list) or not tags
                or any(not isinstance(tag, str) or not tag.strip() for tag in tags)):
            out.append(f"{at}: tags must be a nonempty text list")
        locations = item["locations"]
        if not isinstance(locations, list) or any(not https_url(x) for x in locations):
            out.append(f"{at}: locations must be HTTPS references")
        evidence = item["evidence"]
        evidence_keys = {"status", "reviewed_on", "scope", "source_url", "source_revision", "notes"}
        if not isinstance(evidence, dict) or set(evidence) != evidence_keys:
            out.append(f"{at}: missing or unexpected evidence fields")
            continue
        if evidence["status"] not in ("source-inspected", "repository-resolved", "upstream-unresolved"):
            out.append(f"{at}: unsupported evidence status")
        if url is None and evidence["status"] != "upstream-unresolved":
            out.append(f"{at}: unknown upstream must stay unresolved")
        if evidence["status"] == "upstream-unresolved" and url is not None:
            out.append(f"{at}: unresolved upstream cannot claim a repository URL")
        if not date_ok(evidence["reviewed_on"]) or not https_url(evidence["source_url"]):
            out.append(f"{at}: invalid evidence date or source URL")
        rev = evidence["source_revision"]
        if not isinstance(rev, str) or not re.fullmatch(r"[0-9a-f]{40}", rev):
            out.append(f"{at}: source_revision must pin the collection source commit")
        elif not isinstance(evidence["source_url"], str) or f"/blob/{rev}/" not in evidence["source_url"]:
            out.append(f"{at}: source URL does not pin source_revision")
        if not isinstance(evidence["scope"], str) or not evidence["scope"].strip():
            out.append(f"{at}: evidence scope is required")
        if not isinstance(evidence["notes"], str):
            out.append(f"{at}: evidence notes must be text")
        snap = item["github_snapshot"]
        if snap is not None:
            if (not isinstance(snap, dict)
                    or set(snap) != {"archived", "license_identifier", "default_branch"}
                    or not isinstance(snap["archived"], bool)
                    or not isinstance(snap["default_branch"], str)
                    or not snap["default_branch"]
                    or (snap["license_identifier"] is not None
                        and not isinstance(snap["license_identifier"], str))):
                out.append(f"{at}: malformed GitHub lookup snapshot")
        census = item["historical_census"]
        if census is not None:
            if (not isinstance(census, dict)
                    or set(census) != {"snapshot_date", "sas_files", "license_files_observed"}
                    or not date_ok(census["snapshot_date"])
                    or type(census["sas_files"]) is not int or census["sas_files"] < 0
                    or not isinstance(census["license_files_observed"], str)
                    or not census["license_files_observed"]):
                out.append(f"{at}: malformed historical census")
    return out


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def render_index(data):
    lines = ["# Resource catalog", "", f"Status: {data['status']}", "",
             "Generated from [resources.json](resources.json). Edit that file, then run",
             "`python3 scripts/check_toolkit.py --write-index` from the repository root.", "",
             f"{len(data['resources'])} resources. Source/lookup review date: {data['updated_on']}.", "",
             "September census counts describe the original testbed, not today's upstream.",
             "GitHub license identifiers are dated API observations, not per-file rights",
             "reviews. Unknown identifiers and upstream origins remain explicit.", ""]
    categories = sorted({item["category"] for item in data["resources"]})
    for category in categories:
        lines.extend([f"## {category}", "", "| Resource | Use | Evidence |",
                      "|---|---|---|"])
        for item in sorted(data["resources"], key=lambda r: r["id"]):
            if item["category"] != category:
                continue
            url = item["url"] or item["evidence"]["source_url"]
            evidence = item["evidence"]
            detail = f"{evidence['status']}; [source]({evidence['source_url']})"
            if item["historical_census"]:
                c = item["historical_census"]
                detail += f"; {c['sas_files']} SAS files at {c['snapshot_date']}"
            if item["github_snapshot"]:
                snap = item["github_snapshot"]
                detail += f"; license ID: {snap['license_identifier'] or 'unknown'}"
                if snap["archived"]:
                    detail += "; archived at lookup"
            lines.append(f"| [{cell(item['name'])}]({url}) | {cell(item['description'])} | {cell(detail)} |")
        lines.append("")
    lines.extend(["## Reading the record", "",
                  "Each JSON record carries a stable ID, tags, discovery source and revision,",
                  "additional locations, evidence limits and provenance notes. A source revision",
                  "pins the discovery record; it does not pretend to pin every external project.",
                  "The collected migration scaffold has no known upstream URL. The training",
                  "modules' original and consolidated locations are recorded as one resource.", ""])
    return "\n".join(lines)


def check_paths(root):
    out = []
    for name in ("corpus", "TASKS.csv", "TASKS.md"):
        old = root / name
        target = root / "references/rosetta-code" / name
        if not old.is_symlink() or not target.exists() or old.resolve() != target.resolve():
            out.append(f"compatibility path {name} must link to {target.relative_to(root)}")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-index", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        problems = validate(data) + check_paths(ROOT)
    except (OSError, ValueError) as exc:
        problems = [str(exc)]
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    expected = render_index(data)
    if args.write_index:
        INDEX.write_text(expected, encoding="utf-8")
    elif not INDEX.exists() or INDEX.read_text(encoding="utf-8") != expected:
        print("FAIL: catalog/README.md is stale; run with --write-index")
        return 1
    print(f"PASS: {len(data['resources'])} catalog records, generated index and compatibility paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
