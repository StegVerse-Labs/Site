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

Canonical route binding:

`data/mir-roundtrip-egress-sv002-route-binding.v1.json`

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

The current Goal/COSV is enforced by the request and worker directly. The targeted bridge is therefore not blocked on a separately refreshed aggregate COSV index before this invocation; the canonical vector shard/index fragment remain provenance and the runtime manifest itself carries COSV `50000000100000`.

This package creates no second runtime, transport plane, scheduler, dispatcher, credential path, resident-receiver prerequisite, user-device requirement, or remote-device requirement.

## Evidence boundary

Fresh evidence is required for the current Goal/COSV binding, MIR destination-profile binding, current final StegVerse-side egress, authentic Interlock/InTr egress, MIR MIRROR far-side transition, destination evidence, and Master Records reconstruction of the current final exit transition.

A successful worker receipt may promote one-way MIR MIRROR transport only at explicit provenance `MIR_MIRROR_BUILD_TEST_COUNTERPART_RUNTIME`; it must not be relabeled as authentic external MIR endpoint execution.

Only after one-way duplication is observed may the retained exact return packet proceed through the already-existing governed return-admission path. Full round-trip completion still requires the actual return admission/exit receipt, durable return recording, and final allowed transport-exit transition.

## Current observation

The execution source, standing request, WorkerCoordinator/process adapter bindings, and existing-cadence consumer wiring are materialized in canonical source. No canonical `receipts/mir-roundtrip-egress-authenticity/current.latest.json` was present at the latest reconciliation, so current MIR-specific one-way/full-roundtrip runtime completion remains unclaimed pending the authority-owned resident receipt. No manual user/device step is required.
