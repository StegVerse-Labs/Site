#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "data" / "stegwallet-siwe-runtime.json"
PROMOTION = ROOT / "data" / "stegwallet-siwe-promotion-receipt.json"
ORIGIN = "https://stegverse.org"
ROUTES = {
    "challenge_endpoint": ORIGIN + "/api/stegwallet/siwe/challenge",
    "verify_endpoint": ORIGIN + "/api/stegwallet/siwe/verify",
    "session_endpoint": ORIGIN + "/api/stegwallet/siwe/session",
    "logout_endpoint": ORIGIN + "/api/stegwallet/siwe/logout",
}


def canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: canonical(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    return value


def digest(value: Any) -> str:
    raw = json.dumps(canonical(value), separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def verify_activation(receipt: Mapping[str, Any]) -> None:
    if receipt.get("schema") != "stegwallet.siwe_activation_receipt.v1":
        raise ValueError("unsupported_siwe_activation_receipt")
    material = dict(receipt)
    supplied = material.pop("activation_receipt_sha256", None)
    if supplied != digest(material):
        raise ValueError("siwe_activation_receipt_tampered")
    if receipt.get("status") != "READY_FOR_SITE_PROMOTION":
        raise ValueError("siwe_activation_not_ready")
    if receipt.get("canonical_origin") != ORIGIN:
        raise ValueError("siwe_activation_origin_mismatch")
    if receipt.get("service_id") != "stegwallet-siwe":
        raise ValueError("siwe_activation_service_mismatch")
    if receipt.get("blockers") != []:
        raise ValueError("siwe_activation_has_blockers")
    if receipt.get("site_configuration_promoted") is not False:
        raise ValueError("siwe_activation_preclaims_promotion")
    for field in (
        "wallet_authenticated",
        "transaction_authority",
        "execution_authority",
        "delegation_authority",
        "custody_recorded",
    ):
        if receipt.get(field) is not False:
            raise ValueError(f"siwe_activation_{field}_violation")
    for field in (
        "service_manifest_sha256",
        "proxy_manifest_sha256",
        "health_readiness_sha256",
        "activation_receipt_sha256",
    ):
        value = str(receipt.get(field, ""))
        if len(value) != 71 or not value.startswith("sha256:"):
            raise ValueError(f"siwe_activation_{field}_invalid")


def build_runtime(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema": "stegwallet.siwe_runtime_configuration.v1",
        "state": "READY",
        "canonical_origin": ORIGIN,
        "chain_id": 8453,
        **ROUTES,
        "https_required": True,
        "same_origin_required": True,
        "wallet_authentication_enabled": True,
        "activation_receipt_sha256": receipt["activation_receipt_sha256"],
        "service_manifest_sha256": receipt["service_manifest_sha256"],
        "proxy_manifest_sha256": receipt["proxy_manifest_sha256"],
        "health_readiness_sha256": receipt["health_readiness_sha256"],
        "transaction_authority": False,
        "execution_authority": False,
        "delegation_authority": False,
        "custody_recorded": False,
        "blockers": [],
    }


def promote(receipt: Mapping[str, Any], *, apply: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    verify_activation(receipt)
    runtime = build_runtime(receipt)
    promotion = {
        "schema": "stegwallet.siwe_site_promotion_receipt.v1",
        "status": "PROMOTION_READY" if not apply else "PROMOTED",
        "canonical_origin": ORIGIN,
        "activation_receipt_sha256": receipt["activation_receipt_sha256"],
        "runtime_configuration_sha256": digest(runtime),
        "site_configuration_promoted": bool(apply),
        "wallet_authenticated": False,
        "transaction_authority": False,
        "execution_authority": False,
        "delegation_authority": False,
        "custody_recorded": False,
        "promoted_at": datetime.now(timezone.utc).isoformat() if apply else None,
    }
    promotion["promotion_receipt_sha256"] = digest(promotion)
    if apply:
        RUNTIME.write_text(json.dumps(runtime, indent=2) + "\n", encoding="utf-8")
        PROMOTION.write_text(json.dumps(promotion, indent=2) + "\n", encoding="utf-8")
    return runtime, promotion


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("activation_receipt", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.activation_receipt.read_text(encoding="utf-8"))
    runtime, promotion = promote(receipt, apply=args.apply)
    result = {"runtime_configuration": runtime, "promotion_receipt": promotion}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
