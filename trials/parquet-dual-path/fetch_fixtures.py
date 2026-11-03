#!/usr/bin/env python3
"""Fetch pinned, licensed upstream fixtures without adding binaries to the tree."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SELECTED = {
    'LICENSE': 'LICENSE',
    'test_data/basic/sample.sas7bdat': 'sample.sas7bdat',
    'test_data/missing_data/missing_test.sas7bdat': 'missing.sas7bdat',
    'test_data/missing_data/missing_formats.sas7bcat': 'missing.sas7bcat',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    records = json.loads((ROOT / 'upstream.json').read_text())['files']
    records = [r for r in records if r['path'] in SELECTED]
    args.directory.mkdir(parents=True, exist_ok=True)
    for record in records:
        target = args.directory / SELECTED[record['path']]
        if target.exists():
            data = target.read_bytes()
        else:
            with urllib.request.urlopen(record['url'], timeout=60) as response:
                data = response.read()
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != record['bytes'] or digest != record['sha256']:
            raise SystemExit('upstream identity mismatch: ' + record['path'])
        if not target.exists():
            target.write_bytes(data)
        print(target.name + ': ' + digest)


if __name__ == '__main__':
    main()
