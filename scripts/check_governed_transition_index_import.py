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
            "site_import_grants_execution_authority": False
        }
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        source = temp / "index.json"
        receipt_path = temp / "receipt.json"
        output = temp / "output.json"
        import_status = temp / "status.json"
        source.write_bytes(payload)
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(IMPORTER),
                "--index", str(source),
                "--receipt", str(receipt_path),
                "--output", str(output),
                "--status", str(import_status),
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
        if imported_status.get("state") != "RECEIPTED_EXPORT_IMPORTED":
            return fail("verified import did not produce receipted state")
        if imported_status.get("hash_verified") is not True:
            return fail("verified import did not preserve hash verification")

    print("GOVERNED TRANSITION INDEX IMPORT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
