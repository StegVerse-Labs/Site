#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = os.environ.get("STEGVERSE_PUBLIC_ROOT", "https://stegverse.org").rstrip("/")
PAGE_URL = f"{PUBLIC_ROOT}/stegfin-trade.html"
UI_URL = f"{PUBLIC_ROOT}/assets/stegfin-phone/wallet-user-handoff-ui.js"
BOOTSTRAP_URL = f"{PUBLIC_ROOT}/assets/stegfin-phone/stegid-device-wallet-bootstrap.js"
EXPECTED_UI_BLOB = "114b3c39052d5b1622407080407259a0040a1369"
EXPECTED_BOOTSTRAP_BLOB = "dc1a86bc564146cdaa645620c8fc698e45029440"
EXPECTED_SITE_MERGE = "8c5882b2ff3a17c847d48376b856db32c0331832"
REPORT = Path(
    os.environ.get(
        "STEGVERSE_STEGFIN_PUBLICATION_REPORT",
        os.environ.get(
            "STEGFIN_PUBLICATION_REPORT",
            str(ROOT / "stegfin-public-wallet-transport.report.json"),
        ),
    )
).expanduser().resolve()


def git_blob_sha(data: bytes) -> str:
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def fetch(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "StegVerse-StegFin-Publication-Observer/1.1"},
    )
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as response:
        return int(response.status), response.geturl(), response.read(524288)


def main() -> int:
    report: dict[str, object] = {
        "schema": "site.stegfin_public_wallet_transport_observation.v1",
        "task_id": "SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-PUBLISH",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "state": "BLOCKED",
        "site_merge": EXPECTED_SITE_MERGE,
        "expected_ui_blob": EXPECTED_UI_BLOB,
        "expected_bootstrap_blob": EXPECTED_BOOTSTRAP_BLOB,
        "page_url": PAGE_URL,
        "ui_url": UI_URL,
        "bootstrap_url": BOOTSTRAP_URL,
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "non_tv_tvc_secret_or_token_used": False,
        "github_token_required": False,
        "render_required": False,
        "wallet_signing_authority": "USER_ONLY",
        "broadcast_authority": "USER_ONLY",
        "authority_effect": False,
        "activation_effect": False,
    }
    try:
        page_status, page_final, page = fetch(PAGE_URL)
        ui_status, ui_final, ui = fetch(UI_URL)
        bootstrap_status, bootstrap_final, bootstrap = fetch(BOOTSTRAP_URL)
        ui_blob = git_blob_sha(ui)
        bootstrap_blob = git_blob_sha(bootstrap)
        page_text = page.decode("utf-8", errors="replace")
        ui_text = ui.decode("utf-8", errors="replace")
        bootstrap_text = bootstrap.decode("utf-8", errors="replace")
        required_page = [
            "./assets/stegfin-phone/stegid-device-wallet-bootstrap.js",
            "./assets/stegfin-phone/wallet-user-handoff.js",
            "./assets/stegfin-phone/wallet-user-handoff-ui.js",
            "Review wallet handoff",
            "TV/TVC",
            "USER_ONLY",
        ]
        required_ui = [
            "Open StegVerse in local wallet browser",
            "No injected EIP-1193 wallet is available in this browser. No wallet action occurred.",
            "https://metamask.app.link/dapp/",
            "Safari candidate is not transferred or reused",
            "No wallet relay or hosted wallet middleware is used for transaction authority",
        ]
        required_bootstrap = [
            "platformAuthenticatorProbe",
            "Treat that boolean as an advisory capability hint",
            "navigator.credentials.create",
            "navigator.credentials.get",
            "userVerification: 'required'",
            "uvpaa_hint: probe.uvpaa",
            "credential_authority: 'TV/TVC'",
            "credential_requirement: 'NONE'",
            "automatic_signing: false",
            "automatic_broadcast: false",
        ]
        forbidden_bootstrap = [
            "throw new Error('user-verifying platform authenticator unavailable')",
            "WalletConnect",
            "GITHUB_TOKEN",
            "GH_TOKEN",
            "WALLET_PRIVATE_KEY",
        ]
        missing_page = [marker for marker in required_page if marker not in page_text]
        missing_ui = [marker for marker in required_ui if marker not in ui_text]
        missing_bootstrap = [marker for marker in required_bootstrap if marker not in bootstrap_text]
        forbidden_bootstrap_present = [marker for marker in forbidden_bootstrap if marker in bootstrap_text]
        report.update(
            {
                "page_http_status": page_status,
                "page_final_url": page_final,
                "ui_http_status": ui_status,
                "ui_final_url": ui_final,
                "bootstrap_http_status": bootstrap_status,
                "bootstrap_final_url": bootstrap_final,
                "tls_verified": (
                    page_final.startswith("https://")
                    and ui_final.startswith("https://")
                    and bootstrap_final.startswith("https://")
                ),
                "observed_ui_blob": ui_blob,
                "ui_blob_match": ui_blob == EXPECTED_UI_BLOB,
                "observed_bootstrap_blob": bootstrap_blob,
                "bootstrap_blob_match": bootstrap_blob == EXPECTED_BOOTSTRAP_BLOB,
                "missing_page_markers": missing_page,
                "missing_ui_markers": missing_ui,
                "missing_bootstrap_markers": missing_bootstrap,
                "forbidden_bootstrap_markers_present": forbidden_bootstrap_present,
            }
        )
        if (
            page_status == 200
            and ui_status == 200
            and bootstrap_status == 200
            and report["tls_verified"] is True
            and ui_blob == EXPECTED_UI_BLOB
            and bootstrap_blob == EXPECTED_BOOTSTRAP_BLOB
            and not missing_page
            and not missing_ui
            and not missing_bootstrap
            and not forbidden_bootstrap_present
        ):
            report["state"] = "VERIFIED_PUBLICATION"
            report["publication_proven"] = True
            report["activation_effect"] = "PUBLICATION_ONLY_CURRENT_PHONE_PROOF_REQUIRED"
        else:
            report["publication_proven"] = False
    except Exception as exc:
        report["publication_proven"] = False
        report["error"] = f"{type(exc).__name__}: {exc}"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if report["state"] == "VERIFIED_PUBLICATION":
        print("STEGFIN_PUBLIC_WALLET_TRANSPORT=PASS")
        print(f"SITE_MERGE={EXPECTED_SITE_MERGE}")
        print(f"UI_BLOB={EXPECTED_UI_BLOB}")
        print(f"BOOTSTRAP_BLOB={EXPECTED_BOOTSTRAP_BLOB}")
        print("CURRENT_PHONE_PROOF_REQUIRED=true")
        print("AUTHORITY_GRANTED=false")
        print("GITHUB_TOKEN_REQUIRED=false")
        return 0

    print("STEGFIN_PUBLIC_WALLET_TRANSPORT=BLOCKED")
    print(json.dumps(report, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
