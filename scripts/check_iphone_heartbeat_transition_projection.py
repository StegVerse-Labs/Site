#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "heartbeat-transition" / "index.html"
JS = ROOT / "heartbeat-transition" / "heartbeat-transition.js"
HANDOFF = ROOT / "docs" / "IPHONE_HEARTBEAT_TRANSITION_PROJECTION_MIRROR_HANDOFF.md"

SOURCE_MERGE = "9015c67d8356bf7e9e3db71488b2468581829e7a"
SOURCE_BLOB = "d18d57d83cf19b7799cde1a1b4487e496eca7f76"
CONTRACT_ID = "SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001"
RECEIPT_SCHEMA = "stegverse.iphone-heartbeat-transition-receipt/v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("IPHONE_HEARTBEAT_TRANSITION_PROJECTION_FAIL: " + message)


def main() -> int:
    for path in (HTML, JS, HANDOFF):
        require(path.is_file(), f"missing required surface: {path.relative_to(ROOT)}")

    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    required_html = (
        "StegVerse HB29 → HB30 Transition",
        "Emit HB30 Candidate Receipt",
        "Credential authority",
        "TV/TVC",
        "Second non-StegVerse machine required",
        "Browser receipt authority effect",
        "HB30_CANDIDATE_EMITTED",
        "heartbeat-transition.js",
    )
    for marker in required_html:
        require(marker in html, f"HTML missing marker: {marker}")

    required_js = (
        SOURCE_MERGE,
        SOURCE_BLOB,
        CONTRACT_ID,
        RECEIPT_SCHEMA,
        'physical_execution_surface: "CURRENT_USER_IPHONE"',
        'epoch: 29',
        'generation: 29',
        'epoch: 30',
        'generation: 30',
        'credential_authority: "TV/TVC"',
        'credential_requirement: "NONE"',
        'github_token_runtime_authority: "NONE"',
        'non_tv_tvc_secret_or_token_used: false',
        'worker_authority: false',
        'claim_or_fence_mutation: false',
        'route_authority: false',
        'wallet_authority: false',
        'model_output_authority: "NONE"',
        'another_physical_machine_required: false',
        'location.hostname === "stegverse.org"',
        '/iPhone/i.test',
        'crypto.subtle.digest("SHA-256"',
        'Object.keys(value).sort()',
        'localStorage.setItem(STORAGE_KEY',
        '"HB30_CANDIDATE_EMITTED"',
    )
    for marker in required_js:
        require(marker in js, f"JS missing marker: {marker}")

    forbidden_execution = (
        "fetch(",
        "XMLHttpRequest",
        "WebSocket(",
        "EventSource(",
        "Authorization",
        "Bearer ",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "api.github.com",
        "render.com",
        "vercel.app",
        "workers.dev",
    )
    for marker in forbidden_execution:
        require(marker not in js, f"browser capsule contains prohibited runtime/network marker: {marker}")

    require("canonical(receipt)" in js, "receipt hash is not bound to canonical receipt serialization")
    require("receipt.receipt_sha256 = await sha256Hex" in js, "receipt digest is not emitted from WebCrypto SHA-256")
    require("window.isSecureContext === true" in js, "secure-context gate missing")
    require("state.ready" in js and "button.disabled" in js, "fail-closed readiness gating missing")

    required_handoff = (
        "StegVerse-Labs/.github#209",
        SOURCE_MERGE,
        "Site is transport/materialization only",
        "TV/TVC",
        "CURRENT_USER_IPHONE",
        "physical receipt",
        "WorkerCoordinator",
        "no second non-StegVerse machine",
    )
    for marker in required_handoff:
        require(marker in handoff, f"handoff missing marker: {marker}")

    evidence = {
        "schema": "stegverse.site-iphone-heartbeat-transition-projection-validation/v1",
        "state": "PASS",
        "source_merge": SOURCE_MERGE,
        "legacy_state_git_blob_sha": SOURCE_BLOB,
        "contract_id": CONTRACT_ID,
        "receipt_schema": RECEIPT_SCHEMA,
        "html_sha256": hashlib.sha256(HTML.read_bytes()).hexdigest(),
        "javascript_sha256": hashlib.sha256(JS.read_bytes()).hexdigest(),
        "network_requests_allowed": False,
        "credential_requirement": "NONE",
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "authority_effect": "NONE",
        "physical_transition_proven": False,
        "canonical_hb30_materialized": False,
    }
    print("IPHONE_HEARTBEAT_TRANSITION_PROJECTION_PASS")
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
