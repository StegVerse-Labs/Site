# StegOS HIL Universal InTr Node Sync Mirror Handoff

Updated: 2026-08-29
Repository: `StegVerse-Labs/Site`
Issue: #632 CLOSED_SOURCE_COMPLETE
PR: #633
Merge: `83ee586b4100854a10974484c7480afeffeaa9da`
Upstream ingress owner: `StegVerse-Labs/.github#421` CLOSED_SOURCE_COMPLETE
Upstream ingress merge: `e2bb317438e0afb8bab5b782af619458250c39ef`
Parent HIL activation owner: `StegVerse-Labs/.github#246`

```text
goal_id: SITE-HIL-INTR-NODE-SYNC-632
state: COMPLETE_VALIDATED_MERGED_SOURCE
credential_authority: TV/TVC
github_token_runtime_authority: NONE
authority_effect: NONE_TRANSPORT_TRIGGER_ONLY
network_delivery_observed: false
runtime_materialization_observed: false
receiver_receipt_observed: false
final_validated_head: 6e28f8e09619953e0996aa689b6790ed51a94be4
stegos_node_validation_run: 33274197031 SUCCESS
site_bootstrap_validation_run: 33274197034 SUCCESS
ecosystem_heartbeat_validation_run: 33274197043 SUCCESS
site_handoff_orchestrator_run: 33274197057 SUCCESS
```

## Purpose

Close the source seam from the already-registered browser StegOS Node HIL local outbox to the sovereign HIL materialization ingress without turning the browser into TVC route/EGRESS authority.

The HIL Universal InTr materialization request is an event trigger only. It asks the existing sovereign HIL execution owner to materialize event-ephemerally. It does **not** carry the staged response PDF or provenance bytes and it does not grant WorkerCoordinator execution authority.

Canonical merged source path:

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

`stegos-node/hil-intr-sync-target.json` remains:

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

The browser does not attempt transport while this state is unresolved. Promotion to `CONFORMING_SOVEREIGN_INTR_INGRESS` requires independently observed sovereign runtime evidence and an exact credentialless HTTPS `/intr/materialization` locator. Source/CI cannot mint that state.

## Browser synchronization contract

Before POST, `hil-intr-sync.js` revalidates the entire local outbox entry and recomputes `outbox_entry_hash`. It emits only a `stegos.node_intr_materialization_trigger.v1` direct-Node trigger. There is no `Authorization` header, no `X-StegVerse-Authorization-Id`, and fetch uses `credentials: omit`.

HTTP success alone is insufficient. The browser validates the returned `stegverse.hil-intr-materialization-ingress/v1` receipt against the exact materialization id, request hash, transport-intent hash, payload hash, Node id, Interlock id, outbox-entry hash, trigger body SHA-256, and non-authorizing invariants.

Only then may it persist a separate `stegos.node_intr_delivery_receipt.v1` and advance the Node's `last_stegos_network_sync` observation. That observation still records runtime materialization, receiver receipt, and TVC receipt as false until separately observed.

## Offline continuity

The service-worker shell caches both `hil-intr-sync.js` and the fail-closed target projection. Offline mode therefore preserves the local outbox and target state. Synchronization attempts only while online. The v5 local-outbox cache identifier is retained only as a predecessor-lineage marker while the active cache is `stegos-node-shell-v6-hil-intr-node-sync`.

## Runtime completion boundary

Source implementation, exact-head CI, merge, issue closure, and claim release do not satisfy runtime delivery. The next legitimate transition is:

```text
authentic sovereign ingress runtime observed
-> exact HTTPS /intr/materialization locator projected
-> registered Node sends exact trigger
-> authentic INGRESS_ADMITTED receipt validated
-> Node network-delivery observation advances
-> existing deployment-local materialization consumer executes
-> WorkerCoordinator allocates independent HIL claim/fresh fence
-> HIL receiver readiness evidence
```

Current repository evidence still contains no authentic ingress or resident-consumption receipt, so all runtime observation flags remain false.
