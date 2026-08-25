#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "assets/stegfin-phone/coinbase-skap-ingress.js"
UI = ROOT / "assets/stegfin-phone/coinbase-skap-ingress-ui.js"
CFG = ROOT / "assets/stegfin-phone/coinbase-skap-ingress-config.json"
HTML = ROOT / "stegfin-trade.html"
BOOTSTRAP = ROOT / "assets/stegfin-phone/stegid-device-wallet-bootstrap.js"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    js = JS.read_text(encoding="utf-8")
    ui = UI.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    cfg = json.loads(CFG.read_text(encoding="utf-8"))

    require(cfg.get("schema") == "stegverse.site.coinbase_skap_ingress_config/v1", "config schema invalid")
    require(cfg.get("status") in {"NOT_PROVISIONED", "PROVISIONED"}, "config status invalid")
    require(cfg.get("endpoint_origin") == "https://api.coinbase.com", "endpoint origin invalid")
    require(cfg.get("credential_authority") == "TV/TVC", "credential authority invalid")
    require(cfg.get("physical_execution_surface") == "CURRENT_USER_IPHONE", "physical surface invalid")
    require(cfg.get("second_machine_required") is False, "second machine must not be required")
    require(cfg.get("device_durable_secret_custody") is False, "device custody forbidden")
    require(cfg.get("kv_secret_resolution_authority") is False, "KV resolution forbidden")
    require(cfg.get("github_environment_secret_access") is False, "GitHub secret access forbidden")

    if cfg["status"] == "NOT_PROVISIONED":
        require(cfg.get("recipient_key_id") is None, "unprovisioned config must not claim recipient key id")
        require(cfg.get("recipient_public_jwk") is None, "unprovisioned config must not claim recipient public key")
    else:
        jwk = cfg.get("recipient_public_jwk") or {}
        require(jwk.get("kty") == "EC" and jwk.get("crv") == "P-256", "provisioned recipient key must be P-256 public JWK")
        require("d" not in jwk, "private JWK material forbidden")
        require(str(cfg.get("recipient_key_id") or "").startswith("tvc://skap/browser-ingress/coinbase/"), "recipient key id authority invalid")

    required_js = (
        "P-256", "ECDH", "HKDF", "SHA-256", "AES-GCM",
        "https://api.coinbase.com", "CURRENT_USER_IPHONE",
        "STEGVERSE_BROWSER_CAPSULE", "TV/TVC", "skap://APIs/coinbase/owner/",
        "delete ephemeralPublicJwk.d", "redirect: 'error'",
        "window.StegIDDeviceWalletBootstrap", "issueCurrentPhonePrepareCapability",
        "device_secret_custody_authority: false", "kv_secret_resolution_authority: false",
        "github_environment_secret_access: false", "plaintext_present: false"
    )
    for marker in required_js:
        require(marker in js, f"missing browser ingress invariant: {marker}")

    forbidden_calls = (
        r"localStorage\s*\.\s*setItem\s*\(",
        r"sessionStorage\s*\.\s*setItem\s*\(",
        r"indexedDB\s*\.\s*(open|deleteDatabase)\s*\(",
        r"document\s*\.\s*cookie\s*=",
        r"console\s*\.\s*(log|debug|info|warn|error)\s*\(",
        r"navigator\s*\.\s*sendBeacon\s*\(",
    )
    combined = js + "\n" + ui
    for pattern in forbidden_calls:
        require(re.search(pattern, combined) is None, f"forbidden credential persistence/logging call: {pattern}")

    require("coinbaseApiKeyName" in html and "coinbaseApiPrivateKey" in html, "credential fields missing")
    require(re.search(r'id="coinbaseApiKeyName"[^>]*\sdisabled', html) is not None, "API key input must default disabled")
    require(re.search(r'id="coinbaseApiPrivateKey"[^>]*\sdisabled', html) is not None, "private-key input must default disabled")
    require(re.search(r'id="coinbaseSealCredential"[^>]*\sdisabled', html) is not None, "seal action must default disabled")
    require("coinbase-skap-ingress.js" in html and "coinbase-skap-ingress-ui.js" in html, "SKAP ingress scripts not projected")
    require("SKAP public ingress key" in html, "fail-closed public-key explanation missing")

    require("navigator.credentials.create" in bootstrap, "existing WebAuthn create ceremony missing")
    require("navigator.credentials.get" in bootstrap, "existing WebAuthn get ceremony missing")
    require("userVerification: 'required'" in bootstrap, "WebAuthn user verification weakened")
    require("credential_authority: 'TV/TVC'" in bootstrap, "TV/TVC authority missing from owner authorization surface")

    print("COINBASE_SKAP_PHONE_INGRESS_SOURCE_OK")
    print(f"config_status={cfg['status']}")
    print("physical_surface=CURRENT_USER_IPHONE")
    print("recipient_private_key_on_phone=false")
    print("device_durable_secret_custody=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
