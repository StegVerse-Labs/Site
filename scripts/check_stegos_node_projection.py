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
BASE_CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-registration-offline-history-468.json"
OFFLINE_CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-physical-offline-proof-480.json"

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
OFFLINE_INDEX_MARKERS = (
    'id="offline-reload-proof"',
    'Offline Reload Proof',
    'offline_reload_proof: history.offline_reload_proof || null',
    'network_activation_claimed: false',
)
OFFLINE_JS_MARKERS = (
    'OFFLINE_PROOF_KEY = "offline-reload-proof"',
    'stegos.node_offline_reload_proof.v1',
    'navigator.serviceWorker && navigator.serviceWorker.controller',
    'navigator.onLine === false',
    'service_worker_controlled: true',
    'offline_observed: true',
    'current_network_required: false',
    'network_topology_claimed: false',
    'heartbeat_interlock_observation_verified: false',
    'physical_activation_claimed: false',
    'network_activation_claimed: false',
    'proof_sha256',
    'validateOfflineReloadProof',
    'recordOfflineReloadProof',
)
PROHIBITED_JS = (
    'navigator.userAgent',
    'serialNumber',
    'hardware_id',
    'github_token',
    'GITHUB_TOKEN',
    'RENDER_API',
    'network_topology_claimed: true',
    'physical_activation_claimed: true',
    'network_activation_claimed: true',
)


def validate_projection(
    index: str,
    js: str,
    sw: str,
    base_claim: str,
    offline_claim: str,
    *,
    require_offline_proof: bool,
) -> list[str]:
    failures: list[str] = []
    for marker in INDEX_MARKERS:
        if marker not in index:
            failures.append(f"index missing {marker}")
    for marker in JS_MARKERS:
        if marker not in js:
            failures.append(f"projection missing {marker}")
    if require_offline_proof:
        for marker in OFFLINE_INDEX_MARKERS:
            if marker not in index:
                failures.append(f"offline proof index missing {marker}")
        for marker in OFFLINE_JS_MARKERS:
            if marker not in js:
                failures.append(f"offline proof projection missing {marker}")
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
        if marker not in base_claim:
            failures.append(f"base claim missing {marker}")
    if require_offline_proof:
        for marker in (
            'SITE-STEGOS-NODE-PHYSICAL-OFFLINE-PROOF-480-20260824',
            'site:stegos-node-physical-offline-proof',
            'TV/TVC',
        ):
            if marker not in offline_claim:
                failures.append(f"offline proof claim missing {marker}")
        if (
            '"state": "CLAIMED_FOR_INTEGRATION"' not in offline_claim
            and '"state": "RELEASED_TO_STEGOS_23"' not in offline_claim
        ):
            failures.append(
                "offline proof claim must be active integration or durably released to StegOS#23"
            )
    return failures


def fetch_public_text(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("live observation requires an absolute HTTPS URL")
    request = Request(
        url,
        headers={
            "User-Agent": "StegVerse-Site-Stegos-Node-Observer/1.1",
            "Accept": "text/html,application/javascript,text/javascript,*/*;q=0.1",
        },
    )
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise ValueError(f"live observation returned HTTP {response.status} for {url}")
        return response.read().decode("utf-8")


def validate_live_projection(
    base_url: str,
    base_claim: str,
    offline_claim: str,
    *,
    require_offline_proof: bool,
) -> list[str]:
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

    failures.extend(
        validate_projection(
            index,
            js,
            sw,
            base_claim,
            offline_claim,
            require_offline_proof=require_offline_proof,
        )
    )
    if '"name"' not in manifest or 'StegOS' not in manifest:
        failures.append("live manifest missing StegOS identity")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate StegOS Node source and optional exact public projection")
    parser.add_argument("--live-url", help="Exact deployed StegOS Node directory URL; HTTPS only")
    parser.add_argument(
        "--require-offline-proof",
        action="store_true",
        help="Require the physical offline-reload proof capability in the deployed projection",
    )
    args = parser.parse_args()

    failures: list[str] = []
    for path in (INDEX, JS, SW, MANIFEST, BASE_CLAIM, OFFLINE_CLAIM):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if not failures:
        index = INDEX.read_text(encoding="utf-8")
        js = JS.read_text(encoding="utf-8")
        sw = SW.read_text(encoding="utf-8")
        base_claim = BASE_CLAIM.read_text(encoding="utf-8")
        offline_claim = OFFLINE_CLAIM.read_text(encoding="utf-8")
        # Source must always carry the offline-proof capability. The historical
        # Site#480 claim may be active during integration or durably released.
        failures.extend(
            validate_projection(
                index,
                js,
                sw,
                base_claim,
                offline_claim,
                require_offline_proof=True,
            )
        )
        if args.live_url:
            failures.extend(
                validate_live_projection(
                    args.live_url,
                    base_claim,
                    offline_claim,
                    require_offline_proof=args.require_offline_proof,
                )
            )

    if failures:
        print("STEGOS_NODE_PROJECTION_FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("STEGOS_NODE_PROJECTION_PASS")
    print("STEGOS_NODE_OFFLINE_PROOF_SOURCE_PASS")
    if args.live_url:
        print(f"STEGOS_NODE_PUBLIC_OBSERVATION_PASS {args.live_url}")
        if args.require_offline_proof:
            print("STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS")
        print("AUTHORITY_EFFECT=NONE")
        print("PHYSICAL_NODE_ACTIVATION_CLAIMED=false")
        print("NETWORK_ACTIVATION_CLAIMED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
