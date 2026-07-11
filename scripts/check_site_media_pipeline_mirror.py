#!/usr/bin/env python3
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
    "broadcast-engine",
    "not a live media platform",
    "does not claim live camera use",
    "does not claim live microphone use",
    "public broadcast",
]

# These markers intentionally track the current handoff contract rather than
# legacy prose. The handoff remains the source of truth, while this check
# verifies its preview-only boundary and exact two-workflow declaration.
REQUIRED_HANDOFF_MARKERS = [
    "# Site Mirror Handoff",
    "This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.",
    "Site mode: PREVIEW_ONLY",
    "Workflow target: exactly two operational workflows",
    ".github/workflows/validate.yml",
    ".github/workflows/site-task-runner.yml",
    "Site may draft, classify, visualize, filter, and emit preview candidates.",
    "Site must not execute, mutate repositories, access credentials, grant admissibility or delegation, sign receipts, issue final receipts, admit Master-Records records, or claim reconstruction success.",
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
