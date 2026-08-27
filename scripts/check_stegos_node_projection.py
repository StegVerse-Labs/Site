#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-node" / "index.html"
JS = ROOT / "stegos-node" / "stegos-node.js"
SW = ROOT / "stegos-node" / "service-worker.js"
MANIFEST = ROOT / "stegos-node" / "manifest.webmanifest"
READINESS = ROOT / "stegos-node" / "kv-readiness-snapshot.json"
BASE_CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-registration-offline-history-468.json"
OFFLINE_CLAIM = ROOT / "data" / "session-work-claims.d" / "site-stegos-node-physical-offline-proof-480.json"

INDEX_MARKERS = (
    'id="register-device"',
    'Register Device',
    'id="capture-peer-evidence"',
    'Register &amp; Export Evidence',
    'id="network-sync"',
    'Last StegOS Network Sync',
    'id="personal-kv-sync"',
    'Last Personal KV Sync',
    'id="local-receipt-head"',
    'KnowledgeVault',
    'Device History',
    'id="kv-capability-shell"',
    'KnowledgeVault Capabilities',
    'id="kv-capability-local-ready"',
    'id="kv-capability-local-blocked"',
    'id="kv-capability-governed-ready"',
    'id="kv-capability-governed-blocked"',
    'id="kv-available-modules"',
    'id="kv-available-services"',
    'id="kv-blocked-modules"',
    'id="kv-blocked-services"',
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
    'stegos.site.kv_capability_shell_projection.v1',
    '"source_stegos_view_schema": "stegos.kv_capability_shell_view.v1"',
    '"source_stegos_merge": "4dad89be44e472eb4a5db10bfd294ded803d1456"',
    '"entry_count": 46',
    '"local_ready": 45',
    '"local_blocked": 1',
    '"governed_ready": 0',
    '"governed_blocked": 46',
    'BLOCKED_CURRENT_IDENTITY',
    '"activation_control_present": false',
    '"kv_state_mutation_available": false',
    '"provider_execution_available": false',
    '"activation_performed": false',
    'authority_effect: "NONE"',
    'renderKvCapabilityShell',
    'disabled governed control must expose blockers',
)
READINESS_JS_MARKERS = (
    'KV_READINESS_STATE_KEY = "kv-readiness-device-state"',
    'KV_READINESS_SNAPSHOT_URL = "./kv-readiness-snapshot.json"',
    'stegos.site.kv_device_readiness_state.v1',
    'stegos.kv_readiness_update_envelope.v1',
    'validateKvReadinessSnapshot',
    'initializeKvReadinessBrowserState',
    'applyKvReadinessUpdate',
    'validateKvReadinessBrowserState',
    'stale or replayed KV readiness update',
    'KV readiness envelope prior digest mismatch',
    'KV readiness envelope successor digest mismatch',
    'transport_delivery_performed: false',
    'interlock_delivery_admission_observed: false',
    'kv_mutation_performed: false',
    'provider_operation_authorized: false',
    'execution_authority: "NONE"',
    'stegverse.intr.hop_receipt/v1',
    'stegos.kv_readiness_intr_delivery_admission.v1',
    'stegos.site.kv_readiness_admitted_device_apply.v1',
    'validateKvReadinessIntrReceipt',
    'validateKvReadinessIntrDeliveryAdmission',
    'applyAdmittedKvReadinessDelivery',
    'KV readiness InTr hop must be KV->DEVICE',
    'KV readiness InTr payload does not bind exact envelope',
    'KV readiness delivery admission canonical field mismatch',
    'stale or replayed admitted KV readiness delivery',
    'browser readiness state must remain transport-neutral',
    'transport_delivery_performed: true',
    'interlock_delivery_admission_observed: true',
    'local_state_refresh_performed: true',
)

READINESS_SNAPSHOT_MARKERS = (
    '"schema": "stegverse.kv.activation-readiness-snapshot/v1"',
    '"facts_observed_at": "2026-08-27T04:08:00Z"',
    '"entry_count": 46',
    '"module_count": 13',
    '"service_count": 33',
    '"production_interlock_runtime_activated": false',
    '"activation_performed": false',
    '"authority_effect": "NONE"',
    '"local_ready": 45',
    '"local_blocked": 1',
    '"governed_ready": 0',
    '"governed_blocked": 46',
    '"skap_vault_runtime_boundary_observed"',
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
    readiness: str,
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
    for marker in READINESS_JS_MARKERS:
        if marker not in js:
            failures.append(f"readiness browser projection missing {marker}")
    for marker in READINESS_SNAPSHOT_MARKERS:
        if marker not in readiness:
            failures.append(f"readiness snapshot missing {marker}")
    try:
        readiness_obj = json.loads(readiness)
        if readiness_obj.get("entry_count") != 46 or len(readiness_obj.get("entries", [])) != 46:
            failures.append("readiness snapshot exact entry cardinality mismatch")
        if readiness_obj.get("authority_effect") != "NONE" or readiness_obj.get("activation_performed") is not False:
            failures.append("readiness snapshot authority/activation boundary invalid")
    except json.JSONDecodeError:
        failures.append("readiness snapshot invalid JSON")
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
    for marker in ('CACHE_NAME', 'stegos-node-shell-v4-kv-intr-admitted-apply', './index.html', './stegos-node.js', './kv-readiness-snapshot.json', './manifest.webmanifest'):
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
            "User-Agent": "StegVerse-Site-Stegos-Node-Observer/1.2",
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
        readiness = fetch_public_text(urljoin(base_url, "kv-readiness-snapshot.json"))
    except Exception as exc:
        return [f"live observation failed: {exc}"]

    failures.extend(
        validate_projection(
            index,
            js,
            sw,
            base_claim,
            offline_claim,
            readiness,
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
    for path in (INDEX, JS, SW, MANIFEST, READINESS, BASE_CLAIM, OFFLINE_CLAIM):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if not failures:
        index = INDEX.read_text(encoding="utf-8")
        js = JS.read_text(encoding="utf-8")
        sw = SW.read_text(encoding="utf-8")
        base_claim = BASE_CLAIM.read_text(encoding="utf-8")
        offline_claim = OFFLINE_CLAIM.read_text(encoding="utf-8")
        readiness = READINESS.read_text(encoding="utf-8")
        failures.extend(
            validate_projection(
                index,
                js,
                sw,
                base_claim,
                offline_claim,
                readiness,
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
    print("STEGOS_NODE_ONE_ACTION_PEER_SOURCE_PASS")
    print("STEGOS_NODE_OFFLINE_PROOF_SOURCE_PASS")
    print("STEGOS_NODE_KV_CAPABILITY_SHELL_SOURCE_PASS")
    print("STEGOS_NODE_KV_READINESS_BROWSER_STATE_SOURCE_PASS")
    print("STEGOS_NODE_KV_INTR_BROWSER_APPLY_SOURCE_PASS")
    if args.live_url:
        print(f"STEGOS_NODE_PUBLIC_OBSERVATION_PASS {args.live_url}")
        print("STEGOS_NODE_ONE_ACTION_PEER_PUBLIC_OBSERVATION_PASS")
        print("STEGOS_NODE_KV_CAPABILITY_SHELL_PUBLIC_OBSERVATION_PASS")
        print("STEGOS_NODE_KV_READINESS_BROWSER_STATE_PUBLIC_OBSERVATION_PASS")
        print("STEGOS_NODE_KV_INTR_BROWSER_APPLY_PUBLIC_OBSERVATION_PASS")
        if args.require_offline_proof:
            print("STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS")
        print("AUTHORITY_EFFECT=NONE")
        print("PHYSICAL_NODE_ACTIVATION_CLAIMED=false")
        print("NETWORK_ACTIVATION_CLAIMED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
