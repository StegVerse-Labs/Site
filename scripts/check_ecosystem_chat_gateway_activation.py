#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "ecosystem-chat-gateway.json"
CLIENT = ROOT / "assets" / "ecosystem-chat-transition-identity.js"
HEALTH = ROOT / "assets" / "ecosystem-chat-gateway-health.js"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"


def fail(message: str) -> int:
    print(f"ECOSYSTEM CHAT GATEWAY ACTIVATION: FAIL - {message}")
    return 1


def main() -> int:
    for path in [CONFIG, CLIENT, HEALTH, LOADER]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    client = CLIENT.read_text(encoding="utf-8")
    health = HEALTH.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    if config.get("schema_version") != "1.0.0":
        return fail("schema_version mismatch")
    if config.get("mode") != "GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK":
        return fail("gateway mode mismatch")
    if config.get("fallback") != "LOCAL_CLASSIFICATION":
        return fail("fallback must remain LOCAL_CLASSIFICATION")
    endpoint = config.get("endpoint", "")
    health_endpoint = config.get("health_endpoint", "")
    if config.get("enabled") is True:
        if not endpoint.startswith("https://") or not endpoint.endswith("/api/ecosystem-chat"):
            return fail("enabled endpoint must be HTTPS and end with /api/ecosystem-chat")
        if not health_endpoint.startswith("https://") or not health_endpoint.endswith("/health"):
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
        "final_receipt_id",
        "lifecycle_state",
        "master_record_status",
        "master_record_ref",
        "reconstruction_status",
        "sqlite_persisted",
        "storage_durable_across_restarts",
        "custody_submission",
        "provider_status",
        "provider_receipt_id",
        "estimated_cost_usd",
        "provider_output_is_authority",
        "DETERMINISTIC_FALLBACK",
        "EPHEMERAL_HOST_STORAGE",
        "LOCAL_CLASSIFICATION",
        "AbortController",
    ]:
        if marker not in client:
            return fail(f"client missing marker: {marker}")
    for marker in [
        "Governed gateway",
        "LOCAL FALLBACK",
        "UNAVAILABLE",
        "repository mutation",
        "custody overclaim",
        "sqlite_transition_store",
        "storage_durable_across_restarts",
        "Master-Records submission",
        "governed_provider_enabled",
        "provider_output_is_authority",
        "provider_failure_falls_back",
        "provider credentials are not exposed",
    ]:
        if marker not in health:
            return fail(f"health indicator missing marker: {marker}")
    if "assets/ecosystem-chat-gateway-health.js" not in loader:
        return fail("health indicator is not loaded by Ecosystem Chat")
    print("ECOSYSTEM CHAT GATEWAY ACTIVATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
