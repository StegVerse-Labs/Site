#!/usr/bin/env python3
"""Fail-closed validation for bounded user-LLM capability declarations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "user-llm-bounded-capabilities"
SOURCE_COMMIT = "64183d1ddad9bbbe9f063e2d3a83d06e162017d7"
EXPECTED_ROUTES = {
    "demo_test_suite": ["list", "inspect", "configure", "submit"],
    "entity_sandbox_runner": ["submit", "status", "retrieve_result"],
    "hil_response_packet": ["submit_pdf_metadata"],
}
FALSE_AUTHORITY = {
    "production_execution": False,
    "publication": False,
    "continuity": False,
    "custody": False,
    "site_activation": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "USER-LLM-BOUNDED-CAPABILITY-IMPORT-v1", f"{path}: schema mismatch")
    require(data.get("source_repository") == "StegVerse-org/LLM-adapter", f"{path}: source repository mismatch")
    require(data.get("source_commit") == SOURCE_COMMIT, f"{path}: source commit mismatch")
    require(data.get("capability_state") == "DECLARED_AND_TESTED_NOT_EXECUTION_PROVEN", f"{path}: capability state mismatch")
    require(data.get("routes") == EXPECTED_ROUTES, f"{path}: route declaration mismatch")
    semantics = data.get("routing_semantics") or {}
    require(semantics == {
        "missing_transport": "DEFER",
        "invalid_scope": "DENY",
        "successful_transport": "RETURNED",
        "authority_attached": False,
    }, f"{path}: routing semantics mismatch")
    require(data.get("execution_evidence_observed") is False, f"{path}: execution evidence must remain false")
    require(data.get("authority") == FALSE_AUTHORITY, f"{path}: authority escalation")


def main() -> None:
    if not IMPORT_DIR.exists():
        print("USER_LLM_BOUNDED_CAPABILITY_IMPORT=PASS pending_no_imports")
        return
    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("USER_LLM_BOUNDED_CAPABILITY_IMPORT=PASS pending_no_imports")
        return
    for path in files:
        validate(path)
    print(f"USER_LLM_BOUNDED_CAPABILITY_IMPORT=PASS imports={len(files)}")


if __name__ == "__main__":
    main()
