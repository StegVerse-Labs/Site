import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_tvc_execution_receipt_import",
    ROOT / "scripts/check_tvc_execution_receipt_import.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def add_hash(receipt, field):
    receipt[field] = hashlib.sha256(canonical(receipt)).hexdigest()
    return receipt


def valid_bundle():
    grant_id = "grant-hil-001"
    result_hash = "a" * 64
    execution = add_hash(
        {
            "schema": "stegverse.execution_receipt.v1",
            "grant_id": grant_id,
            "grant_sha256": "b" * 64,
            "validation_decision": "ALLOW",
            "consumer": "tvc-hil-ingress",
            "scope": {
                "request_sha256": "c" * 64,
                "policy_sha256": "d" * 64,
                "action": "hil.intake.verify",
            },
            "result_status": "VERIFIED",
            "result_sha256": result_hash,
            "executed_at": "2026-08-02T09:30:00Z",
            "protected_values_observed": False,
            "scope_expanded": False,
        },
        "execution_receipt_sha256",
    )
    consumption_hash = "e" * 64
    consumption = {
        "schema": "stegverse.execution_grant_consumption_receipt.v1",
        "grant_id": grant_id,
        "result": "CONSUMED",
        "consumer": "tvc-hil-ingress",
        "consumed_at": "2026-08-02T09:30:00Z",
        "consumption_sha256": consumption_hash,
    }
    actual = add_hash(
        {
            "schema": "stegverse.service_actual_receipt.v1",
            "grant_id": grant_id,
            "execution_receipt_sha256": execution["execution_receipt_sha256"],
            "result_sha256": result_hash,
            "observed_at": "2026-08-02T09:30:00Z",
            "status": "VERIFIED",
        },
        "service_actual_sha256",
    )
    ledger = add_hash(
        {
            "schema": "stegverse.ledger_append_receipt.v1",
            "grant_id": grant_id,
            "consumption_sha256": consumption_hash,
            "service_actual_sha256": actual["service_actual_sha256"],
            "appended_at": "2026-08-02T09:30:00Z",
            "append_status": "READY_FOR_AUTHORITATIVE_APPEND",
        },
        "ledger_append_sha256",
    )
    returned = add_hash(
        {
            "schema": "stegverse.requester_return_receipt.v1",
            "grant_id": grant_id,
            "ledger_append_sha256": ledger["ledger_append_sha256"],
            "returned_at": "2026-08-02T09:30:00Z",
            "return_status": "READY_FOR_REQUESTER_RETURN",
        },
        "requester_return_sha256",
    )
    return {
        "schema": "stegverse.site.tvc_execution_receipt_import.v1",
        "source_repository": "StegVerse-Labs/TVC",
        "source_commit": "f" * 40,
        "execution_receipt": execution,
        "consumption_receipt": consumption,
        "service_actual_receipt": actual,
        "ledger_append_receipt": ledger,
        "requester_return_receipt": returned,
        "authority": {
            "site_activation": False,
            "execution": False,
            "publication": False,
            "release": False,
            "custody": False,
        },
    }


def test_valid_bundle_passes():
    MODULE.validate_bundle(valid_bundle())


def test_tampered_execution_hash_rejected():
    bundle = valid_bundle()
    bundle["execution_receipt"]["result_status"] = "ALTERED"
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "execution receipt hash mismatch" in str(exc)
    else:
        raise AssertionError("tampered execution receipt accepted")


def test_linkage_break_rejected():
    bundle = valid_bundle()
    bundle["service_actual_receipt"]["execution_receipt_sha256"] = "0" * 64
    bundle["service_actual_receipt"].pop("service_actual_sha256")
    add_hash(bundle["service_actual_receipt"], "service_actual_sha256")
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "execution linkage mismatch" in str(exc)
    else:
        raise AssertionError("broken chain accepted")


def test_authority_escalation_rejected():
    bundle = valid_bundle()
    bundle["authority"]["site_activation"] = True
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "must not grant site_activation authority" in str(exc)
    else:
        raise AssertionError("authority escalation accepted")


def test_protected_value_field_rejected():
    bundle = valid_bundle()
    bundle["execution_receipt"]["api_key"] = "not-a-real-secret"
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "protected field disclosed" in str(exc)
    else:
        raise AssertionError("protected field accepted")


def test_consumed_state_required():
    bundle = valid_bundle()
    bundle["consumption_receipt"]["result"] = "AVAILABLE"
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "one-time consumption" in str(exc)
    else:
        raise AssertionError("unconsumed grant accepted")


def test_invalid_source_commit_rejected():
    bundle = valid_bundle()
    bundle["source_commit"] = "main"
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "source_commit" in str(exc)
    else:
        raise AssertionError("unpinned source accepted")


def test_scope_expansion_rejected_even_with_recomputed_hash():
    bundle = valid_bundle()
    execution = bundle["execution_receipt"]
    execution["scope_expanded"] = True
    execution.pop("execution_receipt_sha256")
    add_hash(execution, "execution_receipt_sha256")
    try:
        MODULE.validate_bundle(bundle)
    except ValueError as exc:
        assert "scope expansion" in str(exc)
    else:
        raise AssertionError("scope expansion accepted")
