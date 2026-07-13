#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "governed-transition-index.json"
STATUS = ROOT / "data" / "governed-transition-index-import-status.json"
IMPORTER = ROOT / "scripts" / "import_governed_transition_index.py"


def fail(message: str) -> int:
    print(f"GOVERNED TRANSITION INDEX IMPORT: FAIL - {message}")
    return 1


def main() -> int:
    if not INDEX.exists() or not STATUS.exists() or not IMPORTER.exists():
        return fail("required import surface missing")

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    if index.get("projection_type") != "governed_transition_index":
        return fail("projection_type mismatch")
    if status.get("status_type") != "governed_transition_index_import_status":
        return fail("status_type mismatch")
    if status.get("state") not in {"LOCAL_FALLBACK_ACTIVE", "RECEIPTED_EXPORT_IMPORTED"}:
        return fail("unsupported import state")
    if status.get("state") == "LOCAL_FALLBACK_ACTIVE":
        if status.get("hash_verified") is not False or status.get("live_orchestration_feed") is not False:
            return fail("fallback must remain unverified and non-live")
        if status.get("source_receipt") is not None:
            return fail("fallback must not claim a source receipt")

    # Exercise a verified import in a temporary directory without mutating checked-in Site data.
    payload = INDEX.read_bytes()
    receipt = {
        "schema_version": "1.0.0",
        "receipt_type": "governed_transition_index_export_receipt",
        "export_id": "transition-index-export:test:1",
        "source_repository": "master-records/orchestration",
        "source_commit": "TEST_ONLY",
        "artifact_name": "governed-transition-index-export",
        "index_sha256": hashlib.sha256(payload).hexdigest(),
        "record_count": len(index.get("records", [])),
        "authority_boundary": {
            "export_receipt_is_final_transition_receipt": False,
            "export_receipt_is_master_records_admission": False,
            "site_import_grants_admissibility": False,
            "site_import_grants_execution_authority": False,
        },
    }
    executor_handoff = {
        "schema_version": "1.0.0",
        "record_type": "governed_executor_handoff",
        "handoff_id": "executor-handoff:test:1",
        "transition_id": "transition:test:1",
        "run_id": "run:test:1",
        "from_executor": {
            "executor_class": "EXTERNAL_NOTIFICATION_BOOTSTRAP",
            "status": "FALLBACK_ONLY",
        },
        "to_executor": {
            "executor_class": "STEGVERSE_AI_ENTITY",
            "status": "ACTIVE",
        },
        "activation": {
            "state": "ACTIVE",
            "activation_receipt_id": "executor-activation:test:1",
            "completed_checks": ["identity", "capability", "continuity"],
        },
        "authority_boundary": {
            "activation_requires_receipt": True,
            "declaration_grants_execution_authority": False,
        },
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        source = temp / "index.json"
        receipt_path = temp / "receipt.json"
        executor_handoff_path = temp / "executor-handoff.json"
        output = temp / "output.json"
        import_status = temp / "status.json"
        executor_output = temp / "executor-status.json"
        source.write_bytes(payload)
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        executor_handoff_path.write_text(json.dumps(executor_handoff), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(IMPORTER),
                "--index", str(source),
                "--receipt", str(receipt_path),
                "--executor-handoff", str(executor_handoff_path),
                "--output", str(output),
                "--status", str(import_status),
                "--executor-output", str(executor_output),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode != 0:
            return fail(completed.stdout.strip())
        imported_status = json.loads(import_status.read_text(encoding="utf-8"))
        imported_executor = json.loads(executor_output.read_text(encoding="utf-8"))
        if imported_status.get("state") != "RECEIPTED_EXPORT_IMPORTED":
            return fail("verified import did not produce receipted state")
        if imported_status.get("hash_verified") is not True:
            return fail("verified import did not preserve hash verification")
        if imported_status.get("executor_state_imported") is not True:
            return fail("verified import did not preserve executor import state")
        if imported_executor.get("projection_type") != "governed_executor_status":
            return fail("verified import did not produce executor status projection")
        if imported_executor.get("activation", {}).get("activation_receipt_id") != "executor-activation:test:1":
            return fail("verified import did not bind executor activation receipt")
        if imported_executor.get("authority_boundary", {}).get("projection_grants_execution_authority") is not False:
            return fail("executor projection may not grant execution authority")

    print("GOVERNED TRANSITION INDEX IMPORT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
