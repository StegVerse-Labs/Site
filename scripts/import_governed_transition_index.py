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


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a receipted orchestration transition index.")
    parser.add_argument("--index", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--allow-local-fallback", action="store_true")
    args = parser.parse_args()

    if args.index is None or args.receipt is None:
        if not args.allow_local_fallback:
            return fail("--index and --receipt are required unless --allow-local-fallback is set")
        if not args.output.exists():
            return fail("local fallback index is missing")
        index = json.loads(args.output.read_text(encoding="utf-8"))
        error = validate_index(index)
        if error:
            return fail("local fallback invalid: " + error)
        status = {
            "schema_version": "1.0.0",
            "status_type": "governed_transition_index_import_status",
            "state": "LOCAL_FALLBACK_ACTIVE",
            "source": "data/governed-transition-index.json",
            "source_receipt": None,
            "source_commit": None,
            "hash_verified": False,
            "live_orchestration_feed": False,
            "authority_boundary": "Local fallback is a projection fixture and does not grant authority, custody, or reconstruction standing."
        }
        args.status.parent.mkdir(parents=True, exist_ok=True)
        args.status.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print("GOVERNED TRANSITION INDEX IMPORT: LOCAL_FALLBACK_ACTIVE")
        return 0

    if not args.index.exists() or not args.receipt.exists():
        return fail("index or receipt path does not exist")

    payload = args.index.read_bytes()
    index = json.loads(payload.decode("utf-8"))
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
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

    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.index, args.output)
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
        "live_orchestration_feed": False,
        "authority_boundary": "Verified artifact import does not grant execution, admissibility, Master-Records custody, or reconstruction standing."
    }
    args.status.parent.mkdir(parents=True, exist_ok=True)
    args.status.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"GOVERNED TRANSITION INDEX IMPORT: PASS ({len(index.get('records', []))} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
