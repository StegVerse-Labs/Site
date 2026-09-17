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

The generic mechanics are not re-proved as a prerequisite for the MIR invocation. Historical route evidence grants no current authority; the current event still requires the current WorkerCoordinator claim/fence and current Interlock/InTr state transitions.

## Current execution package

The existing process adapter now invokes `StegVerse-Labs/.github/workers/mir_roundtrip_transition_probe_worker.py`. That wrapper directly calls the existing `mir_roundtrip_egress_authenticity_worker.py`; it does not create a second runtime, scheduler, dispatcher, transport, credential path, or device requirement.

The MIR `EVENT_EPHEMERAL` runtime remains transition-materialized. It does not need to be standing idle. The wrapper starts its observations before runtime materialization and emits a Master Records confirmation after every observed event/lease/transport transition.

The live diagnostic is retained at:

`receipts/mir-roundtrip-egress-authenticity/live-transition-diagnostic.latest.json`

and individual packets under:

`receipts/mir-roundtrip-egress-authenticity/live-transition-confirmations/`

The sequence includes WorkerCoordinator claim/fence binding, MIR ingress intent binding, Node proof verification, lease REQUESTED/ADMITTED/PROVISIONING, compute provisioning, EVENT_EPHEMERAL materialization, runtime identity verification, Interlock/InTr ingress, RTC 007/008/009, return queueing, evidence retention/export, release/closure, and exact governed-return packet retention.

Every observed packet is byte-exact ingested/reconstructed through the existing Master Records worker. The diagnostic retains `first_non_return_transition_id`. Master Records remains evidence custody/reconstruction only and cannot create or authorize a missing transition.

## Current diagnostic boundary

Canonical source is now instrumented from the current WorkerCoordinator invocation onward, but no authentic current `live-transition-diagnostic.latest.json` has yet been retained. No current MIR runtime completion is claimed.

The current exact boundary is:

`CURRENT_AUTHENTIC_WORKERCOORDINATOR_EVENT_INVOCATION_NOT_YET_OBSERVED`.

This is not an idle-runtime requirement. It means the current standing MIR event has not yet produced probe #1 on the newly instrumented existing path. Once it does, the ordered probe stream will identify the last successful transition and the first Master Records confirmation-return failure, if any.

## Evidence boundary

Fresh evidence remains required for the current Goal/COSV binding, MIR destination-profile binding, final StegVerse-side egress, authentic Interlock/InTr transport, MIR MIRROR far-side transition, destination evidence, Master Records confirmation/reconstruction, and governed return.

A successful worker receipt may promote one-way MIR MIRROR transport only at provenance `MIR_MIRROR_BUILD_TEST_COUNTERPART_RUNTIME`; it must not be relabeled as authentic external MIR endpoint execution. Full round-trip completion remains separate and requires governed return admission, durable recording, and the final allowed transport-exit transition.
