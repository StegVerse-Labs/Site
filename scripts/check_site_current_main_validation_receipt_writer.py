#!/usr/bin/env python3
"""Validate the deterministic current-main validation receipt writer."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_site_current_main_validation_receipt.py"


def fail(message: str) -> None:
    raise SystemExit(f"SITE_CURRENT_MAIN_RECEIPT_WRITER_FAIL: {message}")


def main() -> int:
    text = WRITER.read_text(encoding="utf-8")
    required = (
        '"stegverse.site.current_main_validation_receipt.v1"',
        '"state": "VERIFIED"',
        'require_env("GITHUB_REPOSITORY")',
        'require_env("GITHUB_SHA")',
        'require_env("GITHUB_RUN_ID")',
        'require_env("GITHUB_RUN_ATTEMPT")',
        'require_env("GITHUB_WORKFLOW")',
        'require_env("GITHUB_JOB")',
        'require_env("GITHUB_REF")',
        'require_env("GITHUB_EVENT_NAME")',
        'result.get("passed") is not True',
        'result.get("output") != "ECOSYSTEM_CHAT_APPLICATION_PASS"',
        'hashlib.sha256(raw).hexdigest()',
        '"conclusion": "success"',
        '"receipt_is_release_authority": False',
        '"receipt_is_deployment_evidence": False',
        '"receipt_is_endpoint_live_evidence": False',
        '"receipt_is_master_records_custody": False',
        '"receipt_is_recorded_status": False',
        'SITE_CURRENT_MAIN_VALIDATION_RECEIPT_WRITTEN',
    )
    missing = [marker for marker in required if marker not in text]
    if missing:
        fail("missing writer invariants: " + ", ".join(missing))

    forbidden = (
        "git push",
        "gh release",
        "contents: write",
        "subprocess.run",
        "requests.post",
    )
    present = [marker for marker in forbidden if marker in text]
    if present:
        fail("writer crossed authority boundary: " + ", ".join(present))

    print("SITE_CURRENT_MAIN_RECEIPT_WRITER_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
