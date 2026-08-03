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
EXAMPLES_SCRIPT = ROOT / "assets" / "gp10-examples-adaptive.js"
SECURITY = ROOT / "assets" / "gp10-security.js"
SECURITY_BASELINE = ROOT / "docs" / "GP10_WORKSPACE_SECURITY_BASELINE.md"
MIRROR_HANDOFF = ROOT / "docs" / "GP10_WORKSPACE_MIRROR_HANDOFF.md"


def main() -> int:
    errors = []
    required_files = [
        (PAGE, "gp10-workspace.html"),
        (EXAMPLES, "gp10-workspace-examples.html"),
        (SCRIPT, "assets/gp10-workspace.js"),
        (INTEGRATION, "assets/gp10-evidence-integration.js"),
        (WIZARD, "assets/gp10-workspace-wizard.js"),
        (EXAMPLES_SCRIPT, "assets/gp10-examples-adaptive.js"),
        (SECURITY, "assets/gp10-security.js"),
        (SECURITY_BASELINE, "docs/GP10_WORKSPACE_SECURITY_BASELINE.md"),
        (MIRROR_HANDOFF, "docs/GP10_WORKSPACE_MIRROR_HANDOFF.md"),
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
    examples_script = EXAMPLES_SCRIPT.read_text(encoding="utf-8")
    security = SECURITY.read_text(encoding="utf-8")
    baseline = SECURITY_BASELINE.read_text(encoding="utf-8")
    handoff = MIRROR_HANDOFF.read_text(encoding="utf-8")

    policy_markers = [
        'name="referrer" content="no-referrer"',
        'http-equiv="Content-Security-Policy"',
        "script-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        'assets/gp10-security.js',
    ]
    required_page = [
        'name="robots" content="noindex,nofollow,noarchive"',
        'assets/gp10-workspace.js',
        'assets/gp10-evidence-integration.js',
        'assets/gp10-workspace-wizard.js',
        'gp10-workspace-examples.html',
        'No execution authority',
        'data-gp10-step',
        *policy_markers,
    ]
    required_examples = [
        'name="robots" content="noindex,nofollow,noarchive"',
        'gp10-workspace.html',
        'assets/gp10-examples-adaptive.js',
        'What the fields mean',
        'DISCOVERY_ONLY', 'COST_PLUS', 'RE_SCOPE', 'REJECT', 'PROCEED',
        'No execution authority',
        *policy_markers,
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
    required_wizard = [
        "data-gp10-step", "data-next-step", "data-prev-step", "activePath()",
        "hasEvidence", "hasEconomics", "hasThresholdProfile", "hardStop()",
        "Commercial-detail steps skipped", "gp10.workspace.guided.draft.v1",
    ]
    required_examples_script = [
        "How the guided pages narrow the search", "very little is known",
        "uncertain but potentially workable", "a hard stop is already known",
        "Hard stop present",
    ]
    required_security = [
        "IDLE_LIMIT_MS", "HIDDEN_LIMIT_MS", "crypto.subtle.digest", "SHA-256",
        "BROWSER_LOCAL_UNCUSTODIED", "execution_authority: false",
        "GP10_BROWSER_INTEGRITY_RECEIPT", "clearFileInputs", "clearGp10Data",
        "does_not_prove", "pagehide", "visibilitychange",
    ]
    required_baseline = [
        "Applicable federal cybersecurity requirements are the minimum floor",
        "NIST SP 800-53 Revision 5", "CISA Secure by Design",
        "Known static-host limitations", "Required migration controls",
    ]
    required_handoff = [
        "GP10-SITE-SECURE-GUIDED-WORKSPACE-001",
        "CLAIMED_FOR_IMPLEMENTATION", "StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md",
        "one logical decision at a time", "federal cybersecurity requirements",
    ]

    checks = [
        (page, required_page, "page"),
        (examples, required_examples, "examples page"),
        (script, required_script, "workspace script"),
        (integration, required_integration, "evidence integration"),
        (wizard, required_wizard, "wizard"),
        (examples_script, required_examples_script, "examples script"),
        (security, required_security, "security script"),
        (baseline, required_baseline, "security baseline"),
        (handoff, required_handoff, "mirror handoff"),
    ]
    for text, markers, label in checks:
        for marker in markers:
            if marker not in text:
                errors.append(f"{label} missing marker: {marker}")

    allowed = {
        PAGE.resolve(), EXAMPLES.resolve(), SCRIPT.resolve(), INTEGRATION.resolve(),
        WIZARD.resolve(), EXAMPLES_SCRIPT.resolve(), SECURITY.resolve(),
        SECURITY_BASELINE.resolve(), MIRROR_HANDOFF.resolve(), Path(__file__).resolve()
    }
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
        print(f"FAIL-CLOSED: {len(errors)} GP10 workspace isolation, security, or contract violation(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: adaptive GP10 workspace preserves logical narrowing, authority boundaries, browser security controls, and public-navigation isolation")
    return 0


if __name__ == "__main__":
    sys.exit(main())