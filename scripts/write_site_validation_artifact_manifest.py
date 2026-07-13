#!/usr/bin/env python3
"""Bind the canonical Site validation result and run receipt into one hash manifest.

The manifest is an artifact-integrity record only. It does not grant deployment,
release, endpoint, custody, admissibility, or RECORDED authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "site_application_validation.result.json"
RECEIPT_PATH = ROOT / "site_current_main_validation.receipt.json"
MANIFEST_PATH = ROOT / "site_current_main_validation.manifest.json"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    for path in (RESULT_PATH, RECEIPT_PATH):
        if not path.is_file():
            raise SystemExit(f"SITE_VALIDATION_MANIFEST_FAIL: missing {path.name}")

    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

    if result.get("passed") is not True or result.get("output") != "ECOSYSTEM_CHAT_APPLICATION_PASS":
        raise SystemExit("SITE_VALIDATION_MANIFEST_FAIL: canonical result is not passing")
    if receipt.get("state") != "VERIFIED" or receipt.get("conclusion") != "success":
        raise SystemExit("SITE_VALIDATION_MANIFEST_FAIL: run receipt is not verified")
    if receipt.get("result_artifact") != RESULT_PATH.name:
        raise SystemExit("SITE_VALIDATION_MANIFEST_FAIL: receipt result path mismatch")
    if receipt.get("result_sha256") != digest(RESULT_PATH):
        raise SystemExit("SITE_VALIDATION_MANIFEST_FAIL: receipt result hash mismatch")

    manifest = {
        "schema": "stegverse.site.current_main_validation_artifact_manifest.v1",
        "state": "COMPLETE",
        "repository": receipt.get("repository"),
        "commit_sha": receipt.get("commit_sha"),
        "workflow": receipt.get("workflow"),
        "job": receipt.get("job"),
        "run_id": receipt.get("run_id"),
        "run_attempt": receipt.get("run_attempt"),
        "validated_at": receipt.get("validated_at"),
        "files": [
            {
                "path": RESULT_PATH.name,
                "media_type": "application/json",
                "sha256": digest(RESULT_PATH),
            },
            {
                "path": RECEIPT_PATH.name,
                "media_type": "application/json",
                "sha256": digest(RECEIPT_PATH),
            },
        ],
        "verification_order": [
            "verify each file SHA-256",
            "verify receipt result_sha256 equals validation result SHA-256",
            "verify receipt commit and workflow identities",
            "verify canonical result output equals ECOSYSTEM_CHAT_APPLICATION_PASS",
        ],
        "authority_boundaries": {
            "manifest_is_release_authority": False,
            "manifest_is_deployment_evidence": False,
            "manifest_is_endpoint_live_evidence": False,
            "manifest_is_master_records_custody": False,
            "manifest_is_recorded_status": False,
        },
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("SITE_VALIDATION_ARTIFACT_MANIFEST_WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
