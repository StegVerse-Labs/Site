# StegOS HIL Universal InTr Node Sync Mirror Handoff

Updated: 2026-08-29
Repository: `StegVerse-Labs/Site`
Issue: #632
Upstream ingress owner: `StegVerse-Labs/.github#421`
Parent HIL activation owner: `StegVerse-Labs/.github#246`

```text
goal_id: SITE-HIL-INTR-NODE-SYNC-632
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
credential_authority: TV/TVC
github_token_runtime_authority: NONE
authority_effect: NONE_TRANSPORT_TRIGGER_ONLY
network_delivery_observed: false
runtime_materialization_observed: false
receiver_receipt_observed: false
```

## Purpose

Close the source seam from the already-registered browser StegOS Node HIL local outbox to the sovereign HIL materialization ingress without turning the browser into TVC route/EGRESS authority.

The HIL Universal InTr materialization request is an event trigger only. It asks the existing sovereign HIL execution owner to materialize event-ephemerally. It does **not** carry the staged response PDF or provenance bytes and it does not grant WorkerCoordinator execution authority.

Canonical source path:

```text
HIL browser fallback store
-> validated Universal InTr materialization request
-> registered StegOS Node write-once local outbox
-> stegos-node/hil-intr-sync.js
-> direct STEGOS_NODE_OUTBOX trigger envelope
-> sovereign /intr/materialization ingress
-> INGRESS_ADMITTED receipt
-> browser records network-delivery observation only
```

The exact response PDF remains in the existing HIL browser fallback store until the real HIL receiver is READY and the existing HIL submission path retries it.

## Fail-closed target discovery

`stegos-node/hil-intr-sync-target.json` is the only source-side runtime locator projection. Its canonical merged default remains:

```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
transport_origin: STEGOS_NODE_OUTBOX
credential_authority: TV/TVC
credential_requirement: NONE
github_token_runtime_authority: NONE
execution_authority: NONE
authority_effect: NONE_DISCOVERY_ONLY
```

The browser does not attempt transport while this state is unresolved. A future projection to `CONFORMING_SOVEREIGN_INTR_INGRESS` requires independently observed sovereign runtime evidence and an exact credentialless HTTPS `/intr/materialization` locator. Source/CI cannot mint that state.

## Browser synchronization contract

Before POST, `hil-intr-sync.js` revalidates the entire local outbox entry and recomputes `outbox_entry_hash`. It then emits:

```text
schema: stegos.node_intr_materialization_trigger.v1
transport_origin: STEGOS_NODE_OUTBOX
node_id: exact registered Node
interlock_id: exact registered Interlock
outbox_entry_hash: exact local write-once entry
node_outbox_entry: complete validated local entry
request_grants_execution_authority: false
claim_or_fence_minted: false
authority_effect: NONE_TRIGGER_ONLY
trigger_sha256: exact canonical trigger hash
```

Transport headers are limited to the canonical InTr origin and exact raw-body SHA-256. There is no `Authorization` header, no `X-StegVerse-Authorization-Id`, and fetch uses `credentials: omit`.

## Delivery observation boundary

HTTP success alone is insufficient. The browser validates the returned `stegverse.hil-intr-materialization-ingress/v1` receipt against the exact materialization id, request hash, transport-intent hash, payload hash, Node id, Interlock id, outbox-entry hash, trigger body SHA-256, and non-authorizing invariants.

Only then may it persist a separate `stegos.node_intr_delivery_receipt.v1` and advance the Node's `last_stegos_network_sync` observation. That observation still records:

```text
network_delivery_observed: true
runtime_materialization_observed: false
receiver_receipt_observed: false
tvc_receipt_observed: false
authority_effect: NONE_OBSERVATION_ONLY
```

The original write-once local outbox entry is not rewritten to manufacture downstream state.

## Offline continuity

The service-worker shell caches both `hil-intr-sync.js` and the fail-closed target projection. Offline mode therefore preserves the local outbox and target state. Synchronization attempts only while `navigator.onLine` is true.

## Validation boundary

Required before merge:

```text
node --check stegos-node/stegos-node.js
node --check stegos-node/hil-intr-sync.js
python scripts/check_stegos_node_projection.py
python scripts/check_hil_intr_node_sync.py
python -m unittest -v tests.test_hil_intr_node_sync
StegOS Node Public Observation source validation: PASS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: PASS
```

No source/CI result is live network-delivery evidence. `network_delivery_observed` remains false until a real registered Node receives an authentic bound ingress receipt from an observed sovereign runtime locator.
