#!/usr/bin/env python3
"""Fail-closed validation for Site's generated StegPay integration status.

The validator proves only that the test integration record is internally bounded
and ready for downstream evidence ingestion. It never grants production payment,
deployment, release, publication, or admissibility authority.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "autonomy" / "generated-stegpay-integration-status.json"
OUTPUT = ROOT / "data" / "autonomy" / "generated-stegpay-integration-validation.json"

EXPECTED_DESTINATIONS = [
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-002/stegguardian-wiki",
]
EXPECTED_REASONS = ["signed_envelope_verified", "stegpay_verified_event"]
AUTHORITY_FIELDS = [
    "production_payment_authority",
    "deployment_authority",
    "release_authority",
    "publication_authority",
    "admissibility_authority",
]
HASH_FIELDS = [
    "event_hash_sha256",
    "envelope_hash_sha256",
    "transport_hash_sha256",
    "producer_receipt_hash_sha256",
]


def canonical_hash(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def validate(source: dict[str, Any]) -> dict[str, Any]:
    verification = source.get("verification") if isinstance(source.get("verification"), dict) else {}
    authority = source.get("authority") if isinstance(source.get("authority"), dict) else {}
    evidence = source.get("source_evidence") if isinstance(source.get("source_evidence"), dict) else {}

    checks = {
        "schema_version": source.get("schema_version") == "1.0",
        "artifact_type": source.get("artifact_type") == "site_generated_stegpay_integration_status",
        "state": source.get("state") == "VERIFIED_TEST_INTEGRATION",
        "source_repository": source.get("source_repository") == "StegVerse-Labs/StegOps-Orchestrator",
        "producer_repository": source.get("producer_repository") == "StegVerse-Labs/StegPay",
        "source_handoff": source.get("source_handoff") == "docs/STEGOPS_ORCHESTRATOR_MIRROR_HANDOFF.md",
        "evidence_paths": all(isinstance(evidence.get(key), str) and bool(evidence.get(key)) for key in ("consumer_receipt", "producer_receipt", "state", "ledger")),
        "event_id": isinstance(verification.get("event_id"), str) and bool(verification.get("event_id")),
        "provider_id": isinstance(verification.get("provider_id"), str) and bool(verification.get("provider_id")),
        "issuer": isinstance(verification.get("issuer"), str) and bool(verification.get("issuer")),
        "key_id": isinstance(verification.get("key_id"), str) and bool(verification.get("key_id")),
        "event_schema_version": verification.get("schema_version") == 1,
        "hashes": all(is_sha256(verification.get(field)) for field in HASH_FIELDS),
        "consumer_state": verification.get("consumer_state") == "deliverables_ready",
        "verified_reasons": verification.get("verified_reasons") == EXPECTED_REASONS,
        "matching_ledger_entries": verification.get("matching_ledger_entries") == 1,
        "producer_consumer_agreement": verification.get("producer_consumer_agreement") is True,
        "transport_not_authority": verification.get("transport_is_authority") is False,
        "test_only": verification.get("test_only") is True,
        "authority_fail_closed": all(authority.get(field) is False for field in AUTHORITY_FIELDS),
        "destinations": source.get("next_destinations") == EXPECTED_DESTINATIONS,
        "manual_user_action_false": source.get("manual_user_action_required") is False,
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {
        "schema_version": "1.0",
        "artifact_type": "site_generated_stegpay_integration_validation",
        "state": "VALID" if not failures else "INVALID",
        "source_path": "data/autonomy/generated-stegpay-integration-status.json",
        "source_canonical_sha256": canonical_hash(source),
        "checks": checks,
        "failures": failures,
        "downstream_ingestion_ready": not failures,
        "authority": {field: False for field in AUTHORITY_FIELDS},
        "manual_user_action_required": False,
    }


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(source, dict):
        raise SystemExit("generated StegPay integration status must be a JSON object")
    result = validate(source)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["state"] != "VALID":
        raise SystemExit("generated StegPay integration status invalid: " + ", ".join(result["failures"]))
    print("GENERATED STEGPAY SITE INTEGRATION: VALID")


if __name__ == "__main__":
    main()
