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

# Validate current durable Site handoff obligations rather than retired workflow counts.
REQUIRED_HANDOFF_MARKERS = [
    "# Site Mirror Handoff",
    "This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.",
    "Goal: fully functional governed Ecosystem Chat request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, and downstream propagation path",
    "Result: ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION",
    ".github/workflows/validate.yml",
    ".github/workflows/ecosystem-chat-activation-retention.yml",
    "Site display != execution",
    "usage retrieval != authority",
    "imported verified receipt != deployment authority",
    "provider-usage custody RECORDED",
    "No tag or release is authorized.",
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


def main():
    failed = False
    failed |= check(PAGE, REQUIRED_PAGE_MARKERS)
    failed |= check(HANDOFF, REQUIRED_HANDOFF_MARKERS)
    if failed:
        return 1
    print("PASS site media pipeline mirror")
    return 0


if __name__ == "__main__":
    sys.exit(main())
