#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "external-chat.html"
CLIENT = ROOT / "assets" / "external-chat.js"
REVIEW_CLIENT = ROOT / "assets" / "external-chat-review.js"
EXAMPLE = ROOT / "data" / "external-chat-example.json"
CATALOG = ROOT / "data" / "external-framework-catalog.json"
CATALOG_RECEIPT = ROOT / "data" / "external-framework-catalog.receipt.json"
IMPORT_STATUS = ROOT / "data" / "external-framework-catalog-import-status.json"
IMPORTER = ROOT / "scripts" / "acquire_external_framework_catalog.py"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT COMPATIBILITY: FAIL - {message}")
    return 1


def canonical_sha256(payload: dict) -> str:
    material = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def main() -> int:
    for path in [PAGE, CLIENT, REVIEW_CLIENT, EXAMPLE, CATALOG, CATALOG_RECEIPT, IMPORT_STATUS, IMPORTER]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    review_client = REVIEW_CLIENT.read_text(encoding="utf-8")
    importer = IMPORTER.read_text(encoding="utf-8")
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    receipt = json.loads(CATALOG_RECEIPT.read_text(encoding="utf-8"))
    import_status = json.loads(IMPORT_STATUS.read_text(encoding="utf-8"))

    for marker in [
        "External Chat", "compatibility evidence only", "does not certify",
        "assets/external-chat.js", "assets/external-chat-review.js",
        "admissibility-wiki/external-frameworks", "Download result packet",
        "Create challenge packet", "Create opt-in review package", "explicitly opt in",
        "does not authorize publication", "Submit package for delegated review",
        "token remains in this page only",
    ]:
        if marker not in page:
            return fail(f"page missing marker: {marker}")

    for marker in [
        "/api/external-framework-compatibility", "compatibility_evidence_only",
        "compatibility_result_is_authority", "submission_retained", "wiki_record_created",
        "No result or receipt was claimed", "external-framework-catalog.json",
        "external-framework-catalog.receipt.json", "downloadResultPacket",
        "downloadChallengePacket", "downloadReviewPackage",
        "external_framework_cooperative_review_package", "submitter_opt_in",
        "raw_submission_included: false", "review_may_change_result_without_receipt: false",
    ]:
        if marker not in client:
            return fail(f"client missing marker: {marker}")

    for marker in [
        "/api/external-review/packages", "Authorization", "Bearer ${token}",
        "raw_submission_stored", "wiki_record_created", "publication_authorized",
        "standing_created", "AWAITING_DELEGATED_REVIEW", "intake_receipt_id",
        "tokenEl.value = ''", "No review receipt or publication state was claimed",
    ]:
        if marker not in review_client:
            return fail(f"review client missing marker: {marker}")

    for marker in [
        "raw.githubusercontent.com/StegVerse-Labs/admissibility-wiki",
        "external-chat-catalog.json", "external-chat-catalog.receipt.json",
        "RECEIPTED_WIKI_CATALOG_IMPORTED", "LOCAL_RECEIPTED_CATALOG_RETAINED",
    ]:
        if marker not in importer:
            return fail(f"catalog importer missing marker: {marker}")

    required = [
        "framework_id", "framework_name", "source_references", "input_artifact_type",
        "output_artifact_type", "actor_or_authority_model", "evidence_model",
        "policy_or_rule_model", "delegation_model", "decision_or_result_model",
        "receipt_or_trace_model", "reconstruction_model", "fail_closed_conditions",
    ]
    missing = [field for field in required if field not in example]
    if missing:
        return fail("example missing fields: " + ", ".join(missing))
    for key in ["execution_authority_claim", "commit_time_authority_claim", "certification_claim", "equivalence_claim"]:
        if example.get(key) is not False:
            return fail(f"example boundary must be false: {key}")

    if catalog.get("artifact_type") != "external_framework_catalog":
        return fail("catalog artifact_type mismatch")
    frameworks = catalog.get("frameworks")
    if not isinstance(frameworks, list) or not frameworks:
        return fail("catalog frameworks must be non-empty")
    ids = [entry.get("framework_id") for entry in frameworks]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        return fail("catalog framework IDs must be unique and non-empty")
    if any(value is not False for value in catalog.get("authority_boundary", {}).values()):
        return fail("catalog authority boundary invalid")

    if receipt.get("receipt_type") != "external_framework_catalog_projection_receipt":
        return fail("catalog receipt_type mismatch")
    if receipt.get("catalog_sha256") != canonical_sha256(catalog):
        return fail("catalog receipt hash mismatch")
    if receipt.get("framework_count") != len(frameworks):
        return fail("catalog receipt count mismatch")
    if receipt.get("projection_only") is not True:
        return fail("catalog receipt must remain projection_only")
    if any(value is not False for value in receipt.get("authority_boundary", {}).values()):
        return fail("catalog receipt boundary invalid")

    if import_status.get("status_type") != "external_framework_catalog_import_status":
        return fail("catalog import status type mismatch")
    if import_status.get("state") not in {"RECEIPTED_WIKI_CATALOG_IMPORTED", "LOCAL_RECEIPTED_CATALOG_RETAINED"}:
        return fail("unsupported catalog import state")
    if import_status.get("publication_authority") is not False or import_status.get("certification_authority") is not False:
        return fail("catalog import status authority boundary invalid")

    print(f"EXTERNAL CHAT COMPATIBILITY: PASS ({len(frameworks)} catalog frameworks, authenticated review transport, {import_status['state']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
