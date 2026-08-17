#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_BLOBS = {
    "assets/stegfin-phone/rpc-resilience.js": "290b567eca2cc9f83e7438a80682ebaf8006ad76",
    "assets/stegfin-phone/phone-direct-route.js": "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
    "assets/stegfin-phone/stegid-device-wallet-bootstrap.js": "9cac39a990a956f16fcde3681cbcc7d47b2fc704",
    "assets/stegfin-phone/device-wallet-identity.js": "1180d8ee929c161978d095c91514cbc3d873d3fd",
    "assets/stegfin-phone/app.js": "433ef5e5db9f9f7af2c7c7df4ba01acc89125403",
    "assets/stegfin-phone/evidence-export.js": "29ddb120fe6d1bd7c5118b41c4ef061d2db90a58",
    "assets/stegfin-phone/styles.css": "3a91c67d6088f75a93955a260985ce686eb5698f",
}
READINESS_PROJECTION = "task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json"
ACTIVE_STATES = {"CLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED"}
RELEASED_STATES = {"MERGED_INTO_CANONICAL_WORKSTREAM", "COMPLETE", "COMPLETE_RELEASED", "RELEASED"}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def require(ok: bool, message: str, failures: list[str]) -> None:
    if not ok:
        failures.append(message)


def require_markers(text: str, label: str, markers: tuple[str, ...], failures: list[str]) -> None:
    for marker in markers:
        require(marker in text, f"{label} invariant missing: {marker}", failures)


def forbid_markers(text: str, label: str, markers: tuple[str, ...], failures: list[str]) -> None:
    for marker in markers:
        require(marker not in text, f"{label} contains prohibited marker: {marker}", failures)


def claim_by_id(registry: dict, claim_id: str) -> dict | None:
    for claim in registry.get("claims", []):
        if claim.get("claim_id") == claim_id:
            return claim
    return None


def main() -> int:
    failures: list[str] = []
    required = [*UPSTREAM_BLOBS, "stegfin-trade.html", READINESS_PROJECTION, "data/session-work-claims.json", "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md"]
    for rel in required:
        require((ROOT / rel).is_file(), f"missing required projection file: {rel}", failures)
    if failures:
        for item in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{item}")
        return 1

    for rel, expected in UPSTREAM_BLOBS.items():
        require(git_blob_sha(ROOT / rel) == expected, f"upstream blob drift: {rel}", failures)

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
    require(scripts == expected_scripts, f"unexpected canonical defer-script order: {scripts}", failures)
    require(not any(src.startswith(("http://", "https://")) for src in scripts), "remote executable script dependency prohibited", failures)
    require_markers(page, "participant page", ("Verify this phone and prepare wallet handoff", "TV/TVC", "USER_ONLY", "StegVerse executes on this phone", "wallet-user-handoff.js", "wallet-user-handoff-ui.js", "DOMContentLoaded"), failures)

    app = (ROOT / "assets/stegfin-phone/app.js").read_text(encoding="utf-8")
    require_markers(app, "wallet review", (
        'const READINESS_URL = "../task-state/STEGFIN-LIVE-ENTRY-003-READINESS.json";',
        "exact_validation_trade_request", "validateReviewableHandoff", "walletReviewRows", "renderWalletReview",
        "requires_user_wallet_signature", "wallet_is_only_signing_authority", "explicit_wallet_confirmation_required",
        "automatic_signing", "automatic_broadcast", "ROUTE_ADMITTED", "TV/TVC", "credential_requirement",
        "exact_erc20_approval", "exact_allowance_atomic", "unlimited_allowance", "Spender / SwapRouter02",
        "Quote minimum out", "Gas estimate", "Review only: this control never contacts a wallet, signs, broadcasts, or settles.",
    ), failures)
    forbid_markers(app, "wallet review", ("eth_sendRawTransaction", "eth_sendTransaction", "personal_sign", "eth_sign", "wallet_requestPermissions", "wallet_addEthereumChain", "window.ethereum.request", "Authorization", "Bearer ", "GITHUB_TOKEN", "RENDER_API_KEY"), failures)

    evidence_export = (ROOT / "assets/stegfin-phone/evidence-export.js").read_text(encoding="utf-8")
    require_markers(evidence_export, "evidence export", (
        "WALLET_HANDOFF_READY", "stegverse.stegid.sanitized_admission_evidence.v1", "IDENTITY_CONTINUITY_VALID",
        "DEVICE_ADMITTED", "DEVICE_POSSESSION", "HUMAN_CONTINUITY", "IDENTITY_CONTINUITY", "PREPARE", "SIGN", "BROADCAST",
        "TV/TVC", "credential_requirement !== 'NONE'", "non_tv_tvc_secret_or_token_used !== false", "hosted_runtime_required !== false",
        "signed !== false", "broadcast !== false", "evidence.evidence_sha256", "receipt.receipt_sha256", "Copy canonical evidence",
        "Share canonical evidence", "MAX_CLOCK_SKEW_MS", "assertFreshReceipt(identity", "assertFreshReceipt(device", "assertFreshReceipt(capability",
        "expires_at", "identity commitment linkage mismatch", "device commitment linkage mismatch", "unexpired StegID admission evidence",
    ), failures)
    forbid_markers(evidence_export, "evidence export", ("window.ethereum", "eth_sendTransaction", "eth_sendRawTransaction", "personal_sign", "eth_sign", "GITHUB_TOKEN", "GH_TOKEN", "ZEROEX_API_KEY", "private_key", "seed_phrase", "fetch(", "XMLHttpRequest", "WebSocket"), failures)

    readiness_text = (ROOT / READINESS_PROJECTION).read_text(encoding="utf-8")
    try:
        readiness = json.loads(readiness_text)
    except json.JSONDecodeError as error:
        readiness = {}
        failures.append(f"source readiness projection invalid JSON: {error}")
    require(readiness.get("schema") == "site.stegfin.phone_source_readiness_projection.v1", "source readiness projection schema mismatch", failures)
    require(readiness.get("source_repository") == "StegVerse-Labs/stegfin-governance", "source readiness owner mismatch", failures)
    require(readiness.get("source_readiness", {}).get("exact_validation_trade_request") == "COMPLETE_INSTALLED", "source trade contract must project COMPLETE_INSTALLED", failures)
    require(readiness.get("trade_boundary", {}).get("chain_id") == "0x2105", "source readiness Base chain mismatch", failures)
    cred = readiness.get("credential_boundary", {})
    require(cred.get("credential_authority") == "TV/TVC" and cred.get("credential_requirement") == "NONE", "source readiness TV/TVC/NONE boundary mismatch", failures)
    require(cred.get("non_tv_tvc_secret_or_token_used") is False and cred.get("github_token_required") is False and cred.get("hosted_runtime_required") is False, "source readiness prohibited credential/host authority", failures)
    require(cred.get("wallet_signing_authority") == "USER_ONLY" and cred.get("broadcast_authority") == "USER_ONLY", "source readiness USER_ONLY boundary mismatch", failures)
    require(readiness.get("authority_effect") == "NONE_READINESS_PROJECTION_ONLY", "source readiness projection must be non-authorizing", failures)

    resilience = (ROOT / "assets/stegfin-phone/rpc-resilience.js").read_text(encoding="utf-8")
    require_markers(resilience, "RPC resilience", ("https://mainnet.base.org", "https://base-rpc.publicnode.com", "credential_authority: 'TV/TVC'", "credential_requirement: 'NONE'", "non_tv_tvc_secret_or_token_used: false", "hosted_runtime_required: false", "render_required: false", "EXPECTED_CHAIN_ID = '0x2105'", "MAX_ATTEMPTS_PER_ENDPOINT = 2", "state: 'FAIL_CLOSED'", "credentials: 'omit'", "eth_chainId"), failures)
    forbid_markers(resilience, "RPC resilience", ("Authorization", "Bearer ", "api-key", "API_KEY", "GITHUB_TOKEN"), failures)

    route = (ROOT / "assets/stegfin-phone/phone-direct-route.js").read_text(encoding="utf-8")
    require_markers(route, "direct route", ("credential_requirement: 'NONE'", "credential_authority: 'TV/TVC'", "non_tv_tvc_secret_or_token_used: false", "provider_secret_required: false", "hosted_runtime_required: false", "render_required: false", "automatic_signing: false", "automatic_broadcast: false", "state: 'WALLET_HANDOFF_READY'", "signed: false", "broadcast: false", "inventory_scope: 'BOUNDED_TRADE_RELEVANT_ASSETS'", "scope_assets: ['ETH_GAS_RESERVE', 'USDC_SELL_ASSET', 'WETH_BUY_ASSET']", "trade_relevant_scope_complete: true", "unknown_asset_enumeration_performed: false", "exhaustive_wallet_asset_discovery_claimed: false", "gas_reserve_sufficient: true"), failures)
    forbid_markers(route, "direct route", ("eth_getLogs", "discoverContracts", "discoveryChunk", "transferTopic", "discovery_complete: true"), failures)

    bootstrap = (ROOT / "assets/stegfin-phone/stegid-device-wallet-bootstrap.js").read_text(encoding="utf-8")
    require_markers(bootstrap, "StegID bootstrap", (
        "requested_capabilities: ['OBSERVE', 'PREPARE']", "granted_capabilities: ['OBSERVE', 'PREPARE']",
        "automatic_signing: false", "automatic_broadcast: false", "expires_at: expiresAt",
        "navigator.credentials.create", "navigator.credentials.get", "userVerification: 'required'",
        "ceremony: 'CREDENTIAL_CREATION'", "ceremony: 'CREDENTIAL_ASSERTION'",
        "if (!created || created.type !== 'public-key' || !created.rawId)",
        "DEVICE_POSSESSION", "HUMAN_CONTINUITY", "credential_authority: 'TV/TVC'",
        "credential_requirement: 'NONE'", "non_tv_tvc_secret_or_token_used: false"
    ), failures)
    creation_index = bootstrap.find("const created = await navigator.credentials.create(")
    creation_proof_index = bootstrap.find("ceremony: 'CREDENTIAL_CREATION'")
    assertion_index = bootstrap.find("const assertion = await navigator.credentials.get(")
    require(creation_index >= 0 and creation_proof_index > creation_index and assertion_index > creation_proof_index,
            "iOS first-passkey creation must return bounded HUMAN_CONTINUITY before later assertion path", failures)
    require("return {" in bootstrap[creation_index:assertion_index] and "ceremony: 'CREDENTIAL_CREATION'" in bootstrap[creation_index:assertion_index],
            "successful first-passkey creation does not return before assertion path", failures)
    forbid_markers(bootstrap, "StegID bootstrap", ("GITHUB_TOKEN", "GH_TOKEN", "GITHUB_PAT", "ZEROEX_API_KEY", "WALLET_PRIVATE_KEY", "WalletConnect"), failures)

    identity = (ROOT / "assets/stegfin-phone/device-wallet-identity.js").read_text(encoding="utf-8")
    require_markers(identity, "StegID identity", ("granted_capabilities.includes('SIGN')", "granted_capabilities.includes('BROADCAST')", "non-TV/TVC credential use prohibited", "stegverse-stegid-device-wallet-v1", "latest-admission", "stegverse.stegid.sanitized_admission_evidence.v1", "IDENTITY_CONTINUITY_VALID", "DEVICE_ADMITTED", "DEVICE_POSSESSION", "HUMAN_CONTINUITY", "IDENTITY_CONTINUITY", "stegid_admission_evidence", "evidence_sha256", "MIN_PREPARE_VALIDITY_MS = 5 * 60 * 1000", "capabilityRequiresRenewal", "assertFreshReceipt", "expired or expires too soon", "clearStalePhoneState", "deleteDirectTerminal", "persistIdentityBoundTerminal", "localStorage.removeItem(WALLET_HANDOFF_KEY)", "StegID identity receipt linkage mismatch", "StegID device receipt linkage mismatch", "granted_capabilities.includes('PREPARE')", "protected credential field prohibited"), failures)
    require("if (raw) return raw;" not in identity, "legacy unconditional stale capability reuse remains", failures)

    claims_path = ROOT / "data/session-work-claims.json"
    try:
        registry = json.loads(claims_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        registry = {}
        failures.append(f"claim registry invalid JSON: {error}")
    for claim_id in (
        "SITE-STEGFIN-PHONE-PROJECTION-261-20260815",
        "SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815",
        "SITE-STEGFIN-PHONE-RPC-RESILIENCE-0004-20260815",
        "SITE-STEGFIN-WALLET-REVIEW-286-20260816",
        "SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289-20260816",
        "SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816",
    ):
        require(claim_by_id(registry, claim_id) is not None, f"required projection claim missing: {claim_id}", failures)
    freshness = claim_by_id(registry, "SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816") or {}
    require(freshness.get("state") in RELEASED_STATES, "StegID freshness projection must be durably released on canonical branches", failures)
    ios_claim = claim_by_id(registry, "SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817") or {}
    require(ios_claim.get("state") in ACTIVE_STATES | RELEASED_STATES, "iOS first-passkey projection claim missing or invalid", failures)
    stale_298 = claim_by_id(registry, "SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT") or {}
    require(stale_298.get("state") in RELEASED_STATES, "completed Site #298 claim remains active/stale", failures)
    active_product_claims = [c for c in registry.get("claims", []) if c.get("state") in ACTIVE_STATES and c.get("branch") != "main"]
    for claim in active_product_claims:
        require(bool(claim.get("claim_expires_when")), f"active product claim lacks release condition: {claim.get('claim_id')}", failures)

    handoff = (ROOT / "docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
    require_markers(handoff, "handoff", (
        "STEGFIN-PHONE-DIRECT-ROUTE-011", "STEGFIN-PHONE-RPC-RESILIENCE-012", "SITE-STEGFIN-PHONE-PROJECTION-261",
        "SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289", "SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292", "STEGFIN-PHONE-STEGID-FRESHNESS-016",
        "TASK-2026-0004", "Site#282", "credential_authority: TV/TVC", "non_tv_tvc_secret_or_token_allowed: false",
        "Render production runtime: PROHIBITED", "WALLET_HANDOFF_READY", "COMPLETE_INSTALLED", "31ed79cb56e8d2366e6d70f22e28c70162c88fd8",
        "290b567eca2cc9f83e7438a80682ebaf8006ad76", "bcba49976a52024a233f998ce290ec4ab42618ff", "STEGFIN-PHONE-WALLET-REVIEW-014",
        "433ef5e5db9f9f7af2c7c7df4ba01acc89125403", "9cac39a990a956f16fcde3681cbcc7d47b2fc704", "1180d8ee929c161978d095c91514cbc3d873d3fd",
        "29ddb120fe6d1bd7c5118b41c4ef061d2db90a58", "StegFin PR #75", "USER_ONLY wallet review", "Copy canonical evidence", "unexpired",
        "SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380", "StegFin #79", "CREDENTIAL_CREATION", "CREDENTIAL_ASSERTION"
    ), failures)

    if failures:
        for item in failures:
            print(f"STEGFIN_PHONE_PROJECTION_FAIL:{item}")
        return 1
    print("STEGFIN_PHONE_PROJECTION_PASS copied_upstream_blobs=7 rpc_resilience=PASS bounded_inventory=PASS source_trade_contract=COMPLETE_INSTALLED stegid_admission_evidence=PASS stegid_freshness=RELEASE_AWARE ios_first_passkey_prepare=PASS wallet_review=USER_ONLY evidence_export=PASS participant_entry=PASS tv_tvc=PASS hosted_runtime_authority=NONE signing_broadcast=USER_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
