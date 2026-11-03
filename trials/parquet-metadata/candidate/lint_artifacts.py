"""Small local style check. This is not the repository's invariant gate."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent
count = 0
violations = []
for path in sorted(root.rglob("*")):
    if path.suffix not in {".py", ".R", ".md", ".json"}:
        continue
    count += 1
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if chr(0x2014) in line or chr(0x2026) in line or re.search(r"\.{3}", line):
            violations.append(f"{path.relative_to(root)}:{line_number}")
if violations:
    raise SystemExit("style violations: " + ", ".join(violations))
print(f"Local artifact style check passed: {count} text files")
