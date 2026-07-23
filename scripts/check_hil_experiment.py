#!/usr/bin/env python3
"""Fail-closed static checks for the HIL public experiment surface."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "humans-as-interoperability-layer.html"
DETAIL_PAGE = ROOT / "humans-as-interoperability-response.html"
SCRIPT = ROOT / "assets" / "hil-experiment.js"
DETAIL_SCRIPT = ROOT / "assets" / "hil-response.js"
MANIFEST = ROOT / "data" / "hil-experiment.json"
RESPONSES = ROOT / "data" / "hil-responses.json"
SUBMISSION_SCHEMA = ROOT / "data" / "schemas" / "hil-submission.schema.json"
RECEIVER_SCHEMA = ROOT / "data" / "schemas" / "hil-receiver-receipt.schema.json"
PRIMARY_B64 = ROOT / "data" / "hil-primary-v0.4.pdf.b64"

EXPECTED_HASH = "97df3006c8d96212560c5fa970dc7bceac66bde23a8b23373491c030ccc0049d"
EXPECTED_PROMPT = (
    "Read this Primary PDF in full and follow every instruction in "
    "Section 8: Independent Response Protocol."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL verification failed: {message}")


def read(path: Path) -> str:
    require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_primary_artifact() -> str:
    if not PRIMARY_B64.exists():
        return "PENDING_INSTALLATION"

    import base64

    encoded = "".join(PRIMARY_B64.read_text(encoding="ascii").split())
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"HIL verification failed: invalid primary base64: {exc}") from exc

    require(payload.startswith(b"%PDF-"), "canonical artifact lacks PDF signature")
    actual = hashlib.sha256(payload).hexdigest()
    require(actual == EXPECTED_HASH, f"canonical artifact hash mismatch: {actual}")
    return "VERIFIED"


def validate_response_index(responses: dict) -> int:
    records = responses.get("responses")
    require(isinstance(records, list), "responses index must contain an array")
    seen: set[str] = set()
    for record in records:
        require(isinstance(record, dict), "response record must be an object")
        response_id = record.get("response_id")
        require(
            isinstance(response_id, str) and re.fullmatch(r"HIL-RESP-[A-Z0-9-]+", response_id),
            "invalid response_id",
        )
        require(response_id not in seen, f"duplicate response_id: {response_id}")
        seen.add(response_id)
        require(record.get("primary_sha256") == EXPECTED_HASH, f"primary hash mismatch for {response_id}")
        artifact_path = record.get("artifact_path")
        require(isinstance(artifact_path, str) and artifact_path.endswith(".pdf"), f"invalid artifact path for {response_id}")
        receiver_hash = record.get("receiver_verified_file_sha256")
        require(
            isinstance(receiver_hash, str) and re.fullmatch(r"[a-f0-9]{64}", receiver_hash),
            f"invalid receiver hash for {response_id}",
        )
    return len(records)


def main() -> None:
    page = read(PAGE)
    detail_page = read(DETAIL_PAGE)
    script = read(SCRIPT)
    detail_script = read(DETAIL_SCRIPT)
    manifest = json.loads(read(MANIFEST))
    responses = json.loads(read(RESPONSES))
    submission_schema = json.loads(read(SUBMISSION_SCHEMA))
    receiver_schema = json.loads(read(RECEIVER_SCHEMA))

    for marker in (
        "Humans as the Interoperability Layer",
        "Download Primary PDF",
        "Exact invocation prompt",
        "Prepare your Response PDF submission",
        "Published response record",
        "browser-local hash        != server custody",
        "submission                != publication",
    ):
        require(marker in page, f"page missing marker: {marker}")

    for marker in (
        "Published response projection",
        "Hash and chain references",
        "master-record inclusion    != shared model intent",
        "assets/hil-response.js",
    ):
        require(marker in detail_page, f"response detail page missing marker: {marker}")

    require(EXPECTED_PROMPT in page, "page prompt differs from canonical prompt")

    for marker in (
        EXPECTED_HASH,
        "data/hil-primary-v0.4.pdf.b64",
        "BROWSER_LOCAL_PREPARED_NOT_SUBMITTED",
        "transmitted: false",
        "custodied: false",
        "accepted: false",
        "published: false",
        "master_record_appended: false",
        "crypto.subtle.digest('SHA-256'",
        "header !== '%PDF-'",
        "data/hil-responses.json",
    ):
        require(marker in script, f"client script missing marker: {marker}")

    for marker in (
        "new URLSearchParams(window.location.search)",
        "data/hil-responses.json",
        "receiver_verified_file_sha256",
        "previous_record_sha256",
        "master_record_release",
    ):
        require(marker in detail_script, f"detail script missing marker: {marker}")

    require(manifest["primary_document"]["sha256"] == EXPECTED_HASH, "manifest primary hash mismatch")
    require(manifest["protocol"]["invocation_prompt"] == EXPECTED_PROMPT, "manifest prompt mismatch")
    require(manifest["authority"] == {
        "execution": False,
        "custody": False,
        "acceptance": False,
        "publication": False,
        "master_record_append": False,
    }, "manifest authority must remain fail-closed")

    require(responses["initiating_trace"]["trace_id"] == "HIL-TRACE-0001", "initiating trace ID mismatch")
    response_count = validate_response_index(responses)

    require(
        submission_schema["$id"] == "https://stegverse.org/schemas/hil-submission-v1.json",
        "submission schema ID mismatch",
    )
    state_values = submission_schema["properties"]["state"]["enum"]
    require("QUARANTINED" in state_values and "PUBLISHED" in state_values, "submission schema lacks required states")

    require(
        receiver_schema["$id"] == "https://stegverse.org/schemas/hil-receiver-receipt-v1.json",
        "receiver schema ID mismatch",
    )
    require(
        receiver_schema["properties"]["authority"]["properties"]["execution"]["const"] is False,
        "receiver receipt must not grant execution authority",
    )

    artifact_state = verify_primary_artifact()
    declared_state = manifest["primary_document"]["artifact_state"]
    require(
        declared_state == artifact_state,
        f"manifest artifact_state={declared_state} but observed state={artifact_state}",
    )

    require(not re.search(r"authority\s*[:=]\s*true", page, re.IGNORECASE), "page appears to claim authority")

    print("HIL_EXPERIMENT_STATIC_VERIFICATION=PASS")
    print(f"HIL_PRIMARY_ARTIFACT={artifact_state}")
    print(f"HIL_PRIMARY_SHA256={EXPECTED_HASH}")
    print(f"HIL_PUBLIC_RESPONSE_COUNT={response_count}")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
