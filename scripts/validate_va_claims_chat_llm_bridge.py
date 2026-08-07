#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PROJECTION = ROOT / "api/va-claim-assistant/runtime-projection.json"
BRIDGE = ROOT / "assets/va-claims-chat-runtime.js"
CHAT = ROOT / "va-claims-chat.html"
TASK = ROOT / "data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json"


def require(value: bool, code: str) -> None:
    if not value:
        raise SystemExit(f"VA_CLAIMS_CHAT_LLM_BRIDGE_FAIL:{code}")


def sha256_shape(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value) is not None


def valid_active_projection(p: dict) -> bool:
    endpoint = p.get("endpoint")
    parsed = urlparse(endpoint) if isinstance(endpoint, str) else None
    return all(
        [
            p.get("schema") == "stegverse.va_claims_chat.runtime_projection.v1",
            p.get("capability") == "COORDINATED_VA_RESOURCES_LLM",
            p.get("state") == "VERIFIED",
            p.get("active") is True,
            parsed is not None and parsed.scheme == "https" and bool(parsed.netloc),
            p.get("endpoint_method") == "POST",
            sha256_shape(p.get("activation_receipt_sha256")),
            sha256_shape(p.get("execution_receipt_sha256")),
            p.get("custody_state") == "RECORDED",
            p.get("reconstruction_state") == "PASS",
            isinstance(p.get("evidence_refs"), list) and len(p["evidence_refs"]) > 0,
            p.get("private_document_upload_active") is False,
            p.get("private_document_retrieval_active") is False,
            p.get("filing_active") is False,
            p.get("authority_effect") is False,
            p.get("activation_effect") is False,
        ]
    )


def main() -> int:
    for path in (PROJECTION, BRIDGE, CHAT, TASK):
        require(path.is_file(), f"missing:{path.relative_to(ROOT)}")

    projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
    require(projection["schema"] == "stegverse.va_claims_chat.runtime_projection.v1", "projection_schema")
    require(projection["capability"] == "COORDINATED_VA_RESOURCES_LLM", "projection_capability")
    require(projection["active"] is False, "unverified_projection_must_be_inactive")
    require(projection["state"] in {"BLOCKED", "REVIEW_REQUIRED", "RETRY"}, "inactive_state")
    require(projection["endpoint"] is None, "inactive_endpoint_must_be_null")
    require(projection["activation_receipt_sha256"] is None, "inactive_activation_receipt")
    require(projection["execution_receipt_sha256"] is None, "inactive_execution_receipt")
    require(projection["private_document_upload_active"] is False, "upload_must_remain_off")
    require(projection["private_document_retrieval_active"] is False, "retrieval_must_remain_off")
    require(projection["filing_active"] is False, "filing_must_remain_off")
    require(projection["authority_effect"] is False, "projection_authority")
    require(projection["activation_effect"] is False, "projection_activation")
    require(not valid_active_projection(projection), "blocked_projection_cannot_activate")

    synthetic = dict(projection)
    synthetic.update(
        {
            "state": "VERIFIED",
            "active": True,
            "endpoint": "https://example.invalid/api/va-claims-chat",
            "activation_receipt_sha256": "a" * 64,
            "execution_receipt_sha256": "b" * 64,
            "custody_state": "RECORDED",
            "reconstruction_state": "PASS",
            "evidence_refs": ["receipt:test"],
        }
    )
    require(valid_active_projection(synthetic), "verified_fixture_should_activate")
    for field, bad in (
        ("endpoint", "http://example.invalid/api"),
        ("activation_receipt_sha256", None),
        ("execution_receipt_sha256", "short"),
        ("custody_state", "PENDING"),
        ("reconstruction_state", "PENDING"),
        ("authority_effect", True),
        ("activation_effect", True),
        ("private_document_upload_active", True),
        ("private_document_retrieval_active", True),
        ("filing_active", True),
    ):
        candidate = dict(synthetic)
        candidate[field] = bad
        require(not valid_active_projection(candidate), f"active_fixture_must_reject:{field}")

    bridge = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "validActiveProjection",
        "COORDINATED_VA_RESOURCES_LLM",
        "ADMITTED_OFFICIAL_VA_ONLY",
        "private_document_context:false",
        "filing_requested:false",
        "credentials:'omit'",
        "authority_effect===true",
        "activation_effect===true",
        "runtime_not_verified",
    ):
        require(marker in bridge, f"bridge_marker:{marker}")
    require("localStorage" not in bridge, "runtime_payload_must_not_use_localstorage")
    require("password" not in bridge.lower(), "bridge_password_marker")

    chat = CHAT.read_text(encoding="utf-8")
    require('src="assets/va-claims-chat-runtime.js"' in chat, "chat_bridge_include")
    require("Private document upload and automated claim filing remain disabled" in chat, "chat_disabled_boundary")
    require("SOURCE-GROUNDED PROCEDURAL HELP" in chat, "chat_truthful_inactive_label")

    task = json.loads(TASK.read_text(encoding="utf-8"))
    require(task["task_id"] == "SITE-VA-COORDINATED-LLM-BRIDGE-002", "task_id")
    require(task["state"] in {"CLAIMED", "COMPLETE", "BLOCKED"}, "task_state")
    require(task["authority_effect"] is False, "task_authority")
    require(task["activation_effect"] is False, "task_activation")

    print("VA_CLAIMS_CHAT_LLM_BRIDGE_PASS:BLOCKED_FAIL_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
