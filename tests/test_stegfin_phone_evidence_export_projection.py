from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "assets" / "stegfin-phone" / "evidence-export.js"
PAGE = ROOT / "stegfin-trade.html"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def test_exact_released_export_blob_and_order() -> None:
    assert git_blob_sha(EXPORT) == "d545063b7024b60de702ece85bd23eac6096c8bb"
    page = PAGE.read_text(encoding="utf-8")
    assert page.index("./assets/stegfin-phone/app.js") < page.index("./assets/stegfin-phone/evidence-export.js")


def test_export_is_non_authorizing_and_fail_closed() -> None:
    source = EXPORT.read_text(encoding="utf-8")
    for required in (
        "WALLET_HANDOFF_READY",
        "IDENTITY_CONTINUITY_VALID",
        "DEVICE_ADMITTED",
        "DEVICE_POSSESSION",
        "HUMAN_CONTINUITY",
        "PREPARE",
        "TV/TVC",
        "credentialRequirement: 'NONE'",
        "walletSigningAuthority: 'USER_ONLY'",
        "broadcastAuthority: 'USER_ONLY'",
        "receipt.receipt_sha256",
        "evidence.evidence_sha256",
    ):
        assert required in source
    for forbidden in (
        "window.ethereum",
        "eth_sendTransaction",
        "eth_sendRawTransaction",
        "personal_sign",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "ZEROEX_API_KEY",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
    ):
        assert forbidden not in source
