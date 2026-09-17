# StegVerse-002 Experiment Rerun — Site Mirror Handoff

Status: ACTIVE
Updated: 2026-09-17
Repository: StegVerse-Labs/Site
Goal Task ID: `STEGVERSE-002-EXPERIMENT-RERUN-001`
COSV: `50000000107000`
Canonical handoff: `StegVerse-002/.github:docs/SELF_CHARACTERIZATION_EXECUTION_SURFACE_MIRROR_HANDOFF.md`
Tracking issue: `StegVerse-Labs/.github#2070`

## Scope

This Site lane repairs only the first unretained invocation seam for the original frozen v0.3 StegVerse-002 self-characterization rerun.

It reuses the existing registered StegVerseNode, root Universal InTr service worker, write-once Node outbox, and same-device EVENT_EPHEMERAL invocation mechanics. It must not create another runtime, listener, scheduler, host, Healer dependency, credential path, authority path, corpus prerequisite, second request, or second user-operated device.

## Exact invocation

```text
goal_task_id = STEGVERSE-002-EXPERIMENT-RERUN-001
cosv_task_vector = 50000000107000
invocation_request_nonce = STEGVERSE-002-EXPERIMENT-RERUN-001-REQUEST-001
requested_invocation_count = 1
second_request_allowed = false
operation = REQUEST_SELF_CHARACTERIZATION
destination = stegos ecosystem / stegverse-002.self-characterization
execution_owner = StegVerse-002/.github
frozen_condition_version = v0.3
```

The SDK payload must match the canonical `StegVerse-org/StegVerse-SDK:stegverse/external_interlock_bootstrap.py` first self-characterization request, with `authority_ref` bound to the current registered Node's Interlock identity. The request/manifest hashes are recomputed from canonical bytes on-device and bound into the invocation object.

## Evidence boundary

Source implementation or tests do not satisfy runtime predicates. Authentic evidence begins only when the current device's existing root InTr worker receives the exact write-once Node trigger and emits its admission receipt.

Before authentic invocation:
- `REQUEST_BOUND`: not observed
- `STEGVERSE_NODE_BOUND_TO_INVOCATION`: not observed
- `INTERLOCK_BOUND_TO_NODE_AND_MANIFEST`: not observed
- `INTR_MATERIALIZATION_ADMITTED`: not observed
- every downstream runtime/principal/Master Records/origin-return predicate: not observed

The launcher retains the exact returned admission receipt locally for later reconciliation. It does not fabricate WorkerCoordinator claim/fence, principal execution, governed egress, Master Records custody/reconstruction, or origin-return evidence.

## Downstream gate

Do not attempt downstream execution until authentic `REQUEST_BOUND` / Node / Interlock / InTr admission evidence has been observed and correlated to this exact nonce. After that gate, continue only through the canonical organization-owned v0.3 principal and Master Records path.

## Manual work

None while source repair is in progress.
