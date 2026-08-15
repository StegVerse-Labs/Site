#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "stegfin-phone"
MANIFEST = SURFACE / "source-manifest.json"
CLAIMS = ROOT / "data" / "session-work-claims.json"
REPORT = ROOT / "stegfin_phone_participant_surface.report.json"
HANDOFF = ROOT / "docs" / "STEGFIN_PHONE_PARTICIPANT_SURFACE_MIRROR_HANDOFF.md"
CLAIM_ID = "SITE-STEGFIN-PHONE-PROJECTION-261-20260815"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def require(ok: bool, message: str, failures: list[str]) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(CLAIMS.read_text(encoding="utf-8"))
    handoff = HANDOFF.read_text(encoding="utf-8")

    require(manifest.get("source_merge_commit") == "e19f64ca53699cc626cf05524ff8398544696067", "upstream merge drift", failures)
    require(manifest.get("source_release_task") == "STEGFIN-PHONE-DIRECT-ROUTE-011", "upstream task drift", failures)
    require(manifest.get("credential_authority") == "TV/TVC", "credential authority drift", failures)
    require(manifest.get("credential_requirement") == "NONE", "credential requirement drift", failures)
    require(manifest.get("non_tv_tvc_secret_or_token_used") is False, "non-TV/TVC secret/token drift", failures)
    require(manifest.get("hosted_runtime_required") is False, "hosted runtime dependency drift", failures)
    require(manifest.get("wallet_signing_authority") == "USER_ONLY", "signing authority drift", failures)
    require(manifest.get("broadcast_authority") == "USER_ONLY", "broadcast authority drift", failures)
    require(manifest.get("inventory_scope") == "BOUNDED_TRADE_RELEVANT_ASSETS", "inventory scope drift", failures)
    require(manifest.get("historical_transfer_log_scan_allowed") is False, "historical log scan allowed", failures)
    require(manifest.get("unknown_asset_enumeration_performed") is False, "unknown asset enumeration drift", failures)
    require(manifest.get("exhaustive_wallet_asset_discovery_claimed") is False, "exhaustive discovery claim drift", failures)

    for relative, expected in manifest.get("files", {}).items():
        path = ROOT / relative
        require(path.is_file(), f"missing projected source: {relative}", failures)
        if path.is_file():
            actual = git_blob_sha1(path)
            require(actual == expected, f"source blob mismatch {relative}: {actual} != {expected}", failures)

    claims = [c for c in registry.get("claims", []) if c.get("claim_id") == CLAIM_ID]
    require(len(claims) == 1, "exact Site projection claim missing or duplicated", failures)
    if len(claims) == 1:
        claim = claims[0]
        require(claim.get("state") in {"CLAIMED_FOR_IMPLEMENTATION", "MERGED_INTO_CANONICAL_WORKSTREAM"}, "projection claim state invalid", failures)
        require(claim.get("dependency_surface_keys") == ["site:stegfin-phone-participant-surface"], "projection dependency surface drift", failures)
        require(claim.get("branch") == "feat/stegfin-phone-participant-surface-261" or claim.get("state") == "MERGED_INTO_CANONICAL_WORKSTREAM", "projection branch drift", failures)

    direct = (SURFACE / "phone-direct-route.js").read_text(encoding="utf-8")
    bootstrap = (SURFACE / "stegid-device-wallet-bootstrap.js").read_text(encoding="utf-8")
    identity = (SURFACE / "device-wallet-identity.js").read_text(encoding="utf-8")
    app = (SURFACE / "app.js").read_text(encoding="utf-8")
    html = (SURFACE / "index.html").read_text(encoding="utf-8")

    for marker in (
        "inventory_scope: 'BOUNDED_TRADE_RELEVANT_ASSETS'",
        "scope_assets: ['ETH_GAS_RESERVE', 'USDC_SELL_ASSET', 'WETH_BUY_ASSET']",
        "trade_relevant_scope_complete: true",
        "unknown_asset_enumeration_performed: false",
        "exhaustive_wallet_asset_discovery_claimed: false",
        "insufficient USDC for exact validation entry",
        "native ETH gas reserve is empty",
        "insufficient native ETH gas reserve",
        "gas_reserve_sufficient: true",
        "TVC-STEGFIN-PHONE-DIRECT-ROUTE-008",
        "credential_requirement: 'NONE'",
        "credential_authority: 'TV/TVC'",
        "provider_secret_required: false",
        "hosted_runtime_required: false",
        "state: 'WALLET_HANDOFF_READY'",
        "state: 'BLOCKED'",
        "signed: false",
        "broadcast: false",
    ):
        require(marker in direct, f"direct carrier marker missing: {marker}", failures)

    for marker in ("eth_getLogs", "discoverContracts", "discoveryChunk", "transferTopic"):
        require(marker not in direct, f"unbounded historical discovery remains: {marker}", failures)

    for marker in (
        "navigator.credentials.create",
        "navigator.credentials.get",
        "userVerification:'required'",
        "DEVICE_POSSESSION",
        "HUMAN_CONTINUITY",
        "IDENTITY_CONTINUITY_VALID",
        "DEVICE_ADMITTED",
        "requested_capabilities:['OBSERVE','PREPARE']",
        "granted_capabilities:['OBSERVE','PREPARE']",
        "credential_authority:'TV/TVC'",
        "credential_requirement:'NONE'",
        "automatic_signing:false",
        "automatic_broadcast:false",
    ):
        require(marker in bootstrap, f"StegID bootstrap marker missing: {marker}", failures)

    for marker in (
        "ALLOW_DEVICE_WALLET_CAPABILITY",
        "StegID PREPARE capability required",
        "granted_capabilities.includes('SIGN')",
        "granted_capabilities.includes('BROADCAST')",
        "identity_continuity_is_not_wallet_authority",
        "selected_carrier = 'STEGVERSE_DIRECT_ONCHAIN'",
    ):
        require(marker in identity, f"identity gate marker missing: {marker}", failures)

    require("StegFinPhoneContinuity.run()" in app, "operator app does not invoke phone carrier", failures)
    require('id="prepareOnPhone"' in html, "participant phone control missing", failures)
    for script in ("phone-direct-route.js", "stegid-device-wallet-bootstrap.js", "device-wallet-identity.js", "app.js"):
        require(script in html, f"participant page missing script: {script}", failures)

    forbidden = (
        "ZEROEX_API_KEY", "WALLET_PRIVATE_KEY", "GITHUB_PAT", "https://tvc.stegverse.org",
        "StegFinLegacyPhoneContinuity", "LEGACY_TVC_PROVIDER",
    )
    combined = "\n".join((direct, bootstrap, identity, html))
    for value in forbidden:
        require(value not in combined, f"forbidden production dependency: {value}", failures)

    require("StegFin PR: #62" in handoff, "handoff lacks hardened release", failures)
    require("Site's pre-work registry" in handoff, "handoff lacks pre-work ownership", failures)

    report = {
        "schema": "stegverse.site.stegfin_phone_participant_surface_validation.v1",
        "task_id": "SITE-STEGFIN-PHONE-PROJECTION-261",
        "status": "FAIL" if failures else "PASS",
        "source_merge_commit": manifest.get("source_merge_commit"),
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "non_tv_tvc_secret_or_token_used": False,
        "hosted_runtime_required": False,
        "wallet_signing_authority": "USER_ONLY",
        "broadcast_authority": "USER_ONLY",
        "failures": failures,
        "live_phone_execution_claimed": False,
        "next_action": "repair exact source/claim drift" if failures else "merge participant projection; actual phone gesture remains StegFin #60 live evidence boundary",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"STEGFIN_PHONE_PARTICIPANT_SURFACE_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
