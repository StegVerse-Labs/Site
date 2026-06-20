#!/usr/bin/env python3
"""Validate the public transition discovery surface.

The transition pages must remain root-level public views of the canonical
transition discovery state. This checker catches page drift, missing shared
scripts, missing view declarations, stale milestone claims, and missing
workflow/iOS mirror governance.
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = ROOT / "assets" / "transition-discovery-state.js"
RENDERER_PATH = ROOT / "assets" / "transition-page-renderer.js"
DOC_PATH = ROOT / "docs" / "TRANSITION_DISCOVERY_PUBLIC_SURFACE.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "transition-discovery-public-surface.yml"
IOS_MIRROR_PATH = ROOT / "iosnoperiod" / "github" / "workflows" / "transition-discovery-public-surface.yml"
IOS_MANIFEST_PATH = ROOT / "iosnoperiod" / "manifest.json"

PAGES = {
    "transition-table.html": "table",
    "transition-milestones.html": "milestones",
    "transition-development-status.html": "development-status",
    "transition-release-snapshot.html": "release-snapshot",
    "transition-release-index.html": "release-index",
    "transition-verification-guide.html": "verification-guide",
    "transition-replay-packet.html": "replay-packet",
}

REQUIRED_STATE_TERMS = [
    "STEGVERSE_TRANSITION_DISCOVERY_STATE",
    "research_premise",
    "unlock_rules",
    "partitions",
    "evidence_records",
    "milestones",
    "frontier",
    "snapshots",
    "verification_expectations",
    "replay_packets",
    "MS-012",
    "MS-012F",
    "T13",
    "T14",
    "RECEIPT_BACKED",
]

REQUIRED_DOC_TERMS = [
    "assets/transition-discovery-state.js",
    "assets/transition-page-renderer.js",
    "transition-table.html",
    "transition-milestones.html",
    "transition-development-status.html",
    "transition-release-snapshot.html",
    "transition-release-index.html",
    "transition-verification-guide.html",
    "transition-replay-packet.html",
    "MS-012",
    "MS-012F",
    "T13, T14",
    "docs/SITE_MIRROR_HANDOFF.md",
    "python scripts/check_transition_discovery_public_surface.py",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_terms(label: str, text: str, terms: list[str]) -> None:
    missing = [term for term in terms if term not in text]
    if missing:
        fail(f"{label} missing required terms: {', '.join(missing)}")


def page_declares_view(text: str, expected_view: str) -> bool:
    direct = f'data-transition-view="{expected_view}"' in text or f"data-transition-view='{expected_view}'" in text
    if direct:
        return True
    if expected_view == "release-snapshot":
        return "release-'+'snapshot" in text or 'release-"+"snapshot' in text
    return False


def validate_workflow() -> None:
    workflow = read(WORKFLOW_PATH)
    mirror = read(IOS_MIRROR_PATH)
    if workflow != mirror:
        fail("iosnoperiod workflow mirror must match canonical workflow exactly")
    require_terms(
        "transition discovery workflow",
        workflow,
        [
            "Transition Discovery Public Surface",
            "workflow_dispatch",
            "assets/transition-discovery-state.js",
            "assets/transition-page-renderer.js",
            "scripts/check_transition_discovery_public_surface.py",
            "python scripts/check_transition_discovery_public_surface.py",
        ],
    )
    manifest = json.loads(read(IOS_MANIFEST_PATH))
    entries = manifest.get("authoritative_paths", [])
    expected = {
        "canonical": ".github/workflows/transition-discovery-public-surface.yml",
        "mirror": "iosnoperiod/github/workflows/transition-discovery-public-surface.yml",
    }
    if not any(entry.get("canonical") == expected["canonical"] and entry.get("mirror") == expected["mirror"] for entry in entries):
        fail("iosnoperiod manifest does not map transition discovery workflow canonical/mirror paths")


def main() -> None:
    state = read(STATE_PATH)
    renderer = read(RENDERER_PATH)
    doc = read(DOC_PATH)

    require_terms("canonical discovery state", state, REQUIRED_STATE_TERMS)
    require_terms("public surface doc", doc, REQUIRED_DOC_TERMS)

    if "querySelector(\"[data-transition-view]\")" not in renderer:
        fail("renderer does not locate data-transition-view root")
    if "transition-discovery-renderer-style" not in renderer:
        fail("renderer does not inject shared transition discovery styling")
    for view in PAGES.values():
        if view not in renderer:
            fail(f"renderer missing view key/content for {view}")

    for page, view in PAGES.items():
        text = read(ROOT / page)
        if "assets/transition-discovery-state.js" not in text:
            fail(f"{page} does not load canonical discovery state")
        if "assets/transition-page-renderer.js" not in text:
            fail(f"{page} does not load shared renderer")
        if not page_declares_view(text, view):
            fail(f"{page} does not declare expected view {view}")

    receipt_status_count = len(re.findall(r'status:\s*"RECEIPT_BACKED"', state))
    if receipt_status_count < 2:
        fail("canonical state must keep at least T13/T14 receipt-backed")

    validate_workflow()
    print("transition discovery public surface checks passed")


if __name__ == "__main__":
    main()
