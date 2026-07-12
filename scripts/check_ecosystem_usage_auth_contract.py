#!/usr/bin/env python3
"""Validate the Site-owned authenticated usage retrieval contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "ecosystem-usage-live-contract.json"
CLIENT_PATH = ROOT / "assets" / "ecosystem-usage-auth-client.js"


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_USAGE_AUTH_CONTRACT_FAIL: {message}")


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    client = CLIENT_PATH.read_text(encoding="utf-8")

    if contract.get("schema") != "stegverse.site.ecosystem_usage_live_contract.v1":
        fail("contract schema drift")
    if contract.get("status") != "PREPARED_NOT_DEPLOYED":
        fail("prepared transport must not claim deployment")

    auth = contract.get("authentication", {})
    expected_auth = {
        "mode": "same_origin_session",
        "browser_credentials": "same-origin",
        "authorization_header_from_site_config": False,
        "token_in_query": False,
        "token_in_local_storage": False,
        "secret_material_rendered": False,
    }
    for key, value in expected_auth.items():
        if auth.get(key) != value:
            fail(f"authentication boundary drift: {key}")

    transport = contract.get("transport", {})
    if transport.get("same_origin_required_for_credentials") is not True:
        fail("credentials must remain same-origin")
    if transport.get("cross_origin_credentials_allowed") is not False:
        fail("cross-origin credentials must remain prohibited")
    if transport.get("cache") != "no-store" or transport.get("method") != "GET":
        fail("transport method/cache boundary drift")
    timeout = transport.get("timeout_ms")
    if not isinstance(timeout, int) or timeout < 1000 or timeout > 30000:
        fail("timeout must remain bounded to 1-30 seconds")

    response = contract.get("response", {})
    if response.get("schema") != "stegverse.usage.session.v1":
        fail("response schema drift")
    if response.get("source_class") != "LIVE_USAGE_API":
        fail("live source classification drift")
    if response.get("requested_session_identity_must_match") is not True:
        fail("session identity binding missing")
    if response.get("retrieval_receipt_required") is not True:
        fail("retrieval receipt requirement missing")
    if set(response.get("allowed_evidence_classes", [])) != {"MEASURED", "CONFIGURED", "DERIVED", "UNAVAILABLE"}:
        fail("evidence class set drift")

    fallback = contract.get("fallback", {})
    for key in (
        "authentication_failure_may_fallback",
        "identity_mismatch_may_fallback",
        "contract_invalid_may_fallback",
        "receipt_missing_may_fallback",
    ):
        if fallback.get(key) is not False:
            fail(f"integrity failure must not silently fallback: {key}")

    boundaries = contract.get("authority_boundaries", {})
    if any(value is not False for value in boundaries.values()):
        fail("retrieval contract exceeded Site authority")

    required_client_markers = (
        "INTEGRITY_HTTP_STATUSES",
        "400, 401, 403, 409, 422",
        "throw new UsageIntegrityError(`usage request rejected with HTTP ${response.status}`)",
        "credentials: sameOrigin ? 'same-origin' : 'omit'",
        "cache: 'no-store'",
        "AbortController",
        "live usage response changed session identity",
        "retrieval receipt changed session identity",
        "authority_granted !== false",
        "custody_recorded !== false",
        "UNAVAILABLE metric must retain null value",
        "window.StegVerseUsageAuthClient",
        "authority: 'none'",
        "custody: 'not-recorded-by-site'",
    )
    missing = [marker for marker in required_client_markers if marker not in client]
    if missing:
        fail("client markers missing: " + ", ".join(missing))

    forbidden = ("Authorization: Bearer", "localStorage.setItem", "credentials: 'include'")
    present = [marker for marker in forbidden if marker in client]
    if present:
        fail("credential-isolation violation: " + ", ".join(present))

    print("ECOSYSTEM_USAGE_AUTH_CONTRACT_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
