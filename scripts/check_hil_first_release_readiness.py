#!/usr/bin/env python3
"""Fail-closed validation for the first HIL Master Record release readiness ledger."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "hil-first-release-readiness.json"
HEX64 = set("0123456789abcdef")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL first release readiness validation failed: {message}")


def is_hash(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX64


def main() -> None:
    require(LEDGER.is_file(), "missing readiness ledger")
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "HIL-FIRST-RELEASE-READINESS-v1", "schema mismatch")
    require(data.get("experiment_id") == "HIL-2026", "experiment mismatch")
    require(data.get("authority_effect") == "NONE", "authority effect must remain NONE")

    required = data.get("required_inputs", {})
    candidate = data.get("candidate_generation", {})
    authorization = data.get("authorization", {})
    for key in ("site_import", "master_record_release", "orchestration_submission", "public_acquisition"):
        require(authorization.get(key) is False, f"{key} must remain false before separate authorization")

    complete_values = [
        required.get("authorized_external_deployment_observation"),
        required.get("site_imported_publication_record"),
        required.get("stable_response_identifier"),
        required.get("response_pdf_hash"),
        required.get("provenance_hash"),
        required.get("receiver_receipt_hash_or_reference"),
        required.get("private_review_receipt_hash"),
        required.get("publication_record_hash"),
    ]
    established = all(value != "NOT_ESTABLISHED" for value in complete_values)

    if established:
        require(required["stable_response_identifier"].startswith("HIL-RESP-"), "stable response id invalid")
        for key in ("response_pdf_hash", "provenance_hash", "private_review_receipt_hash", "publication_record_hash"):
            require(is_hash(required[key]), f"{key} must be a SHA-256")
        previous = required.get("previous_release_hash")
        require(previous is None or is_hash(previous), "previous release hash invalid")
        require(candidate.get("dry_run_available") is True, "dry-run builder must be available")
        require(data.get("state") in {"READY_FOR_DRY_RUN", "CANDIDATE_BUILT_PENDING_AUTHORIZATION"}, "state inconsistent with established inputs")
    else:
        require(data.get("state") == "WAITING_FOR_AUTHORIZED_EXTERNAL_CYCLE", "incomplete inputs must remain waiting")
        require(candidate.get("candidate_generated") is False, "candidate cannot be generated from incomplete evidence")
        require(candidate.get("candidate_path") is None, "candidate path must be null")
        require(candidate.get("candidate_sha256") is None, "candidate hash must be null")

    print("HIL_FIRST_RELEASE_READINESS=PASS")
    print(f"HIL_FIRST_RELEASE_STATE={data['state']}")
    print("HIL_RELEASE_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
