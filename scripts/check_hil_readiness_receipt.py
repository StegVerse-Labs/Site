#!/usr/bin/env python3
"""Fail-closed validator for imported HIL bounded readiness observations."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RECEIPT = Path("data/hil-readiness/HIL-LIVE-READINESS-OBSERVATION-v2-run-30173147748.json")
EXPECTED_PRIMARY = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
EXPECTED_PROMPT = "0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    supplied_hash = payload.pop("observation_sha256", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(hashlib.sha256(canonical).hexdigest() == supplied_hash, "receipt hash mismatch")
    require(payload.get("schema_version") == "HIL-LIVE-READINESS-OBSERVATION-v2", "schema mismatch")
    require(payload.get("observation_scope") == "GITHUB_HOSTED_EPHEMERAL_DEPLOYMENT_PROOF", "scope mismatch")
    require(payload.get("observed_state") == "CONTROLLED_CYCLE_READY", "readiness state mismatch")
    require(payload.get("credential_separation_verified") is True, "credential separation not established")
    require(payload.get("durable_path_reused_across_process_restart") is True, "restart path reuse not established")
    require(payload.get("external_production_deployment_claimed") is False, "invalid production claim")
    require(payload.get("authority_granted") is False, "invalid authority claim")
    before = payload.get("intake_before_restart", {})
    after = payload.get("intake_after_restart", {})
    publication = payload.get("publication_after_restart", {})
    require(before.get("state") == after.get("state") == "READY", "intake readiness mismatch")
    require(publication.get("state") == "READY", "publication readiness mismatch")
    require(before.get("primary_sha256") == after.get("primary_sha256") == EXPECTED_PRIMARY, "primary mismatch")
    require(before.get("prompt_sha256") == after.get("prompt_sha256") == EXPECTED_PROMPT, "prompt mismatch")
    require(publication.get("append_only") is True, "publication is not append-only")
    require(publication.get("master_record_append_authority") is False, "master-record authority overclaim")
    print("HIL bounded readiness receipt: PASS")


if __name__ == "__main__":
    main()
