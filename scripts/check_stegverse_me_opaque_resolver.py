#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
contract=json.loads((ROOT/"data/stegverse-me-opaque-resolver-contract.json").read_text())
script=(ROOT/"stegos-node/stegverse-me-opaque-resolver.js").read_text()
page=(ROOT/"stegos-node/stegverse-me-resolver.html").read_text()
handoff=(ROOT/"docs/STEGVERSE_ME_OPAQUE_NODE_RESOLVER_MIRROR_HANDOFF.md").read_text()
claim=json.loads((ROOT/"data/session-work-claims.d/site-stegverse-me-opaque-resolver-680.json").read_text())["claims"][0]
assert contract["schema"]=="stegverse.site.opaque-node-local-continuity-resolver/v1"
assert contract["canonical_domain"]=="stegverse.me"
assert contract["route_possession_grants_access"] is False
assert contract["private_kv_readback_performed"] is False
assert contract["authenticated_interlock_admission_performed"] is False
assert contract["server_identity_registry_required"] is False
assert contract["specific_external_platform_required"] is False
assert contract["dns_mutation_allowed"] is False
assert contract["authority_effect"]=="NONE" and contract["activation_effect"] is False
assert contract["production"]=={"origin_selected":False,"dns_configured":False,"tls_observed":False,"authenticated_resolution_observed":False,"private_kv_readback_observed":False,"activation_claimed":False}
for token in ("stegos.web_node.v1","stegos.web_device_continuity_root.v1","stegos.web_device_node_binding_receipt.v1","OPAQUE_NODE_ROUTE_MISMATCH","route_possession_grants_access: false","private_kv_readback_performed: false","authority_effect: \"NONE\"","activation_effect: false"):
    assert token in script, token
for token in ("stegos-web-bootstrap-v1","device-continuity-root","FAIL_CLOSED","The route itself grants no access"):
    assert token in page, token
assert any(marker in handoff for marker in ("State: IMPLEMENTATION_CLAIM_ADMISSION","State: VALIDATION_CLAIM_ADMISSION","State: RELEASED"))
assert claim["state"] in {"CLAIMED_FOR_IMPLEMENTATION","CLAIMED_FOR_VALIDATION","RELEASED"}
assert claim["authority_effect"] is False and claim["activation_effect"] is False
print("STEGVERSE_ME_OPAQUE_RESOLVER_PASS")
print("DNS_MUTATION_PERFORMED=false")
print("PRIVATE_KV_READBACK=false")
print("AUTHORITY_EFFECT=NONE")
print("ACTIVATION_EFFECT=false")
