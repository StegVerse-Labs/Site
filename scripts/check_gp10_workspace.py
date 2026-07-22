#!/usr/bin/env python3
"""Fail-closed static check for the temporary unlinked GP10 workspace."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "gp10-workspace.html"
SCRIPT = ROOT / "assets" / "gp10-workspace.js"


def main() -> int:
    errors = []
    if not PAGE.exists():
        errors.append("gp10-workspace.html is missing")
    if not SCRIPT.exists():
        errors.append("assets/gp10-workspace.js is missing")
    if errors:
        print("FAIL-CLOSED:")
        for error in errors:
            print(f"- {error}")
        return 1

    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    required_page = [
        'name="robots" content="noindex,nofollow,noarchive"',
        'assets/gp10-workspace.js',
        'No execution authority',
    ]
    required_script = [
        "BROWSER_LOCAL_UNCUSTODIED",
        "execution_authority: false",
        "DISCOVERY_ONLY",
        "COST_PLUS",
        "RE_SCOPE",
        "REJECT",
        "PROCEED",
        "localStorage",
    ]
    for marker in required_page:
        if marker not in page:
            errors.append(f"page missing marker: {marker}")
    for marker in required_script:
        if marker not in script:
            errors.append(f"script missing marker: {marker}")

    excluded = {PAGE.resolve(), SCRIPT.resolve(), Path(__file__).resolve()}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.resolve() in excluded:
            continue
        if any(part in {".git", "node_modules", "docs"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".html", ".xml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "gp10-workspace.html" in text:
            errors.append(f"temporary workspace is linked by {path.relative_to(ROOT)}")

    if errors:
        print(f"FAIL-CLOSED: {len(errors)} GP10 workspace isolation violation(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: GP10 workspace exists, preserves authority boundaries, and is not linked by Site pages or XML indexes")
    return 0


if __name__ == "__main__":
    sys.exit(main())