#!/usr/bin/env python3
"""Verify StegVerse AI Entry readiness manifest and disabled-live boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "ecosystem-chat-ai-entry-readiness.json"

REQUIRED_INSTALLED = {
    "route_manifest",
    "deterministic_backend_scaffold",
    "browser_adapter",
    "api_wrapper",
    "provider_adapter_manifest",
    "sdk_access_boundary",
    "receipt_preview",
}

REQUIRED_DISABLED = {
    "live_provider_calls",
    "live_sdk_calls",
    "credential_surface",
    "execution_authority",
    "real_receipt_issuance",
    "reconstruction_claims",
    "repo_mutation",
}


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_READINESS_FAIL: {message}")


def main() -> int:
    if not READINESS.exists():
        fail("missing readiness manifest")
    manifest = json.loads(READINESS.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "stegverse.ecosystem_chat.ai_entry_readiness.v0.1":
        fail("bad schema_version")
    if manifest.get("status") != "local_ready_live_disabled":
        fail("status must be local_ready_live_disabled")
    if manifest.get("canonical_validation_command") != "python scripts/check_ecosystem_chat_ai_entry.py":
        fail("bad canonical validation command")

    installed = manifest.get("installed_boundaries", {})
    if set(installed) != REQUIRED_INSTALLED:
        fail("installed boundary keys mismatch")
    for key, value in installed.items():
        if value is not True:
            fail(f"installed boundary {key} must be true")

    disabled = manifest.get("disabled_until_governed_activation", {})
    if set(disabled) != REQUIRED_DISABLED:
        fail("disabled boundary keys mismatch")
    for key, value in disabled.items():
        if value is not True:
            fail(f"disabled boundary {key} must be true")

    requirements = manifest.get("next_activation_requirements", [])
    if not isinstance(requirements, list) or len(requirements) < 5:
        fail("next_activation_requirements must be detailed")
    joined = "\n".join(requirements).lower()
    for phrase in ("secret boundary", "sdk receipt", "comparison-only", "real receipts"):
        if phrase not in joined:
            fail(f"activation requirements missing phrase: {phrase}")

    print("ECOSYSTEM_CHAT_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
