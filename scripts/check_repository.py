"""Portable checks for repository content; no network or experiment execution."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rlworkbench.core import load, validate
from handbook import check as check_handbook

errors = []
errors += check_handbook()
files = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md"]
files += list((ROOT / "docs").glob("*.md")) + list((ROOT / "templates").glob("*.md"))
for p in files:
    text = p.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^\s)]+)\)", text):
        url = urlsplit(target.strip("<>"))
        if url.scheme or url.netloc or not url.path:
            continue
        path = (p.parent / unquote(url.path)).resolve()
        if not path.exists():
            errors.append(f"{p.relative_to(ROOT)}: missing local link {target}")
    for marker in ("/Users/", "/home/yingwen", "codex://threads/"):
        if marker in text:
            errors.append(f"private context marker in {p.relative_to(ROOT)}: {marker}")
for folder in ("profiles", "catalog", "examples", "protocols", "schemas"):
    for p in (ROOT/folder).glob("*.json"):
        value = load(p)
        if folder in {"profiles", "protocols"}:
            errors += [f"{p.relative_to(ROOT)}: {e}" for e in validate(value, native=folder == "profiles")]
        if folder == "catalog":
            ids = [x['id'] for x in value['items']]
            if len(ids) != len(set(ids)):
                errors.append(f"duplicate catalog IDs in {p.name}")
            for item in value['items']:
                if item['implementation_status'] not in {'builtin_tutorial','optional_adapter','reference_only'}:
                    errors.append(f"unknown capability state: {item['id']}")
print(json.dumps({"status": "failed" if errors else "passed", "errors": errors, "markdown_files": len(files)}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
