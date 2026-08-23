#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-node" / "index.html"
JS = ROOT / "stegos-node" / "stegos-node.js"
SW = ROOT / "stegos-node" / "service-worker.js"
MANIFEST = ROOT / "stegos-node" / "manifest.webmanifest"
CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-registration-offline-history-468.json"

INDEX_MARKERS = (
    'id="register-device"',
    'Register Device',
    'id="network-sync"',
    'Last StegOS Network Sync',
    'id="personal-kv-sync"',
    'Last Personal KV Sync',
    'id="local-receipt-head"',
    'KnowledgeVault',
    'Device History',
)
JS_MARKERS = (
    'stegos.node_handoff_receipt.v1',
    'receipt_number: 1',
    'transition: "NODE_REGISTERED"',
    'prior_state: "UNREGISTERED"',
    'resulting_state: "REGISTERED"',
    'continuity_parent: "GENESIS"',
    'credential_authority: "TV/TVC"',
    'authority_effect: "NONE"',
    'hardware_attestation_claimed: false',
    'knowledge_vault_materialization_enabled: true',
    'last_personal_kv_sync',
    'last_stegos_network_sync',
    'section_views_are_filtered_projections: true',
    'competing_logs_allowed: false',
    'wall_clock_is_causal_order: false',
    'current_network_required: false',
    'crypto.getRandomValues',
    'random.fill(0)',
)
PROHIBITED_JS = (
    'navigator.userAgent',
    'serialNumber',
    'hardware_id',
    'github_token',
    'GITHUB_TOKEN',
    'RENDER_API',
)


def validate_projection(index: str, js: str, sw: str, claim: str) -> list[str]:
    failures: list[str] = []
    for marker in INDEX_MARKERS:
        if marker not in index:
            failures.append(f"index missing {marker}")
    for marker in JS_MARKERS:
        if marker not in js:
            failures.append(f"projection missing {marker}")
    for marker in PROHIBITED_JS:
        if marker in js:
            failures.append(f"prohibited projection marker {marker}")
    for marker in ('CACHE_NAME', './index.html', './stegos-node.js', './manifest.webmanifest'):
        if marker not in sw:
            failures.append(f"service worker missing {marker}")
    for marker in (
        'SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468-20260823',
        'site:stegos-node-registration-offline-history',
        'TV/TVC',
    ):
        if marker not in claim:
            failures.append(f"claim missing {marker}")
    return failures


def fetch_public_text(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("live observation requires an absolute HTTPS URL")
    request = Request(
        url,
        headers={
            "User-Agent": "StegVerse-Site-Stegos-Node-Observer/1.0",
            "Accept": "text/html,application/javascript,text/javascript,*/*;q=0.1",
        },
    )
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise ValueError(f"live observation returned HTTP {response.status} for {url}")
        return response.read().decode("utf-8")


def validate_live_projection(base_url: str, claim: str) -> list[str]:
    failures: list[str] = []
    if not base_url.endswith("/"):
        base_url += "/"
    try:
        index = fetch_public_text(base_url)
        js = fetch_public_text(urljoin(base_url, "stegos-node.js"))
        sw = fetch_public_text(urljoin(base_url, "service-worker.js"))
        manifest = fetch_public_text(urljoin(base_url, "manifest.webmanifest"))
    except Exception as exc:
        return [f"live observation failed: {exc}"]

    failures.extend(validate_projection(index, js, sw, claim))
    if '"name"' not in manifest or 'StegOS' not in manifest:
        failures.append("live manifest missing StegOS identity")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate StegOS Node source and optional exact public projection")
    parser.add_argument("--live-url", help="Exact deployed StegOS Node directory URL; HTTPS only")
    args = parser.parse_args()

    failures: list[str] = []
    for path in (INDEX, JS, SW, MANIFEST, CLAIM):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if not failures:
        index = INDEX.read_text(encoding="utf-8")
        js = JS.read_text(encoding="utf-8")
        sw = SW.read_text(encoding="utf-8")
        claim = CLAIM.read_text(encoding="utf-8")
        failures.extend(validate_projection(index, js, sw, claim))
        if args.live_url:
            failures.extend(validate_live_projection(args.live_url, claim))

    if failures:
        print("STEGOS_NODE_PROJECTION_FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("STEGOS_NODE_PROJECTION_PASS")
    if args.live_url:
        print(f"STEGOS_NODE_PUBLIC_OBSERVATION_PASS {args.live_url}")
        print("AUTHORITY_EFFECT=NONE")
        print("PHYSICAL_NODE_ACTIVATION_CLAIMED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
