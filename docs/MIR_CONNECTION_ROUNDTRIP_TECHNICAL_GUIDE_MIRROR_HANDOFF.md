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
StegOS MIR-profile canonical runtime binding merge: `StegVerse-Labs/StegOS@5ba7a6baf13017dfafdacb55b8f0bd47ead926c6`
StegOS MIR NODE MIRROR executed round-trip merge: `StegVerse-Labs/StegOS@b52800a6cec226432c9cb8fec3f2e65abbd4b49c`
Site complete-manifest return continuity merge: `StegVerse-Labs/Site@419a77da87e77f832ea903723cbdbc7359fb6532`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / MIR NODE MIRROR STATE-TRANSITION ROUND TRIP EXECUTED / STEGVERSE RETURN-ADMISSION + DOWNSTREAM TRANSITIONS REMAIN`

## Runtime truth model

For this trajectory, state transitions are runtime truth. Time and authority are state variables evaluated inside the transition model. Receipts, hashes, manifests, and retained records are durable representations of transitions; they are not a separate prerequisite called "runtime evidence".

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
- retain exact response-to/correlation continuity.

## MIR NODE MIRROR transition execution now established

StegOS PR `#373` bound MIR-profile processing into the canonical `EVENT_EPHEMERAL` runtime lane so the MIR profile is actually consumed as a bounded consequence of the existing `LeaseMachine` / Universal InTr transition machinery rather than remaining adjacent source. The exact-head CI failure initially exposed a wrong `correlation_id` keyword in the new test; that concrete defect was repaired and StegOS CI run `34780732208` passed before merge `5ba7a6baf13017dfafdacb55b8f0bd47ead926c6`.

StegOS subsequently merged reusable local runtime custody bindings (`RetainedNodeProofVerifier`, `LocalReturnPathCarrier`, `LocalEvidenceExporter`, `LocalClosureRetainer`) and PR `#376` executed the MIR NODE MIRROR build/test round trip through the merged MIR-profile runtime path. Exact-head StegOS CI run `34782385311` passed and merge `b52800a6cec226432c9cb8fec3f2e65abbd4b49c` retained the executed path.

That execution caused the canonical lease/runtime state machine to progress through its transition history, executed the MIR-profile mirror bounded operation, produced an `EXTERNAL_FRAMEWORK_INGRESS` receipt bound to the request correlation and exact outbound manifest, produced canonical request/response InTr hop receipts, queued the return, retained execution evidence, and closed the lease. This is runtime execution of the MIR NODE MIRROR path. It is not authentic external MIR endpoint visitation.

## Current transition truth

```text
MIR-profile request construction: implemented
MIR-profile canonical runtime binding: implemented
EVENT_EPHEMERAL lease state-machine execution for MIR NODE MIRROR: observed in executed build/test run
canonical runtime request InTr hop transition: observed in executed build/test run
MIR NODE MIRROR bounded processing transition: observed in executed build/test run
EXTERNAL_FRAMEWORK_INGRESS transition/receipt: observed in executed build/test run
canonical runtime response InTr hop transition: observed in executed build/test run
return queue / local evidence / closure retention: observed in executed build/test run
STEGVERSE_RETURN_EXIT produced by Site return-admission path: not yet observed
SDK:EvaluatorReviewIngress transition from that returned manifest: not yet observed
Master Records custody/readback when requested: not yet observed
Publisher transition when declared: not yet observed
SDK return binding: not yet observed
final StegVerse-side governed egress: not yet observed
far-side final transition/caller receipt: not yet observed
authentic external MIR endpoint substitution: not yet observed
```

The remaining gap is therefore not "runtime evidence." The next required state transition is the Site/Interlock return admission that must consume the returned manifest, derive `STEGVERSE_RETURN_EXIT` from that admitted return, and enter `SDK:EvaluatorReviewIngress`.

## Next admissible work

1. Treat the merged MIR NODE MIRROR execution as completed runtime transitions with mirror provenance; do not reset them to false merely because later transitions remain open.
2. Inspect the Site return path for an actual runtime caller of `window.StegVerseMirAccountingReturn.submit(...)`.
3. If no caller exists, that missing consumer/binding is the implementation failure to repair. Do not describe it as waiting for evidence.
4. Cause the returned MIR NODE MIRROR manifest to pass through the existing Site Universal InTr materialization path and derive `STEGVERSE_RETURN_EXIT` only from the admitted return receipt.
5. Continue the same manifest into `SDK:EvaluatorReviewIngress`, then the manifest-selected downstream stages. Claim each resulting transition when it occurs; do not withhold earlier runtime truth because later transitions remain open.
6. Substitute authentic MIR later without redesigning the manifest/correlation/transition choreography.

## Completion boundary

This Goal Task remains `ACTIVE`. MIR NODE MIRROR runtime state transitions are now established. Completion still requires the remaining StegVerse return-admission/downstream transitions plus authentic external MIR endpoint substitution where the Goal Task requires it. Source construction or CI alone must not be substituted for a transition that did not occur; conversely, an actually executed transition must not be relabeled as "no runtime evidence" merely because the trajectory is incomplete.
