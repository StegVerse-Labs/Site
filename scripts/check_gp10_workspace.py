#!/usr/bin/env python3
"""Fail-closed static check for the temporary unlisted GP10 workspace pair."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "gp10-workspace.html"
EXAMPLES = ROOT / "gp10-workspace-examples.html"
SCRIPT = ROOT / "assets" / "gp10-workspace.js"
INTEGRATION = ROOT / "assets" / "gp10-evidence-integration.js"
WIZARD = ROOT / "assets" / "gp10-workspace-wizard.js"


def main() -> int:
    errors = []
    required_files = [
        (PAGE, "gp10-workspace.html"),
        (EXAMPLES, "gp10-workspace-examples.html"),
        (SCRIPT, "assets/gp10-workspace.js"),
        (INTEGRATION, "assets/gp10-evidence-integration.js"),
        (WIZARD, "assets/gp10-workspace-wizard.js"),
    ]
    for path, label in required_files:
        if not path.exists():
            errors.append(f"{label} is missing")
    if errors:
        print("FAIL-CLOSED:")
        for error in errors:
            print(f"- {error}")
        return 1

    page = PAGE.read_text(encoding="utf-8")
    examples = EXAMPLES.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    integration = INTEGRATION.read_text(encoding="utf-8")
    wizard = WIZARD.read_text(encoding="utf-8")

    required_page = [
        'name="robots" content="noindex,nofollow,noarchive"',
        'assets/gp10-workspace.js',
        'assets/gp10-evidence-integration.js',
        'assets/gp10-workspace-wizard.js',
        'gp10-workspace-examples.html',
        'No execution authority',
        'data-gp10-step',
    ]
    required_examples = [
        'name="robots" content="noindex,nofollow,noarchive"',
        'gp10-workspace.html',
        'What the fields mean',
        'DISCOVERY_ONLY', 'COST_PLUS', 'RE_SCOPE', 'REJECT', 'PROCEED',
        'No execution authority',
    ]
    required_script = [
        "BROWSER_LOCAL_UNCUSTODIED", "execution_authority: false", "DISCOVERY_ONLY",
        "COST_PLUS", "RE_SCOPE", "REJECT", "PROCEED", "localStorage",
    ]
    required_integration = [
        "crypto.subtle.digest", "original_sha256", "QUALIFIED_REVIEW_REQUIRED",
        "BROWSER_LOCAL_UNCUSTODIED", "execution_authority: false", "localStorage",
        "evidenceReviewQueue", "exportValidationBundle", "owner_role", "authority_class",
        "created_at", "asset:", "observations:", "conflicts:",
    ]
    required_wizard = ["data-gp10-step", "data-next-step", "data-prev-step", "Step ${current + 1}"]

    for marker in required_page:
        if marker not in page:
            errors.append(f"page missing marker: {marker}")
    for marker in required_examples:
        if marker not in examples:
            errors.append(f"examples page missing marker: {marker}")
    for marker in required_script:
        if marker not in script:
            errors.append(f"workspace script missing marker: {marker}")
    for marker in required_integration:
        if marker not in integration:
            errors.append(f"evidence integration missing marker: {marker}")
    for marker in required_wizard:
        if marker not in wizard:
            errors.append(f"wizard missing marker: {marker}")

    allowed = {PAGE.resolve(), EXAMPLES.resolve(), SCRIPT.resolve(), INTEGRATION.resolve(), WIZARD.resolve(), Path(__file__).resolve()}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.resolve() in allowed:
            continue
        if any(part in {".git", "node_modules", "docs"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".html", ".xml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "gp10-workspace.html" in text or "gp10-workspace-examples.html" in text:
            errors.append(f"temporary GP10 pages are linked by {path.relative_to(ROOT)}")

    if errors:
        print(f"FAIL-CLOSED: {len(errors)} GP10 workspace isolation or contract violation(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: guided GP10 workspace and examples page preserve authority boundaries and remain isolated from public Site navigation")
    return 0


if __name__ == "__main__":
    sys.exit(main())