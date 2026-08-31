#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
sync=(ROOT/"stegos-node/device-kv-intr-sync.js").read_text()
target=json.loads((ROOT/"stegos-node/device-kv-intr-sync-target.json").read_text())
page=(ROOT/"my-kv-directory.html").read_text()
portable=(ROOT/"assets/my-kv-portable-direct-source-bridge.js").read_text()

required=[
 "stegverse.device-kv-intr-materialization-ingress/v1",
 'JSON.stringify({ boundary: "KV", subsystem: "KnowledgeVault:Interlock" })',
 'StegVerse-Labs/continuity-vault-kit#79',
 "STEGOS_NODE_OUTBOX",
 "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY",
 "INGRESS_ADMITTED",
 "runtime_materialization_observed: false",
 "network_delivery_observed: true",
 "claim_or_fence_minted: false",
 'credential_authority: "TV/TVC"',
 'github_token_runtime_authority: "NONE"',
 "/intr/materialization",
]
for marker in required:
    if marker not in sync:
        raise SystemExit("DEVICE_KV sync missing: "+marker)

if target!={
 "schema":"stegos.site.device_kv_intr_sync_target.v1",
 "state":"AWAITING_SOVEREIGN_INTR_INGRESS",
 "ingress_url":None,
 "transport_origin":"STEGOS_NODE_OUTBOX",
 "runtime_ingress_observed":False,
 "configuration_authority":"StegVerse sovereign profiled InTr runtime evidence projection",
 "credential_authority":"TV/TVC",
 "credential_requirement":"NONE",
 "github_token_runtime_authority":"NONE",
 "execution_authority":"NONE",
 "authority_effect":"NONE_DISCOVERY_ONLY",
}:
    raise SystemExit("DEVICE_KV target must remain exact fail-closed baseline")

order=[
 'assets/stegverse-node-continuity.js',
 'stegos-node/device-kv-intr-sync.js',
 'assets/my-kv-directory.js',
 'assets/my-kv-portable-direct-source-bridge.js',
]
positions=[page.find(x) for x in order]
if any(x<0 for x in positions) or positions!=sorted(positions):
    raise SystemExit("My KV directory Node/sync script order invalid")
if 'StegVerseDeviceKVInTrSync.attempt()' not in portable:
    raise SystemExit("portable source bridge does not trigger DEVICE_KV egress")
if "CONFORMING_SOVEREIGN_INTR_INGRESS" not in sync or "AWAITING_SOVEREIGN_INTR_INGRESS" not in sync:
    raise SystemExit("DEVICE_KV target lifecycle missing")
print("DEVICE_KV InTr sync static checks: PASS")
