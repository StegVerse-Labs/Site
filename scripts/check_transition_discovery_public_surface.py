#!/usr/bin/env python3
"""Validate the governed transition discovery public surface."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "js_state": ROOT / "assets" / "transition-discovery-state.js",
    "json_state": ROOT / "data" / "transition-discovery-state-v1.json",
    "page_contract": ROOT / "data" / "transition-page-contract-v1.json",
    "receipt": ROOT / "data" / "transition-discovery-receipt-v1.json",
    "machine_status": ROOT / "data" / "transition-discovery-status-v1.json",
    "renderer": ROOT / "assets" / "transition-page-renderer.js",
    "public_doc": ROOT / "docs" / "TRANSITION_DISCOVERY_PUBLIC_SURFACE.md",
    "receipt_doc": ROOT / "docs" / "TRANSITION_DISCOVERY_RECEIPT.md",
    "status_doc": ROOT / "docs" / "TRANSITION_DISCOVERY_STATUS.md",
    "workflow": ROOT / ".github" / "workflows" / "transition-discovery-public-surface.yml",
    "ios_workflow": ROOT / "iosnoperiod" / "github" / "workflows" / "transition-discovery-public-surface.yml",
    "ios_manifest": ROOT / "iosnoperiod" / "manifest.json",
}

PAGES = {
    "transition-table.html": "table",
    "transition-milestones.html": "milestones",
    "transition-development-status.html": "development-status",
    "transition-release-snapshot.html": "release-snapshot",
    "transition-release-index.html": "release-index",
    "transition-verification-guide.html": "verification-guide",
    "transition-replay-packet.html": "replay-packet",
}

EXPECTED_RELEASE = "MS-012"
EXPECTED_FRONTIER = "MS-012F"
EXPECTED_RECEIPT_PARTITIONS = ["T13", "T14"]
EXPECTED_BOUNDARY = "pending_publisher_closure_evidence"
VALIDATION_COMMAND = "python scripts/check_transition_discovery_public_surface.py"
EXPECTED_RESULT = "transition discovery public surface checks passed"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read(path))


def require_terms(label: str, text: str, terms: list[str]) -> None:
    missing = [term for term in terms if term not in text]
    if missing:
        fail(f"{label} missing required terms: {', '.join(missing)}")


def page_declares_view(text: str, view: str) -> bool:
    if f'data-transition-view="{view}"' in text or f"data-transition-view='{view}'" in text:
        return True
    return view == "release-snapshot" and ("release-'+'snapshot" in text or 'release-"+"snapshot' in text)


def validate_release_block(label: str, data: dict) -> None:
    if data.get("current_release") != EXPECTED_RELEASE:
        fail(f"{label} current_release must be {EXPECTED_RELEASE}")
    if data.get("current_frontier") != EXPECTED_FRONTIER:
        fail(f"{label} current_frontier must be {EXPECTED_FRONTIER}")
    if data.get("receipt_backed_partitions") != EXPECTED_RECEIPT_PARTITIONS:
        fail(f"{label} receipt_backed_partitions must be T13/T14")
    if data.get("site_mirror_activation") != EXPECTED_BOUNDARY:
        fail(f"{label} must preserve pending Publisher closure boundary")


def validate_json_state(js_state: str) -> None:
    data = load_json(FILES["json_state"])
    if data.get("schema") != "stegverse.transition_discovery_state.v1":
        fail("JSON discovery state has wrong schema")
    validate_release_block("JSON discovery state", data)
    ids = {partition.get("id"): partition for partition in data.get("partitions", [])}
    if len(ids) < 16:
        fail("JSON discovery state must list all 16 current transition partitions")
    for partition_id in EXPECTED_RECEIPT_PARTITIONS:
        if ids.get(partition_id, {}).get("status") != "RECEIPT_BACKED":
            fail(f"JSON discovery state must keep {partition_id} receipt-backed")
        if f'id: "{partition_id}"' not in js_state and f'id":"{partition_id}"' not in js_state:
            fail(f"canonical JS state missing {partition_id}")
    boundary = data.get("boundary", {})
    if boundary.get("site_mirror_activation") != EXPECTED_BOUNDARY:
        fail("JSON boundary must preserve pending Publisher closure boundary")


def validate_page_contract() -> None:
    contract = load_json(FILES["page_contract"])
    if contract.get("schema") != "stegverse.transition_page_contract.v1":
        fail("page contract has wrong schema")
    validate_release_block("page contract", contract.get("release_expectations", {}))
    pages = {entry.get("path"): entry for entry in contract.get("pages", [])}
    if set(pages) != set(PAGES):
        fail("page contract must list exactly the seven transition pages")
    for path, view in PAGES.items():
        entry = pages[path]
        if entry.get("view") != view:
            fail(f"page contract view mismatch for {path}")
        if "assets/transition-discovery-state.js" not in entry.get("must_load", []):
            fail(f"page contract missing JS state load for {path}")
        if "assets/transition-page-renderer.js" not in entry.get("must_load", []):
            fail(f"page contract missing renderer load for {path}")
        if "data/transition-discovery-state-v1.json" not in entry.get("must_expose", []):
            fail(f"page contract missing JSON exposure for {path}")
    if contract.get("workflow_contract", {}).get("required_command") != VALIDATION_COMMAND:
        fail("page contract workflow required_command mismatch")


def validate_receipt() -> None:
    receipt = load_json(FILES["receipt"])
    if receipt.get("schema") != "stegverse.transition_discovery_receipt.v1":
        fail("receipt has wrong schema")
    validate_release_block("receipt", receipt.get("state", {}))
    artifacts = receipt.get("artifacts", {})
    for key in [
        "browser_state", "machine_state", "page_contract", "receipt", "machine_status",
        "receipt_doc", "status_doc", "renderer", "validator", "documentation",
        "workflow", "ios_workflow_mirror", "ios_manifest",
    ]:
        if not artifacts.get(key):
            fail(f"receipt missing artifact pointer: {key}")
    if artifacts.get("machine_status") != "data/transition-discovery-status-v1.json":
        fail("receipt machine_status artifact mismatch")
    if artifacts.get("status_doc") != "docs/TRANSITION_DISCOVERY_STATUS.md":
        fail("receipt status_doc artifact mismatch")
    if set(receipt.get("public_pages", [])) != set(PAGES):
        fail("receipt must list exactly the seven transition pages")
    validation = receipt.get("validation", {})
    if validation.get("command") != VALIDATION_COMMAND:
        fail("receipt validation command mismatch")
    for check in ["machine-readable status exists", "status handoff exists", "Publisher closure boundary remains pending"]:
        if check not in validation.get("checks", []):
            fail(f"receipt validation checks missing: {check}")


def validate_machine_status() -> None:
    status = load_json(FILES["machine_status"])
    if status.get("schema") != "stegverse.transition_discovery_status.v1":
        fail("machine status has wrong schema")
    validate_release_block("machine status", status)
    if status.get("status") != "public_surface_governed":
        fail("machine status must be public_surface_governed")
    blocked = status.get("blocked", [])
    if not blocked or blocked[0].get("item") != "Publisher-to-Site mirror activation":
        fail("machine status must identify Publisher-to-Site mirror activation as blocked")
    if "docs/SITE_MIRROR_HANDOFF.md" not in blocked[0].get("unlock_condition", ""):
        fail("machine status unlock condition must reference Site mirror handoff")
    if status.get("validation", {}).get("command") != VALIDATION_COMMAND:
        fail("machine status validation command mismatch")


def validate_docs() -> None:
    public_doc = read(FILES["public_doc"])
    receipt_doc = read(FILES["receipt_doc"])
    status_doc = read(FILES["status_doc"])
    require_terms("public surface doc", public_doc, [
        "data/transition-discovery-state-v1.json",
        "data/transition-page-contract-v1.json",
        "data/transition-discovery-receipt-v1.json",
        "data/transition-discovery-status-v1.json",
        "docs/TRANSITION_DISCOVERY_RECEIPT.md",
        "docs/TRANSITION_DISCOVERY_STATUS.md",
        "status handoff identifies Publisher closure evidence as the only mirror-activation blocker",
        "docs/SITE_MIRROR_HANDOFF.md",
        VALIDATION_COMMAND,
    ])
    require_terms("receipt doc", receipt_doc, [
        "Transition Discovery Receipt",
        "data/transition-discovery-receipt-v1.json",
        EXPECTED_RELEASE,
        EXPECTED_FRONTIER,
        "T13, T14",
        "ALLOW",
        EXPECTED_BOUNDARY,
        VALIDATION_COMMAND,
        EXPECTED_RESULT,
        "does not activate the Publisher-to-Site mirror",
    ])
    require_terms("status doc", status_doc, [
        "Transition Discovery Status",
        "status: public_surface_governed",
        f"current_release: {EXPECTED_RELEASE}",
        f"current_frontier: {EXPECTED_FRONTIER}",
        "receipt_backed_partitions: T13, T14",
        f"site_mirror_activation: {EXPECTED_BOUNDARY}",
        "Publisher closure evidence has not been provided to Site.",
        "Provide governed Publisher closure evidence satisfying docs/SITE_MIRROR_HANDOFF.md.",
        "It must not claim Publisher-to-Site mirror activation.",
        VALIDATION_COMMAND,
        EXPECTED_RESULT,
    ])


def validate_workflow() -> None:
    workflow = read(FILES["workflow"])
    mirror = read(FILES["ios_workflow"])
    if workflow != mirror:
        fail("iosnoperiod workflow mirror must match canonical workflow exactly")
    require_terms("transition discovery workflow", workflow, [
        "Transition Discovery Public Surface",
        "workflow_dispatch",
        "assets/transition-discovery-state.js",
        "assets/transition-page-renderer.js",
        "data/transition-discovery-state-v1.json",
        "data/transition-page-contract-v1.json",
        "data/transition-discovery-receipt-v1.json",
        "data/transition-discovery-status-v1.json",
        "docs/TRANSITION_DISCOVERY_RECEIPT.md",
        "docs/TRANSITION_DISCOVERY_STATUS.md",
        VALIDATION_COMMAND,
    ])
    manifest = load_json(FILES["ios_manifest"])
    if not any(
        entry.get("canonical") == ".github/workflows/transition-discovery-public-surface.yml"
        and entry.get("mirror") == "iosnoperiod/github/workflows/transition-discovery-public-surface.yml"
        for entry in manifest.get("authoritative_paths", [])
    ):
        fail("iosnoperiod manifest does not map transition discovery workflow canonical/mirror paths")


def main() -> None:
    js_state = read(FILES["js_state"])
    renderer = read(FILES["renderer"])

    require_terms("canonical discovery state", js_state, [
        "STEGVERSE_TRANSITION_DISCOVERY_STATE", "research_premise", "unlock_rules",
        "partitions", "evidence_records", "milestones", "frontier", "snapshots",
        "verification_expectations", "replay_packets", EXPECTED_RELEASE, EXPECTED_FRONTIER,
        "T13", "T14", "RECEIPT_BACKED",
    ])
    validate_json_state(js_state)
    validate_page_contract()
    validate_receipt()
    validate_machine_status()
    validate_docs()

    require_terms("transition renderer", renderer, [
        "querySelector(\"[data-transition-view]\")",
        "transition-discovery-renderer-style",
        "data/transition-discovery-state-v1.json",
        "Open machine-readable discovery state JSON",
        "Machine-readable discovery state JSON",
        "Machine-readable mirror",
    ])
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

    if len(re.findall(r'status:\s*"RECEIPT_BACKED"', js_state)) < 2:
        fail("canonical state must keep at least T13/T14 receipt-backed")

    validate_workflow()
    print(EXPECTED_RESULT)


if __name__ == "__main__":
    main()
