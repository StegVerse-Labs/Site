# ERL Same-Device Site Projection Mirror Handoff

Goal Task ID: `SS-ERL-ACTIVE-RESEARCH-INTR-RUNTIME-BINDING-001`
Component: Site projection of merged `SS-ERL-SAME-DEVICE-PORTABLE-EXECUTION-001`
COSV ID: `40000100100000`
Repository: `StegVerse-Labs/Site`
Branch: `erl-same-device-site-projection-001`
Status: `SOURCE_PROJECTION_ACTIVE`

## Purpose

Project the already-merged StegOS ERL same-device portable execution profile onto Site's existing current-iPhone browser/service-worker execution surface without creating a second route, listener, scheduler, device prerequisite, storage plane, or authority layer.

## Reused canonical surfaces

- existing `/stegos-bootstrap/resident-task` dispatcher from `service-worker-v13-runtime.js`;
- existing Site generated InTr artifact `assets/generated/site-browser-intr-connectors.js`;
- existing portable WorkerCoordinator implementation and `hil-portable-state-bridge.js` state store;
- canonical DEVICE_KV portable checkout package `stegos-bootstrap/workercoordinator-portable-device-kv.json`;
- established DEVICE_KV IndexedDB store `stegverse-device-local-intr-v1 / kv_files`;
- TV/TVC remains credential authority;
- GitHub and Heartbeat retain no runtime authority.

## Execution order

```text
existing /stegos-bootstrap/resident-task
 -> ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1 profile
 -> deterministic ERL binding
 -> InTr hop 1 EXTERNAL_SYSTEM -> STEGOS_ECOSYSTEM
 -> InTr hop 2 STEGOS_ECOSYSTEM -> DEVICE_SYSTEM
 -> canonical DEVICE_KV WorkerCoordinator checkout/fence
 -> exact-byte DEVICE_KV write-once staging + exact readback
 -> InTr hop 3 DEVICE_SYSTEM -> KV
 -> local evidence journal entry
```

The provider proof remains reference-only and is not replayed. Master Records custody/reconstruction remains explicitly unobserved until an authentic runtime chain is produced and submitted through the existing custody interface.

## Invariants

- no remote device enumeration, wait, or presence gate;
- no second user-operated device;
- no new fetch listener or public route;
- no Task Registry runtime gate;
- no caller-supplied WorkerCoordinator claim or fencing token;
- no provider re-execution;
- no synthetic runtime-evidence claim from source or CI;
- task-journal persistence is evidence-only; payload persistence remains DEVICE_KV `kv_files`.

## Validation boundary

Source merge and CI can prove only that the projection is present and preserves the declared contracts. They cannot prove that the current iPhone executed the three transitions, mutated DEVICE_KV, produced exact readback, or completed Master Records custody/reconstruction.

## Remaining work after source projection

1. invoke the existing `/stegos-bootstrap/resident-task` ERL profile from the current iPhone execution surface;
2. retain the authentic three-hop receipt chain and terminal exact-byte KV readback evidence;
3. submit that authentic evidence to the already-merged Master Records Universal InTr custody interface;
4. require reconstruction confirmation before reconciling the parent Goal.

Manual Work: None.
