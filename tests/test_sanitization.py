"""Historical-input exceptions stop applying when bytes or paths change."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'sanitization_gate', ROOT / 'scripts/check_sanitization.py')
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class FrozenCitationExceptionTests(unittest.TestCase):
    def setUp(self):
        rows = json.loads((ROOT / 'scripts/sanitization-allowlist.json').read_text())
        self.rows = [r for r in rows if 'sha256' in r]
        self.paths = [ROOT / 'trials/state-boundaries/packets' / task /
                      'skills/sas-translate/references/evidence.md'
                      for task in ('merge', 'widths')]

    def scan(self, files, rows=None):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            with patch.object(GATE, 'load_allowlist', return_value=self.rows if rows is None else rows):
                with contextlib.redirect_stdout(io.StringIO()):
                    return GATE.run('buntas', root)

    def test_exact_frozen_packets_are_accepted(self):
        self.assertEqual(self.scan({p.relative_to(ROOT): p.read_bytes() for p in self.paths}), 0)

    def test_changed_bytes_lose_exception(self):
        for path in self.paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(self.scan({path.relative_to(ROOT): path.read_bytes() + b'\n'}), 1)

    def test_same_bytes_elsewhere_are_rejected(self):
        self.assertEqual(self.scan({'other/evidence.md': self.paths[0].read_bytes()}), 1)

    def test_different_forbidden_token_is_rejected(self):
        path = self.paths[0]
        token = next(p for p in GATE.ESTATE if p.startswith('tail'))
        content = path.read_bytes() + token.encode()
        rows = [dict(row, sha256=hashlib.sha256(content).hexdigest()) for row in self.rows]
        self.assertEqual(self.scan({path.relative_to(ROOT): content}, rows), 1)

    def test_existing_declared_exceptions_keep_their_behavior(self):
        path = self.paths[0]
        row = {'path': '^history[.]md$', 'pattern': self.rows[0]['pattern']}
        self.assertEqual(self.scan({'history.md': path.read_bytes()}, [row]), 0)


if __name__ == '__main__':
    unittest.main()
