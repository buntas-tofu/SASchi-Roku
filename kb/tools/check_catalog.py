#!/usr/bin/env python3
"""Validate the provider-independent inventory; not a SAS execution gate."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check():
    catalog = json.loads((ROOT / 'collections.json').read_text())
    assert catalog['schema_version'] == 1
    ids, paths, collections = set(), set(), set()
    for collection in catalog['collections']:
        name = collection['id']
        assert name not in collections, name
        collections.add(name)
        meta = collection['metadata']
        assert meta['corpus'] == name
        assert meta['review_status'] in {'unreviewed', 'reviewed', 'superseded'}
        assert meta['validation_basis'] in {'asserted', 'corroborated', 'gate', 'receipt'}
        actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'landmines' / name).glob('*.md')
                  if p.name not in {'README.md', 'SOURCES.md'}}
        declared = set()
        for doc in collection['documents']:
            ident, path = doc['id'], doc['path']
            assert ident not in ids and path not in paths, doc
            assert re.fullmatch(r'(ML|LQ|SL)-\d{3}', ident), ident
            assert path.startswith(f'landmines/{name}/') and '..' not in Path(path).parts
            ids.add(ident)
            paths.add(path)
            declared.add(path)
            body = (ROOT / path).read_text()
            assert body.startswith(f'# {ident}:'), path
            assert doc['source_url'].startswith('https://') and doc['source_rev'], path
            assert doc['source_url'] in body, path
        assert actual == declared, (name, actual ^ declared)
    sources = json.loads((ROOT / 'research/SOURCES_20260915.json').read_text())['sources']
    source_ids = {s['id'] for s in sources}
    assert len(source_ids) == len(sources)
    for path in paths:
        refs = re.findall(r'^- ([PSTC]\d+):', (ROOT / path).read_text(), re.M)
        assert set(refs) <= source_ids, path
    queue = list(csv.DictReader((ROOT / 'research/SAS_FIXTURE_QUEUE_20260915.csv').open()))
    assert len({r['card_id'] for r in queue}) == len(queue)
    assert all(r['card_id'] in ids and r['execution_status'] == 'DESIGN_ONLY_NOT_RUN' for r in queue)
    imports = json.loads((ROOT / 'IMPORT_MANIFEST.json').read_text())['files']
    assert len({i['path'] for i in imports}) == len(imports)
    for item in imports:
        assert re.fullmatch('[0-9a-f]{64}', item['original_sha256'])
        assert re.fullmatch('[0-9a-f]{64}', item['imported_sha256'])
    for folder in [ROOT, ROOT / 'landmines', ROOT / 'research']:
        files = folder.glob('*.md') if folder == ROOT else folder.rglob('*.md')
        for p in files:
            body = p.read_text()
            assert not re.search(r'\u2014|\u2026|\.{3}', body), p
            for link in re.findall(r'\]\(([^)]+)\)', body):
                if '://' in link or link.startswith('#'):
                    continue
                target = link.split('#')[0]
                assert (p.parent / target).is_file(), (p, target)
    print(f'PASS: {len(collections)} collections, {len(paths)} cards, source metadata, local links, import records, {len(queue)} proposed tests')


if __name__ == '__main__':
    check()
