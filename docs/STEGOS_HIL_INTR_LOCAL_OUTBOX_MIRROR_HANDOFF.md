# StegOS HIL Universal InTr Local Outbox Mirror Handoff

Updated: 2026-08-29

```text
goal_id: SITE-HIL-INTR-STEGOS-NODE-OUTBOX-617
issue: StegVerse-Labs/Site#617
repository: StegVerse-Labs/Site
branch: feat/hil-intr-stegos-node-outbox-20260829
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
credential_authority: TV/TVC
github_runtime_authority: NONE
authority_effect: NONE_LOCAL_CONTINUITY_ONLY
```

## Purpose

Bridge the participant browser HIL staging store into the already-registered StegOS Node local continuity boundary without representing that local import as network delivery.

Canonical source chain:

```text
Site #608
  HIL browser stages exact PDF + provenance + Universal InTr intent + materialization request
StegOS #91
  defines stegverse.universal-intr-materialization-request/v1
.github #410
  sovereign runtime consumes HIL materialization requests once they reach runtime/intr-materialization
Site #617
  imports pending staged request into registered StegOS Node local outbox only
```

## Non-claims

```text
network_delivery_observed=false
runtime_materialization_observed=false
receiver_receipt_observed=false
TVC_receipt_observed=false
execution_authority=NONE
request_grants_execution_authority=false
claim_or_fence_minted=false
Last StegOS Network Sync is not advanced by local import
```

Actual StegOS Node -> sovereign runtime synchronization remains a separate next gate.

## Implemented source

```text
stegos-node/stegos-node.js
  DB_VERSION = 2
  object store = intr_outbox
  HIL source DB = stegverse-hil-v3 / response_files
  participant state source = localStorage stegverse.hil.submissions.v1
  importer = importPendingHilIntrToNodeOutbox()
  reconciler = reconcilePendingHilIntrOutbox()

stegos-node/index.html
  HIL InTr Local Outbox status
  distinct from Last StegOS Network Sync

stegos-node/service-worker.js
  cache = stegos-node-shell-v5-hil-intr-local-outbox

scripts/check_stegos_node_projection.py
tests/test_stegos_node_projection.py
.github/workflows/stegos-node-public-observation.yml
```

Admission is restricted to participant records whose current materialization state is exactly `QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION`. A staged object that was already satisfied by a direct receiver receipt is not imported merely because its bytes remain in IndexedDB.

The Node independently reconstructs and verifies:

```text
exact response PDF SHA-256
provenance response SHA-256
provenance canonical SHA-256
HIL payload binding SHA-256
Universal InTr intent SHA-256
materialization request SHA-256
deterministic materialization ID
exact payload_ref = indexeddb://stegverse-hil-v3/response_files/response:<operation_id>
destination = STEGOS_ECOSYSTEM / HIL:Ingress
downstream owner = StegVerse-Labs/.github#246
```

The Node must already have canonical Receipt #1. Outbox identity is the materialization ID. An identical retry is idempotent; a different entry under the same materialization ID fails closed as `StegOS InTr outbox write-once collision`.

## Remaining boundary

```text
browser HIL staging -> registered StegOS Node local outbox: IMPLEMENTED_ON_BRANCH
node local outbox -> sovereign runtime intr-materialization/: NOT IMPLEMENTED / NOT OBSERVED
sovereign HIL materialization consumption: NOT OBSERVED
receiver receipt: NOT OBSERVED
HIL custody receipt: NOT OBSERVED
TVC receipt: NOT OBSERVED
```

`Last StegOS Network Sync` is deliberately not updated by local import. A future actual outbound sync lane must earn that state with transport evidence.
