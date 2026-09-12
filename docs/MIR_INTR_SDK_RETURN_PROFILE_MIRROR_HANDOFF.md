# MIR historical-accounting return -> SDK Universal InTr handoff

Updated: 2026-09-11
Goal Task ID: `MIR-INTR-SDK-RETURN-PROFILE-001`
Parent Goal: `MIR-STEGVERSE-HISTORICAL-ACCOUNTING-RUN-002`
Parent SDK issue: `StegVerse-org/StegVerse-SDK#217`
COSV ID: `50000000100000`
Site issue: `StegVerse-Labs/Site#1266`
Implementation PR: `StegVerse-Labs/Site#1268`
Merge: `a75fc28245b0d8b006159181cd582190b0fa635e`
Status: `SOURCE INTEGRATION MERGED / AUTHENTIC MIR RETURN + RESIDENT RUN-2 EXECUTION PENDING`

## Purpose

Route the authentic MIR historical-accounting response artifact back into the existing SDK evaluation surface without inventing a MIR-specific transport.

Canonical sequence:

```text
StegVerse Run-2 governance execution
-> exact bounded history handoff to MIR
-> MIR performs source-native historical accounting
-> MIR emits source-native accounting artifact
-> MIR-return adapter binds exact artifact to the original test/handoff
-> existing evaluator-read-review Universal InTr profile
-> registered StegOS Node write-once intr_outbox
-> existing /intr/materialization route
-> SDK:EvaluatorReviewIngress
-> SDK performs next evaluation / delta
```

## Merged route

The canonical StegOS connector registry already defines profile `evaluator-read-review`:

```text
operation: READ_REVIEW
source: DEVICE_SYSTEM / Site:EvaluatorReview
destination: STEGOS_ECOSYSTEM / SDK:EvaluatorReviewIngress
payload schema: stegverse.evaluator_review.interlock_request.v1
authority effect: NONE
```

PR #1268 merged the return adapter and extended the existing root `intr-service-worker.js` to advertise and admit `SDK:EvaluatorReviewIngress` using downstream owner `StegVerse-Labs/.github#431`. The implementation reuses the existing root `/intr/profile` + `/intr/materialization` runtime, canonical generated connector, registered Node write-once `intr_outbox`, and existing transport trigger. It does not create another listener or transport.

The evaluator ingress receipt is intentionally admission-only. It reports `runtime_execution_attempted=false`, `consumer_dispatch_attempted=false`, and `sdk_delta_evaluation_observed=false`. Therefore source integration does not claim that SDK evaluation occurred.

## Return binding

Before the MIR response is accepted, the adapter requires:

- Run-2 `test_id`;
- positive integer revision;
- exact original manifested-run SHA-256;
- exact MIR handoff/request identifier in `response_to`;
- expected MIR response class;
- exact returned artifact bytes;
- exact artifact SHA-256 recomputed locally.

The adapter wraps those bindings in the existing evaluator-review request. The source-native artifact is retained byte-for-byte; transport metadata does not reinterpret MIR semantics.

## Exact-head validation before merge

Exact head `b5ade1a1ed71f6a9f853cf8c2ac312c982e18349` passed:

```text
MIR InTr SDK Return Profile #4: PASS
Ecosystem Heartbeat Orchestration #2344: PASS
Site Handoff Orchestrator #3636: PASS
No Required Third-Party Runtime #112: PASS
Validate StegOS Persistent Card UX #235: PASS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority #12227: PASS
```

The persistent-card validation initially exposed a stale exact-profile-list assertion in the existing Master Records checker. The wrapper was remediated to require the existing KV/HIL/Master Records profiles individually while permitting additive canonical profiles. This did not remove or weaken the required existing profiles.

These are source/CI validations only. GitHub Actions is evidence transport/validation and is not resident runtime authority.

## Authority boundaries

```text
MIR historical accounting authority: MIR only
StegVerse governance/delta authority: StegVerse only
Interlock/InTr: transport/admission only
Site: projection/initiation only
Heartbeat: carrier only
credential authority: TV/TVC
GitHub Actions runtime authority: NONE
```

## Remaining completion boundary

Source integration is merged. The end-to-end Run-2 test still requires authentic execution:

```text
StegVerse governance test executes
-> authentic exact history package handed to MIR
-> MIR actually ingests and records the state changes
-> MIR emits authentic historical-accounting artifact
-> MIR-return adapter observes that exact artifact
-> resident Universal InTr admits the return packet
-> SDK receives the exact MIR artifact
-> SDK compares MIR accounting to original Run-2 state/change data
-> delta result retained
-> Publisher documents the complete run and evidence
```

No authentic MIR response, resident return admission, SDK delta result, or Publisher end-to-end report is claimed by the merged source implementation.

## Next continuation

Bind the actual MIR response observer/shared carrier to `StegVerseMirAccountingReturn.submit(...)`, execute the full Run-2 governance -> MIR accounting -> return -> SDK delta path, retain authentic receipts/artifacts, and then pass the complete evidence package through Publisher.
