#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/va-claim-assistant/filing-integration-contract.json"
OUT = ROOT / "data/va-claim-assistant/filing-integration-contract-validation.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(contract.get("contract_id") == "SV-VA-FILING-INTEGRATION-001", "contract id mismatch", errors)
    require(contract.get("state") == "CONTRACT_READY_TRANSPORT_UNAVAILABLE", "contract state mismatch", errors)

    package = contract.get("package_requirements", {})
    for key in (
        "claimed_conditions_selected_by_veteran",
        "material_facts_confirmed_by_veteran",
        "evidence_index",
        "source_document_hashes",
        "page_anchors_for_record_facts",
        "assistant_inferences_separately_labeled",
        "contradictions_and_unfavorable_evidence_preserved",
        "missing_evidence_preserved",
        "current_form_and_rule_versions",
        "package_sha256",
        "change_log",
    ):
        require(package.get(key) is True, f"package requirement missing: {key}", errors)

    review = contract.get("veteran_review", {})
    require(review.get("required") is True, "veteran review not required", errors)
    require(review.get("confirm_each_material_fact") is True, "material fact confirmation missing", errors)
    require(review.get("select_each_claimed_condition") is True, "condition selection missing", errors)
    require(review.get("approval_is_package_hash_bound") is True, "hash-bound approval missing", errors)
    require(review.get("approval_revocable_before_submission") is True, "revocation missing", errors)

    authorization = contract.get("authorization", {})
    require(authorization.get("veteran_submission_authority_preserved") is True, "veteran authority not preserved", errors)
    require(authorization.get("assistant_may_not_sign") is True, "assistant signature prohibition missing", errors)
    require(authorization.get("assistant_may_not_select_claimed_conditions") is True, "assistant condition-selection prohibition missing", errors)
    require(authorization.get("assistant_may_not_confirm_material_facts") is True, "assistant fact-confirmation prohibition missing", errors)

    transport = contract.get("transport_admission", {})
    require(transport.get("active_transport") is None, "transport unexpectedly active", errors)
    require(transport.get("browser_automation_without_explicit_admission_allowed") is False, "unauthorized browser automation allowed", errors)
    require(transport.get("credential_collection_by_site_allowed") is False, "site credential collection allowed", errors)
    require(transport.get("repository_local_submission_secrets_allowed") is False, "repository-local secrets allowed", errors)
    require(transport.get("tvc_capability_receipt_required") is True, "TVC receipt not required", errors)

    execution = contract.get("submission_execution", {})
    require(execution.get("enabled") is False, "submission unexpectedly enabled", errors)
    require(execution.get("idempotency_key_required") is True, "idempotency missing", errors)
    require(execution.get("package_hash_must_match_authorization") is True, "authorization hash binding missing", errors)
    require(execution.get("partial_failure_must_stop") is True, "partial failure does not stop", errors)
    require(execution.get("automatic_retry_without_state_reconstruction_allowed") is False, "unsafe retry allowed", errors)
    require(execution.get("duplicate_submission_must_be_prevented") is True, "duplicate prevention missing", errors)

    custody = contract.get("custody_and_reconstruction", {})
    require(custody.get("reconstruction_pass_required") is True, "reconstruction PASS not required", errors)
    require(custody.get("raw_private_documents_published") is False, "raw private document publication allowed", errors)

    authority = contract.get("authority", {})
    for key, value in authority.items():
        require(value is False, f"authority unexpectedly enabled: {key}", errors)

    fail_closed = set(contract.get("fail_closed_conditions", []))
    required_fail_closed = {
        "material_fact_unconfirmed",
        "claimed_condition_not_selected_by_veteran",
        "package_hash_missing_or_changed",
        "authorization_missing_expired_revoked_or_hash_mismatched",
        "authorized_transport_unavailable",
        "duplicate_submission_detected",
        "custody_or_reconstruction_unavailable",
        "partial_failure_state_unreconstructed",
    }
    require(required_fail_closed.issubset(fail_closed), "required fail-closed conditions missing", errors)

    body = {
        "schema_version": "1.0.0",
        "state": "PASS" if not errors else "FAIL",
        "contract_id": contract.get("contract_id"),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "submission_enabled": execution.get("enabled"),
        "active_transport": transport.get("active_transport"),
        "veteran_submission_authority_preserved": authorization.get("veteran_submission_authority_preserved"),
        "exact_package_authorization_required": authorization.get("exact_package_sha256_required"),
        "duplicate_prevention_required": execution.get("duplicate_submission_must_be_prevented"),
        "reconstruction_pass_required": custody.get("reconstruction_pass_required"),
        "authority_effect": False,
        "activation_effect": False,
        "errors": errors,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
