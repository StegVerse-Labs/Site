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
Site handoff reconciliation merge: `StegVerse-Labs/Site@03445e805ad04ab24486b5890f1906b9c7d00807`
Site README restoration after erroneous marker write: `StegVerse-Labs/Site@4b7b6d0c6d5bd8c3e6cbf3c4c898a83e01e48cd1`
Canonical task record reconciliation merge: `StegVerse-Labs/.github@fe6be6d791520d8f11ebd0e413f99f241a03a84d`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
SDK completion-capsule carry-forward merge: `StegVerse-org/StegVerse-SDK@233632c35b0093166c16bdc660aa08e4ee1fe95a`
SDK completion-capsule handoff reconciliation: `StegVerse-org/StegVerse-SDK@183bc5b3ebc66c3f13a433b6b004e92a2bc0f80c`, `StegVerse-org/StegVerse-SDK@ff249a286379d74646cb6e9c45cd9b8c7636480e`
Publisher MIR artifact-return binding merge: `GCAT-BCAT-Engine/Publisher@40018e94a04e794e35dd499b4adc4296edb4b34c`
Publisher MIR artifact-return handoff reconciliation: `GCAT-BCAT-Engine/Publisher@68f7b2bd8876a30478ff0e16a44d4c4023af5d8f`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / MIR NODE MIRROR + SITE RETURN-ADMISSION + RETAINED EXACT RETURN PACKET BINDING + SDK COMPLETION CAPSULE + PUBLISHER ARTIFACT-RETURN BINDING MERGED / SDK RETURN AND EGRESS TRANSITIONS REMAIN`

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

## Retained exact return packet binding established

Site issue `#1313` identified the concrete delivery/consumer defect: StegOS retained an exact packet under schema `stegverse.canonical-runtime-exact-return-packet/v1`, while Site previously proved return admission only from a locally constructed return artifact shape.

Site PR `#1318` implemented `retainedPacketToConsumerInput(...)` and `consumeRetainedPacket(...)` on the existing `StegVerseExternalCounterpartReturnConsumer`. The binding requires retained packet schema `stegverse.canonical-runtime-exact-return-packet/v1`, profile `MIR`, exact `packet_sha256`, non-empty `packet_utf8`, valid decoded JSON, decoded `mirror_return`, manifest continuity, external ingress receipt, manifest hash continuity, and correlation continuity before passing the decoded object through the existing MIR accounting return adapter. The test rejects a synthesized non-retained fixture shape and rejects retained-packet digest mismatch.

PR `#1318` was validated at exact head `26762524c04880efd95c642d1c1ab6d96d99185f` by:

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority #12566: SUCCESS
MIR InTr SDK Return Profile #30: SUCCESS
Site Handoff Orchestrator #3809: SUCCESS
Ecosystem Heartbeat Orchestration #2465: SUCCESS
```

PR `#1318` was squash-merged as `StegVerse-Labs/Site@26b501080f1c00fb4b3204d719619afa8a11acae`. Handoff reconciliation was committed as `03445e805ad04ab24486b5890f1906b9c7d00807`, canonical task-record reconciliation as `StegVerse-Labs/.github@fe6be6d791520d8f11ebd0e413f99f241a03a84d`, and an erroneous README marker write was restored as `StegVerse-Labs/Site@4b7b6d0c6d5bd8c3e6cbf3c4c898a83e01e48cd1`. The README restoration preserved prior README content and no README behavior change was retained.

## SDK completion capsule established

SDK issue `StegVerse-org/StegVerse-SDK#239` identified that the SDK processing result was not a sufficient downstream transition input because it did not carry the admitted manifest object or normalized completion block forward.

SDK PR `#240` added `stegverse.sdk.downstream-completion-capsule/v1` to the SDK processing result, preserving the admitted manifest, normalized `completion`, `manifest_hash`, `completion_hash`, `response_to`, `retained_packet_sha256`, derived Publisher/egress declarations, and `authority_effect = NONE`. The exact head `4114b75727746a40ca43e7ab4040abf1d45b22ad` was validated by `SDK Package Artifact Validation (Non-Authorizing) #192: SUCCESS` and merged as `StegVerse-org/StegVerse-SDK@233632c35b0093166c16bdc660aa08e4ee1fe95a`.

## Publisher artifact-return binding established

Publisher issue `GCAT-BCAT-Engine/Publisher#70` identified that the next SDK return binding requires exact canonical Publisher return bytes under schema `stegverse.publisher.artifact-return/v1`.

Publisher PR `#71` extended the existing exact-byte `stegverse.publisher.artifact-transfer/v1` -> `stegverse.publisher.artifact-return/v1` path with optional `stegverse.publisher.mir-roundtrip-binding/v1` metadata. The binding validates the SDK `stegverse.sdk.downstream-completion-capsule/v1` when `completion.publisher.required = true`, preserves `manifest_hash`, `completion_hash`, `response_to`, `retained_packet_sha256`, SDK processor state, source export ID/hash, Publisher transfer/generation IDs, exact artifact manifest/hashes, and no-authority flags, and promotes only `publisher_transition_observed` after exact artifact rendering and artifact-manifest verification.

PR `#71` exact head `598fc305103a710052d74c5389610ad1956cbd32` was validated by:

```text
Architecture Guard #829: SUCCESS
Publisher Check #304: SUCCESS
Validate KV document pipeline #11: SUCCESS
Publisher Readiness #301: SUCCESS
Validate ERL KV Provider Proof Projection #7: SUCCESS
```

PR `#71` was squash-merged as `GCAT-BCAT-Engine/Publisher@40018e94a04e794e35dd499b4adc4296edb4b34c` and reconciled in the Publisher MIR handoff at `GCAT-BCAT-Engine/Publisher@68f7b2bd8876a30478ff0e16a44d4c4023af5d8f`.

This establishes the Publisher artifact-return binding in source/build-test provenance only. It does not complete SDK return binding, final governed StegVerse-side egress, Interlock/InTr egress, far-side final transition/caller receipt, communication completion, or authentic external MIR endpoint substitution.

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
SDK manifest-selected processing after evaluator ingress: implemented/merged with downstream completion capsule at SDK source/build-test provenance
Master Records custody/readback when requested: not yet caused
Publisher artifact-return binding when declared: implemented/merged at Publisher source/build-test provenance
SDK return binding: not yet caused
final StegVerse-side governed egress: not yet caused
Interlock/InTr egress: not yet caused
far-side final transition/caller receipt: not yet caused
authentic external MIR endpoint substitution: not yet caused
communication_complete: false
```

## Next admissible work

1. Preserve all already-executed mirror, retained-packet, Site return-admission, SDK completion-capsule, and Publisher artifact-return binding transitions as runtime/source/build-test truth at their stated provenance.
2. Bind exact Publisher return bytes through SDK return assembly to the original request and initiator.
3. Execute the applicable final governed StegVerse-side egress transition without creating a MIR-specific egress mechanism.
4. Observe Interlock/InTr egress and the far-side final transition/caller receipt.
5. Substitute authentic MIR later without redesigning the manifest/correlation/transition choreography.
6. Use `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001` for additional admissibility-wiki framework profiles rather than creating per-framework transport implementations.

## Completion boundary

This Goal Task remains `ACTIVE`. MIR NODE MIRROR, retained exact packet binding, Site return-admission, SDK completion-capsule carry-forward, and Publisher artifact-return binding are established at their stated provenance. Completion still requires SDK return binding, final governed StegVerse-side egress, Interlock/InTr egress, far-side final transition/caller receipt, and authentic external MIR endpoint substitution where the Goal Task requires it.
