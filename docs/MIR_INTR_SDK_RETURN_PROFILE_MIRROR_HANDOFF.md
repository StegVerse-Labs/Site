# MIR historical-accounting return -> SDK Universal InTr handoff

Updated: 2026-09-13
Goal Task ID: `MIR-INTR-SDK-RETURN-PROFILE-001`
Parent Goal: `MIR-STEGVERSE-HISTORICAL-ACCOUNTING-RUN-002`
Parent SDK issue: `StegVerse-org/StegVerse-SDK#217`
COSV ID: `50000000100000`
Site issue: `StegVerse-Labs/Site#1266`
Status: `ACTIVE / MANIFEST CONTINUITY IMPLEMENTATION`

## Purpose

Route MIR historical-accounting return data into the existing SDK evaluation surface without inventing a MIR-specific transport, while preserving the complete StegVerse manifest state across the external round trip.

Canonical sequence:

```text
StegVerse complete manifest + Run-2 payload
-> outbound Interlock/InTr
-> external counterpart / MIR mirror
-> original manifest state + EXTERNAL_FRAMEWORK_INGRESS receipt + optional MIR result
-> existing evaluator-read-review Universal InTr return
-> actual InTr ingress receipt
-> STEGVERSE_RETURN_EXIT receipt derived from that receipt
-> manifest-qualified SDK:EvaluatorReviewIngress
-> SDK performs next declared evaluation / delta
```

## Manifest re-entry invariant

Entry into StegVerse requires a manifest. A returning external-framework object must carry the exact manifest state that left StegVerse, bound by SHA-256, plus receipted external transitions required for re-entry.

The minimum valid external response may be semantic silence: no business/evaluation result is required, but the round trip still requires the original manifest state plus the two boundary transition classes:

1. `EXTERNAL_FRAMEWORK_INGRESS`
2. `STEGVERSE_RETURN_EXIT`

The external system may use a different internal representation while outside StegVerse. Any external transitions it wants StegVerse to evaluate must be recomposed into the agreed manifest shape with receipts. External authority semantics remain source-native data/evidence and do not become StegVerse authority.

## Existing route reused

The canonical StegOS connector registry already defines `evaluator-read-review`:

```text
operation: READ_REVIEW
source: DEVICE_SYSTEM / Site:EvaluatorReview
destination: STEGOS_ECOSYSTEM / SDK:EvaluatorReviewIngress
payload schema: stegverse.evaluator_review.interlock_request.v1
authority effect: NONE
```

The Site uses the existing generated connector, registered-Node outbox, `/intr/profile`, and `/intr/materialization`. No second route/listener/transport is created.

## Return binding

Before return transport is built, the adapter requires and verifies:

- Run-2 `test_id` and revision;
- exact `response_to` correlation;
- expected response class;
- complete manifest object;
- locally recomputed manifest SHA-256 matching the outbound binding;
- `manifest_continuation.outbound_manifest` exactly equal to that manifest;
- `EXTERNAL_FRAMEWORK_INGRESS` receipt bound to the same manifest hash;
- explicit requirement for the next boundary receipt class `STEGVERSE_RETURN_EXIT`;
- exact returned artifact bytes and locally recomputed artifact SHA-256.

After actual InTr return admission, the adapter creates `STEGVERSE_RETURN_EXIT` only from the real ingress receipt/materialization binding and appends it to the manifest continuation. Static source cannot satisfy this runtime predicate.

## State-variable/namespace invariant

Authority and time remain StegVerse state variables evaluated inside the state-transition model. The MIR or external framework may define authority according to its own system; that definition may return as source-native evidence but cannot be injected as StegVerse authority through the manifest.

## Fail-closed conditions

Fail closed on missing complete manifest, manifest/hash mismatch, outbound-manifest state mismatch, missing external ingress receipt, wrong receipt manifest binding, missing return-exit requirement, invalid test/response binding, artifact digest mismatch, unavailable registered Node, unavailable canonical connector/carrier/profile, materialization collision, ingress receipt mismatch, or authority-bearing transport fields.

## Evidence classification

Source tests/CI prove deterministic manifest preservation, receipt-chain construction rules, profile reuse, fail-closed behavior, and exact request/receipt validation. They do not prove an authentic runtime round trip.

Runtime round-trip boundary evidence requires the same manifest/correlation to carry both actual receipt classes. MIR-specific evaluation evidence is additive when requested by the manifest.
