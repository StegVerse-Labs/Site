#!/usr/bin/env python3
"""Verify AI Entry validation stabilization index."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "ai-entry-validation-stabilization.json"
EXPECTED_CLASSES = {
    "route_precedence",
    "optional_dependency_import",
    "pytest_helper_compatibility",
}


def fail(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_VALIDATION_STABILIZATION_FAIL: {message}")


def main() -> int:
    if not INDEX.exists():
        fail("missing stabilization index")
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if data.get("schema_version") != "stegverse.ai_entry.validation_stabilization.v0.1":
        fail("bad schema version")
    classes = {item.get("failure_class") for item in data.get("failure_classes_repaired", [])}
    if classes != EXPECTED_CLASSES:
        fail("failure class set mismatch")
    for item in data.get("failure_classes_repaired", []):
        checks = item.get("automated_checks", [])
        if not checks:
            fail(f"{item.get('failure_class')} missing automated checks")
        for check in checks:
            if not isinstance(check, str) or not check:
                fail("invalid automated check entry")
    boundary = data.get("current_boundary", {})
    for key in ("live_provider_calls_enabled", "live_sdk_calls_enabled", "execution_authority_issued", "real_receipt_issued"):
        if boundary.get(key) is not False:
            fail(f"{key} must be false")
    print("AI_ENTRY_VALIDATION_STABILIZATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
