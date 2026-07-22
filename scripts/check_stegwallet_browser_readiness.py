#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegwallet.html"
SCRIPT = ROOT / "assets" / "stegwallet-readiness.js"


def require(text: str, marker: str, source: str) -> None:
    if marker not in text:
        raise SystemExit(f"STEGWALLET_READINESS_CHECK_FAIL: missing {marker!r} in {source}")


def prohibit(text: str, marker: str, source: str) -> None:
    if marker.lower() in text.lower():
        raise SystemExit(f"STEGWALLET_READINESS_CHECK_FAIL: prohibited {marker!r} in {source}")


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "Run readiness self-test",
        "readiness-output",
        "stegwallet-readiness.js",
        "readiness receipt            != wallet authentication or authority",
    ):
        require(page, marker, PAGE.name)
    for marker in (
        "stegwallet.wallet_browser_readiness.v1",
        "eth_accounts",
        "eth_chainId",
        "eth_getBalance",
        "READY_FOR_GOAL_CONFIGURATION",
        "NOT_READY",
        "wallet_authenticated: false",
        "signature_requested: false",
        "transaction_requested: false",
        "execution_authority: false",
        "custody_recorded: false",
        "receipt_sha256",
        "0x2105",
    ):
        require(script, marker, SCRIPT.name)
    for marker in (
        "eth_requestAccounts",
        "personal_sign",
        "eth_sign",
        "eth_sendTransaction",
        "wallet_switchEthereumChain",
        "wallet_addEthereumChain",
        "private key",
        "seed phrase",
        "mnemonic",
    ):
        prohibit(script, marker, SCRIPT.name)
    print("STEGWALLET_BROWSER_READINESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
