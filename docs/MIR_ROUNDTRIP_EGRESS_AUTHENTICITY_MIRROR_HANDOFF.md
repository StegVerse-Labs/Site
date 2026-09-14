# MIR round-trip egress and authenticity mirror handoff

Updated: 2026-09-14
Goal Task ID: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Completed predecessor: `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001`
COSV ID: `50000000100000`
Parent issue: `StegVerse-Labs/Site#1277`
Parent handoff: `StegVerse-Labs/Site/docs/MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md`
SDK return predecessor merge: `StegVerse-org/StegVerse-SDK@b4927ed277c4993662f9e7e4ffd717f677ad5459`
Reusable LLM Adapter egress source: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Reusable LLM Adapter handoff: `StegVerse-org/LLM-adapter/docs/SOUTHBOUND_SDK_RETURN_EGRESS_MIRROR_HANDOFF.md`
Status: `ACTIVE / CHECKED_OUT / DOWNSTREAM EGRESS-AUTHENTICITY SUCCESSOR MATERIALIZED`

## Goal

Complete the remaining MIR round-trip downstream chain after exact SDK Publisher-return assembly, without reopening the exhausted parent Goal Task or redesigning reusable transport/runtime components.

The required sequence is:

```text
stegverse.sdk.publisher-return-binding/v1
-> RTC-STEGVERSE-EGRESS-007
-> RTC-INTERLOCK-INTR-TRANSPORT-008
-> RTC-FARSIDE-FINAL-009
-> authentic external MIR endpoint substitution without choreography redesign
-> reconcile parent guide only after evidence supports each predicate
```

This successor is genuinely separable from the parent and predecessor. It owns a stable downstream input (`stegverse.sdk.publisher-return-binding/v1`), a bounded egress/transport/far-side transition sequence, and an endpoint-provenance completion predicate. It is not created merely to reset a prompt counter.

## Canonical current truth

Established before this successor:

- retained exact MIR NODE MIRROR packet binding: established at stated mirror/build-test provenance;
- Site return admission and `STEGVERSE_RETURN_EXIT`: established at stated Site build/test provenance;
- SDK manifest-selected processing completion capsule: merged as `233632c35b0093166c16bdc660aa08e4ee1fe95a`;
- Publisher exact artifact-return MIR binding: merged as `40018e94a04e794e35dd499b4adc4296edb4b34c`;
- SDK exact Publisher-return assembly continuity: exact-head validated and merged as `b4927ed277c4993662f9e7e4ffd717f677ad5459`;
- reusable LLM Adapter source for `RTC-STEGVERSE-EGRESS-007`: merged as `7c7c43a0171360ce7ed4cc2873b29686147845ae`.

Not established merely by those source/build-test merges:

- live final StegVerse-side egress transition for this MIR round trip;
- authentic Interlock/InTr egress admission for this same execution;
- far-side final transition/caller receipt for this same execution;
- authentic external MIR endpoint substitution;
- terminal `communication_complete = true`;
- release or deployment.

## Reuse contract

The first transition must reuse the existing LLM Adapter `RTC-STEGVERSE-EGRESS-007` path. Do not create a MIR-specific egress mechanism or duplicate InTr transport.

The existing LLM Adapter contract consumes exact canonical `stegverse.sdk.publisher-return-binding/v1` bytes with:

- `communication_state = READY_FOR_FINAL_STEGVERSE_EGRESS_TRANSITION`;
- `sdk_return_binding_observed = true`;
- final StegVerse surface `LLM_ADAPTER`;
- transport `INTERLOCK_INTR`;
- `far_side_transition_required = true`;
- `authority_effect = NONE`;
- downstream completion still false before egress.

The component emits `stegverse.llm-adapter.southbound-final-transition/v1` and an exact-byte Interlock/InTr handoff bound to the SDK return hash. Interlock/InTr remains transition authority; LLM Adapter does not self-admit transport.

## Allowed next transitions

1. Reconcile the existing LLM Adapter reusable egress handoff against its already-merged source `7c7c43a0171360ce7ed4cc2873b29686147845ae` and current main.
2. Construct or consume an exact SDK Publisher-return binding that satisfies the merged SDK #242 contract without fabricating live MIR provenance.
3. Execute or classify the existing `RTC-STEGVERSE-EGRESS-007` transition through the authorized existing path.
4. Require authentic same-execution `RTC-INTERLOCK-INTR-TRANSPORT-008` admission evidence before promoting Interlock/InTr egress.
5. Require authentic same-execution `RTC-FARSIDE-FINAL-009` receipt before promoting the far-side transition or communication completion.
6. Substitute authentic external MIR endpoint provenance through the same manifest/correlation choreography without redesign.
7. Reconcile the parent technical guide/task record only from supported evidence.

## Fail-closed boundaries

- Source/CI validation may prove code behavior but may not be promoted into live transition execution.
- GitHub Actions has no runtime/transport authority.
- LLM Adapter may frame the final StegVerse-side transition but may not grant Interlock/InTr admission.
- Interlock/InTr admission does not itself prove far-side receipt.
- Far-side receipt from MIR NODE MIRROR does not satisfy authentic external MIR substitution.
- Authentic external MIR provenance must not retroactively rewrite earlier mirror provenance.
- `communication_complete` remains false until the required far-side terminal transition is actually supported for the authentic choreography required by this goal.
- TV/TVC remains credential authority where credentials are required.

## Completion predicates

This successor is complete only when the canonical records distinguish and support, without conflation:

- final StegVerse-side egress transition;
- Interlock/InTr egress transition;
- far-side final transition/caller receipt;
- authentic external MIR endpoint substitution where required;
- terminal communication state;
- preserved no-authority and provenance boundaries.

If any later predicate remains unsupported, keep it false and route the next bounded transition rather than describing it as a generic blocker.
