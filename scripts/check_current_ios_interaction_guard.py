#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-bootstrap" / "index.html"
GUARD = ROOT / "stegos-bootstrap" / "current-ios-interaction-guard.js"
MANIFEST = ROOT / "stegos-bootstrap" / "current-ios-interaction-manifest.json"

MUTATIONS = [
    "establish", "activate-chat", "admit-evidence", "run-inference",
    "run-de006-inference", "run-sv001", "commit-mr-sv001"
]
READ_ONLY = ["replay", "evidence", "copy-evidence"]


def fail(reason: str) -> None:
    raise SystemExit("CURRENT_IOS_INTERACTION_GUARD_FAIL: " + reason)


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    guard = GUARD.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("schema") != "stegverse.site-current-ios-interaction-manifest/v1": fail("manifest schema")
    if manifest.get("state") != "HOLD_UI_ORCHESTRATION_CONFLICT": fail("source must remain HOLD")
    if manifest.get("active_action_id") is not None or manifest.get("enabled_mutation_control_id") is not None: fail("HOLD exposes mutation")
    if manifest.get("authority_effect") != "NONE_UI_SERIALIZATION_ONLY": fail("authority effect")
    if manifest.get("credential_authority") != "TV/TVC" or manifest.get("github_token_runtime_authority") != "NONE": fail("credential boundary")

    if '<script src="./current-ios-interaction-guard.js"></script>' not in html: fail("bootstrap does not load guard")
    if 'id="interaction-guard-state"' not in html or 'id="interaction-guard-action"' not in html: fail("coordinator panel missing")

    for control in MUTATIONS:
        needle = f'id="{control}"'
        pos = html.find(needle)
        if pos < 0: fail("missing mutation control " + control)
        tag_start = html.rfind("<button", 0, pos)
        tag_end = html.find(">", pos)
        tag = html[tag_start:tag_end + 1]
        if " disabled" not in tag: fail("mutation control not default-disabled: " + control)
        if control not in guard: fail("guard does not enumerate mutation control: " + control)

    for field in ["canonical-evidence", "inference-prompt", "mr-sv001-receipt"]:
        pos = html.find(f'id="{field}"')
        if pos < 0: fail("missing mutation input " + field)
        tag_start = html.rfind("<textarea", 0, pos)
        tag_end = html.find(">", pos)
        if " readonly" not in html[tag_start:tag_end + 1]: fail("mutation input not default-readonly: " + field)
        if field not in guard: fail("guard does not bind mutation input: " + field)

    for control in READ_ONLY:
        if f'id="{control}"' not in html: fail("missing read-only control " + control)
        if control not in guard: fail("guard does not enumerate read-only control " + control)

    required_guard_fragments = [
        'manifest.state !== "ADMITTED_SINGLE_ACTION"',
        "consumedActionId",
        "stopImmediatePropagation",
        "MutationObserver",
        "failClosed",
        'credential_authority !== "TV/TVC"',
        'github_token_runtime_authority !== "NONE"',
        'interaction_guard_ts=',
        'cache: "no-store"',
        'service-worker.js?current_ios_guard=991',
        'refreshGuardedWorker',
    ]
    for fragment in required_guard_fragments:
        if fragment not in guard: fail("guard invariant missing: " + fragment)

    print("CURRENT_IOS_INTERACTION_GUARD_PASS")
    print("state=HOLD_UI_ORCHESTRATION_CONFLICT")
    print("mutation_controls=7 default_disabled=true")
    print("mutation_inputs=3 default_readonly=true")
    print("read_only_controls=3")
    print("manifest_cache_bypass=true")
    print("guarded_service_worker_refresh=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
