#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegwallet.html"
SCRIPT = ROOT / "assets" / "stegwallet-siwe.js"
CONFIG = ROOT / "data" / "stegwallet-siwe-runtime.json"


def require(text: str, marker: str, source: str) -> None:
    if marker not in text:
        raise SystemExit(f"STEGWALLET_SIWE_CHECK_FAIL: missing {marker!r} in {source}")


def prohibit(text: str, marker: str, source: str) -> None:
    if marker.lower() in text.lower():
        raise SystemExit(f"STEGWALLET_SIWE_CHECK_FAIL: prohibited {marker!r} in {source}")


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))

    for marker in (
        "Authenticate browser session",
        "Sign in with wallet",
        "SIWE session receipt",
        "SIWE session                 = off-chain wallet authentication only",
        "SIWE session                 != trade admissibility or transaction authority",
        'src="assets/stegwallet-siwe.js"',
    ):
        require(page, marker, PAGE.name)

    for marker in (
        "stegwallet.siwe_runtime_configuration.v1",
        "stegwallet.siwe_challenge.v1",
        "stegwallet.siwe_session_receipt.v1",
        "personal_sign",
        "eth_accounts",
        "eth_chainId",
        "same-origin",
        "credentials: 'include'",
        "transaction_authority !== false",
        "execution_authority !== false",
        "delegation_authority !== false",
        "location.origin !== config.canonical_origin",
    ):
        require(script, marker, SCRIPT.name)

    for marker in (
        "eth_sendTransaction",
        "wallet_switchEthereumChain",
        "wallet_addEthereumChain",
        "eth_requestAccounts",
        "privateKey",
        "seed phrase",
        "mnemonic",
        "localStorage",
        "sessionStorage",
    ):
        prohibit(script, marker, SCRIPT.name)

    if config != {
        "schema": "stegwallet.siwe_runtime_configuration.v1",
        "state": "CONFIGURATION_REQUIRED",
        "canonical_origin": "https://stegverse.org",
        "chain_id": 8453,
        "challenge_endpoint": None,
        "verify_endpoint": None,
        "session_endpoint": None,
        "https_required": True,
        "same_origin_required": True,
        "wallet_authentication_enabled": False,
        "transaction_authority": False,
        "execution_authority": False,
        "delegation_authority": False,
        "custody_recorded": False,
        "blockers": [
            "authenticated_siwe_service_not_deployed",
            "challenge_endpoint_not_configured",
            "verification_endpoint_not_configured",
            "session_endpoint_not_configured",
        ],
    }:
        raise SystemExit("STEGWALLET_SIWE_CHECK_FAIL: runtime configuration is not the expected fail-closed record")

    require(script, "$('siwe-sign-in').disabled = !enabled", SCRIPT.name)
    require(script, "if (config.wallet_authentication_enabled !== true) return false", SCRIPT.name)
    require(script, "No signature can be requested.", SCRIPT.name)
    print("STEGWALLET_SIWE_CLIENT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
