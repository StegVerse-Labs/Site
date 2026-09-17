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

The generic mechanics are not re-proved as a prerequisite for the MIR invocation. Historical identifiers prove the prior lane and grant no present authority.

## Current resident execution package

The existing sovereign WorkerCoordinator/runtime path now has an explicit current MIR execution package in `StegVerse-Labs/.github`:

- `control/task-vectors/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
- `control/task-vector-index.d/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
- `control/worker-registry.d/mir-roundtrip-egress-authenticity-001.json`
- `control/process-worker-adapters.d/mir-roundtrip-egress-authenticity-001.json`
- `control/resident-execution-request.d/mir-roundtrip-egress-authenticity-001.json`
- `workers/mir_roundtrip_egress_authenticity_worker.py`

The worker accepts only a fresh WorkerCoordinator claim/fence, binds the current Goal/COSV and `destination_profile=MIR`, validates the current retained registered Node receipt, then calls the already-existing StegOS `run_mir_profile_transition` through `SovereignLocalEventRuntimeAdapter`. It retains the exact MIR MIRROR return bytes and uses the existing Master Records reusable-task lifecycle worker for destination-owned ingest and exact-byte reconstruction.

This package creates no second runtime, transport plane, scheduler, dispatcher, credential path, resident-receiver prerequisite, user-device requirement, or remote-device requirement.

## Evidence boundary

Fresh evidence is required for the current Goal/COSV binding, MIR destination-profile binding, current final StegVerse-side egress, authentic Interlock/InTr egress, MIR MIRROR far-side transition, destination evidence, and Master Records reconstruction of the current final exit transition.

A successful worker receipt may promote one-way MIR MIRROR transport only at explicit provenance `MIR_MIRROR_BUILD_TEST_COUNTERPART_RUNTIME`; it must not be relabeled as authentic external MIR endpoint execution.

Only after one-way duplication is observed may the retained exact return packet proceed through the already-existing governed return-admission path. Full round-trip completion still requires the actual return admission/exit receipt, durable return recording, and final allowed transport-exit transition.

## Current observation

The standing resident execution request is materialized in canonical source. No canonical `receipts/mir-roundtrip-egress-authenticity/current.latest.json` was present when this README was reconciled, so current MIR-specific runtime execution and one-way/full-roundtrip completion remain unclaimed pending the authority-owned resident receipt.
