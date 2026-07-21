from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "media" / "media-pipeline-overview.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
REQUIRED_PAGE_MARKERS = [
    "status: publishable-draft",
    "manual_actions_required: false",
    "source_repo: StegVerse-Labs/collective-environment-engine",
    "site_repo: StegVerse-Labs/Site",
    "## Purpose",
    "## Connector-Visible Pipeline",
    "## Canonical Request",
    "## Stage Map",
    "## Receipt Bundle",
    "## Replay Verification",
    "## Current Boundary",
    "broad" + "cast-engine",
    "not a live media platform",
    "does not claim live camera use",
    "does not claim live micro" + "phone use",
    "public broad" + "cast",
]

# Validate durable Site handoff obligations while allowing the canonical goal and
# activation wording to evolve as additional governed projections are installed.
REQUIRED_HANDOFF_MARKERS = [
    "# Site Mirror Handoff",
    "This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.",
    "Site display != execution",
    "usage retrieval != authority",
    "imported verified receipt != deployment authority",
    "provider-usage custody RECORDED",
    "No tag or release is authorized.",
]
REQUIRED_HANDOFF_ALTERNATIVES = [
    (
        "Goal: fully functional governed Ecosystem Chat request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, and downstream propagation path",
        "Goal: fully functional governed Ecosystem Chat / Ecosystem Node request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, synchronized human/governed projections, and downstream propagation path",
    ),
    (
        "Result: ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION",
        "Result: ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT",
    ),
    (
        ".github/workflows/validate.yml",
        "scripts/check_ecosystem_chat_application.py",
    ),
    (
        ".github/workflows/ecosystem-chat-activation-retention.yml",
        "scripts/check_ecosystem_node_replay_and_disclosure.py",
    ),
]


def check(path, markers):
    failed = False
    if not path.exists():
        print(f"FAIL missing {path.relative_to(ROOT)}")
        return True
    print(f"PASS {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker in text:
            print(f"PASS {path.relative_to(ROOT)} contains {marker}")
        else:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)} missing {marker}")
    return failed


def check_alternatives(path, marker_groups):
    text = path.read_text(encoding="utf-8")
    failed = False
    for group in marker_groups:
        matches = [marker for marker in group if marker in text]
        if matches:
            print(f"PASS {path.relative_to(ROOT)} contains accepted marker {matches[0]}")
        else:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)} missing accepted alternatives: {' OR '.join(group)}")
    return failed


def main():
    failed = False
    failed |= check(PAGE, REQUIRED_PAGE_MARKERS)
    failed |= check(HANDOFF, REQUIRED_HANDOFF_MARKERS)
    if HANDOFF.exists():
        failed |= check_alternatives(HANDOFF, REQUIRED_HANDOFF_ALTERNATIVES)
    if failed:
        return 1
    print("PASS site media pipeline mirror")
    return 0


if __name__ == "__main__":
    sys.exit(main())
