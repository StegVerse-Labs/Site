# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-14
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Parent Goal Prompt Count: `20/20` — exhausted; do not add further goal prompts to this task.
Status: `INACTIVE COORDINATION SHELL / DECOMPOSED TO CANONICAL SUCCESSORS / COMMUNICATION COMPLETION NOT CLAIMED`

## Canonical source/evidence chain retained

The following established artifacts remain canonical at their stated provenance:

- Reusable Task Component Model: `StegVerse-Labs/.github@b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`;
- Site retained MIR exact return packet binding: `StegVerse-Labs/Site@26b501080f1c00fb4b3204d719619afa8a11acae`;
- SDK Publisher-return baseline binding: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`;
- SDK completion-capsule carry-forward: `StegVerse-org/StegVerse-SDK@233632c35b0093166c16bdc660aa08e4ee1fe95a`;
- Publisher MIR artifact-return binding: `GCAT-BCAT-Engine/Publisher@40018e94a04e794e35dd499b4adc4296edb4b34c`;
- reusable LLM Adapter final StegVerse-side egress source: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`;
- SDK MIR Publisher-return exact continuity assembly: `StegVerse-org/StegVerse-SDK@b4927ed277c4993662f9e7e4ffd717f677ad5459`.

The parent technical-guide task is not complete merely because these source/build-test components are merged. The parent has reached its prompt ceiling and therefore now serves only as immutable coordination/history while genuinely separable remaining work advances under successor Goal Task IDs.

## Runtime truth model

For this trajectory, state transitions are runtime truth. Time and authority are state variables evaluated inside the transition model. Receipts, hashes, manifests, retained packets, and retained records are durable representations of transitions; they are not a separate prerequisite called "runtime evidence".

Do not use `awaiting runtime evidence` as a generic blocker label. If a required transition does not occur, identify the concrete missing transition, unconsumed request, denied admission, missing binding, missing authentic endpoint, or missing later receipt.

Mirror-versus-authentic-MIR is provenance. MIR NODE MIRROR execution remains valid mirror provenance and must not be rewritten when authentic external MIR is later substituted.

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

No MIR-specific duplicate transport/runtime implementation is authorized by this choreography.

## Established retained-packet and return-admission continuity

Site PR `#1318` bound the exact retained `stegverse.canonical-runtime-exact-return-packet/v1` wrapper into the existing external-counterpart return consumer. It validates profile `MIR`, exact packet SHA-256, decoded JSON, mirror-return shape, manifest continuity, external ingress receipt, manifest hash, and response/correlation continuity before the existing accounting-return adapter and return-admission path consume it.

Exact head `26762524c04880efd95c642d1c1ab6d96d99185f` passed:

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority #12566: SUCCESS
MIR InTr SDK Return Profile #30: SUCCESS
Site Handoff Orchestrator #3809: SUCCESS
Ecosystem Heartbeat Orchestration #2465: SUCCESS
```

The merge is `26b501080f1c00fb4b3204d719619afa8a11acae`. This preserves MIR NODE MIRROR / Site build-test provenance and does not substitute authentic external MIR.

## Established SDK completion capsule

SDK PR `#240` added `stegverse.sdk.downstream-completion-capsule/v1`, preserving admitted manifest, normalized completion, `manifest_hash`, `completion_hash`, `response_to`, `retained_packet_sha256`, Publisher/egress declarations, and `authority_effect = NONE`.

Exact head `4114b75727746a40ca43e7ab4040abf1d45b22ad` passed `SDK Package Artifact Validation (Non-Authorizing) #192: SUCCESS` and merged as `233632c35b0093166c16bdc660aa08e4ee1fe95a`.

## Established Publisher artifact return

Publisher PR `#71` added optional `stegverse.publisher.mir-roundtrip-binding/v1` continuity on the existing exact-byte artifact-transfer/return path. The return preserves SDK capsule hashes/correlation, SDK processor state, exact Publisher return identities, no-authority flags, and promotes only Publisher observation at that boundary.

Exact head `598fc305103a710052d74c5389610ad1956cbd32` passed:

```text
Architecture Guard #829: SUCCESS
Publisher Check #304: SUCCESS
Validate KV document pipeline #11: SUCCESS
Publisher Readiness #301: SUCCESS
Validate ERL KV Provider Proof Projection #7: SUCCESS
```

The merge is `40018e94a04e794e35dd499b4adc4296edb4b34c`.

## SDK return assembly successor completed

The exhausted parent was decomposed to genuinely separable successor `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001`, canonical issue `StegVerse-Labs/.github#1888`, handoff `StegVerse-org/StegVerse-SDK/docs/MIR_SDK_RETURN_ASSEMBLY_CONTINUITY_MIRROR_HANDOFF.md`.

SDK PR `#242` now requires the independently retained original SDK completion capsule whenever the exact Publisher return carries `stegverse.publisher.mir-roundtrip-binding/v1`. It fails closed unless the Publisher-carried capsule exactly equals the original SDK capsule and remains bound to the original admitted manifest/completion, response correlation, retained-packet hash, SDK processor state, Publisher return identity fields, no-authority state, and false downstream predicates.

Exact head `fe8b01cd3ad9f6b54f124883e3e2c2d869302e6f` passed:

```text
Publisher SDK Return Binding Validation (Non-Authorizing) #2: SUCCESS
SDK Package Artifact Validation (Non-Authorizing) #193: SUCCESS
```

PR `#242` was squash-merged as `StegVerse-org/StegVerse-SDK@b4927ed277c4993662f9e7e4ffd717f677ad5459`.

This establishes SDK return assembly at source/build-test provenance only. It does not prove a live authentic-MIR runtime instance traversed the SDK assembler.

## Current transition truth

```text
MIR-profile request construction: implemented
MIR NODE MIRROR bounded round-trip transitions: executed at mirror/build-test provenance
StegOS exact return packet retention: executed at mirror/build-test provenance
Site retained exact return packet binding: implemented/validated/merged
Site return admission / STEGVERSE_RETURN_EXIT / evaluator ingress: established at stated Site build-test provenance
SDK manifest-selected processing completion capsule: implemented/validated/merged
Publisher exact artifact-return MIR binding: implemented/validated/merged
SDK exact Publisher-return assembly continuity: implemented/validated/merged at source/build-test provenance
SDK return binding live authentic-MIR runtime observation: false
final StegVerse-side governed egress for the remaining chain: not yet established by this reconciliation
Interlock/InTr egress for the remaining chain: not yet established
far-side final transition/caller receipt for the remaining chain: not yet established
authentic external MIR endpoint substitution: not yet established
communication_complete: false
```

## Successor decomposition and next work

Parent Goal Prompt Count is exhausted at `20/20`; no further execution prompts belong to this Goal Task.

Completed source/build-test successor:

```text
MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001
-> RTC-SDK-RETURN-006
-> source/build-test completion only
```

Active downstream successor:

```text
MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001
-> RTC-STEGVERSE-EGRESS-007
-> RTC-INTERLOCK-INTR-TRANSPORT-008
-> RTC-FARSIDE-FINAL-009
-> authentic external MIR endpoint substitution without choreography redesign
```

Canonical successor handoff: `docs/MIR_ROUNDTRIP_EGRESS_AUTHENTICITY_MIRROR_HANDOFF.md`.
Canonical successor issue: `StegVerse-Labs/.github#1891`.

The first bounded transition under that successor is to reconcile and reuse the existing LLM Adapter `RTC-STEGVERSE-EGRESS-007` implementation from `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`, then materialize/consume an exact SDK return input without fabricating authentic MIR provenance.

## Authority boundaries

- GitHub Actions: validation/evidence transport only; runtime authority `NONE`.
- LLM Adapter: protocol/framing and applicable final StegVerse-side framework transition only.
- Interlock/InTr: egress admission/state-transition authority.
- TV/TVC: credential authority where required.
- MIR: source-native external semantics/history/accounting authority on its side.
- StegVerse: StegVerse governance authority.
- Far-side final receipt remains separate from Interlock/InTr egress admission.

## README maintenance

The Site README has no new executable behavior to project from this coordination-only decomposition. Existing README restoration remains intact; no README byte change is required by this handoff reconciliation.

## Parent completion boundary

This parent record is **inactive/decomposed, not completed**. Its unsatisfied downstream predicates are owned by `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`. Do not mark this parent complete, release-ready, deployed, authentically MIR-connected, or terminally communicated unless the successor later supplies evidence that satisfies those predicates and the parent documentation is reconciled from that evidence.
