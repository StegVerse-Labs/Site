#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "governed-transition-index.json"
DEFAULT_STATUS = ROOT / "data" / "governed-transition-index-import-status.json"
DEFAULT_EXECUTOR_OUTPUT = ROOT / "data" / "governed-executor-status.json"


def fail(message: str) -> int:
    print(f"GOVERNED TRANSITION INDEX IMPORT: FAIL - {message}")
    return 1


def validate_index(index: dict) -> str | None:
    if index.get("schema_version") != "1.0.0":
        return "schema_version must be 1.0.0"
    if index.get("projection_type") != "governed_transition_index":
        return "projection_type mismatch"
    if not isinstance(index.get("records"), list):
        return "records must be a list"
    return None


def project_executor_handoff(handoff: dict) -> dict:
    if handoff.get("record_type") != "governed_executor_handoff":
        raise ValueError("executor handoff record_type mismatch")
    activation = handoff.get("activation", {})
    target = handoff.get("to_executor", {})
    source = handoff.get("from_executor", {})
    if activation.get("state") != "ACTIVE":
        raise ValueError("executor handoff must be ACTIVE")
    if not activation.get("activation_receipt_id"):
        raise ValueError("ACTIVE executor handoff requires activation_receipt_id")
    if target.get("executor_class") != "STEGVERSE_AI_ENTITY" or target.get("status") != "ACTIVE":
        raise ValueError("native executor must be ACTIVE")
    if source.get("executor_class") != "EXTERNAL_NOTIFICATION_BOOTSTRAP" or source.get("status") != "FALLBACK_ONLY":
        raise ValueError("bootstrap executor must be FALLBACK_ONLY")
    boundary = handoff.get("authority_boundary", {})
    if boundary.get("activation_requires_receipt") is not True:
        raise ValueError("activation receipt boundary missing")
    if boundary.get("declaration_grants_execution_authority") is not False:
        raise ValueError("handoff may not grant execution authority")
    return {
        "schema_version": "1.0.0",
        "projection_type": "governed_executor_status",
        "source_repository": "master-records/orchestration",
        "handoff_id": handoff.get("handoff_id"),
        "transition_id": handoff.get("transition_id"),
        "run_id": handoff.get("run_id"),
        "from_executor": source,
        "to_executor": target,
        "activation": {
            "state": activation.get("state"),
            "activation_receipt_id": activation.get("activation_receipt_id"),
            "completed_checks": activation.get("completed_checks", []),
        },
        "authority_boundary": {
            "projection_grants_execution_authority": False,
            "projection_grants_publication_authority": False,
            "projection_grants_admissibility": False,
            "projection_is_master_records_custody": False,
            "activation_is_per_transition_authority": False,
        },
        "projection_note": "Derived projection of a receipted orchestration executor state. Site does not activate executors or grant task authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a receipted orchestration transition index.")
    parser.add_argument("--index", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--executor-handoff", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--executor-output", type=Path, default=DEFAULT_EXECUTOR_OUTPUT)
    parser.add_argument("--allow-local-fallback", action="store_true")
    args = parser.parse_args()

    if args.index is None or args.receipt is None:
        if not args.allow_local_fallback:
            return fail("--index and --receipt are required unless --allow-local-fallback is set")
        if not args.output.exists() or not args.executor_output.exists():
            return fail("local fallback projection is missing")
        index = json.loads(args.output.read_text(encoding="utf-8"))
        executor = json.loads(args.executor_output.read_text(encoding="utf-8"))
        error = validate_index(index)
        if error:
            return fail("local fallback invalid: " + error)
        if executor.get("projection_type") != "governed_executor_status":
            return fail("local executor fallback invalid")
        status = {
            "schema_version": "1.0.0",
            "status_type": "governed_transition_index_import_status",
            "state": "LOCAL_FALLBACK_ACTIVE",
            "source": "data/governed-transition-index.json",
            "source_receipt": None,
            "source_commit": None,
            "hash_verified": False,
            "executor_state_imported": True,
            "executor_activation_receipt_id": executor.get("activation", {}).get("activation_receipt_id"),
            "live_orchestration_feed": False,
            "authority_boundary": "Local fallback is a projection fixture and does not grant authority, custody, or reconstruction standing."
        }
        args.status.parent.mkdir(parents=True, exist_ok=True)
        args.status.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print("GOVERNED TRANSITION INDEX IMPORT: LOCAL_FALLBACK_ACTIVE")
        return 0

    if not args.index.exists() or not args.receipt.exists():
        return fail("index or receipt path does not exist")
    if args.executor_handoff is None or not args.executor_handoff.exists():
        return fail("executor handoff path is required for receipted import")

    payload = args.index.read_bytes()
    index = json.loads(payload.decode("utf-8"))
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    handoff = json.loads(args.executor_handoff.read_text(encoding="utf-8"))
    error = validate_index(index)
    if error:
        return fail(error)
    if receipt.get("receipt_type") != "governed_transition_index_export_receipt":
        return fail("receipt_type mismatch")
    if receipt.get("artifact_name") != "governed-transition-index-export":
        return fail("artifact_name mismatch")
    digest = hashlib.sha256(payload).hexdigest()
    if receipt.get("index_sha256") != digest:
        return fail("index hash does not match export receipt")
    if receipt.get("record_count") != len(index.get("records", [])):
        return fail("record_count mismatch")
    boundary = receipt.get("authority_boundary", {})
    if any(boundary.get(key) is not False for key in [
        "export_receipt_is_final_transition_receipt",
        "export_receipt_is_master_records_admission",
        "site_import_grants_admissibility",
        "site_import_grants_execution_authority",
    ]):
        return fail("export receipt authority boundary invalid")
    try:
        executor_projection = project_executor_handoff(handoff)
    except ValueError as exc:
        return fail(str(exc))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.index, args.output)
    args.executor_output.parent.mkdir(parents=True, exist_ok=True)
    args.executor_output.write_text(json.dumps(executor_projection, indent=2) + "\n", encoding="utf-8")
    status = {
        "schema_version": "1.0.0",
        "status_type": "governed_transition_index_import_status",
        "state": "RECEIPTED_EXPORT_IMPORTED",
        "source": receipt.get("source_repository"),
        "source_receipt": receipt.get("export_id"),
        "source_commit": receipt.get("source_commit"),
        "hash_verified": True,
        "index_sha256": digest,
        "record_count": len(index.get("records", [])),
        "executor_state_imported": True,
        "executor_activation_receipt_id": executor_projection["activation"]["activation_receipt_id"],
        "live_orchestration_feed": False,
        "authority_boundary": "Verified artifact import does not grant execution, admissibility, Master-Records custody, executor activation, or reconstruction standing."
    }
    args.status.parent.mkdir(parents=True, exist_ok=True)
    args.status.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"GOVERNED TRANSITION INDEX IMPORT: PASS ({len(index.get('records', []))} record(s), executor ACTIVE)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
