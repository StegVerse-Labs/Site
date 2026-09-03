# StegOS HIL Universal InTr Node Sync Mirror Handoff

Updated: 2026-08-29
Repository: `StegVerse-Labs/Site`
Issue: #632
PR: #633
Upstream ingress owner: `StegVerse-Labs/.github#421`
Parent HIL activation owner: `StegVerse-Labs/.github#246`

```text
goal_id: SITE-HIL-INTR-NODE-SYNC-632
state: IMPLEMENTED_VALIDATED_MERGE_PENDING
credential_authority: TV/TVC
github_token_runtime_authority: NONE
authority_effect: NONE_TRANSPORT_TRIGGER_ONLY
network_delivery_observed: false
runtime_materialization_observed: false
receiver_receipt_observed: false
stegos_node_validation_run: 33274147339 SUCCESS
site_bootstrap_validation_run: 33274147345 SUCCESS
ecosystem_heartbeat_validation_run: 33274147341 SUCCESS
site_handoff_orchestrator_run: 33274147343 SUCCESS
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

The service-worker shell caches both `hil-intr-sync.js` and the fail-closed target projection. Offline mode therefore preserves the local outbox and target state. Synchronization attempts only while `navigator.onLine` is true. The v5 local-outbox cache identifier is retained only as a predecessor-lineage marker while the active cache is `stegos-node-shell-v6-hil-intr-node-sync`.

## Exact-head validation

Source head `eb714d5a4ee9a8e00992375f4c230d9f76b48dad` passed:

```text
StegOS Node Public Observation                         33274147339 SUCCESS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority 33274147345 SUCCESS
Ecosystem Heartbeat Orchestration                      33274147341 SUCCESS
Site Handoff Orchestrator                              33274147343 SUCCESS
```

The reconciliation commit itself must pass the same applicable exact-head gates before merge. No source/CI result is live network-delivery evidence. `network_delivery_observed` remains false until a real registered Node receives an authentic bound ingress receipt from an observed sovereign runtime locator.


## Claim terminalization reconciliation — 2026-09-02

The source implementation already merged through PR #633 as `83ee586b4100854a10974484c7480afeffeaa9da`. The stale active claim has now been terminalized to `RELEASED` on current `main`.

Validation evidence from the merged implementation head:

- Site Handoff Orchestrator `33274280891` — SUCCESS
- StegOS Node Public Observation `33274197031` — SUCCESS
- Ecosystem Heartbeat Orchestration `33274197043` — SUCCESS
- Site Bootstrap Validate `33274197034` — SUCCESS

This terminalization does not claim live Node->ingress delivery. It only closes the source-implementation ownership lane. Runtime delivery remains governed by the released HIL target projector and an authentic conforming ingress target, with no second user-operated device requirement.


## Same-device successor integration — 2026-09-02

The released Node-sync contract now has a canonical same-device successor: Site PR #941 / `20b7603be8e88dd714fa4cef3337552704f9e4e8`.

The HIL sync client no longer treats the static target projection as the only available ingress path. It first registers/refreshes the root `/intr-service-worker.js`, reads `/intr/profile`, and accepts the current registered iPhone only when that profile explicitly advertises `HIL:Ingress`.

The static `stegos-node/hil-intr-sync-target.json` remains fail-closed and is now the fallback for a genuinely external sovereign ingress.

Same-device admission is local InTr evidence, not network sync:

```text
local_ingress_observed=true
network_delivery_observed=false
runtime_materialization_observed=false
receiver_receipt_observed=false
tvc_receipt_observed=false
```

No second user-operated device is required.
