#!/usr/bin/env python3
"""Bind a successful Site validation result to the current GitHub Actions run.

This writer also executes the repository's ST-018 capture path so the canonical
Site Bootstrap workflow produces validation-evidence receipts before the
standalone native-main custody workflow is relied upon.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "site_application_validation.result.json"
RECEIPT_PATH = ROOT / "site_current_main_validation.receipt.json"
ST018_CAPTURE = ROOT / "scripts" / "capture_validation_manifest.py"
ST018_RECEIPT = ROOT / "reports" / "validation-execution-receipt.json"
ST018_LOG = ROOT / "reports" / "site-current-main-validation-evidence.log"


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"SITE_CURRENT_MAIN_RECEIPT_FAIL: missing environment variable {name}")
    return value


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if not RESULT_PATH.is_file():
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: validation result missing")

    raw = RESULT_PATH.read_bytes()
    result = json.loads(raw.decode("utf-8"))
    if result.get("passed") is not True or result.get("output") != "ECOSYSTEM_CHAT_APPLICATION_PASS":
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: validation result is not a passing canonical result")

    repository = require_env("GITHUB_REPOSITORY")
    sha = require_env("GITHUB_SHA")
    run_id = require_env("GITHUB_RUN_ID")
    run_attempt = require_env("GITHUB_RUN_ATTEMPT")
    workflow = require_env("GITHUB_WORKFLOW")
    job = require_env("GITHUB_JOB")
    ref = require_env("GITHUB_REF")
    event_name = require_env("GITHUB_EVENT_NAME")

    if repository != "StegVerse-Labs/Site":
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: unexpected repository identity")
    if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha.lower()):
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: invalid commit SHA")
    if not run_id.isdigit() or not run_attempt.isdigit():
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: invalid workflow run identity")

    capture = subprocess.run(
        [sys.executable, str(ST018_CAPTURE)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(capture.stdout, end="")
    if capture.returncode != 0:
        raise SystemExit(
            f"SITE_CURRENT_MAIN_RECEIPT_FAIL: ST-018 capture exited {capture.returncode}"
        )
    if not ST018_RECEIPT.is_file() or not ST018_LOG.is_file():
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: ST-018 evidence files missing")
    st018 = json.loads(ST018_RECEIPT.read_text(encoding="utf-8"))
    if st018.get("status") != "PASS":
        raise SystemExit("SITE_CURRENT_MAIN_RECEIPT_FAIL: ST-018 receipt is not PASS")

    receipt = {
        "schema": "stegverse.site.current_main_validation_receipt.v1",
        "state": "VERIFIED",
        "repository": repository,
        "commit_sha": sha,
        "ref": ref,
        "event_name": event_name,
        "workflow": workflow,
        "job": job,
        "run_id": int(run_id),
        "run_attempt": int(run_attempt),
        "conclusion": "success",
        "validated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result_artifact": RESULT_PATH.name,
        "result_sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "result_output": "ECOSYSTEM_CHAT_APPLICATION_PASS",
        "passed_command_count": len(result.get("passed_commands", [])),
        "live_route_verification_phase": result.get("live_route_verification_phase"),
        "st018": {
            "status": st018.get("status"),
            "receipt_path": str(ST018_RECEIPT.relative_to(ROOT)),
            "receipt_sha256": sha256(ST018_RECEIPT),
            "log_path": str(ST018_LOG.relative_to(ROOT)),
            "log_sha256": sha256(ST018_LOG),
            "validator_count": len(st018.get("validators", [])),
        },
        "authority_boundaries": {
            "receipt_is_release_authority": False,
            "receipt_is_deployment_evidence": False,
            "receipt_is_endpoint_live_evidence": False,
            "receipt_is_master_records_custody": False,
            "receipt_is_recorded_status": False,
        },
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("SITE_CURRENT_MAIN_VALIDATION_RECEIPT_WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
