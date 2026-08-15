#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

UPSTREAM_BLOBS = {
    "assets/stegfin-phone/phone-direct-route.js": "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
    "assets/stegfin-phone/stegid-device-wallet-bootstrap.js": "01df37b655f1dae8650c9102ffbd85f72432c47f",
    "assets/stegfin-phone/device-wallet-identity.js": "0f18f416dee3d2707ac47964a6b24fe918d6ef68",
    "assets/stegfin-phone/app.js": "ade469ac61df37da46bef1376cfdbb10d3c9b5f1",
    "assets/stegfin-phone/styles.css": "3a91c67d6088f75a93955a260985ce686eb5698f",
}

REQUIRED = [
    *UPSTREAM_BLOBS,
    "stegfin-trade.html",
    "data/session-work-claims.json",
    "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md",
]


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def require(ok: bool, message: str, failures: list[str]) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        require((ROOT / rel).is_file(), f"missing required projection file: {rel}", failures)

    if failures:
        for item in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{item}")
        return 1

    for rel, expected in UPSTREAM_BLOBS.items():
        actual = git_blob_sha(ROOT / rel)
        require(actual == expected, f"upstream blob drift: {rel} {actual} != {expected}", failures)

    page = (ROOT / "stegfin-trade.html").read_text(encoding="utf-8")
    scripts = re.findall(r'<script\s+src="([^"]+)"', page)
    require(scripts == [
        "./assets/stegfin-phone/phone-direct-route.js",
        "./assets/stegfin-phone/stegid-device-wallet-bootstrap.js",
        "./assets/stegfin-phone/device-wallet-identity.js",
        "./assets/stegfin-phone/app.js",
    ], f"unexpected phone script order: {scripts}", failures)
    require(not any(src.startswith(("http://", "https://")) for src in scripts), "remote executable script dependency prohibited", failures)
    require("Verify this phone and prepare wallet handoff" in page, "participant PREPARE entry missing", failures)
    require("TV/TVC" in page, "TV/TVC authority statement missing", failures)
    require("USER_ONLY" in page, "USER_ONLY wallet boundary missing", failures)
    require("StegVerse executes on this phone" in page, "phone sovereign execution statement missing", failures)

    route = (ROOT / "assets/stegfin-phone/phone-direct-route.js").read_text(encoding="utf-8")
    for phrase in (
        "credential_requirement: 'NONE'",
        "credential_authority: 'TV/TVC'",
        "non_tv_tvc_secret_or_token_used: false",
        "provider_secret_required: false",
        "hosted_runtime_required: false",
        "render_required: false",
        "automatic_signing: false",
        "automatic_broadcast: false",
        "state: 'WALLET_HANDOFF_READY'",
        "signed: false",
        "broadcast: false",
        "https://mainnet.base.org",
        "inventory_scope: 'BOUNDED_TRADE_RELEVANT_ASSETS'",
        "scope_assets: ['ETH_GAS_RESERVE', 'USDC_SELL_ASSET', 'WETH_BUY_ASSET']",
        "trade_relevant_scope_complete: true",
        "unknown_asset_enumeration_performed: false",
        "exhaustive_wallet_asset_discovery_claimed: false",
        "insufficient USDC for exact validation entry",
        "native ETH gas reserve is empty",
        "insufficient native ETH gas reserve",
        "gas_reserve_sufficient: true",
    ):
        require(phrase in route, f"direct route invariant missing: {phrase}", failures)

    for forbidden in ("eth_getLogs", "discoverContracts", "discoveryChunk", "transferTopic", "discovery_complete: true"):
        require(forbidden not in route, f"unbounded/exhaustive inventory dependency remains: {forbidden}", failures)

    bootstrap = (ROOT / "assets/stegfin-phone/stegid-device-wallet-bootstrap.js").read_text(encoding="utf-8")
    require("requested_capabilities:['OBSERVE','PREPARE']" in bootstrap, "StegID request must be OBSERVE+PREPARE only", failures)
    require("granted_capabilities:['OBSERVE','PREPARE']" in bootstrap, "StegID grant must be OBSERVE+PREPARE only", failures)
    require("automatic_signing:false" in bootstrap and "automatic_broadcast:false" in bootstrap, "StegID must not gain signing/broadcast authority", failures)

    identity = (ROOT / "assets/stegfin-phone/device-wallet-identity.js").read_text(encoding="utf-8")
    require("granted_capabilities.includes('SIGN')" in identity and "granted_capabilities.includes('BROADCAST')" in identity, "identity guard must reject SIGN/BROADCAST", failures)
    require("non-TV/TVC credential use prohibited" in identity, "identity guard must reject non-TV/TVC credentials", failures)

    claims = (ROOT / "data/session-work-claims.json").read_text(encoding="utf-8")
    require('"claim_id": "SITE-STEGFIN-PHONE-PROJECTION-261-20260815"' in claims, "released projection claim missing", failures)
    require('"claim_id": "SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815"' in claims, "hardening projection claim missing", failures)
    require('"state": "CLAIMED_FOR_IMPLEMENTATION"' in claims or '"state": "MERGED_INTO_CANONICAL_WORKSTREAM"' in claims, "hardening projection claim not active/released", failures)

    handoff = (ROOT / "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
    for phrase in (
        "STEGFIN-PHONE-DIRECT-ROUTE-011",
        "SITE-STEGFIN-PHONE-PROJECTION-261",
        "credential_authority: TV/TVC",
        "non_tv_tvc_secret_or_token_allowed: false",
        "Render production runtime: PROHIBITED",
        "WALLET_HANDOFF_READY",
        "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
        "e19f64ca53699cc626cf05524ff8398544696067",
    ):
        require(phrase in handoff, f"handoff invariant missing: {phrase}", failures)

    if failures:
        for item in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{item}")
        return 1

    print("STEGFIN_PHONE_PROJECTION_PASS copied_upstream_blobs=5 bounded_inventory=PASS participant_entry=PASS tv_tvc=PASS hosted_runtime_authority=NONE signing_broadcast=USER_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
