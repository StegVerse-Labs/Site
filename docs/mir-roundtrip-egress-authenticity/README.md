# MIR Round-Trip Egress Authenticity

Canonical Goal Task: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Canonical handoff: `docs/MIR_ROUNDTRIP_EGRESS_AUTHENTICITY_MIRROR_HANDOFF.md`
COSV: `50000000100000`

## Execution order

This task reuses the historically successful StegVerse-002 execution mechanics first, then applies only the current MIR-specific invocation and evidence requirements.

```text
registered StegVerse Node
-> Interlock
-> InTr materialization
-> bounded invocation lease
-> EVENT_EPHEMERAL runtime
-> execution-time runtime identity
-> authority-owned continuation
-> independent Master Records reconstruction
```

Canonical route binding: `data/mir-roundtrip-egress-sv002-route-binding.v1.json`.

The generic mechanics are not re-proved as a prerequisite for the MIR invocation. The frozen successful route artifact is evidence of the prior lane and grants no present authority; the current event still requires a fresh WorkerCoordinator claim/fence and current Interlock/InTr receipts.

## Current resident execution package

The existing sovereign WorkerCoordinator/runtime path has an explicit current MIR execution package in `StegVerse-Labs/.github`:

- `control/task-vectors/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
- `control/task-vector-index.d/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
- `control/worker-registry.d/mir-roundtrip-egress-authenticity-001.json`
- `control/process-worker-adapters.d/mir-roundtrip-egress-authenticity-001.json`
- `control/resident-execution-request.d/mir-roundtrip-egress-authenticity-001.json`
- `workers/mir_roundtrip_egress_authenticity_worker.py`
- `scripts/consume_mir_roundtrip_egress_authenticity_request.py`

The standing request is wired into the already-existing `canonical_work_coordination` resident cadence. That existing consumer visits the MIR request before its ordinary legacy request set and calls the existing targeted resident bridge; no second dispatcher or scheduler is created.

The worker accepts only a fresh WorkerCoordinator claim/fence, binds the current Goal/COSV and `destination_profile=MIR`, hashes/binds the frozen successful SV002 route without revalidating generic route mechanics, then calls the already-existing StegOS `run_mir_profile_transition` through `SovereignLocalEventRuntimeAdapter`. It retains the exact MIR MIRROR return bytes and uses the existing Master Records reusable-task lifecycle worker for destination-owned ingest and exact-byte reconstruction.

## Autonomous invocation chain

Canonical source now explicitly traces the existing path:

```text
run_heartbeat_runtime.py --continuous
-> repair_resident_worker_presence.ensure_worker_presence
-> run_worker_runtime.py --continuous
-> first task-capable WorkerCoordinator cycle
-> local resident dispatch
-> dispatch_resident_execution_requests.py
-> canonical_work_coordination
-> consume-canonical-work-coordination-bootstrap.py
-> consume_mir_roundtrip_egress_authenticity_request.py
-> refresh_and_execute_resident_task.py
-> existing WorkerCoordinator fresh claim/fence
-> mir_roundtrip_egress_authenticity_worker.py
-> existing StegOS EVENT_EPHEMERAL MIR runtime
-> Master Records reconstruction
```

The earlier self-heal startup-starvation defect has already been repaired: the WorkerCoordinator records its first task-capable cycle before potentially long tick-zero resident maintenance. Therefore no new scheduler/dispatcher/runtime source repair is required for this chain.

Source-trace preflight: `StegVerse-Labs/.github/receipts/preflight/MIR-AUTONOMOUS-INVOCATION-CHAIN-001.json`.

## Current observation

The source chain is validated. Current authentic runtime consumption is not.

No canonical current MIR runtime receipt, MIR request-consumption receipt, or current runtime-presence receipt was observed during the latest reconciliation. The available remote-runtime connector also had no reachable authorized device/surface. That connector result is only reachability evidence and does not prove that no sovereign runtime exists elsewhere.

Passive waiting is not accepted as execution. The unresolved boundary is explicitly `AUTHENTIC_SOVEREIGN_RUNTIME_SURFACE_OR_RUNTIME_RECEIPT_NOT_OBSERVED`.

This package creates no second runtime, transport plane, scheduler, dispatcher, credential path, resident-receiver prerequisite, user-device requirement, or remote-device requirement.

## Evidence boundary

Fresh evidence is required for the current Goal/COSV binding, MIR destination-profile binding, current final StegVerse-side egress, authentic Interlock/InTr egress, MIR MIRROR far-side transition, destination evidence, and Master Records reconstruction of the current final exit transition.

A successful worker receipt may promote one-way MIR MIRROR transport only at explicit provenance `MIR_MIRROR_BUILD_TEST_COUNTERPART_RUNTIME`; it must not be relabeled as authentic external MIR endpoint execution.

Only after one-way duplication is observed may the retained exact return packet proceed through the already-existing governed return-admission path. Full round-trip completion still requires the actual return admission/exit receipt, durable return recording, and final allowed transport-exit transition.
