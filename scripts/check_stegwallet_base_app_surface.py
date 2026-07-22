#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / "stegwallet.html").read_text(encoding="utf-8")
js = (root / "assets/stegwallet.js").read_text(encoding="utf-8")
doc = (root / "docs/STEGWALLET_BASE_APP_DOMAIN_STRATEGY.md").read_text(encoding="utf-8")

required_html = [
    "Base App and injected wallets",
    "basename-alias",
    "environment-status",
    "Open wallet approval",
    "domain / Basename / profile  != execution authority",
]
required_js = [
    "stegwallet.browser_environment.v1",
    "environment_trusted_for_authority: false",
    "canonical_web_origin: location.origin",
    "basename_grants_authority: false",
    "domain_grants_authority: false",
    "private_key_requested",
    "eth_sendTransaction",
]
required_doc = [
    "stegverse.org",
    "stegverse.base.eth",
    "registration does not host the web application",
    "No registration transaction is authorized",
]

missing = [f"html:{item}" for item in required_html if item not in html]
missing += [f"js:{item}" for item in required_js if item not in js]
missing += [f"doc:{item}" for item in required_doc if item not in doc]

for forbidden in ("seed phrase input", "private key input", "domain_grants_authority: true", "basename_grants_authority: true"):
    if forbidden in html.lower() or forbidden in js.lower():
        missing.append(f"forbidden:{forbidden}")

if missing:
    raise SystemExit("StegWallet Base App surface validation failed: " + ", ".join(missing))

print("StegWallet Base App surface: PASS")
