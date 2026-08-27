# Site StegOS KnowledgeVault Admitted InTr Browser Apply Mirror Handoff

> STATUS RECONCILIATION: the pre-merge completion block in this file is superseded by `docs/STEGOS_KV_INTR_BROWSER_APPLY_RECONCILIATION_MIRROR_HANDOFF.md` at commit 36928b2e0d80d54221a78415c252a1a7b9202871. PR #551 is MERGED/VALIDATED; direct deployed marker observation and live InTr delivery remain unobserved.

Updated: 2026-08-27

```text
repository: StegVerse-Labs/Site
issue: #549
branch: feat/stegos-kv-intr-browser-apply-549
claim: SITE-STEGOS-KV-INTR-BROWSER-APPLY-549-20260827
state: IMPLEMENTED_ON_BRANCH_CI_PENDING
source_authority: StegVerse-Labs/StegOS
source_delivery_admission: issue #80 / PR #81 / fe13ba4fd8fa6db75b4b9abca6fab9b11ca3cacb
source_admitted_device_apply: issue #82 / PR #83 / e8601cb90c9ebdf7928ccd78cf8d5e5c41c8ca02
source_reconciliation: ba16ecf5da0a2aa89c94046f98d5cfb61f5b7b7b
credential_authority: TV/TVC
authority_effect: NONE
activation_effect: false
live_intr_delivery_observed: false
```

## Goal

Project the merged StegOS admitted readiness-delivery semantics into the existing public `/stegos-node/` browser runtime.

The existing local-only API:

`applyKvReadinessUpdate(envelope, priorSnapshot, successorSnapshot)`

must remain transport-unbound and non-authorizing.

A separate admitted-delivery API may advance the browser-local readiness head only after validating the exact canonical InTr KV->DEVICE receipt and exact StegOS delivery-admission bindings.

## Required admitted input

```text
stegos.kv_readiness_intr_delivery_admission.v1
stegos.kv_readiness_update_envelope.v1
exact prior KV readiness snapshot
exact successor KV readiness snapshot
stegverse.intr.hop_receipt/v1
exact expected device boundary identity
current IndexedDB KV readiness head
```

## Canonical InTr boundary

```text
direction=FORWARD
hop_index=1
from_role=KV
to_role=DEVICE
boundary_verification=VERIFIED
transition_state=RECEIVED
payload_hash=SHA-256(canonical complete readiness envelope)
secret_plaintext_present=false
authority_transfer=false
receipt_hash valid
```

The browser must reject missing/extra canonical receipt fields and malformed digest fields.

## Browser composition semantics

The admitted browser apply path must:

1. validate current browser readiness state;
2. validate the transport-neutral readiness envelope;
3. validate prior/successor readiness snapshots;
4. validate the canonical KV->DEVICE InTr receipt;
5. validate and reconstruct the exact delivery admission;
6. require admission prior snapshot == current browser readiness head;
7. call the existing local-only `applyKvReadinessUpdate`;
8. bind the resulting browser state to the admitted envelope/prior/successor;
9. return a separate deterministic composition receipt.

Transport truth must not be written into the browser readiness state object.

Expected separation:

```text
outer admitted-apply receipt:
  transport_delivery_performed=true
  interlock_delivery_admission_observed=true
  local_state_refresh_performed=true

nested browser readiness state:
  transport_delivery_performed=false
  interlock_delivery_admission_observed=false
  local_state_refresh_performed=true
```

Both remain:

```text
kv_mutation_performed=false
activation_performed=false
provider_operation_authorized=false
execution_authority=NONE
authority_effect=NONE
```

## Existing surfaces that must remain unchanged

- Register Device / Receipt #1;
- Register & Export Evidence;
- physical evidence export;
- offline reload proof;
- Personal KV sync;
- StegOS Network sync;
- Device History;
- capability shell rendering;
- local-only readiness update API.

No activation control is added.

## Collision boundary

This lane owns only:

- `stegos-node/stegos-node.js`;
- `stegos-node/service-worker.js`;
- `scripts/check_stegos_node_projection.py`;
- `tests/test_stegos_node_projection.py`;
- this handoff;
- the #549 claim fragment.

Released #534/#542 lanes are incidental dependencies only.

## Non-claims

Source, CI, deployment, or public source-marker observation cannot establish a real InTr event.

```text
live KV->DEVICE InTr receipt: NOT OBSERVED
live admitted readiness delivery: NOT OBSERVED
production Interlock activation: NOT CLAIMED
module/service activation: NOT CLAIMED
provider operation: NOT AUTHORIZED
execution authority: NONE
authority_effect: NONE
```

## Completion gates

```text
pre-work claim: COMPLETE
handoff: COMPLETE
browser admitted-delivery API: IMPLEMENTED_ON_BRANCH
canonical receipt validation: IMPLEMENTED_ON_BRANCH
delivery admission validation: IMPLEMENTED_ON_BRANCH
browser composition receipt: IMPLEMENTED_ON_BRANCH
tests/validator: IMPLEMENTED_ON_BRANCH
service-worker cache migration: IMPLEMENTED_ON_BRANCH
Site orchestration/heartbeat: PENDING
merge: PENDING
direct public source-marker observation: PENDING
live InTr delivery: NOT OBSERVED / SEPARATE
runtime activation: NOT CLAIMED
```


## Implemented browser source

```text
local-only API preserved:
  applyKvReadinessUpdate(...)

new admitted-delivery API:
  validateKvReadinessIntrReceipt(...)
  validateKvReadinessIntrDeliveryAdmission(...)
  applyAdmittedKvReadinessDelivery(...)
```

The new path enforces the exact canonical InTr receipt field set and the exact StegOS #80 delivery-admission field set before local application.

The resulting Site composition receipt is:

`stegos.site.kv_readiness_admitted_device_apply.v1`

Its digest binds the complete updated browser readiness state. The nested state remains transport-neutral.

Service-worker cache version:

`stegos-node-shell-v4-kv-intr-admitted-apply`

Observer markers:

```text
STEGOS_NODE_KV_INTR_BROWSER_APPLY_SOURCE_PASS
STEGOS_NODE_KV_INTR_BROWSER_APPLY_PUBLIC_OBSERVATION_PASS
```

These markers prove source/deployment presence only. They do not prove a real InTr delivery.
