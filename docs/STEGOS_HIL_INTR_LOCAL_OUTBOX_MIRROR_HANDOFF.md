# StegOS HIL Universal InTr Local Outbox Mirror Handoff

Updated: 2026-08-29

```text
goal_id: SITE-HIL-INTR-STEGOS-NODE-OUTBOX-617
issue: StegVerse-Labs/Site#617
repository: StegVerse-Labs/Site
merge: 8fc92612eb4d6b647d1ba72d5f30e861e9ee41a1
state: COMPLETE_VALIDATED_MERGED
credential_authority: TV/TVC
github_runtime_authority: NONE
authority_effect: NONE_LOCAL_CONTINUITY_ONLY
network_delivery_observed: false
```

## Purpose

Bridge the participant browser HIL staging store into the already-registered StegOS Node local continuity boundary without representing that local import as network delivery.

Canonical source chain:

```text
Site #608
  HIL browser stages exact PDF + provenance + Universal InTr intent + materialization request
StegOS #91
  defines stegverse.universal-intr-materialization-request/v1
.github merged HIL materialization consumer
  sovereign runtime consumes HIL materialization requests once they reach runtime/intr-materialization
Site #617 / merge 8fc92612eb4d6b647d1ba72d5f30e861e9ee41a1
  imports pending staged request into registered StegOS Node local outbox only
Site #632
  successor Node-outbox -> sovereign-ingress synchronization source lane
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

## Merged implementation

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

## Successor synchronization boundary

The old `NOT IMPLEMENTED` synchronization statement is superseded by Site #632 and `.github` #421/#422 source work. The correct lifecycle is now:

```text
browser HIL staging -> registered StegOS Node local outbox: COMPLETE_VALIDATED_MERGED
node local outbox -> direct sovereign materialization-ingress trigger: IMPLEMENTED_ON_SITE_632_BRANCH_VALIDATION_PENDING
far-side direct Node ingress origin: IMPLEMENTED_ON_DOTGITHUB_422_BRANCH_VALIDATION_PENDING
actual network delivery: NOT OBSERVED
sovereign HIL materialization consumption: NOT OBSERVED
receiver receipt: NOT OBSERVED
HIL custody receipt: NOT OBSERVED
TVC receipt: NOT OBSERVED
```

The successor synchronization module may advance `Last StegOS Network Sync` only after validating an authentic bound `INGRESS_ADMITTED` receipt. Local outbox import alone never advances it.
