#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json"
REGISTRY = ROOT / "data/session-work-claims.json"
HANDOFF = ROOT / "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md"
RELEASE_RECEIPT = ROOT / "receipts/stegfin-phone-stegid-freshness-292-release.json"
FRESHNESS_CLAIM = "SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816"

UPSTREAM_BLOBS = {
    "assets/stegfin-phone/rpc-resilience.js": "290b567eca2cc9f83e7438a80682ebaf8006ad76",
    "assets/stegfin-phone/phone-direct-route.js": "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
    "assets/stegfin-phone/stegid-device-wallet-bootstrap.js": "403d164b21a1c6e812d31f7ab45635baab59b73c",
    "assets/stegfin-phone/device-wallet-identity.js": "1180d8ee929c161978d095c91514cbc3d873d3fd",
    "assets/stegfin-phone/app.js": "433ef5e5db9f9f7af2c7c7df4ba01acc89125403",
    "assets/stegfin-phone/evidence-export.js": "29ddb120fe6d1bd7c5118b41c4ef061d2db90a58",
    "assets/stegfin-phone/styles.css": "3a91c67d6088f75a93955a260985ce686eb5698f",
}


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_all(text: str, fragments: tuple[str, ...], label: str, failures: list[str]) -> None:
    for fragment in fragments:
        require(fragment in text, f"{label} missing: {fragment}", failures)


def prohibit_all(text: str, fragments: tuple[str, ...], label: str, failures: list[str]) -> None:
    for fragment in fragments:
        require(fragment not in text, f"{label} prohibited marker: {fragment}", failures)


def main() -> int:
    failures: list[str] = []
    required = [*UPSTREAM_BLOBS, "stegfin-trade.html", str(READINESS.relative_to(ROOT)), str(REGISTRY.relative_to(ROOT)), str(HANDOFF.relative_to(ROOT))]
    for rel in required:
        require((ROOT / rel).is_file(), f"missing required projection file: {rel}", failures)
    if failures:
        for failure in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{failure}")
        return 1

    for rel, expected in UPSTREAM_BLOBS.items():
        actual = blob_sha(ROOT / rel)
        require(actual == expected, f"upstream blob drift: {rel} {actual} != {expected}", failures)

    page = (ROOT / "stegfin-trade.html").read_text(encoding="utf-8")
    scripts = re.findall(r'<script\s+src="([^"]+)"', page)
    expected_scripts = [
        "./assets/stegfin-phone/rpc-resilience.js",
        "./assets/stegfin-phone/phone-direct-route.js",
        "./assets/stegfin-phone/stegid-device-wallet-bootstrap.js",
        "./assets/stegfin-phone/device-wallet-identity.js",
        "./assets/stegfin-phone/app.js",
        "./assets/stegfin-phone/evidence-export.js",
    ]
    require(scripts == expected_scripts, f"unexpected phone script order: {scripts}", failures)
    require(not any(s.startswith(("http://", "https://")) for s in scripts), "remote executable script dependency prohibited", failures)
    require_all(page, ("Verify this phone and prepare wallet handoff", "TV/TVC", "USER_ONLY", "StegVerse executes on this phone"), "participant page", failures)

    app = (ROOT / "assets/stegfin-phone/app.js").read_text(encoding="utf-8")
    require_all(app, (
        'const READINESS_URL = "../task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json";',
        "exact_validation_trade_request", "validateReviewableHandoff", "walletReviewRows", "renderWalletReview",
        "candidate.requires_user_wallet_signature !== true", "handoff.wallet_is_only_signing_authority !== true",
        "handoff.explicit_wallet_confirmation_required !== true", "handoff.automatic_signing !== false",
        "handoff.automatic_broadcast !== false", "route.decision !== 'ROUTE_ADMITTED'", "route.authority !== 'TV/TVC'",
        "route.credential_requirement !== 'NONE'", "candidate.purpose === 'exact_erc20_approval'", "candidate.exact_allowance_atomic",
        "candidate.unlimited_allowance === false", "Spender / SwapRouter02", "Quote minimum out", "Gas estimate",
        "Review only: this control never contacts a wallet, signs, broadcasts, or settles.", "No wallet action occurred."
    ), "wallet review", failures)
    prohibit_all(app, ("eth_sendRawTransaction", "eth_sendTransaction", "personal_sign", "eth_sign", "window.ethereum.request", "GITHUB_TOKEN", "RENDER_API_KEY"), "wallet review", failures)

    resilience = (ROOT / "assets/stegfin-phone/rpc-resilience.js").read_text(encoding="utf-8")
    require_all(resilience, (
        "https://mainnet.base.org", "https://base-rpc.publicnode.com", "credential_authority: 'TV/TVC'",
        "credential_requirement: 'NONE'", "non_tv_tvc_secret_or_token_used: false", "hosted_runtime_required: false",
        "render_required: false", "EXPECTED_CHAIN_ID = '0x2105'", "MAX_ATTEMPTS_PER_ENDPOINT = 2", "state: 'FAIL_CLOSED'",
        "credentials: 'omit'", "eth_chainId"
    ), "RPC resilience", failures)
    prohibit_all(resilience, ("Authorization", "Bearer ", "API_KEY", "GITHUB_TOKEN", "RENDER"), "RPC resilience", failures)

    route = (ROOT / "assets/stegfin-phone/phone-direct-route.js").read_text(encoding="utf-8")
    require_all(route, (
        "credential_requirement: 'NONE'", "credential_authority: 'TV/TVC'", "non_tv_tvc_secret_or_token_used: false",
        "provider_secret_required: false", "hosted_runtime_required: false", "render_required: false",
        "automatic_signing: false", "automatic_broadcast: false", "state: 'WALLET_HANDOFF_READY'", "signed: false", "broadcast: false",
        "inventory_scope: 'BOUNDED_TRADE_RELEVANT_ASSETS'", "scope_assets: ['ETH_GAS_RESERVE', 'USDC_SELL_ASSET', 'WETH_BUY_ASSET']",
        "trade_relevant_scope_complete: true", "unknown_asset_enumeration_performed: false", "exhaustive_wallet_asset_discovery_claimed: false",
        "gas_reserve_sufficient: true"
    ), "direct route", failures)
    prohibit_all(route, ("eth_getLogs", "discoverContracts", "discoveryChunk", "transferTopic", "discovery_complete: true"), "direct route inventory", failures)

    bootstrap = (ROOT / "assets/stegfin-phone/stegid-device-wallet-bootstrap.js").read_text(encoding="utf-8")
    require_all(bootstrap, (
        "requested_capabilities: ['OBSERVE', 'PREPARE']", "granted_capabilities: ['OBSERVE', 'PREPARE']",
        "automatic_signing: false", "automatic_broadcast: false", "const expiresAt = expires.toISOString()", "expires_at: expiresAt",
        "navigator.credentials.get", "userVerification: 'required'", "DEVICE_POSSESSION", "HUMAN_CONTINUITY",
        "credential_authority: 'TV/TVC'", "credential_requirement: 'NONE'", "non_tv_tvc_secret_or_token_used: false"
    ), "StegID bootstrap", failures)

    identity = (ROOT / "assets/stegfin-phone/device-wallet-identity.js").read_text(encoding="utf-8")
    require_all(identity, (
        "stegverse.stegid.sanitized_admission_evidence.v1", "IDENTITY_CONTINUITY_VALID", "DEVICE_ADMITTED", "DEVICE_POSSESSION",
        "HUMAN_CONTINUITY", "IDENTITY_CONTINUITY", "stegid_admission_evidence", "evidence_sha256",
        "granted_capabilities.includes('PREPARE')", "granted_capabilities.includes('SIGN')", "granted_capabilities.includes('BROADCAST')",
        "non-TV/TVC credential use prohibited", "MIN_PREPARE_VALIDITY_MS = 5 * 60 * 1000", "capabilityRequiresRenewal",
        "assertFreshReceipt", "expired or expires too soon", "clearStalePhoneState", "deleteDirectTerminal", "persistIdentityBoundTerminal",
        "localStorage.removeItem(WALLET_HANDOFF_KEY)", "StegID identity receipt linkage mismatch", "StegID device receipt linkage mismatch",
        "assertFreshReceipt(capability", "assertFreshReceipt(admissionEvidence.identity_continuity", "assertFreshReceipt(admissionEvidence.device_admission",
        "assertFreshReceipt(admissionEvidence.wallet_capability", "protected credential field prohibited"
    ), "StegID freshness", failures)
    require("if (raw) return raw;" not in identity, "legacy unconditional stale capability reuse remains", failures)

    exporter = (ROOT / "assets/stegfin-phone/evidence-export.js").read_text(encoding="utf-8")
    require_all(exporter, (
        "WALLET_HANDOFF_READY", "stegverse.stegid.sanitized_admission_evidence.v1", "IDENTITY_CONTINUITY_VALID", "DEVICE_ADMITTED",
        "DEVICE_POSSESSION", "HUMAN_CONTINUITY", "IDENTITY_CONTINUITY", "PREPARE", "SIGN", "BROADCAST", "TV/TVC",
        "MAX_CLOCK_SKEW_MS", "assertFreshReceipt(identity", "assertFreshReceipt(device", "assertFreshReceipt(capability", "expires_at",
        "identity commitment linkage mismatch", "device commitment linkage mismatch", "unexpired StegID admission evidence",
        "non_tv_tvc_secret_or_token_used !== false", "hosted_runtime_required !== false", "signed !== false", "broadcast !== false",
        "navigator.clipboard", "navigator.share", "Copy canonical evidence", "Share canonical evidence", "USER_ONLY"
    ), "evidence exporter", failures)
    prohibit_all(exporter, ("window.ethereum", "eth_sendTransaction", "eth_sendRawTransaction", "personal_sign", "eth_sign", "GITHUB_TOKEN", "GH_TOKEN", "ZEROEX_API_KEY", "fetch(", "XMLHttpRequest", "WebSocket"), "evidence exporter", failures)

    try:
        readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"source readiness projection invalid JSON: {exc}")
        readiness = {}
    cred = readiness.get("credential_boundary", {})
    require(readiness.get("schema") == "site.stegfin.phone_source_readiness_projection.v1", "source readiness schema mismatch", failures)
    require(readiness.get("source_readiness", {}).get("exact_validation_trade_request") == "COMPLETE_INSTALLED", "source trade contract must be COMPLETE_INSTALLED", failures)
    require(readiness.get("trade_boundary", {}).get("chain_id") == "0x2105", "source readiness chain mismatch", failures)
    require(cred.get("credential_authority") == "TV/TVC" and cred.get("credential_requirement") == "NONE", "source readiness TV/TVC/NONE mismatch", failures)
    require(cred.get("non_tv_tvc_secret_or_token_used") is False, "source readiness permits non-TV/TVC secret/token", failures)
    require(cred.get("provider_secret_required") is False and cred.get("provider_secret_exported") is False, "source readiness provider secret drift", failures)
    require(cred.get("github_token_required") is False and cred.get("hosted_runtime_required") is False, "source readiness hosted/token authority drift", failures)
    require(cred.get("wallet_signing_authority") == "USER_ONLY" and cred.get("broadcast_authority") == "USER_ONLY", "source readiness USER_ONLY drift", failures)

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    claim = next((c for c in registry.get("claims", []) if c.get("claim_id") == FRESHNESS_CLAIM), None)
    if RELEASE_RECEIPT.is_file():
        release = json.loads(RELEASE_RECEIPT.read_text(encoding="utf-8"))
        require(claim is None or claim.get("state") not in {"CLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED"}, "released freshness claim remains active", failures)
        require(release.get("state") == "COMPLETE_RELEASED_PRODUCT", "freshness release receipt state mismatch", failures)
        require(release.get("site_product_merge") == "1ef161a9e4b72579408a22057e5eccb8300c34a6", "freshness release merge mismatch", failures)
        require(release.get("pages_build") == 1156068305 and release.get("pages_status") == "built", "freshness Pages release mismatch", failures)
        require(release.get("pages_commit") == "1ef161a9e4b72579408a22057e5eccb8300c34a6", "freshness Pages commit mismatch", failures)
        require(release.get("credential_authority") == "TV/TVC" and release.get("credential_requirement") == "NONE", "release TV/TVC/NONE mismatch", failures)
        require(release.get("non_tv_tvc_secret_or_token_used") is False and release.get("render_required") is False, "release authority boundary drift", failures)
        require(release.get("wallet_signing_authority") == "USER_ONLY" and release.get("broadcast_authority") == "USER_ONLY", "release USER_ONLY boundary drift", failures)
    else:
        require(claim is not None and claim.get("state") == "CLAIMED_FOR_IMPLEMENTATION", "active freshness projection requires active implementation claim", failures)

    handoff = HANDOFF.read_text(encoding="utf-8")
    require_all(handoff, (
        "SITE-STEGFIN-PHONE-PROJECTION-261", "STEGFIN-PHONE-DIRECT-ROUTE-011", "STEGFIN-PHONE-RPC-RESILIENCE-012",
        "SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289", "SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292", "STEGFIN-PHONE-STEGID-FRESHNESS-016",
        "TASK-2026-0004", "Site#282", "COMPLETE_INSTALLED", "credential_authority: TV/TVC", "non_tv_tvc_secret_or_token_allowed: false",
        "Render production runtime: PROHIBITED", "WALLET_HANDOFF_READY", "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
        "290b567eca2cc9f83e7438a80682ebaf8006ad76", "bcba49976a52024a233f998ce290ec4ab42618ff",
        "433ef5e5db9f9f7af2c7c7df4ba01acc89125403", "403d164b21a1c6e812d31f7ab45635baab59b73c",
        "1180d8ee929c161978d095c91514cbc3d873d3fd", "29ddb120fe6d1bd7c5118b41c4ef061d2db90a58",
        "StegFin PR #75", "USER_ONLY", "unexpired"
    ), "handoff", failures)

    if failures:
        for failure in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{failure}")
        return 1

    state = "COMPLETE_RELEASED_PRODUCT" if RELEASE_RECEIPT.is_file() else "CLAIMED_FOR_IMPLEMENTATION"
    print(f"STEGFIN_PHONE_PROJECTION_PASS state={state} copied_upstream_blobs=7 stegid_freshness=PASS rpc_resilience=PASS bounded_inventory=PASS source_trade_contract=COMPLETE_INSTALLED tv_tvc=PASS non_tv_tvc_secret_token=NONE hosted_runtime_authority=NONE signing_broadcast=USER_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
