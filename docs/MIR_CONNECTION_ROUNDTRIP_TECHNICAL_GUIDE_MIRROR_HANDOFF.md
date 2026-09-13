# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-13
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Reusable Task Component Model merge: `StegVerse-Labs/.github@b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`
StegOS reusable external mirror merge: `StegVerse-Labs/StegOS@50573809ba5335edca14107b60f285642236a78a`
StegOS reusable round-trip evidence verifier merge: `StegVerse-Labs/StegOS@16c0778dafb345893e82dd293f31c0b54d785481`
StegOS receipt-correlation normalization merge: `StegVerse-Labs/StegOS@17102159e5614886072dea53cef96cfa722632bd`
StegOS outbound/evidence-package assembly merge: `StegVerse-Labs/StegOS@310b6233578b07d02fe8a03e9cf6d02b5f5b4c9d`
Site complete-manifest return continuity merge: `StegVerse-Labs/Site@419a77da87e77f832ea903723cbdbc7359fb6532`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / MIR-PROFILE MIRROR + COMPLETE MANIFEST RETURN + CORRELATION-NORMALIZED EVIDENCE PACKAGE PATH MERGED / AUTHENTIC RUNTIME EVIDENCE NOT YET OBSERVED`

## Canonical reusable composition

The Goal Task identity and COSV remain unchanged. Reuse/componentization remains mandatory before any additional task-specific orchestration.

```text
MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001
  -> RTC-MANIFEST-001
  -> RTC-GOVERNED-PROCESSING-002
  -> RTC-ROUNDTRIP-003
  -> RTC-EVIDENCE-CUSTODY-004
  -> RTC-PUBLISHER-005
  -> RTC-SDK-RETURN-006
  -> RTC-STEGVERSE-EGRESS-007
  -> RTC-INTERLOCK-INTR-TRANSPORT-008
  -> RTC-FARSIDE-FINAL-009
```

The external counterpart mirror is framework-neutral; MIR is a profile rather than a dedicated transport/runtime implementation.

## Merged mirror/profile contract

- preserve the exact outbound StegVerse manifest and SHA-256 binding;
- append `EXTERNAL_FRAMEWORK_INGRESS` evidence at the far-side boundary;
- allow receipt-only semantic silence when no source-native evaluation result is required;
- keep MIR/external authority semantics source-native and non-authorizing inside StegVerse;
- require the original manifest plus receipted continuation for re-entry;
- append `STEGVERSE_RETURN_EXIT` only after actual StegVerse-side InTr return admission;
- keep authority/time as StegVerse state variables and external authority namespaces isolated.

The MIR profile separates confirmed, contracted, inferred, and unknown external facts. Unknown MIR details remain unknown rather than being invented.

## Reusable round-trip evidence path

StegOS now contains a framework-neutral verifier for an observed external round-trip evidence package. It validates exact manifest/hash continuity, exact `response_to`/correlation continuity, one ordered `EXTERNAL_FRAMEWORK_INGRESS` receipt, one ordered `STEGVERSE_RETURN_EXIT` receipt, same-manifest/same-correlation receipt binding, and non-authorizing receipt semantics. Optional source-native evidence may be present but cannot acquire StegVerse authority by transport.

The verifier is now aligned with the actual merged receipt producers: MIR mirror ingress receipts expose explicit `correlation_id`, while the existing Site return-exit producer may carry the same binding as `response_to`. The verifier accepts either field only when its value exactly matches the package correlation; no mismatch is tolerated.

StegOS also now exposes:

```text
build_run2_request(...)
assemble_external_roundtrip_evidence(...)
```

`build_run2_request(...)` constructs the exact MIR-profile outbound request from caller-owned complete manifest/history/correlation state and computes canonical hash bindings. `assemble_external_roundtrip_evidence(...)` accepts already-observed continuation receipts and packages them for fail-closed verification. Neither function creates transport receipts, admits a transition, or claims runtime authenticity.

StegOS CI run `34779062282` passed before merge `17102159e5614886072dea53cef96cfa722632bd`.
StegOS CI run `34779165905` passed before merge `310b6233578b07d02fe8a03e9cf6d02b5f5b4c9d`.

## Authority invariants

- Task Registry: coordination only.
- WorkerCoordinator: claim/fence authority.
- Interlock/InTr: governed transition/admission authority.
- TV/TVC: credential/provider authority.
- KV/SKAP Vault: sole user-verification authority.
- StegOS runtime adapters: execution/transport implementation only.
- Master Records: observed-reality custody/reconstruction.
- HeartBeat: synchronization/timing/freshness/liveness/state correlation/observability only.
- GitHub: source/evidence coordination only; runtime authority `NONE`.

Source/provider/framework/adapter/device/transport identity must not select processing semantics.

```text
admitted manifest
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

## Current evidence truth

The reusable MIR-profile path now has deterministic source validation and source-side packet/evidence assembly for the required manifest/correlation/receipt structure. No known source-contract mismatch remains between the current mirror ingress receipt, Site return-exit receipt, and reusable verifier.

This does not establish authentic runtime occurrence.

```text
qualifying outbound Interlock/InTr runtime materialization observed: false
qualifying external/MIR-facing runtime ingress receipt observed: false
qualifying MIR evaluation observed: false
qualifying return Interlock/InTr runtime materialization observed: false
qualifying StegVerse return runtime ingress observed: false
Master Records runtime custody/readback observed: false
Publisher runtime execution observed: false
SDK runtime return binding observed: false
final StegVerse-side runtime egress transition observed: false
far-side final transition observed: false
roundtrip runtime verified: false
```

## Next admissible work

Do not treat absent external runtime evidence as a reason to stop independently controllable work.

1. Use merged `build_run2_request(...)` to materialize the exact MIR-profile outbound manifest/history/correlation package from the selected complete manifest state.
2. Drive that package through the existing canonical `EVENT_EPHEMERAL` + Interlock/InTr path wherever that established runtime path is available. Do not create another runtime, relay, observer, credential route, or second transport.
3. Retain the actual `EXTERNAL_FRAMEWORK_INGRESS` and `STEGVERSE_RETURN_EXIT` receipts against the same manifest hash/correlation.
4. Feed that observed continuation into merged `assemble_external_roundtrip_evidence(...)` and the reusable verifier. Do not manufacture either receipt to satisfy the predicate.
5. If the mirror is the far side, classify a successful run as authentic StegVerse mirror-runtime evidence only; do not claim authentic MIR visitation.
6. Substitute authentic MIR later without changing manifest/correlation/evidence choreography.
7. After return admission, continue through canonical SDK manifest ingress, manifest-selected processing, declared Master Records/Publisher stages, SDK return binding, governed StegVerse egress, and far-side final transition without inferring later receipts from earlier ones.
8. Reconcile the guide only against actual observed runtime evidence.

## Completion boundary

This Goal Task remains `ACTIVE`. Source construction, CI, mirror/profile validation, deterministic evidence verification, request assembly, and evidence-package assembly do not satisfy authentic runtime completion. Completion requires the end-to-end observed runtime predicates and guide reconciliation.
