# ERL Authentic InTr Execution Invoker Mirror Handoff

Goal Task ID: `SS-ERL-AUTHENTIC-INTR-EXECUTION-EVIDENCE-002`
Parent Goal Task ID: `SS-ERL-ACTIVE-RESEARCH-INTR-RUNTIME-BINDING-001`
COSV ID: `40000100100000`
Repository: `StegVerse-Labs/Site`
Branch: `erl-authentic-intr-execution-invoker-002`
Status: `SOURCE_BINDING_ACTIVE`

## Purpose

Expose the already-merged ERL same-device execution profile through a browser-local machine-owned invocation carrier on the existing StegOS service-worker surface. This does not add a runtime route, listener, scheduler, device gate, credential path, WorkerCoordinator, KV implementation, or authority plane.

## Canonical runtime path

```text
current StegOS HTTPS page materialization
-> existing service-worker registration/ready state
-> existing POST /stegos-bootstrap/resident-task
-> ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1
-> hop 1 EXTERNAL_SYSTEM -> STEGOS_ECOSYSTEM
-> hop 2 STEGOS_ECOSYSTEM -> DEVICE_SYSTEM
-> existing DEVICE_KV WorkerCoordinator checkout/fence
-> exact-byte DEVICE_KV write/readback
-> hop 3 DEVICE_SYSTEM -> KV
-> retained local ERL execution evidence
```

The browser carrier sends no device id, node id, execution-surface identity, claim id, or fencing token. WorkerCoordinator claim/fence remains owned by the existing terminal DEVICE_KV path.

## Interaction-queue boundary

`control/current-user-ios-interaction-queue.json` explicitly states that machine-owned resident/service-worker/entity transitions are outside the human-device instruction queue and remain governed by their own contemporaneous Interlock/InTr governance. The ERL invocation carrier is therefore not a new human-authority mutation control and MUST NOT depend on the queue changing from `HOLD_UI_ORCHESTRATION_CONFLICT`.

## Retry boundary

Before submitting, the carrier reads the existing local StegOS evidence bundle. If a retained `stegverse.erl.same-device-portable-execution-receipt/v1` for this Goal/COSV already exists in terminal state, it returns that retained evidence and does not resubmit. Blind consequence retry remains prohibited.

## Provider boundary

The existing provider proof is reference-only and MUST NOT be replayed:

- source: `ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET`
- provider file: `google-drive:file:1KKBS1drUFVh-czLpmg5koRgDs4YMf-gG`
- size: `1015`
- SHA-256: `94470c58db24e544c3edfcd390cca395375a348879ec3c53451ba517ff917763`

## Completion boundary

Source merge only makes authentic execution reachable. It does not prove that the current iPhone activated the updated service worker, submitted the ERL envelope, traversed any InTr hop, mutated/read back DEVICE_KV, or entered Master Records custody.

The source component is complete only after exact-head Site validation and merge. The successor Goal remains ACTIVE until authentic local execution evidence plus Master Records custody/reconstruction are observed.

Manual Work: None for source implementation. Authentic current-iPhone execution still requires the current browser surface to materialize the merged runner; navigation/materialization is not treated as transition authority.
