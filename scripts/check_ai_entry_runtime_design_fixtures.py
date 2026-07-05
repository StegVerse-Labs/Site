#!/usr/bin/env python3
"""Verify AI Entry runtime design fixtures remain design-only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "fixtures" / "ecosystem-chat" / "runtime-design-request.example.json"
RESPONSE = ROOT / "fixtures" / "ecosystem-chat" / "runtime-design-response.example.json"
FALSE_KEYS = (
    "provider_ready",
    "sdk_ready",
    "credential_ready",
    "authority_ready",
    "receipt_ready",
    "activation_ready",
    "execution_ready",
    "repo_write_ready",
)


def stop(message: str) -> None:
    raise SystemExit(f"AI_ENTRY_RUNTIME_DESIGN_FIXTURES_FAIL: {message}")


def main() -> int:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    response = json.loads(RESPONSE.read_text(encoding="utf-8"))
    if request.get("schema_version") != "stegverse.ai_entry.runtime_design_request.v0.1":
        stop("bad request schema version")
    if response.get("schema_version") != "stegverse.ai_entry.runtime_design_response.v0.1":
        stop("bad response schema version")
    if request.get("request_id") != response.get("request_id"):
        stop("request response mismatch")
    if request.get("mode") != "design_only" or response.get("response_state") != "design_only":
        stop("fixtures must remain design_only")
    requested = request.get("requested_readiness", {})
    outputs = response.get("readiness_outputs", {})
    for key in FALSE_KEYS:
        if requested.get(key) is not False:
            stop(f"request {key} must be false")
        if outputs.get(key) is not False:
            stop(f"response {key} must be false")
    if response.get("ready") is not False:
        stop("response ready must be false")
    if not response.get("missing_inputs"):
        stop("missing inputs required")
    print("AI_ENTRY_RUNTIME_DESIGN_FIXTURES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
