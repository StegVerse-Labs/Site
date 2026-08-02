#!/usr/bin/env python3
"""Validate a sanitized TVC execution receipt bundle before Site projection.

This validator verifies canonical hashes and linkage across the execution, service-actual,
ledger, and requester-return receipts. It rejects protected-value disclosure and all
attempts to convert imported evidence into Site, execution, publication, release, or
custody authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
PROTECTED_KEYS = {
    "token", "secret", "password", "credential", "api_key", "apikey",
    "authorization", "private_key", "protected_value", "protected_values"
}
AUTHORITY_KEYS = ("site_activation", "execution", "publication", "release", "custody")


def canonical(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_without(value: Mapping[str, Any], field: str) -> str:
    body = dict(value)
    body.pop(field, None)
    return hashlib.sha256(canonical(body)).hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def reject_protected_values(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = key.lower().replace("-", "_")
            if normalized in PROTECTED_KEYS or any(part in normalized for part in ("secret", "password", "credential", "private_key")):
                fail(f"protected field disclosed at {path}.{key}")
            reject_protected_values(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_protected_values(item, f"{path}[{index}]")


def require_sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        fail(f"{field} must be lowercase sha256")
    return value


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be non-empty text")
    return value


def validate_bundle(data: Mapping[str, Any]) -> None:
    reject_protected_values(data)
    if data.get("schema") != "stegverse.site.tvc_execution_receipt_import.v1":
        fail("unexpected import schema")
    if data.get("source_repository") != "StegVerse-Labs/TVC":
        fail("unexpected source repository")
    source_commit = data.get("source_commit")
    if not isinstance(source_commit, str) or not COMMIT_RE.fullmatch(source_commit):
        fail("source_commit must be a 40-character lowercase git sha")

    authority = data.get("authority")
    if not isinstance(authority, dict) or set(authority) != set(AUTHORITY_KEYS):
        fail("authority object must contain exactly the five bounded authority fields")
    for key in AUTHORITY_KEYS:
        if authority.get(key) is not False:
            fail(f"import must not grant {key} authority")

    execution = data.get("execution_receipt")
    consumption = data.get("consumption_receipt")
    actual = data.get("service_actual_receipt")
    ledger = data.get("ledger_append_receipt")
    returned = data.get("requester_return_receipt")
    for name, receipt in (
        ("execution_receipt", execution),
        ("consumption_receipt", consumption),
        ("service_actual_receipt", actual),
        ("ledger_append_receipt", ledger),
        ("requester_return_receipt", returned),
    ):
        if not isinstance(receipt, dict):
            fail(f"{name} must be an object")

    if execution.get("schema") != "stegverse.execution_receipt.v1":
        fail("unexpected execution receipt schema")
    if execution.get("validation_decision") != "ALLOW":
        fail("execution receipt was not independently allowed")
    if execution.get("protected_values_observed") is not False:
        fail("execution receipt observed protected values")
    if execution.get("scope_expanded") is not False:
        fail("execution scope expansion is prohibited")
    require_text(execution.get("consumer"), "execution.consumer")
    if not isinstance(execution.get("scope"), dict) or not execution["scope"]:
        fail("execution scope must be a non-empty object")
    for key, value in execution["scope"].items():
        require_text(key, "execution.scope key")
        require_text(value, f"execution.scope.{key}")
    require_sha(execution.get("grant_sha256"), "execution.grant_sha256")
    require_sha(execution.get("result_sha256"), "execution.result_sha256")
    execution_hash = require_sha(execution.get("execution_receipt_sha256"), "execution.execution_receipt_sha256")
    if digest_without(execution, "execution_receipt_sha256") != execution_hash:
        fail("execution receipt hash mismatch")

    grant_id = require_text(execution.get("grant_id"), "execution.grant_id")
    if consumption.get("grant_id") != grant_id or consumption.get("result") != "CONSUMED":
        fail("consumption receipt is not a matching one-time consumption")
    consumption_hash = require_sha(consumption.get("consumption_sha256"), "consumption.consumption_sha256")

    if actual.get("schema") != "stegverse.service_actual_receipt.v1":
        fail("unexpected service actual schema")
    if actual.get("grant_id") != grant_id:
        fail("service actual grant linkage mismatch")
    if actual.get("execution_receipt_sha256") != execution_hash:
        fail("service actual execution linkage mismatch")
    if actual.get("result_sha256") != execution.get("result_sha256"):
        fail("service actual result linkage mismatch")
    actual_hash = require_sha(actual.get("service_actual_sha256"), "actual.service_actual_sha256")
    if digest_without(actual, "service_actual_sha256") != actual_hash:
        fail("service actual receipt hash mismatch")

    if ledger.get("schema") != "stegverse.ledger_append_receipt.v1":
        fail("unexpected ledger receipt schema")
    if ledger.get("grant_id") != grant_id:
        fail("ledger grant linkage mismatch")
    if ledger.get("consumption_sha256") != consumption_hash:
        fail("ledger consumption linkage mismatch")
    if ledger.get("service_actual_sha256") != actual_hash:
        fail("ledger service-actual linkage mismatch")
    if ledger.get("append_status") != "READY_FOR_AUTHORITATIVE_APPEND":
        fail("ledger receipt is not bounded to authoritative append readiness")
    ledger_hash = require_sha(ledger.get("ledger_append_sha256"), "ledger.ledger_append_sha256")
    if digest_without(ledger, "ledger_append_sha256") != ledger_hash:
        fail("ledger append receipt hash mismatch")

    if returned.get("schema") != "stegverse.requester_return_receipt.v1":
        fail("unexpected requester return schema")
    if returned.get("grant_id") != grant_id:
        fail("requester return grant linkage mismatch")
    if returned.get("ledger_append_sha256") != ledger_hash:
        fail("requester return ledger linkage mismatch")
    if returned.get("return_status") != "READY_FOR_REQUESTER_RETURN":
        fail("requester return is not bounded readiness")
    returned_hash = require_sha(returned.get("requester_return_sha256"), "returned.requester_return_sha256")
    if digest_without(returned, "requester_return_sha256") != returned_hash:
        fail("requester return receipt hash mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    data = json.loads(args.path.read_text())
    validate_bundle(data)
    print("PASS: sanitized TVC execution receipt import is hash-bound, linked, non-secret, and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
