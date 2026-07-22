#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegwallet.html"
SCRIPT = ROOT / "assets" / "stegwallet.js"


def require(text: str, marker: str, source: str) -> None:
    if marker not in text:
        raise SystemExit(f"STEGWALLET_CHECK_FAIL: missing {marker!r} in {source}")


def prohibit(text: str, marker: str, source: str) -> None:
    if marker.lower() in text.lower():
        raise SystemExit(f"STEGWALLET_CHECK_FAIL: prohibited {marker!r} in {source}")


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    for marker in (
        "StegWallet",
        "Connect wallet",
        "Approve every trade",
        "Bounded delegated goal",
        "stegwallet.signature_request.v1",
        "Open MetaMask approval",
        "HPS delegation receipt",
        "private key / seed phrase     = never requested",
    ):
        require(page, marker, PAGE.name)

    for marker in (
        "eth_requestAccounts",
        "wallet_switchEthereumChain",
        "wallet_addEthereumChain",
        "eth_getBalance",
        "eth_sendTransaction",
        "eth_getTransactionReceipt",
        "stegwallet.goal_mandate.v1",
        "stegwallet.signature_request.v1",
        "transaction_sha256",
        "decision_sha256",
        "requires_user_signature",
        "private_key_requested",
        "delegated_bounded",
        "0x2105",
    ):
        require(script, marker, SCRIPT.name)

    for marker in (
        "mnemonic",
        "seed input",
        "private key input",
        "STEGVERSE_PROVIDER_TOKEN",
        "exec(",
        "child_process",
    ):
        prohibit(page + "\n" + script, marker, "StegWallet Site surface")

    # Only a verified imported signature request may enable the wallet-send control.
    require(script, "state.verifiedRequest = null", SCRIPT.name)
    require(script, "$('send-request').disabled = true", SCRIPT.name)
    require(script, "state.verifiedRequest = payload", SCRIPT.name)
    require(script, "$('send-request').disabled = false", SCRIPT.name)
    require(script, "if (!request) throw new Error('Verify an admitted signature request first.')", SCRIPT.name)
    require(script, "const currentHash = await sha256(request.transaction)", SCRIPT.name)
    require(script, "if (currentHash !== request.transaction_sha256)", SCRIPT.name)

    print("STEGWALLET_CRYPTO_GOALS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
