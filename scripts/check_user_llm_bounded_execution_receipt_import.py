#!/usr/bin/env python3
"""Fail-closed validation for bounded user-LLM execution receipt imports."""
from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "user-llm-bounded-execution-receipts"
ROUTE_SCOPES = {
    "demo_test_suite": {
        "list": "demo:read",
        "inspect": "demo:read",
        "configure": "demo:submit",
        "submit": "demo:submit",
    },
    "entity_sandbox_runner": {
        "submit": "sandbox:submit",
        "status": "sandbox:read",
        "retrieve_result": "sandbox:read",
    },
    "hil_response_packet": {"submit_pdf_metadata": "hil:submit"},
}
FALSE_CLAIMS = {
    "production_execution": False,
    "publication": False,
    "continuity": False,
    "custody": False,
    "master_record_release": False,
    "site_activation": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def is_hex(value: object, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and all(c in "0123456789abcdef" for c in value)


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "USER-LLM-BOUNDED-EXECUTION-RECEIPT-IMPORT-v1", f"{path}: schema mismatch")
    require(data.get("source_repository") == "StegVerse-org/LLM-adapter", f"{path}: source repository mismatch")
    require(is_hex(data.get("source_commit"), 40), f"{path}: invalid source commit")
    require(is_hex(data.get("source_evidence_sha256"), 64), f"{path}: invalid source evidence hash")
    evidence_path = data.get("source_evidence_path")
    require(isinstance(evidence_path, str) and evidence_path.startswith("receipts/user-llm-bounded-execution/") and evidence_path.endswith(".json"), f"{path}: invalid evidence path")

    route = data.get("route")
    action = data.get("action")
    require(route in ROUTE_SCOPES, f"{path}: unsupported route")
    require(action in ROUTE_SCOPES[route], f"{path}: unsupported action")
    require(data.get("required_scope") == ROUTE_SCOPES[route][action], f"{path}: route scope mismatch")
    require(is_hex(data.get("request_hash"), 64), f"{path}: invalid request hash")
    require(is_hex(data.get("result_hash"), 64), f"{path}: invalid result hash")
    require(data.get("status") == "RETURNED", f"{path}: only RETURNED proves bounded execution")
    require(data.get("transport_configured") is True, f"{path}: configured transport not proven")
    require(data.get("execution_observed") is True, f"{path}: execution not observed")
    require(data.get("authority_attached") is False, f"{path}: authority attached")
    require(data.get("claims") == FALSE_CLAIMS, f"{path}: claim or authority escalation")

    endpoint = data.get("transport_endpoint")
    if endpoint is not None:
        require(isinstance(endpoint, str), f"{path}: transport endpoint must be a string")
        parsed = urlparse(endpoint)
        require(parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password, f"{path}: transport endpoint must be credential-free HTTPS")
        require(not parsed.query and not parsed.fragment, f"{path}: endpoint query or fragment forbidden")
        try:
            ip = ipaddress.ip_address(parsed.hostname)
        except ValueError:
            ip = None
        require(ip is None or (ip.is_global and not ip.is_multicast), f"{path}: non-public transport endpoint")


def main() -> None:
    if not IMPORT_DIR.exists():
        print("USER_LLM_BOUNDED_EXECUTION_RECEIPT_IMPORT=PASS pending_no_imports")
        return
    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("USER_LLM_BOUNDED_EXECUTION_RECEIPT_IMPORT=PASS pending_no_imports")
        return
    for path in files:
        validate(path)
    print(f"USER_LLM_BOUNDED_EXECUTION_RECEIPT_IMPORT=PASS imports={len(files)}")


if __name__ == "__main__":
    main()
