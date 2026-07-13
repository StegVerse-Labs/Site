#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "requests/external-chat-activation-request-2026-07-13.json"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION REQUEST: FAIL - {message}")
    return 1


def main() -> int:
    if not REQUEST.exists():
        return fail(f"missing {REQUEST.relative_to(ROOT)}")
    try:
        payload = json.loads(REQUEST.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"invalid JSON: {exc}")

    if payload.get("schema_version") != "1.0.0":
        return fail("schema_version mismatch")
    if payload.get("record_type") != "external_chat_activation_request":
        return fail("record_type mismatch")
    if payload.get("repository") != "StegVerse-Labs/Site" or payload.get("branch") != "main":
        return fail("repository or branch mismatch")
    if payload.get("requested_transition") != "run_existing_validation_deployment_and_post_deployment_external_chat_observation_chain":
        return fail("requested transition mismatch")
    if payload.get("success_result") != "OBSERVED_NON_MUTATING_PUBLIC_PATHS":
        return fail("success result mismatch")

    sequence = payload.get("required_workflow_sequence")
    if sequence != ["Site Bootstrap Validate", "Site Task Runner"]:
        return fail("workflow sequence mismatch")

    required_observations = set(payload.get("required_observations", []))
    expected_observations = {
        "external_chat_page_http_200",
        "external_review_page_http_200",
        "review_health_package_only_storage_true",
        "review_health_raw_artifact_storage_allowed_false",
        "review_health_publication_authority_false",
        "mutation_health_commit_time_revalidation_required_true",
        "mutation_health_publication_transition_is_mutation_authority_false",
        "mutation_health_mutation_enabled_false",
    }
    if required_observations != expected_observations:
        return fail("required observations drift")

    required_artifacts = set(payload.get("required_artifacts", []))
    expected_artifacts = {
        "site-task-diagnostic-<run_id>-<run_attempt>",
        "external-chat-live-verification-<run_id>-<run_attempt>",
        "external-chat-activation-evidence-<run_id>-<run_attempt>",
    }
    if required_artifacts != expected_artifacts:
        return fail("required artifact set drift")

    boundary = payload.get("authority_boundary")
    expected_boundary = {
        "request_authorizes_existing_validation_and_deployment_sequence": True,
        "request_authorizes_repository_mutation": False,
        "request_authorizes_external_framework_publication": False,
        "request_authorizes_certification": False,
        "request_creates_standing": False,
        "production_mutation_must_remain_disabled": True,
        "canonical_status_promotion_remains_separately_governed": True,
    }
    if boundary != expected_boundary:
        return fail("authority boundary drift")
    if payload.get("failure_posture") != "fail_closed_and_preserve_machine_readable_evidence":
        return fail("failure posture mismatch")
    if payload.get("required_next_transition_after_success") != "admissibility_wiki_exact_artifact_sync_and_separately_authorized_observation_status_promotion":
        return fail("next transition mismatch")

    print("EXTERNAL CHAT ACTIVATION REQUEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
