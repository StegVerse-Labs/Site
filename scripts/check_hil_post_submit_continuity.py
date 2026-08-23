#!/usr/bin/env python3
"""Fail-closed contract check for HIL governed submit -> prepended result-page continuity."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "humans-as-interoperability-layer.html"
CLIENT = ROOT / "assets" / "hil-direct-upload-v1.js"
RESULT_PAGE = ROOT / "hil-accepted.html"
RESULT_CLIENT = ROOT / "assets" / "hil-post-submit-continuity.js"
WORKER = ROOT / "src" / "worker.js"
RECEIVER_CONFIG = ROOT / "data" / "hil-receiver-config.json"

PRIMARY_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"HIL_POST_SUBMIT_CONTINUITY=FAIL missing={path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise SystemExit(f"HIL_POST_SUBMIT_CONTINUITY=FAIL reason={reason}")


def main() -> None:
    page = read(PAGE)
    client = read(CLIENT)
    result_page = read(RESULT_PAGE)
    result_client = read(RESULT_CLIENT)
    worker = read(WORKER)
    receiver_config = json.loads(read(RECEIVER_CONFIG))

    require("assets/hil-direct-upload-v1.js" in page, "public_page_missing_submit_client")
    require("next Site page begins with the exact submission-result packet" in page, "participant_flow_not_declared")
    require("/api/hil/upload" not in client, "legacy_upload_endpoint_still_present")
    require("const READINESS = '/api/hil/readiness'" in client, "readiness_route_missing")
    require("const INGRESS = '/api/hil/submissions'" in client, "canonical_submission_route_missing")
    require("HIL-RESPONSE-PROVENANCE-v1.1" in client, "provenance_contract_missing")
    require("HIL-RECEIVER-RECEIPT-v2" in client, "receiver_receipt_validation_missing")
    require(PRIMARY_SHA256 in client and PROMPT_SHA256 in client, "canonical_identity_binding_missing")
    require("custody_state !== 'EXACT_BYTES_PERSISTED'" in client, "durable_custody_check_missing")
    require("registry_state !== 'RECORDED'" in client, "registry_check_missing")
    require("hil-accepted.html?submission_id=" in client, "governed_success_does_not_advance_to_result_page")
    require("hil-receipt.html?submission_id=" in client, "local_fallback_receipt_path_missing")
    require("LOCAL_FALLBACK_PENDING_RESUBMISSION" in client, "local_fallback_not_distinguished")

    packet_pos = result_page.find('id="submission-result-packet"')
    next_pos = result_page.find('id="next-lifecycle-stage"')
    require(packet_pos >= 0, "result_packet_section_missing")
    require(next_pos > packet_pos, "result_packet_not_prepended_before_next_stage")
    require("HIL Submission Result Packet" in result_page, "result_packet_heading_missing")
    require("assets/hil-post-submit-continuity.js" in result_page, "result_packet_client_missing")

    for marker in (
        "HIL-SUBMISSION-RESULT-PACKET-v1",
        "HIL-RECEIVER-RECEIPT-v2",
        "EXACT_BYTES_PERSISTED",
        "RECORDED",
        "/api/hil/submissions/${encodeURIComponent(submissionId)}",
        "/api/hil/submissions/${encodeURIComponent(submissionId)}/content",
        "retrieved_packet_hash_mismatch",
        "exact_byte_verification",
        "private_review_authorized: false",
        "publication_authorized: false",
        "release_authorized: false",
        "master_record_append_authorized: false",
        "execution_authorized: false",
    ):
        require(marker in result_client, f"result_client_missing:{marker}")

    require("receiver.stegverse.com" not in result_client, "stale_cross_origin_receiver_hardcode_present")
    require("GITHUB_TOKEN" not in client and "GITHUB_TOKEN" not in result_client, "github_token_runtime_authority_present")
    require("Authorization" not in client and "Authorization" not in result_client, "client_credential_header_present")

    for marker in (
        "url.pathname === '/api/hil/readiness'",
        "url.pathname === '/api/hil/submissions'",
        "submissionStatus(url, env)",
        "submissionContent(url, env)",
        "post_persistence_exact_byte_verification_failed",
    ):
        require(marker in worker, f"worker_contract_missing:{marker}")

    receiver_base = receiver_config.get("receiver_base_url")
    receiver_state = receiver_config.get("configuration_state")
    configured_same_origin = (
        receiver_base == "https://stegverse.org"
        and receiver_state == "CONFORMING_HTTPS_RECEIVER_CONFIGURED"
    )
    fail_closed_unconfigured = (
        receiver_base is None
        and receiver_state == "AWAITING_CONFORMING_HTTPS_RECEIVER"
    )
    require(configured_same_origin or fail_closed_unconfigured, "receiver_discovery_state_invalid")
    require(receiver_config.get("participant_visible_provider") is False, "provider_branding_not_hidden")
    require(receiver_config.get("readiness_path") == "/api/hil/readiness", "receiver_config_readiness_mismatch")
    require(receiver_config.get("submission_path") == "/api/hil/submissions", "receiver_config_submission_mismatch")
    require(receiver_config.get("transport_requirements", {}).get("embedded_credentials_allowed") is False, "embedded_credentials_not_fail_closed")

    print("HIL_POST_SUBMIT_CONTINUITY=PASS")
    print("HIL_GOVERNED_SUBMIT_ROUTE=/api/hil/submissions")
    print("HIL_GOVERNED_RESULT_PAGE=hil-accepted.html")
    print("HIL_RESULT_PACKET=HIL-SUBMISSION-RESULT-PACKET-v1")
    print("HIL_LOCAL_FALLBACK=hil-receipt.html")
    print("HIL_GITHUB_TOKEN_RUNTIME_AUTHORITY=NONE")
    print("HIL_PUBLICATION_AUTHORITY_FROM_RESULT_PACKET=false")
    print(f"HIL_RECEIVER_DISCOVERY_STATE={receiver_state}")
    print(f"HIL_RUNTIME_READY_PROVEN={'true' if configured_same_origin else 'false'}")


if __name__ == "__main__":
    main()
