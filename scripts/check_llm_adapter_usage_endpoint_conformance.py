#!/usr/bin/env python3
"""Validate positive and negative authenticated usage endpoint conformance fixtures."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "data" / "llm-adapter-usage-endpoint-conformance.json"
ALLOWED_EVIDENCE = {"MEASURED", "CONFIGURED", "DERIVED", "UNAVAILABLE"}
REQUIRED_EVENT_FIELDS = {
    "measurement_id",
    "session_id",
    "transition_id",
    "origin_entry_point",
    "entry_point",
    "entry_point_role",
    "interaction_type",
    "metric_owner",
    "measurement_source",
    "metrics",
    "timestamp",
    "receipt_refs",
}


class ContractError(ValueError):
    def __init__(self, failure_class: str, message: str) -> None:
        super().__init__(message)
        self.failure_class = failure_class


def require(condition: bool, failure_class: str, message: str) -> None:
    if not condition:
        raise ContractError(failure_class, message)


def validate_payload(payload: dict[str, Any], requested_session: str) -> None:
    require(payload.get("schema") == "stegverse.usage.session.v1", "SCHEMA_INVALID", "response schema mismatch")
    require(payload.get("session_id") == requested_session, "IDENTITY_MISMATCH", "response session identity mismatch")
    require(payload.get("source_class") == "LIVE_USAGE_API", "SOURCE_CLASS_INVALID", "source class mismatch")
    require(isinstance(payload.get("events"), list), "EVENTS_INVALID", "events must be an array")

    receipt = payload.get("retrieval_receipt")
    require(isinstance(receipt, dict), "RECEIPT_MISSING", "retrieval receipt missing")
    require(receipt.get("session_id") == requested_session, "IDENTITY_MISMATCH", "receipt session mismatch")
    for field in ("receipt_id", "retrieved_at", "producer_identity", "policy_reference"):
        require(bool(receipt.get(field)), "RECEIPT_INVALID", f"retrieval receipt missing {field}")
    require(receipt.get("authority_granted") is False, "AUTHORITY_OVERREACH", "retrieval receipt granted authority")
    require(receipt.get("custody_recorded") is False, "CUSTODY_OVERREACH", "retrieval receipt claimed custody")

    for event in payload["events"]:
        require(isinstance(event, dict), "EVENT_INVALID", "event must be an object")
        missing = sorted(REQUIRED_EVENT_FIELDS - set(event))
        require(not missing, "EVENT_INVALID", f"event missing fields {missing}")
        require(event.get("session_id") == requested_session, "IDENTITY_MISMATCH", "event session mismatch")
        require(isinstance(event.get("metrics"), dict), "METRICS_INVALID", "metrics must be an object")
        require(isinstance(event.get("receipt_refs"), list), "RECEIPT_REFS_INVALID", "receipt_refs must be an array")
        for metric_name, metric in event["metrics"].items():
            require(bool(metric_name) and isinstance(metric, dict), "METRIC_INVALID", "metric invalid")
            evidence_class = metric.get("evidence_class")
            require(evidence_class in ALLOWED_EVIDENCE, "EVIDENCE_CLASS_INVALID", f"invalid evidence class {evidence_class}")
            if evidence_class == "UNAVAILABLE":
                require(metric.get("value") is None, "UNAVAILABLE_VALUE_INVALID", "UNAVAILABLE metric must use null")


def main() -> int:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if document.get("schema") != "stegverse.site.llm_adapter_usage_endpoint_conformance.v1":
        raise SystemExit("USAGE_ENDPOINT_CONFORMANCE_FAIL: fixture schema drift")
    requested_session = document.get("requested_session_id")
    cases = document.get("cases")
    if not requested_session or not isinstance(cases, list) or len(cases) < 7:
        raise SystemExit("USAGE_ENDPOINT_CONFORMANCE_FAIL: incomplete fixture set")

    observed: dict[str, str] = {}
    for case in cases:
        case_id = case.get("case_id")
        expected = case.get("expected")
        if not case_id or expected not in {"ALLOW", "DENY"}:
            raise SystemExit("USAGE_ENDPOINT_CONFORMANCE_FAIL: malformed case declaration")
        try:
            validate_payload(case.get("payload", {}), requested_session)
            outcome = "ALLOW"
            failure_class = "NONE"
        except ContractError as error:
            outcome = "DENY"
            failure_class = error.failure_class
        if outcome != expected:
            raise SystemExit(f"USAGE_ENDPOINT_CONFORMANCE_FAIL: {case_id} expected {expected} observed {outcome}")
        if expected == "DENY" and failure_class != case.get("failure_class"):
            raise SystemExit(
                f"USAGE_ENDPOINT_CONFORMANCE_FAIL: {case_id} expected failure {case.get('failure_class')} observed {failure_class}"
            )
        observed[case_id] = outcome if outcome == "ALLOW" else f"DENY:{failure_class}"

    required_cases = {
        "valid_live_usage_response",
        "session_identity_drift",
        "missing_retrieval_receipt",
        "authority_overreach",
        "custody_overreach",
        "invalid_evidence_class",
        "unavailable_value_violation",
    }
    if set(observed) != required_cases:
        raise SystemExit(f"USAGE_ENDPOINT_CONFORMANCE_FAIL: unexpected cases {sorted(set(observed) ^ required_cases)}")

    print("USAGE_ENDPOINT_CONFORMANCE_PASS")
    for case_id in sorted(observed):
        print(f"{case_id}={observed[case_id]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
