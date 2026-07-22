#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "data" / "stegwallet-base-dev-publication-candidate.json"
PAGE = ROOT / "stegwallet.html"
SCRIPT = ROOT / "assets" / "stegwallet.js"


def fail(message: str) -> None:
    raise SystemExit(f"STEGWALLET_BASE_DEV_CHECK_FAIL: {message}")


def main() -> int:
    payload = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    if payload.get("schema") != "stegverse.base_dev_publication_candidate.v1":
        fail("unsupported schema")
    app = payload.get("application", {})
    for field in ("name", "tagline", "description", "category", "primary_url", "canonical_origin"):
        if not str(app.get(field, "")).strip():
            fail(f"missing application.{field}")
    primary = urlparse(app["primary_url"])
    origin = urlparse(app["canonical_origin"])
    if primary.scheme != "https" or origin.scheme != "https":
        fail("primary URL and origin must use HTTPS")
    if primary.netloc != origin.netloc:
        fail("primary URL and canonical origin host mismatch")
    if app.get("supported_chain_ids") != [8453]:
        fail("Base mainnet chain identity missing")
    if app.get("basename_role") != "display-routing-alias-only":
        fail("Basename role may not grant authority")

    security = payload.get("security_posture", {})
    required_false = (
        "private_key_requested",
        "seed_phrase_requested",
        "wallet_connection_grants_authority",
        "basename_grants_authority",
        "site_display_grants_authority",
    )
    for field in required_false:
        if security.get(field) is not False:
            fail(f"security posture violation: {field}")
    for field in ("imported_signature_request_required", "user_signature_required_for_mode_1", "hps_delegation_required_for_mode_2"):
        if security.get(field) is not True:
            fail(f"required security gate missing: {field}")

    gates = payload.get("publication_gates", {})
    if payload.get("published") is not False or payload.get("authority_granted") is not False:
        fail("candidate may not claim publication or authority")
    if payload.get("state") != "PENDING_DEPLOYMENT_AND_BASE_DEV_REGISTRATION":
        fail("unexpected candidate state")
    incomplete = [key for key, value in gates.items() if value is False]
    if not incomplete:
        fail("candidate incorrectly has no blockers")
    if app.get("builder_code") is not None or app.get("icon_url") is not None or app.get("screenshots") != []:
        fail("unverified Base.dev assets or builder code present")

    for marker in ("StegWallet", "Base App", "stegwallet.signature_request.v1"):
        if marker not in page:
            fail(f"missing Site marker: {marker}")
    for marker in ("eth_sendTransaction", "requires_user_signature", "private_key_requested"):
        if marker not in script:
            fail(f"missing wallet runtime marker: {marker}")

    print("STEGWALLET_BASE_DEV_PUBLICATION_CANDIDATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
