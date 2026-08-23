#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-node" / "index.html"
JS = ROOT / "stegos-node" / "stegos-node.js"
SW = ROOT / "stegos-node" / "service-worker.js"
MANIFEST = ROOT / "stegos-node" / "manifest.webmanifest"
CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-registration-offline-history-468.json"

failures = []
for path in (INDEX, JS, SW, MANIFEST, CLAIM):
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")

if not failures:
    index = INDEX.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    sw = SW.read_text(encoding="utf-8")
    claim = CLAIM.read_text(encoding="utf-8")

    required_index = (
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
    for marker in required_index:
        if marker not in index:
            failures.append(f"index missing {marker}")

    required_js = (
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
    for marker in required_js:
        if marker not in js:
            failures.append(f"projection missing {marker}")

    prohibited = (
        'navigator.userAgent',
        'serialNumber',
        'hardware_id',
        'github_token',
        'GITHUB_TOKEN',
        'RENDER_API',
    )
    for marker in prohibited:
        if marker in js:
            failures.append(f"prohibited projection marker {marker}")

    for marker in ('CACHE_NAME', './index.html', './stegos-node.js', './manifest.webmanifest'):
        if marker not in sw:
            failures.append(f"service worker missing {marker}")

    for marker in (
        'SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468-20260823',
        'CLAIMED_FOR_INTEGRATION',
        'site:stegos-node-registration-offline-history',
        'TV/TVC',
    ):
        if marker not in claim:
            failures.append(f"claim missing {marker}")

if failures:
    print("STEGOS_NODE_PROJECTION_FAIL")
    for failure in failures:
        print(failure)
    sys.exit(1)

print("STEGOS_NODE_PROJECTION_PASS")
