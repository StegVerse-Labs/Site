#!/usr/bin/env python3
"""Validate the Site-to-LLM-adapter authenticated usage endpoint handoff."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "llm-adapter-usage-endpoint-handoff.json"


def fail(message: str) -> None:
    raise SystemExit(f"LLM_ADAPTER_USAGE_HANDOFF_FAIL: {message}")


def main() -> int:
    packet = json.loads(PATH.read_text(encoding="utf-8"))

    if packet.get("schema") != "stegverse.site.llm_adapter_usage_endpoint_handoff.v1":
        fail("schema drift")
    if packet.get("source_repository") != "StegVerse-Labs/Site":
        fail("source repository drift")
    if packet.get("destination_repository") != "StegVerse-org/LLM-adapter":
        fail("destination repository drift")
    if packet.get("state") != "AWAITING_DESTINATION_HANDOFF_AUTHORITY":
        fail("handoff must remain blocked until destination authority exists")

    route = packet.get("route_contract", {})
    expected_route = {
        "method": "GET",
        "path_template": "/api/usage/sessions/{session_id}",
        "request_authentication": "same_origin_session",
        "cache": "no-store",
        "response_schema": "stegverse.usage.session.v1",
        "source_class": "LIVE_USAGE_API",
    }
    for key, value in expected_route.items():
        if route.get(key) != value:
            fail(f"route contract drift: {key}")

    receipt = packet.get("retrieval_receipt_requirements", {})
    for key in (
        "session_id_must_match_request",
        "receipt_id_required",
        "retrieved_at_required",
        "producer_identity_required",
        "policy_reference_required",
    ):
        if receipt.get(key) is not True:
            fail(f"receipt requirement missing: {key}")
    if receipt.get("authority_granted") is not False or receipt.get("custody_recorded") is not False:
        fail("retrieval receipt exceeded authority or custody boundary")

    evidence = packet.get("evidence_requirements", {})
    if set(evidence.get("allowed_classes", [])) != {"MEASURED", "CONFIGURED", "DERIVED", "UNAVAILABLE"}:
        fail("evidence class drift")
    for key in (
        "unavailable_value_must_be_null",
        "configured_values_may_not_be_relabelled_measured",
        "metric_owner_and_measurement_id_must_be_stable",
    ):
        if evidence.get(key) is not True:
            fail(f"evidence invariant missing: {key}")

    failures = packet.get("failure_contract", {})
    expected_statuses = {
        "unauthenticated": 401,
        "unauthorized": 403,
        "invalid_session_identity": 400,
        "session_conflict": 409,
        "invalid_contract_output": 422,
    }
    for key, value in expected_statuses.items():
        if failures.get(key) != value:
            fail(f"failure status drift: {key}")
    for key in (
        "authentication_failure_may_fallback",
        "identity_mismatch_may_fallback",
        "receipt_missing_may_fallback",
    ):
        if failures.get(key) is not False:
            fail(f"integrity failure fallback prohibited: {key}")

    boundaries = packet.get("authority_boundaries", {})
    if any(value is not False for value in boundaries.values()):
        fail("handoff exceeded Site authority")

    blocker = packet.get("blocker", {})
    if blocker.get("code") != "DESTINATION_HANDOFF_MISSING":
        fail("destination handoff blocker missing")
    if "*_MIRROR_HANDOFF.md" not in str(blocker.get("detail", "")):
        fail("blocker detail does not identify required handoff")

    required_activation = {
        "current destination *_MIRROR_HANDOFF.md authorizes endpoint work",
        "destination tests pass",
        "same-origin authenticated deployment observed",
        "sample response validates against Site contract",
        "retrieval receipt validates",
        "no bearer/query/local-storage secret surface",
        "Site current-main validation passes after configuration",
    }
    if set(packet.get("activation_evidence_required", [])) != required_activation:
        fail("activation evidence set drift")

    print("LLM_ADAPTER_USAGE_HANDOFF_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
