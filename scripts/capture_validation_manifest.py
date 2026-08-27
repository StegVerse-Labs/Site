#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "validation_manifests/repository-core.json"
SCHEMA_PATH = ROOT / "schemas/validation-execution-receipt.schema.json"
REPORTS = ROOT / "reports"
RECEIPT_PATH = REPORTS / "validation-execution-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    results = []
    overall_pass = True

    for validator in manifest["validators"]:
        log_path = ROOT / validator["log_path"]
        log_path.parent.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(
            validator["command"],
            cwd=ROOT,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log_path.write_text(proc.stdout or "", encoding="utf-8")
        if validator.get("required", True) and proc.returncode != 0:
            overall_pass = False
        results.append(
            {
                "id": validator["id"],
                "command": validator["command"],
                "exit_code": proc.returncode,
                "log_path": validator["log_path"],
                "sha256": sha256(log_path),
                "size_bytes": log_path.stat().st_size,
            }
        )

    receipt = {
        "schema_version": "ST-018-EXECUTION-RECEIPT-v1",
        "repository": manifest["repository"],
        "commit_sha": os.environ.get("GITHUB_SHA", "0" * 40),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "local"),
        "run_id": int(os.environ.get("GITHUB_RUN_ID", "1")),
        "run_attempt": int(os.environ.get("GITHUB_RUN_ATTEMPT", "1")),
        "status": "PASS" if overall_pass else "FAIL",
        "validators": results,
        "authority": manifest["authority"],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    try:
        from stegverse_jsonschema import validate
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validate(receipt, schema)
    except Exception as exc:
        print(f"receipt schema validation failed: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"status": receipt["status"], "receipt": str(RECEIPT_PATH.relative_to(ROOT))}))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
