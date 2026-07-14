#!/usr/bin/env python3
"""Validate the Site activation ledger without granting activation authority."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "SITE_ACTIVATION_LEDGER.json"

EXPECTED_GATES = {
    "site_same_run_artifact_set",
    "llm_adapter_current_main_validation",
    "sdk_current_main_validation",
    "same_origin_authenticated_deployment",
    "live_endpoint_conformance",
    "master_records_authenticated_custody",
    "reconstructability",
}


def fail(message: str) -> None:
    raise SystemExit(f"site_activation_ledger_invalid:{message}")


def main() -> None:
    if not LEDGER.exists():
        fail("missing_ledger")

    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(type(exc).__name__)

    if data.get("schema") != "stegverse.site.activation-ledger.v1":
        fail("schema")
    if data.get("checkpoint") != "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED":
        fail("checkpoint")
    if data.get("contract_status") != "PREPARED_NOT_DEPLOYED":
        fail("contract_status")
    if data.get("activation_status") != "BLOCKED":
        fail("activation_status")

    for field in (
        "live_transport_enabled",
        "authority_granted",
        "custody_recorded",
        "release_authorized",
    ):
        if data.get(field) is not False:
            fail(f"{field}_must_be_false")

    gates = data.get("gates")
    if not isinstance(gates, dict):
        fail("gates_not_object")
    if set(gates) != EXPECTED_GATES:
        fail("gate_inventory")

    for name, gate in gates.items():
        if not isinstance(gate, dict):
            fail(f"{name}_not_object")
        if gate.get("status") not in {"NOT_OBSERVED", "VERIFIED"}:
            fail(f"{name}_invalid_status")

    if gates["site_same_run_artifact_set"].get("same_run_required") is not True:
        fail("same_run_requirement")
    if gates["same_origin_authenticated_deployment"].get("usage_api_base") is not None:
        fail("usage_api_base_must_remain_null")
    if gates["same_origin_authenticated_deployment"].get("browser_secret_surface_allowed") is not False:
        fail("browser_secret_surface")
    if gates["master_records_authenticated_custody"].get("local_persistence_is_custody") is not False:
        fail("local_persistence_custody_boundary")
    if gates["reconstructability"].get("required_result") != "PASS":
        fail("reconstructability_requirement")

    all_verified = all(gate["status"] == "VERIFIED" for gate in gates.values())
    if all_verified:
        fail("all_gates_verified_requires_separate_authorized_transition")

    print("site_activation_ledger:PASS_BLOCKED")


if __name__ == "__main__":
    main()
