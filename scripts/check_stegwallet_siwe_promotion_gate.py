#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMOTER_PATH = ROOT / "scripts" / "promote_stegwallet_siwe_runtime.py"

spec = importlib.util.spec_from_file_location("siwe_promoter", PROMOTER_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: promoter import failed")
promoter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promoter)


def receipt() -> dict:
    value = {
        "schema": "stegwallet.siwe_activation_receipt.v1",
        "status": "READY_FOR_SITE_PROMOTION",
        "service_id": "stegwallet-siwe",
        "canonical_origin": "https://stegverse.org",
        "service_manifest_sha256": "sha256:" + "1" * 64,
        "proxy_manifest_sha256": "sha256:" + "2" * 64,
        "health_readiness_sha256": "sha256:" + "3" * 64,
        "edge_to_origin_authentication_required": True,
        "direct_origin_authentication_allowed": False,
        "blockers": [],
        "site_configuration_promoted": False,
        "wallet_authenticated": False,
        "transaction_authority": False,
        "execution_authority": False,
        "delegation_authority": False,
        "custody_recorded": False,
        "verified_at": "2026-07-22T18:00:00+00:00",
    }
    value["activation_receipt_sha256"] = promoter.digest(value)
    return value


def rehash(value: dict) -> None:
    value["activation_receipt_sha256"] = promoter.digest(
        {key: item for key, item in value.items() if key != "activation_receipt_sha256"}
    )


def expect_error(value: dict, expected: str) -> None:
    try:
        promoter.promote(value, apply=False)
    except ValueError as exc:
        if str(exc) != expected:
            raise SystemExit(f"STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: expected {expected}, got {exc}")
    else:
        raise SystemExit(f"STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: expected {expected}")


def main() -> int:
    source = receipt()
    runtime, promotion = promoter.promote(source, apply=False)
    if runtime["state"] != "READY" or runtime["wallet_authentication_enabled"] is not True:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: valid receipt did not create READY runtime")
    if runtime["logout_endpoint"] != "https://stegverse.org/api/stegwallet/siwe/logout":
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: logout endpoint missing")
    if runtime["edge_to_origin_authentication_required"] is not True:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: edge authentication requirement missing")
    if runtime["direct_origin_authentication_allowed"] is not False:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: direct-origin authentication enabled")
    if promotion["status"] != "PROMOTION_READY" or promotion["site_configuration_promoted"] is not False:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: dry run preclaimed promotion")
    for field in ("transaction_authority", "execution_authority", "delegation_authority", "custody_recorded"):
        if runtime[field] is not False or promotion[field] is not False:
            raise SystemExit(f"STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: {field} granted")

    changed = copy.deepcopy(source)
    changed["canonical_origin"] = "https://evil.example"
    expect_error(changed, "siwe_activation_receipt_tampered")

    changed = copy.deepcopy(source)
    changed["transaction_authority"] = True
    rehash(changed)
    expect_error(changed, "siwe_activation_transaction_authority_violation")

    changed = copy.deepcopy(source)
    changed["status"] = "CONFIGURATION_REQUIRED"
    rehash(changed)
    expect_error(changed, "siwe_activation_not_ready")

    changed = copy.deepcopy(source)
    changed["edge_to_origin_authentication_required"] = False
    rehash(changed)
    expect_error(changed, "siwe_activation_edge_authentication_missing")

    changed = copy.deepcopy(source)
    changed["direct_origin_authentication_allowed"] = True
    rehash(changed)
    expect_error(changed, "siwe_activation_direct_origin_allowed")

    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "promotion.json"
        runtime, promotion = promoter.promote(source, apply=False)
        output.write_text(json.dumps({"runtime": runtime, "promotion": promotion}), encoding="utf-8")
        if not output.exists():
            raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: dry-run artifact missing")

    committed = json.loads((ROOT / "data" / "stegwallet-siwe-runtime.json").read_text(encoding="utf-8"))
    if committed["state"] != "CONFIGURATION_REQUIRED" or committed["wallet_authentication_enabled"] is not False:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: repository configuration activated without live receipt")
    if committed["edge_to_origin_authentication_required"] is not True:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: disabled runtime lost edge requirement")
    if committed["direct_origin_authentication_allowed"] is not False:
        raise SystemExit("STEGWALLET_SIWE_PROMOTION_CHECK_FAIL: disabled runtime allows direct origin")

    print("STEGWALLET_SIWE_PROMOTION_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
