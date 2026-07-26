#!/usr/bin/env python3
"""Fail-closed validation for the public HIL v1.1 Site contract."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
PROTOCOL = "HIL-PROTOCOL-v1.1"
PROMPT_VERSION = "HIL-PROMPT-v1.1"
PROVENANCE = "HIL-RESPONSE-PROVENANCE-v1.1"


def load_json(path: str) -> dict:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def verify_receiver_config() -> None:
    config = load_json("data/hil-receiver-config.json")
    require(config.get("schema_version") == "HIL-RECEIVER-DISCOVERY-v1", "receiver discovery schema drift")
    require(config.get("readiness_path") == "/api/hil/readiness", "readiness path drift")
    require(config.get("submission_path") == "/api/hil/submissions", "submission path drift")
    require(config.get("participant_visible_provider") is False, "provider branding must remain hidden")

    base_url = config.get("receiver_base_url")
    state = config.get("configuration_state")
    if base_url is None:
        require(state == "AWAITING_CONFORMING_HTTPS_RECEIVER", "unconfigured receiver must fail closed")
    else:
        require(isinstance(base_url, str) and base_url.strip(), "receiver URL must be a non-empty string")
        parsed = urlparse(base_url)
        require(parsed.scheme == "https", "public receiver URL must use HTTPS")
        require(bool(parsed.netloc), "public receiver URL must include a host")
        require(not parsed.username and not parsed.password, "receiver URL must not embed credentials")
        require(not parsed.query and not parsed.fragment, "receiver URL must not include query or fragment")
        require(state == "CONFORMING_HTTPS_RECEIVER_CONFIGURED", "configured receiver state mismatch")

    authority = config.get("authority") or {}
    require(all(authority.get(key) is False for key in ("execution", "publication", "master_record_append")), "receiver config grants authority")


def verify_manifest() -> None:
    manifest = load_json("data/hil-experiment.json")
    primary = manifest.get("primary_document") or {}
    protocol = manifest.get("protocol") or {}
    submission = manifest.get("submission") or {}

    require(manifest.get("schema_version") == "HIL-EXPERIMENT-v1.1", "experiment schema drift")
    require(primary.get("version") == "v1.1", "Primary version drift")
    require(primary.get("sha256") == PRIMARY, "Primary hash drift")
    require(protocol.get("version") == PROTOCOL, "protocol version drift")
    require(protocol.get("prompt_version") == PROMPT_VERSION, "prompt version drift")
    require(protocol.get("prompt_sha256") == PROMPT, "prompt hash drift")
    require(submission.get("provenance_schema_version") == PROVENANCE, "provenance schema drift")
    require(submission.get("current_transport") == "SITE_DISCOVERS_CONFORMING_GATEWAY_FAIL_CLOSED", "transport posture drift")
    require(submission.get("browser_local_hashing") is True, "browser hashing must remain enabled")
    require(submission.get("server_custody") is False, "Site must not claim receiver custody")


def verify_client() -> None:
    client = (ROOT / "assets/hil-experiment-v1.1.js").read_text(encoding="utf-8")
    required_literals = (PRIMARY, PROMPT, PROTOCOL, PROMPT_VERSION, PROVENANCE, "HIL-RECEIVER-RECEIPT-v2")
    for literal in required_literals:
        require(literal in client, f"client contract missing {literal}")
    require("participant_metadata_required === false" in client, "client must verify optional participant metadata")
    require("crypto.subtle.digest('SHA-256'" in client, "client-side SHA-256 verification missing")
    require("receipt.receipt_sha256" in client, "receipt hash verification missing")
    require(re.search(r"setInterval\(\(\) => checkGatewayReadiness", client) is not None, "readiness retry missing")


def main() -> None:
    verify_receiver_config()
    verify_manifest()
    verify_client()
    print("HIL_SITE_CONTRACT=PASS")


if __name__ == "__main__":
    main()
