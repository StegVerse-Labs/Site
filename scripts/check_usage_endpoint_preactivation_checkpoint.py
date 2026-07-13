#!/usr/bin/env python3
"""Validate that Site preparation is complete without claiming endpoint activation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "data" / "usage-endpoint-preactivation-checkpoint.json"
LEDGER = ROOT / "data" / "usage-endpoint-activation-evidence.json"
CONFIG = ROOT / "data" / "ecosystem-usage-config.json"
CONTRACT = ROOT / "data" / "ecosystem-usage-live-contract.json"


def fail(message: str) -> None:
    raise SystemExit(f"USAGE_ENDPOINT_PREACTIVATION_CHECKPOINT_FAIL: {message}")


def main() -> int:
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if checkpoint.get("schema") != "stegverse.site.usage_endpoint_preactivation_checkpoint.v1":
        fail("schema drift")
    if checkpoint.get("state") != "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED":
        fail("checkpoint state drift")
    if checkpoint.get("repository") != "StegVerse-Labs/Site":
        fail("repository identity drift")

    required_completed = {
        "authenticated retrieval contract",
        "fail-closed browser client",
        "public ledger client loading",
        "disabled transport configuration",
        "destination handoff packet",
        "positive and negative endpoint conformance suite",
        "activation evidence ledger",
        "canonical validation integration",
    }
    if set(checkpoint.get("completed_site_scope", [])) != required_completed:
        fail("completed Site scope drift")

    posture = checkpoint.get("configuration_posture", {})
    if posture.get("usage_api_base") is not None:
        fail("checkpoint configures an endpoint")
    if posture.get("live_transport_enabled") is not False:
        fail("checkpoint enables live transport")
    if posture.get("contract_status") != "PREPARED_NOT_DEPLOYED":
        fail("checkpoint claims deployment")
    if posture.get("activation_evidence_state") != "BLOCKED":
        fail("checkpoint claims activation readiness")

    if config.get("usage_api_base") is not None:
        fail("current config has an endpoint while blocked")
    if config.get("live_transport", {}).get("enabled") is not False:
        fail("current config has live transport enabled while blocked")
    if contract.get("status") != "PREPARED_NOT_DEPLOYED":
        fail("current contract claims deployment")
    if ledger.get("state") != "BLOCKED":
        fail("activation ledger is not blocked")

    claims = checkpoint.get("claims", {})
    if any(value is not False for value in claims.values()):
        fail("checkpoint exceeds preactivation authority")

    continuation = checkpoint.get("continuation", {})
    if continuation.get("next_repository") != "StegVerse-org/LLM-adapter":
        fail("continuation repository drift")
    if continuation.get("site_resume_condition") != "all activation evidence requirements are VERIFIED":
        fail("Site resume condition drift")

    if not checkpoint.get("unmet_external_or_live_prerequisites"):
        fail("blocked checkpoint must preserve unmet prerequisites")

    print("USAGE_ENDPOINT_PREACTIVATION_CHECKPOINT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
