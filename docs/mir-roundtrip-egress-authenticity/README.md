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

The existing sovereign WorkerCoordinator/runtime path has an explicit current MIR execution package in `StegVerse-Labs/.github`, including the current task vector/index, worker/process-adapter registration, resident request, `workers/mir_roundtrip_egress_authenticity_worker.py`, and `scripts/consume_mir_roundtrip_egress_authenticity_request.py`.

The standing request is wired into the already-existing `canonical_work_coordination` resident cadence. No second dispatcher, scheduler, WorkerCoordinator, runtime plane, credential path, or device prerequisite is created.

The `EVENT_EPHEMERAL` MIR runtime is transition-materialized, not a pre-existing idle runtime surface. The current unresolved runtime boundary is therefore the first authentic MIR event ingress / Interlock-InTr state transition, not remote-runtime reachability.

## Master Records confirmation packets

`StegVerse-Labs/.github/workers/reusable_task_master_records_roundtrip.py` now detects MIR one-way evidence and fans the observed route into separate confirmation packets. Each packet is individually ingested by Master Records and reconstructed byte-for-byte before the aggregate one-way evidence can be accepted.

The confirmation sequence is:

```text
01 CURRENT_GOAL_COSV_BOUND
02 CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED
03 RTC-STEGVERSE-EGRESS-007
04 RTC-INTERLOCK-INTR-TRANSPORT-008
05 RTC-FARSIDE-FINAL-009
06 MIR_DESTINATION_EVIDENCE_RETAINED
07 EXACT_GOVERNED_RETURN_PACKET_RETAINED
```

Packets are retained under the current one-way evidence directory in `transition-confirmations/`. Every packet has `authority_effect=NONE_CONFIRMATION_EVIDENCE_ONLY`; Master Records remains custody/reconstruction authority only and cannot create a transition that was not observed.

The diagnostic continues across the whole observed sequence and returns `first_non_return_transition_id` for the earliest transition whose confirmation does not come back from Master Records. If a transition itself was not observed, its packet is classified `TRANSITION_NOT_OBSERVED` and is not fabricated or sent as successful evidence.

The aggregate one-way Master Records return is accepted only after every observed transition confirmation returns successfully. Unit coverage is in `StegVerse-Labs/.github/tests/test_mir_transition_master_records_confirmation.py`.

## Current diagnostic boundary

No authentic current MIR event-ingress / Interlock-InTr state-transition receipt is presently retained in canonical evidence. Therefore the current known break remains **before the first authentic transport-state confirmation can be produced**:

`AUTHENTIC_MIR_EVENT_INGRESS_OR_STATE_TRANSITION_RECEIPT_NOT_OBSERVED`.

This is distinct from a Master Records return-path failure. Once the current event reaches Interlock/InTr and emits transition evidence, the new per-transition packets will identify the exact first Master Records non-return, if any.

## Evidence boundary

Fresh evidence remains required for the current Goal/COSV binding, MIR destination-profile binding, final StegVerse-side egress, authentic Interlock/InTr transport, MIR MIRROR far-side transition, destination evidence, Master Records confirmation/reconstruction, and governed return.

A successful worker receipt may promote one-way MIR MIRROR transport only at provenance `MIR_MIRROR_BUILD_TEST_COUNTERPART_RUNTIME`; it must not be relabeled as authentic external MIR endpoint execution. Full round-trip completion remains separate and requires governed return admission, durable recording, and the final allowed transport-exit transition.
