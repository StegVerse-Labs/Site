#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

UPSTREAM_BLOBS = {
    "assets/stegfin-phone/rpc-resilience.js": "290b567eca2cc9f83e7438a80682ebaf8006ad76",
    "assets/stegfin-phone/phone-direct-route.js": "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
    "assets/stegfin-phone/stegid-device-wallet-bootstrap.js": "01df37b655f1dae8650c9102ffbd85f72432c47f",
    "assets/stegfin-phone/device-wallet-identity.js": "efc2c9c21d369bbc3d6817599f74496f918d721b",
    "assets/stegfin-phone/app.js": "433ef5e5db9f9f7af2c7c7df4ba01acc89125403",
    "assets/stegfin-phone/styles.css": "3a91c67d6088f75a93955a260985ce686eb5698f",
}

READINESS_PROJECTION = "task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json"

REQUIRED = [
    *UPSTREAM_BLOBS,
    "stegfin-trade.html",
    READINESS_PROJECTION,
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
        "./assets/stegfin-phone/rpc-resilience.js",
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

    app = (ROOT / "assets/stegfin-phone/app.js").read_text(encoding="utf-8")
    require('const READINESS_URL = "../task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json";' in app, "phone app readiness URL drifted", failures)
    require("exact_validation_trade_request" in app, "phone app no longer renders source trade readiness", failures)
    for phrase in (
        "function validateReviewableHandoff(local)",
        "function walletReviewRows(local)",
        "function renderWalletReview(local)",
        "button.disabled = !reviewable",
        "candidate.requires_user_wallet_signature !== true",
        "handoff.wallet_is_only_signing_authority !== true",
        "handoff.explicit_wallet_confirmation_required !== true",
        "handoff.automatic_signing !== false",
        "handoff.automatic_broadcast !== false",
        "route.decision !== 'ROUTE_ADMITTED'",
        "route.authority !== 'TV/TVC'",
        "route.credential_requirement !== 'NONE'",
        "candidate.purpose === 'exact_erc20_approval'",
        "candidate.exact_allowance_atomic",
        "candidate.unlimited_allowance === false",
        "Spender / SwapRouter02",
        "Quote minimum out",
        "Gas estimate",
        "Yes · USER_ONLY",
        "Review only: this control never contacts a wallet, signs, broadcasts, or settles.",
        "No wallet action occurred.",
    ):
        require(phrase in app, f"wallet review invariant missing: {phrase}", failures)
    for forbidden in (
        "eth_sendRawTransaction",
        "eth_sendTransaction",
        "personal_sign",
        "eth_sign",
        "wallet_requestPermissions",
        "wallet_addEthereumChain",
        "window.ethereum.request",
        "Authorization",
        "Bearer ",
        "GITHUB_TOKEN",
        "RENDER_API_KEY",
    ):
        require(forbidden not in app, f"wallet review contains prohibited authority/API marker: {forbidden}", failures)

    readiness_text = (ROOT / READINESS_PROJECTION).read_text(encoding="utf-8")
    try:
        readiness = json.loads(readiness_text)
    except json.JSONDecodeError as error:
        failures.append(f"source readiness projection invalid JSON: {error}")
        readiness = {}
    require(readiness.get("schema") == "site.stegfin.phone_source_readiness_projection.v1", "source readiness projection schema mismatch", failures)
    require(readiness.get("source_repository") == "StegVerse-Labs/stegfin-governance", "source readiness owner mismatch", failures)
    require(readiness.get("source_path") == "task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json", "source readiness canonical path mismatch", failures)
    require(readiness.get("source_readiness", {}).get("exact_validation_trade_request") == "COMPLETE_INSTALLED", "source trade contract must project COMPLETE_INSTALLED", failures)
    require(readiness.get("trade_boundary", {}).get("chain_id") == "0x2105", "source readiness Base chain mismatch", failures)
    cred = readiness.get("credential_boundary", {})
    require(cred.get("credential_authority") == "TV/TVC", "source readiness credential authority must be TV/TVC", failures)
    require(cred.get("credential_requirement") == "NONE", "source readiness credential requirement must be NONE", failures)
    require(cred.get("non_tv_tvc_secret_or_token_used") is False, "source readiness must deny non-TV/TVC secret/token use", failures)
    require(cred.get("provider_secret_required") is False and cred.get("provider_secret_exported") is False, "source readiness must not require/export provider secret", failures)
    require(cred.get("github_token_required") is False, "source readiness must not require GitHub token", failures)
    require(cred.get("hosted_runtime_required") is False, "source readiness must not require hosted runtime", failures)
    require(cred.get("wallet_signing_authority") == "USER_ONLY" and cred.get("broadcast_authority") == "USER_ONLY", "source readiness must preserve USER_ONLY signing/broadcast", failures)
    require(readiness.get("authority_effect") == "NONE_READINESS_PROJECTION_ONLY", "source readiness projection must be non-authorizing", failures)
    for forbidden in ("provider_secret_ref", "vault://", "Authorization", "Bearer ", "API_KEY", "GITHUB_TOKEN"):
        require(forbidden not in readiness_text, f"participant readiness projection leaks prohibited credential marker: {forbidden}", failures)

    resilience = (ROOT / "assets/stegfin-phone/rpc-resilience.js").read_text(encoding="utf-8")
    for phrase in (
        "https://mainnet.base.org",
        "https://base-rpc.publicnode.com",
        "credential_authority: 'TV/TVC'",
        "credential_requirement: 'NONE'",
        "non_tv_tvc_secret_or_token_used: false",
        "hosted_runtime_required: false",
        "render_required: false",
        "EXPECTED_CHAIN_ID = '0x2105'",
        "MAX_ATTEMPTS_PER_ENDPOINT = 2",
        "state: 'FAIL_CLOSED'",
    ):
        require(phrase in resilience, f"RPC resilience invariant missing: {phrase}", failures)
    require("credentials: 'omit'" in resilience, "RPC resilience must not send ambient credentials", failures)
    require("eth_chainId" in resilience, "fallback endpoint chain-id probe missing", failures)
    for forbidden in ("Authorization", "Bearer ", "api-key", "API_KEY", "GITHUB_TOKEN", "RENDER"):
        require(forbidden not in resilience, f"prohibited credential/host marker in RPC resilience asset: {forbidden}", failures)

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
    for phrase in (
        "stegverse-stegid-device-wallet-v1",
        "latest-admission",
        "stegverse.stegid.sanitized_admission_evidence.v1",
        "IDENTITY_CONTINUITY_VALID",
        "DEVICE_ADMITTED",
        "DEVICE_POSSESSION",
        "HUMAN_CONTINUITY",
        "IDENTITY_CONTINUITY",
        "stegid_admission_evidence",
        "evidence_sha256",
    ):
        require(phrase in identity, f"StegID sanitized admission evidence invariant missing: {phrase}", failures)
    require("granted_capabilities.includes('PREPARE')" in identity, "sanitized StegID evidence must prove PREPARE", failures)
    require("protected credential field prohibited" in identity, "sanitized evidence must retain protected-field rejection", failures)

    claims = (ROOT / "data/session-work-claims.json").read_text(encoding="utf-8")
    require('"claim_id": "SITE-STEGFIN-PHONE-PROJECTION-261-20260815"' in claims, "released projection claim missing", failures)
    require('"claim_id": "SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815"' in claims, "hardening projection claim missing", failures)
    require('"claim_id": "SITE-STEGFIN-PHONE-RPC-RESILIENCE-0004-20260815"' in claims, "RPC resilience projection claim missing", failures)
    require('"claim_id": "SITE-STEGFIN-WALLET-REVIEW-286-20260816"' in claims, "wallet review projection claim missing", failures)

    handoff = (ROOT / "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
    for phrase in (
        "STEGFIN-PHONE-DIRECT-ROUTE-011",
        "STEGFIN-PHONE-RPC-RESILIENCE-012",
        "SITE-STEGFIN-PHONE-PROJECTION-261",
        "TASK-2026-0004",
        "Site#282",
        "credential_authority: TV/TVC",
        "non_tv_tvc_secret_or_token_allowed: false",
        "Render production runtime: PROHIBITED",
        "WALLET_HANDOFF_READY",
        "COMPLETE_INSTALLED",
        "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
        "290b567eca2cc9f83e7438a80682ebaf8006ad76",
        "bcba49976a52024a233f998ce290ec4ab42618ff",
        "STEGFIN-PHONE-WALLET-REVIEW-014",
        "433ef5e5db9f9f7af2c7c7df4ba01acc89125403",
        "USER_ONLY wallet review",
    ):
        require(phrase in handoff, f"handoff invariant missing: {phrase}", failures)

    if failures:
        for item in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{item}")
        return 1

    print("STEGFIN_PHONE_PROJECTION_PASS copied_upstream_blobs=6 rpc_resilience=PASS bounded_inventory=PASS source_trade_contract=COMPLETE_INSTALLED stegid_admission_evidence=PASS wallet_review=USER_ONLY participant_entry=PASS tv_tvc=PASS hosted_runtime_authority=NONE signing_broadcast=USER_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
