#!/usr/bin/env python3
"""Validate the independent Site validation artifact bundle verifier."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_site_validation_artifact_bundle.py"


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    required = (
        "SITE_VALIDATION_ARTIFACT_BUNDLE_VERIFIED",
        "SITE_VALIDATION_BUNDLE_FAIL",
        "site_application_validation.result.json",
        "site_current_main_validation.receipt.json",
        "site_current_main_validation.manifest.json",
        "ECOSYSTEM_CHAT_APPLICATION_PASS",
        "stegverse.site.current_main_validation_receipt.v1",
        "stegverse.site.current_main_validation_artifact_manifest.v1",
        "manifest/receipt identity mismatch",
        "receipt result hash mismatch",
        "manifest exceeded authority boundary",
        "receipt exceeded authority boundary",
    )
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise SystemExit("SITE_VALIDATION_BUNDLE_VERIFIER_CHECK_FAIL: missing " + ", ".join(missing))
    forbidden = (
        "requests.", "urllib.request", "subprocess.run", "git push", "gh release",
        "repository_dispatch", "workflow_dispatch",
    )
    present = [marker for marker in forbidden if marker in text]
    if present:
        raise SystemExit("SITE_VALIDATION_BUNDLE_VERIFIER_CHECK_FAIL: forbidden capability " + ", ".join(present))
    print("SITE_VALIDATION_BUNDLE_VERIFIER_CHECK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
