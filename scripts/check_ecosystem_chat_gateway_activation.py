#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "ecosystem-chat-gateway.json"
CLIENT = ROOT / "assets" / "ecosystem-chat-transition-identity.js"


def fail(message: str) -> int:
    print(f"ECOSYSTEM CHAT GATEWAY ACTIVATION: FAIL - {message}")
    return 1


def main() -> int:
    if not CONFIG.exists() or not CLIENT.exists():
        return fail("gateway config or client missing")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    client = CLIENT.read_text(encoding="utf-8")
    if config.get("schema_version") != "1.0.0":
        return fail("schema_version mismatch")
    if config.get("mode") != "GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK":
        return fail("gateway mode mismatch")
    if config.get("fallback") != "LOCAL_CLASSIFICATION":
        return fail("fallback must remain LOCAL_CLASSIFICATION")
    endpoint = config.get("endpoint", "")
    health = config.get("health_endpoint", "")
    if config.get("enabled") is True:
        if not endpoint.startswith("https://") or not endpoint.endswith("/api/ecosystem-chat"):
            return fail("enabled endpoint must be HTTPS and end with /api/ecosystem-chat")
        if not health.startswith("https://") or not health.endswith("/health"):
            return fail("enabled health endpoint must be HTTPS and end with /health")
    boundary = config.get("authority_boundary", {})
    for key in [
        "site_execution_authority",
        "gateway_execution_authority",
        "gateway_receipt_is_final",
        "master_records_authority",
    ]:
        if boundary.get(key) is not False:
            return fail(f"authority boundary must be false: {key}")
    for marker in [
        "transition_identity",
        "identity mismatch",
        "gateway_receipt_id",
        "final_receipt=false",
        "LOCAL_CLASSIFICATION",
        "AbortController",
    ]:
        if marker not in client:
            return fail(f"client missing marker: {marker}")
    print("ECOSYSTEM CHAT GATEWAY ACTIVATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
