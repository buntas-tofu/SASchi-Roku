#!/usr/bin/env python3
"""Replay a separate repaired attempt with the unchanged frozen parent harness."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

import verify

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    original = json.loads((ROOT / 'delivery.json').read_text())
    for name, digest in original['hashes'].items():
        assert sha(ROOT / name) == digest, 'original delivery drift: ' + name
    repair = json.loads((ROOT / 'repair/delivery.json').read_text())
    assert repair['original_delivery_sha256'] == sha(ROOT / 'delivery.json')
    assert sha(ROOT / 'repair/converted.py') == repair['hashes']['candidate/converted.py']
    with tempfile.TemporaryDirectory(prefix='roku-parquet-repair-attempt-') as temp:
        root = Path(temp)
        frozen = json.loads((ROOT / 'freeze.json').read_text())
        for name in frozen['hashes']:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        shutil.copyfile(ROOT / 'freeze.json', root / 'freeze.json')
        shutil.copytree(ROOT / 'candidate', root / 'candidate',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copyfile(ROOT / 'repair/converted.py', root / 'candidate/converted.py')
        shutil.copyfile(ROOT / 'repair/delivery.json', root / 'delivery.json')
        verify.ROOT = root
        result = verify.main()
    return result


if __name__ == '__main__':
    sys.exit(main())
