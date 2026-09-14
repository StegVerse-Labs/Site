# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-14
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Retained-packet binding issue: `StegVerse-Labs/Site#1313`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Reusable Task Component Model merge: `StegVerse-Labs/.github@b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`
Reusable external-framework rollout merge: `StegVerse-Labs/.github@49692b2fe410053fc1b0b83a7d27c39fca887d27`
StegOS reusable external mirror merge: `StegVerse-Labs/StegOS@50573809ba5335edca14107b60f285642236a78a`
StegOS reusable round-trip evidence verifier merge: `StegVerse-Labs/StegOS@16c0778dafb345893e82dd293f31c0b54d785481`
StegOS receipt-correlation normalization merge: `StegVerse-Labs/StegOS@17102159e5614886072dea53cef96cfa722632bd`
StegOS outbound/evidence-package assembly merge: `StegVerse-Labs/StegOS@310b6233578b07d02fe8a03e9cf6d02b5f5b4c9d`
StegOS MIR-profile canonical runtime binding merge: `StegVerse-Labs/StegOS@5ba7a6baf13017dfafdacb55b8f0bd47ead926c6`
StegOS MIR NODE MIRROR executed round-trip merge: `StegVerse-Labs/StegOS@b52800a6cec226432c9cb8fec3f2e65abbd4b49c`
Site complete-manifest return continuity merge: `StegVerse-Labs/Site@419a77da87e77f832ea903723cbdbc7359fb6532`
Site retained MIR exact return packet binding merge: `StegVerse-Labs/Site@26b501080f1c00fb4b3204d719619afa8a11acae`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / MIR NODE MIRROR + SITE RETURN-ADMISSION + RETAINED EXACT RETURN PACKET BINDING EXECUTED IN BUILD-TEST PROVENANCE / DOWNSTREAM TRANSITIONS REMAIN`

## Runtime truth model

For this trajectory, state transitions are runtime truth. Time and authority are state variables evaluated inside the transition model. Receipts, hashes, manifests, retained packets, and retained records are durable representations of transitions; they are not a separate prerequisite called "runtime evidence".

Do not use `awaiting runtime evidence` as a blocker description. If a required transition does not occur, identify the concrete failure instead: missing transition-producing code, missing Interlock/InTr binding, an unconsumed transition request, a denied transition, or a missing later transition.

A mirror-versus-authentic-MIR distinction is provenance, not a distinction between runtime and non-runtime. An executed MIR NODE MIRROR transition is runtime execution with counterpart provenance `MIR NODE MIRROR`. Authentic external MIR later satisfies the separate endpoint-substitution predicates.

## Canonical reusable composition

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

## Authority/state namespace invariant

External frameworks may define authority according to their own internal standards. Those external semantics may return as source-native data, claims, receipts, decisions, or evidence, but they do not become StegVerse authority merely by crossing the manifest boundary. StegVerse evaluates authority and time as state variables during its own state transitions.

## Manifest/round-trip invariant

- preserve the exact outbound StegVerse manifest and SHA-256 binding;
- append `EXTERNAL_FRAMEWORK_INGRESS` at the far-side boundary;
- allow receipt-only semantic silence when no source-native result is required;
- preserve MIR/external semantics as source-native evidence;
- return the original manifest plus receipted continuation;
- append `STEGVERSE_RETURN_EXIT` only after StegVerse-side return admission;
- retain exact response-to/correlation continuity;
- when a StegOS retained packet exists, verify and consume the exact `stegverse.canonical-runtime-exact-return-packet/v1` wrapper instead of reconstructing an equivalent fixture.

## MIR NODE MIRROR transition execution established

StegOS PR `#373` bound MIR-profile processing into the canonical `EVENT_EPHEMERAL` runtime lane so the MIR profile is actually consumed as a bounded consequence of the existing `LeaseMachine` / Universal InTr transition machinery rather than remaining adjacent source. The exact-head CI failure initially exposed a wrong `correlation_id` keyword in the new test; that concrete defect was repaired and StegOS CI run `34780732208` passed before merge `5ba7a6baf13017dfafdacb55b8f0bd47ead926c6`.

StegOS subsequently merged reusable local runtime custody bindings (`RetainedNodeProofVerifier`, `LocalReturnPathCarrier`, `LocalEvidenceExporter`, `LocalClosureRetainer`) and PR `#376` executed the MIR NODE MIRROR build/test round trip through the merged MIR-profile runtime path. Exact-head StegOS CI run `34782385311` passed and merge `b52800a6cec226432c9cb8fec3f2e65abbd4b49c` retained the executed path.

That execution caused the canonical lease/runtime state machine to progress through its transition history, executed the MIR-profile mirror bounded operation, produced an `EXTERNAL_FRAMEWORK_INGRESS` receipt bound to the request correlation and exact outbound manifest, produced canonical request/response InTr hop receipts, queued the return, retained execution evidence, retained an exact return packet, and closed the lease. This is runtime execution of the MIR NODE MIRROR path. It is not authentic external MIR endpoint visitation.

## Site return-admission transition execution established

The previous Site return implementation exposed `window.StegVerseMirAccountingReturn.submit(...)` but had no caller that consumed a returned external-counterpart manifest and caused the next transition. That implementation gap was repaired by Site PR `#1297`, which added the reusable `StegVerseExternalCounterpartReturnConsumer`.

The bounded Site runtime execution invokes the actual return adapter, queues the existing Universal InTr materialization request, receives an admitted InTr return, derives `STEGVERSE_RETURN_EXIT` only from that admitted return, reaches `SDK_EVALUATOR_INGRESS_ADMITTED`, and records `EXTERNAL_COUNTERPART_RETURN_ADMITTED` in Node continuity.

The first execution attempt exposed a concrete Node-runtime incompatibility: the test attempted to assign the read-only Node `crypto` global. That code defect was repaired. MIR InTr SDK Return Profile run `34790610901` then passed, including the step `Execute MIR NODE MIRROR return through Site consumer and InTr admission`.

## Retained exact return packet binding established

Site issue `#1313` identified the remaining concrete delivery/consumer defect: StegOS retained an exact packet under schema `stegverse.canonical-runtime-exact-return-packet/v1`, while Site previously proved return admission only from a locally constructed return artifact shape.

Site PR `#1318` implemented `retainedPacketToConsumerInput(...)` and `consumeRetainedPacket(...)` on the existing `StegVerseExternalCounterpartReturnConsumer`. The binding requires retained packet schema `stegverse.canonical-runtime-exact-return-packet/v1`, profile `MIR`, exact `packet_sha256`, non-empty `packet_utf8`, valid decoded JSON, decoded `mirror_return`, manifest continuity, external ingress receipt, manifest hash continuity, and correlation continuity before passing the decoded object through the existing MIR accounting return adapter. The test now rejects a synthesized non-retained fixture shape and rejects retained-packet digest mismatch.

PR `#1318` was validated at exact head `26762524c04880efd95c642d1c1ab6d96d99185f` by:

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority #12566: SUCCESS
MIR InTr SDK Return Profile #30: SUCCESS
Site Handoff Orchestrator #3809: SUCCESS
Ecosystem Heartbeat Orchestration #2465: SUCCESS
```

PR `#1318` was squash-merged as `StegVerse-Labs/Site@26b501080f1c00fb4b3204d719619afa8a11acae`.

This establishes the Site-side retained exact packet binding in source and build/test runtime provenance. It does not complete manifest-selected SDK processing after ingress, declared Master Records/Publisher stages, SDK return binding, final governed StegVerse-side egress, far-side final transition/caller receipt, or authentic external MIR endpoint substitution.

## Current transition truth

```text
MIR-profile request construction: implemented
MIR-profile canonical runtime binding: implemented
EVENT_EPHEMERAL lease state-machine execution for MIR NODE MIRROR: executed, mirror build/test provenance
canonical runtime request InTr hop transition: executed, mirror build/test provenance
MIR NODE MIRROR bounded processing transition: executed, mirror build/test provenance
EXTERNAL_FRAMEWORK_INGRESS transition/receipt: executed, mirror build/test provenance
canonical runtime response InTr hop transition: executed, mirror build/test provenance
return queue / local evidence / closure retention: executed, mirror build/test provenance
StegOS exact return packet retention: executed, mirror build/test provenance
Site external-counterpart return consumer: executed, Site build/test provenance
Site retained exact return packet binding: implemented and exact-head validated, Site build/test provenance
Site Universal InTr return admission from retained-packet path: executed, Site build/test provenance
STEGVERSE_RETURN_EXIT: executed, Site build/test provenance
SDK:EvaluatorReviewIngress admission state: executed, Site build/test provenance
Node EXTERNAL_COUNTERPART_RETURN_ADMITTED transition record: executed, Site build/test provenance
SDK manifest-selected processing after evaluator ingress: not yet caused
Master Records custody/readback when requested: not yet caused
Publisher transition when declared: not yet caused
SDK return binding: not yet caused
final StegVerse-side governed egress: not yet caused
far-side final transition/caller receipt: not yet caused
authentic external MIR endpoint substitution: not yet caused
```

## Registry-driven reusable rollout continuation

The framework-neutral counterpart architecture is now generalized as reusable identity `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`. `StegVerse-Labs/.github#1800` tracks the capability, and `.github` PR `#1801` passed exact-head Organization Control `34797138353`, Deterministic Repository Suite `34797138357`, and Heartbeat validation `34797138326` before squash merge `49692b2fe410053fc1b0b83a7d27c39fca887d27`.

That reusable task consumes one exact entry from the canonical `StegVerse-Labs/admissibility-wiki` external-framework registry and composes the already-existing external-adapter/manifest/governed-processing/round-trip/custody/SDK-return/egress/InTr components. It does not create a second transport, scheduler, WorkerCoordinator, credential path, custody plane, Publisher, or user-verification mechanism, and it does not change this Goal Task identity or any MIR completion predicate.

Framework-specific invocations retain exact framework/source/version/counterpart provenance. A source-blocked or runtime-unavailable framework fails closed for that invocation without blocking unrelated framework entries. Executed mirror/build-test transitions remain runtime truth at their recorded provenance; authentic external endpoint substitution remains a separate transition predicate.

## README review

The Site root README already documents the reusable external-counterpart/return and governed InTr architecture used by this Goal. No README mutation was required for PR `#1318`; the retained-packet binding is an implementation detail of the existing Site consumer path and does not change public product behavior, route semantics, authority boundaries, or public runtime behavior.

## Next admissible work

1. Preserve all already-executed mirror, retained-packet, and Site return-admission transitions as runtime truth at their stated provenance.
2. Continue the admitted retained MIR return from `SDK:EvaluatorReviewIngress` into the manifest-selected SDK processor.
3. Execute declared Master Records custody/readback/reconstruction only when requested by the admitted manifest.
4. Execute Publisher projection only when declared by the complete manifest.
5. Bind Publisher/processing output through SDK return assembly to the original request and initiator.
6. Execute the applicable final governed StegVerse-side egress transition without creating a MIR-specific egress mechanism.
7. Observe Interlock/InTr egress and the far-side final transition/caller receipt.
8. Substitute authentic MIR later without redesigning the manifest/correlation/transition choreography.
9. Use `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001` for additional admissibility-wiki framework profiles rather than creating per-framework transport implementations.

## Completion boundary

This Goal Task remains `ACTIVE`. MIR NODE MIRROR, retained exact packet binding, and Site return-admission state transitions are established at build/test runtime provenance. Completion still requires manifest-selected SDK processing after ingress, declared custody/Publisher stages, SDK return binding, final governed StegVerse-side egress, far-side final transition/caller receipt, and authentic external MIR endpoint substitution where the Goal Task requires it.
