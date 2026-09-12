# MIR historical-accounting return -> SDK Universal InTr handoff

Updated: 2026-09-11
Goal Task ID: `MIR-INTR-SDK-RETURN-PROFILE-001`
Parent Goal: `MIR-STEGVERSE-HISTORICAL-ACCOUNTING-RUN-002`
Parent SDK issue: `StegVerse-org/StegVerse-SDK#217`
COSV ID: `50000000100000`
Site issue: `StegVerse-Labs/Site#1266`
Status: `ACTIVE / IMPLEMENTATION`

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

## Existing route reused

The canonical StegOS connector registry already defines profile `evaluator-read-review`:

```text
operation: READ_REVIEW
source: DEVICE_SYSTEM / Site:EvaluatorReview
destination: STEGOS_ECOSYSTEM / SDK:EvaluatorReviewIngress
payload schema: stegverse.evaluator_review.interlock_request.v1
authority effect: NONE
```

The Site already carries the generated browser connector for that profile and already has the generic registered-Node method `StegVerseNodeContinuity.queueIntrMaterializationRequest(...)`.

The device-local Universal InTr ingress already exposes `/intr/profile` and `/intr/materialization`; this task extends that existing ingress to advertise/admit the already-canonical SDK evaluator profile. It does not create another route.

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

## Fail-closed conditions

Fail closed on missing/invalid test binding, mismatched `response_to`, unsupported response class, artifact digest mismatch, unavailable registered Node, unavailable canonical connector/carrier, unavailable SDK evaluator profile, materialization collision, ingress receipt mismatch, or any authority-bearing field.

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

## Evidence classification

Source tests/CI may prove deterministic binding, profile reuse, fail-closed behavior, and exact request/receipt validation. They do not prove an authentic MIR response occurred or that resident Run 2 executed.

## Next continuation

After source implementation merges, bind the actual MIR response observer/shared carrier to the adapter entrypoint. An authentic MIR artifact should invoke the adapter, produce an authentic bound ingress receipt, and only then become input to the SDK Run-2 delta evaluation.
