#!/usr/bin/env python3
"""Verify the canonical public HIL v1.1 paper, governed client, result continuity, and manifest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data" / "HIL_Canonical_Paper_v1_1.pdf"
PAGE = ROOT / "humans-as-interoperability-layer.html"
CLIENT = ROOT / "assets" / "hil-direct-upload-v1.js"
RESULT_PAGE = ROOT / "hil-accepted.html"
RESULT_CLIENT = ROOT / "assets" / "hil-post-submit-continuity.js"
MANIFEST = ROOT / "data" / "hil-experiment.json"
RECEIVER_CONFIG = ROOT / "data" / "hil-receiver-config.json"

EXPECTED_SIZE = 87271
EXPECTED_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
EXPECTED_PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
EXPECTED_PATH = "data/HIL_Canonical_Paper_v1_1.pdf"
EXPECTED_PROTOCOL = "HIL-PROTOCOL-v1.1"
EXPECTED_PROMPT = "HIL-PROMPT-v1.1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL v1.1 release verification failed: {message}")


def main() -> None:
    require(PDF.is_file(), f"missing canonical PDF: {PDF.relative_to(ROOT)}")
    payload = PDF.read_bytes()
    require(payload.startswith(b"%PDF-"), "canonical artifact lacks PDF signature")
    require(len(payload) == EXPECTED_SIZE, f"canonical PDF size is {len(payload)}, expected {EXPECTED_SIZE}")
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == EXPECTED_SHA256, f"canonical PDF SHA-256 is {digest}, expected {EXPECTED_SHA256}")

    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    result_page = RESULT_PAGE.read_text(encoding="utf-8")
    result_client = RESULT_CLIENT.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    receiver = json.loads(RECEIVER_CONFIG.read_text(encoding="utf-8"))

    for marker in (
        "Canonical experiment input · v1.1",
        "Download Canonical v1.1 Primary PDF",
        "HIL_Canonical_Paper_v1_1.pdf",
        EXPECTED_SHA256,
        "assets/hil-direct-upload-v1.js",
        "id=\"upload-form\"",
        "id=\"response-file\"",
        "id=\"upload-response\"",
        "aria-live=\"polite\"",
        "next Site page begins with the exact submission-result packet",
    ):
        require(marker in page, f"public page missing marker: {marker}")

    for marker in (
        "const READINESS = '/api/hil/readiness'",
        "const INGRESS = '/api/hil/submissions'",
        "new FormData()",
        "crypto.subtle.digest('SHA-256'",
        "response_pdf",
        "provenance_manifest",
        "HIL-RESPONSE-PROVENANCE-v1.1",
        "HIL-RECEIVER-RECEIPT-v2",
        "redirect: 'error'",
        "INDEXED_DB",
        "local_fallback_hash_verification_failed",
        "EXACT_BYTES_PERSISTED",
        "RECORDED",
        "hil-accepted.html?submission_id=",
        "LOCAL_FALLBACK_PENDING_RESUBMISSION",
        EXPECTED_SHA256,
        EXPECTED_PROMPT_SHA256,
        EXPECTED_PROTOCOL,
    ):
        require(marker in client, f"direct-upload client missing marker: {marker}")

    require("/api/hil/upload" not in client, "legacy /api/hil/upload route remains canonical")
    require("GITHUB_TOKEN" not in client and "Authorization" not in client, "browser runtime credential path introduced")

    packet_pos = result_page.find('id="submission-result-packet"')
    next_pos = result_page.find('id="next-lifecycle-stage"')
    require(packet_pos >= 0 and next_pos > packet_pos, "submission result packet is not prepended")
    for marker in (
        "HIL-SUBMISSION-RESULT-PACKET-v1",
        "/api/hil/submissions/${encodeURIComponent(submissionId)}",
        "/api/hil/submissions/${encodeURIComponent(submissionId)}/content",
        "retrieved_packet_hash_mismatch",
        "publication_authorized: false",
        "release_authorized: false",
        "master_record_append_authorized: false",
        "execution_authorized: false",
    ):
        require(marker in result_client, f"result continuity missing marker: {marker}")
    require("GITHUB_TOKEN" not in result_client and "Authorization" not in result_client, "result page runtime credential path introduced")

    primary = manifest["primary_document"]
    protocol = manifest["protocol"]
    require(manifest["schema_version"] == "HIL-EXPERIMENT-v1.1", "manifest schema mismatch")
    require(primary["version"] == "v1.1", "manifest primary version mismatch")
    require(primary["artifact_path"] == EXPECTED_PATH, "manifest artifact path mismatch")
    require(primary["size_bytes"] == EXPECTED_SIZE, "manifest size mismatch")
    require(primary["sha256"] == EXPECTED_SHA256, "manifest hash mismatch")
    require(protocol["version"] == EXPECTED_PROTOCOL, "manifest protocol version mismatch")
    require(protocol["prompt_version"] == EXPECTED_PROMPT, "manifest prompt version mismatch")
    require(protocol["prompt_sha256"] == EXPECTED_PROMPT_SHA256, "manifest prompt hash mismatch")
    require(manifest["submission"]["provenance_manifest_required"] is True, "provenance must remain required")
    require(all(value is False for value in manifest["authority"].values()), "authority must remain fail-closed")

    receiver_base = receiver.get("receiver_base_url")
    receiver_state = receiver.get("configuration_state")
    configured_same_origin = (
        receiver_base == "https://stegverse.org"
        and receiver_state == "CONFORMING_HTTPS_RECEIVER_CONFIGURED"
    )
    fail_closed_unconfigured = (
        receiver_base is None
        and receiver_state == "AWAITING_CONFORMING_HTTPS_RECEIVER"
    )
    require(configured_same_origin or fail_closed_unconfigured, "receiver discovery state invalid")
    require(receiver.get("participant_visible_provider") is False, "provider branding must remain hidden")
    require(receiver.get("readiness_path") == "/api/hil/readiness", "readiness route mismatch")
    require(receiver.get("submission_path") == "/api/hil/submissions", "submission route mismatch")
    require(receiver.get("transport_requirements", {}).get("embedded_credentials_allowed") is False, "embedded credentials must remain prohibited")
    require(all(receiver.get("authority", {}).get(key) is False for key in ("execution", "publication", "master_record_append")), "receiver discovery must not grant authority")

    print("HIL_V1_1_RELEASE_VERIFICATION=PASS")
    print(f"HIL_V1_1_PDF_SIZE={len(payload)}")
    print(f"HIL_V1_1_PDF_SHA256={digest}")
    print(f"HIL_V1_1_ARTIFACT_PATH={EXPECTED_PATH}")
    print(f"HIL_V1_1_PROTOCOL={EXPECTED_PROTOCOL}")
    print(f"HIL_V1_1_PROMPT={EXPECTED_PROMPT}")
    print("HIL_V1_1_GOVERNED_RECEIVER=/api/hil/submissions")
    print("HIL_V1_1_RESULT_PACKET=HIL-SUBMISSION-RESULT-PACKET-v1")
    print("HIL_V1_1_LOCAL_FALLBACK=HASH_VERIFIED_NONCUSTODIAL")
    print("HIL_V1_1_GITHUB_TOKEN_RUNTIME_AUTHORITY=NONE")
    print("HIL_V1_1_AUTHORITY=NONE")
    print(f"HIL_RECEIVER_DISCOVERY_STATE={receiver_state}")
    print(f"HIL_PUBLIC_RECEIVER_READY_PROVEN={'true' if configured_same_origin else 'false'}")


if __name__ == "__main__":
    main()
