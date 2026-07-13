#!/usr/bin/env python3
"""Validate the fail-closed activation evidence ledger for live usage retrieval."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "usage-endpoint-activation-evidence.json"
CONFIG = ROOT / "data" / "ecosystem-usage-config.json"


def fail(message: str) -> None:
    raise SystemExit(f"USAGE_ENDPOINT_ACTIVATION_EVIDENCE_FAIL: {message}")


def main() -> int:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))

    if ledger.get("schema") != "stegverse.site.usage_endpoint_activation_evidence.v1":
        fail("schema drift")

    requirements = ledger.get("requirements", {})
    required_keys = {
        "destination_handoff_authority",
        "destination_endpoint_tests",
        "same_origin_authenticated_deployment",
        "sample_response_conformance",
        "retrieval_receipt_validation",
        "no_browser_secret_surface",
        "site_current_main_validation",
        "master_records_custody",
        "reconstructability",
    }
    if set(requirements) != required_keys:
        fail("requirement set drift")

    allowed_statuses = {"MISSING", "UNOBSERVED", "PREPARED_NOT_OBSERVED", "VERIFIED"}
    for name, entry in requirements.items():
        if not isinstance(entry, dict):
            fail(f"invalid requirement entry: {name}")
        if entry.get("status") not in allowed_statuses:
            fail(f"invalid requirement status: {name}")
        if entry.get("status") == "VERIFIED" and not entry.get("evidence_ref"):
            fail(f"verified requirement missing evidence: {name}")

    activation = ledger.get("activation_rule", {})
    if activation.get("ready_state") != "READY_TO_ENABLE":
        fail("ready state drift")
    if activation.get("all_requirements_must_equal") != "VERIFIED":
        fail("all-requirements rule drift")
    for key in (
        "site_may_set_usage_api_base_before_ready",
        "site_may_enable_live_transport_before_ready",
        "site_may_claim_live_before_ready",
        "site_may_claim_recorded_before_custody_and_reconstructability",
    ):
        if activation.get(key) is not False:
            fail(f"activation boundary weakened: {key}")

    all_verified = all(entry.get("status") == "VERIFIED" for entry in requirements.values())
    expected_state = "READY_TO_ENABLE" if all_verified else "BLOCKED"
    if ledger.get("state") != expected_state:
        fail(f"state must be {expected_state}")

    live = config.get("live_transport", {})
    if expected_state != "READY_TO_ENABLE":
        if live.get("enabled") is not False:
            fail("live transport enabled while activation evidence is blocked")
        if config.get("usage_api_base") is not None:
            fail("usage_api_base configured while activation evidence is blocked")

    boundaries = ledger.get("authority_boundaries", {})
    if any(value is not False for value in boundaries.values()):
        fail("evidence ledger claims authority")

    blockers = ledger.get("current_blockers", [])
    if expected_state == "BLOCKED" and not blockers:
        fail("blocked state requires explicit blockers")
    if expected_state == "READY_TO_ENABLE" and blockers:
        fail("ready state may not retain blockers")

    custody = requirements["master_records_custody"].get("status")
    reconstructability = requirements["reconstructability"].get("status")
    if (custody == "VERIFIED") != (reconstructability == "VERIFIED"):
        fail("custody and reconstructability must advance together")

    print(f"USAGE_ENDPOINT_ACTIVATION_EVIDENCE_PASS: {expected_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
