#!/usr/bin/env python3
"""Validate the public transition discovery surface.

The transition pages must remain root-level public views of the canonical
transition discovery state. This checker catches page drift, missing shared
scripts, missing view declarations, stale milestone claims, missing JSON state,
missing page contract state, missing receipt state, missing receipt documentation,
missing status handoff, missing renderer JSON links, and missing workflow/iOS
mirror governance.
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = ROOT / "assets" / "transition-discovery-state.js"
JSON_STATE_PATH = ROOT / "data" / "transition-discovery-state-v1.json"
PAGE_CONTRACT_PATH = ROOT / "data" / "transition-page-contract-v1.json"
RECEIPT_PATH = ROOT / "data" / "transition-discovery-receipt-v1.json"
RECEIPT_DOC_PATH = ROOT / "docs" / "TRANSITION_DISCOVERY_RECEIPT.md"
STATUS_DOC_PATH = ROOT / "docs" / "TRANSITION_DISCOVERY_STATUS.md"
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
    "data/transition-discovery-state-v1.json",
    "data/transition-page-contract-v1.json",
    "data/transition-discovery-receipt-v1.json",
    "docs/TRANSITION_DISCOVERY_RECEIPT.md",
    "docs/TRANSITION_DISCOVERY_STATUS.md",
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

REQUIRED_RECEIPT_DOC_TERMS = [
    "Transition Discovery Receipt",
    "data/transition-discovery-receipt-v1.json",
    "MS-012",
    "MS-012F",
    "T13, T14",
    "ALLOW",
    "pending_publisher_closure_evidence",
    "python scripts/check_transition_discovery_public_surface.py",
    "transition discovery public surface checks passed",
    "docs/SITE_MIRROR_HANDOFF.md",
    "does not activate the Publisher-to-Site mirror",
]

REQUIRED_STATUS_DOC_TERMS = [
    "Transition Discovery Status",
    "status: public_surface_governed",
    "current_release: MS-012",
    "current_frontier: MS-012F",
    "receipt_backed_partitions: T13, T14",
    "site_mirror_activation: pending_publisher_closure_evidence",
    "Publisher-to-Site mirror activation",
    "Publisher closure evidence has not been provided to Site.",
    "Provide governed Publisher closure evidence satisfying docs/SITE_MIRROR_HANDOFF.md.",
    "It must not claim Publisher-to-Site mirror activation.",
    "python scripts/check_transition_discovery_public_surface.py",
    "transition discovery public surface checks passed",
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


def validate_json_state(state_text: str) -> None:
    data = json.loads(read(JSON_STATE_PATH))
    if data.get("schema") != "stegverse.transition_discovery_state.v1":
        fail("JSON discovery state has wrong schema")
    if data.get("current_release") != "MS-012":
        fail("JSON discovery state current_release must be MS-012")
    if data.get("current_frontier") != "MS-012F":
        fail("JSON discovery state current_frontier must be MS-012F")
    if data.get("receipt_backed_partitions") != ["T13", "T14"]:
        fail("JSON discovery state receipt_backed_partitions must be T13/T14")
    ids = {partition.get("id"): partition for partition in data.get("partitions", [])}
    if len(ids) < 16:
        fail("JSON discovery state must list all 16 current transition partitions")
    for partition_id in ["T13", "T14"]:
        if ids.get(partition_id, {}).get("status") != "RECEIPT_BACKED":
            fail(f"JSON discovery state must keep {partition_id} receipt-backed")
        if f'id: "{partition_id}"' not in state_text and f'id":"{partition_id}"' not in state_text:
            fail(f"canonical JS state missing {partition_id}")
    if data.get("boundary", {}).get("site_mirror_activation") != "pending_publisher_closure_evidence":
        fail("JSON discovery state must preserve pending Publisher closure boundary")


def validate_page_contract() -> None:
    contract = json.loads(read(PAGE_CONTRACT_PATH))
    if contract.get("schema") != "stegverse.transition_page_contract.v1":
        fail("transition page contract has wrong schema")
    expectations = contract.get("release_expectations", {})
    if expectations.get("current_release") != "MS-012":
        fail("page contract current_release must be MS-012")
    if expectations.get("current_frontier") != "MS-012F":
        fail("page contract current_frontier must be MS-012F")
    if expectations.get("receipt_backed_partitions") != ["T13", "T14"]:
        fail("page contract receipt_backed_partitions must be T13/T14")
    if expectations.get("site_mirror_activation") != "pending_publisher_closure_evidence":
        fail("page contract must preserve pending Publisher closure boundary")
    pages = {entry.get("path"): entry for entry in contract.get("pages", [])}
    if set(pages) != set(PAGES):
        fail("page contract must list exactly the seven transition pages")
    for path, view in PAGES.items():
        entry = pages[path]
        if entry.get("view") != view:
            fail(f"page contract view mismatch for {path}")
        must_load = entry.get("must_load", [])
        if "assets/transition-discovery-state.js" not in must_load or "assets/transition-page-renderer.js" not in must_load:
            fail(f"page contract missing shared loads for {path}")
        if "data/transition-discovery-state-v1.json" not in entry.get("must_expose", []):
            fail(f"page contract missing JSON exposure for {path}")
    workflow_contract = contract.get("workflow_contract", {})
    if workflow_contract.get("required_command") != "python scripts/check_transition_discovery_public_surface.py":
        fail("page contract workflow required_command mismatch")


def validate_receipt() -> None:
    receipt = json.loads(read(RECEIPT_PATH))
    if receipt.get("schema") != "stegverse.transition_discovery_receipt.v1":
        fail("transition discovery receipt has wrong schema")
    state = receipt.get("state", {})
    if state.get("current_release") != "MS-012" or state.get("current_frontier") != "MS-012F":
        fail("receipt must preserve MS-012/MS-012F")
    if state.get("receipt_backed_partitions") != ["T13", "T14"]:
        fail("receipt must preserve T13/T14 receipt-backed partitions")
    if state.get("site_mirror_activation") != "pending_publisher_closure_evidence":
        fail("receipt must preserve pending Publisher closure boundary")
    artifacts = receipt.get("artifacts", {})
    required_artifacts = [
        "browser_state",
        "machine_state",
        "page_contract",
        "receipt",
        "receipt_doc",
        "status_doc",
        "renderer",
        "validator",
        "documentation",
        "workflow",
        "ios_workflow_mirror",
        "ios_manifest",
    ]
    for key in required_artifacts:
        if not artifacts.get(key):
            fail(f"receipt missing artifact pointer: {key}")
    if artifacts.get("receipt_doc") != "docs/TRANSITION_DISCOVERY_RECEIPT.md":
        fail("receipt_doc artifact must point to docs/TRANSITION_DISCOVERY_RECEIPT.md")
    if artifacts.get("status_doc") != "docs/TRANSITION_DISCOVERY_STATUS.md":
        fail("status_doc artifact must point to docs/TRANSITION_DISCOVERY_STATUS.md")
    if set(receipt.get("public_pages", [])) != set(PAGES):
        fail("receipt must list exactly the seven transition pages")
    validation = receipt.get("validation", {})
    if validation.get("command") != "python scripts/check_transition_discovery_public_surface.py":
        fail("receipt validation command mismatch")
    if "human-readable receipt exists" not in validation.get("checks", []):
        fail("receipt validation checks must require human-readable receipt")
    if "status handoff exists" not in validation.get("checks", []):
        fail("receipt validation checks must require status handoff")
    if "Publisher closure boundary remains pending" not in validation.get("checks", []):
        fail("receipt validation checks must preserve Publisher closure boundary")


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
            "data/transition-discovery-state-v1.json",
            "data/transition-page-contract-v1.json",
            "data/transition-discovery-receipt-v1.json",
            "docs/TRANSITION_DISCOVERY_RECEIPT.md",
            "docs/TRANSITION_DISCOVERY_STATUS.md",
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
    receipt_doc = read(RECEIPT_DOC_PATH)
    status_doc = read(STATUS_DOC_PATH)

    require_terms("canonical discovery state", state, REQUIRED_STATE_TERMS)
    require_terms("public surface doc", doc, REQUIRED_DOC_TERMS)
    require_terms("human-readable receipt doc", receipt_doc, REQUIRED_RECEIPT_DOC_TERMS)
    require_terms("transition status handoff", status_doc, REQUIRED_STATUS_DOC_TERMS)
    validate_json_state(state)
    validate_page_contract()
    validate_receipt()

    if "querySelector(\"[data-transition-view]\")" not in renderer:
        fail("renderer does not locate data-transition-view root")
    if "transition-discovery-renderer-style" not in renderer:
        fail("renderer does not inject shared transition discovery styling")
    require_terms(
        "transition renderer",
        renderer,
        [
            "data/transition-discovery-state-v1.json",
            "Open machine-readable discovery state JSON",
            "Machine-readable discovery state JSON",
            "Machine-readable mirror",
        ],
    )
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
