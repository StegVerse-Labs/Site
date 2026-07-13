#!/usr/bin/env python3
"""Validate the deterministic Site validation artifact manifest writer."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_site_validation_artifact_manifest.py"


def fail(message: str) -> None:
    raise SystemExit(f"SITE_VALIDATION_MANIFEST_WRITER_FAIL: {message}")


def main() -> int:
    text = WRITER.read_text(encoding="utf-8")
    required = (
        "stegverse.site.current_main_validation_artifact_manifest.v1",
        "site_application_validation.result.json",
        "site_current_main_validation.receipt.json",
        "site_current_main_validation.manifest.json",
        "ECOSYSTEM_CHAT_APPLICATION_PASS",
        "receipt result hash mismatch",
        "sha256:",
        "verify each file SHA-256",
        "manifest_is_release_authority\": False",
        "manifest_is_deployment_evidence\": False",
        "manifest_is_endpoint_live_evidence\": False",
        "manifest_is_master_records_custody\": False",
        "manifest_is_recorded_status\": False",
        "SITE_VALIDATION_ARTIFACT_MANIFEST_WRITTEN",
    )
    missing = [marker for marker in required if marker not in text]
    if missing:
        fail("missing writer markers: " + ", ".join(missing))

    forbidden = (
        "git push",
        "gh release",
        "contents: write",
        "subprocess.run",
        "requests.",
    )
    present = [marker for marker in forbidden if marker in text]
    if present:
        fail("writer crossed artifact-only boundary: " + ", ".join(present))

    print("SITE_VALIDATION_MANIFEST_WRITER_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
