# MIR round-trip egress authenticity mirror handoff

Updated: 2026-09-14
Goal Task ID: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Predecessor Goal Task ID: `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/.github#1891`
Canonical registry: `StegVerse-Labs/.github/data/canonical-task-records/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
SDK return materialization merge: `StegVerse-org/StegVerse-SDK@d7f57428cb817c5f308b7cd545bfac29ca0a817c`
Publisher return carrier-routing merge: `StegVerse-Labs/.github@bf8a726da8688bcfbf625b82a388ae8c79080666`
SDK-owned return ingress/materialization source merge: `StegVerse-Labs/.github@61d064229939d714bd85ba15fd7a6355f37d0647`
Canonical registry reconciliation merge: `StegVerse-Labs/.github@e95c30099d7c88a2757b96005ab75df74da0e973`
Reusable egress source merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / CHECKED_OUT / SDK RETURN SOURCE CHAIN CONNECTED / AUTHENTIC SDK RETURN RUNTIME INPUT STILL NOT OBSERVED`

## State-transition invariant

Every process step is a distinct state transition. Owner selection, reverse ingress admission, exact-byte materialization, final StegVerse-side egress, Interlock/InTr admission and transport, far-side arrival, governed return receipt, durable return recording, final transport-exit transition, and post-transport reconstruction are separate transitions. Evidence for one transition must not promote another. A downstream failure cannot rewrite already completed upstream truth.

## Reused downstream chain

```text
verified MIR Publisher artifact-return
-> existing reverse Publisher-return InTr ingress
-> existing StegVerse-SDK publisher-return materialization
-> stegverse.sdk.publisher-return-binding/v1
-> RTC-STEGVERSE-EGRESS-007
-> RTC-INTERLOCK-INTR-TRANSPORT-008
-> RTC-FARSIDE-FINAL-009
-> governed return receipt and durable record
-> final allowed transport-exit transition
-> SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED=true
-> post-transport downstream domains as required
```

Do not create a MIR-specific transport, scheduler, listener, credential authority, governance engine, custody implementation, or second runtime plane.

## Established source truth

- The SDK exact-return materialization seam merged in SDK PR #245 as `d7f57428cb817c5f308b7cd545bfac29ca0a817c`.
- Publisher reverse-owner routing merged in `.github` PR #1902 as `bf8a726da8688bcfbf625b82a388ae8c79080666`: verified MIR-bound returns select `StegVerse-org/StegVerse-SDK`; ordinary Publisher returns retain the KV owner.
- Post-routing inspection found the next concrete state-transition defect: the existing universal Publisher-return ingress recognized only the KV owner, so an SDK-owned MIR return could not enter the existing return-consumer/materialization branch.
- `.github` issue #1904 and PR #1905 repaired that defect without adding an ingress or transport plane. Merge `61d064229939d714bd85ba15fd7a6355f37d0647` extends the already-existing Publisher-return discriminator to exactly two permitted owners and preserves the actual owner string for fail-closed validation.
- Both owner paths reuse the same reverse payload, transport intent, receipt chain, carrier binding, ingress receipt namespace, dispatcher, TV/TVC credential boundary, and GitHub runtime authority `NONE`.
- For `StegVerse-org/StegVerse-SDK`, the existing consumer validates the reverse transport and recovers continuity only from the verified carried state: original admitted manifest from `roundtrip_binding.sdk_processor_state.manifest`, original `manifest_receipt_id` from `sdk_processor_state.processor_result.manifest_receipt_id`, exact Publisher artifact-return bytes from the reverse payload, and original `stegverse.sdk.downstream-completion-capsule/v1` from the verified MIR binding.
- The SDK-owner branch then invokes only the already-merged local `StegVerse-SDK` `materialize_publisher_return_binding()` seam. Successful exact materialization may represent only `sdk_return_binding_observed=true`; all later predicates remain false.
- Exact head `679584c5b22409228143a15d9b114008970ae2ec` passed organization control-plane validation, Heartbeat validation, and the complete deterministic repository suite before PR #1905 merged.
- Canonical registry reconciliation merged as `e95c30099d7c88a2757b96005ab75df74da0e973`.

These are source/build facts only. They do not prove that an authentic same-execution MIR Publisher return has traversed the repaired carrier after the source merges.

## First missing runtime transition

```text
transition: OBSERVE_OR_MATERIALIZE_AUTHENTIC_PREDECESSOR_SDK_RETURN_INPUT_THROUGH_EXISTING_AUTHORIZED_CARRIER
owner: StegVerse-org/StegVerse-SDK / existing authorized resident carrier
required_input: authentic same-execution verified MIR Publisher artifact-return addressed to StegVerse-org/StegVerse-SDK
required_continuity:
  original admitted manifest
  authentic manifest_receipt_id
  exact Publisher artifact-return bytes
  original SDK downstream completion capsule
materialization_surface: merged local materialize_publisher_return_binding()
required_output_schema: stegverse.sdk.publisher-return-binding/v1
required_state: READY_FOR_FINAL_STEGVERSE_EGRESS_TRANSITION
authentic_predecessor_sdk_return_input_observed: false
sdk_return_runtime_observed: false
```

No equivalent inputs may be reconstructed, invented, or synthesized merely because the source path can now consume them.

## Runtime predicates not established

```text
authentic predecessor SDK return input observed: false
SDK return materialization observed in authentic resident execution: false
live exact SDK return consumed by RTC-STEGVERSE-EGRESS-007: false
final StegVerse-side egress transition observed: false
authentic Interlock/InTr egress observed: false
far-side final transition/caller receipt observed: false
governed return record durably recorded: false
final allowed transport-exit transition observed: false
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED: false
authentic external MIR endpoint substitution observed: false
communication_complete: false
```

## Transport terminal boundary

Transport is complete only after all three terminal predicates are authentic:

```text
RETURN_RECORD_RECEIVED = true
RETURN_RECORD_DURABLY_RECORDED = true
FINAL_ALLOWED_TRANSPORT_EXIT_TRANSITION_OBSERVED = true
```

Only then may:

```text
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED = true
TRANSPORT_SUBPROBLEM = COMPLETE
```

Master Records ingress, reconstruction, mirroring, reconciliation, persistence, projection, measurement, or any later downstream action occurs after that boundary and cannot retroactively rewrite transport truth.

## Preserved authority boundaries

- GitHub Actions is validation/evidence transport only; runtime authority is `NONE`.
- TV/TVC retains credential authority where required.
- Publisher return routing only selects the verified next owner.
- The shared Publisher-return ingress validates and dispatches the already-selected owner; it grants no execution or transport authority.
- SDK materialization has exact-byte retention/assembly authority only and does not grant egress or runtime provenance.
- LLM Adapter owns protocol/framing and the applicable final StegVerse-side framework transition only.
- Interlock/InTr owns governed admission and state transitions.
- MIR owns authentic external MIR semantics/provenance.
- Site remains a coordination/public mirror and is not runtime or transition authority.

## README review

The Site `README.md` remains adequate. This reconciliation records source connectivity in another repository and does not alter Site runtime semantics, so no README byte change is required.

## Next bounded transition

Continue only `OBSERVE_OR_MATERIALIZE_AUTHENTIC_PREDECESSOR_SDK_RETURN_INPUT_THROUGH_EXISTING_AUTHORIZED_CARRIER` against the repaired source chain. Inspect authorized resident/carrier outputs produced after merge `61d064229939d714bd85ba15fd7a6355f37d0647`. If an authentic same-execution SDK-owned MIR Publisher return is present and all four continuity inputs are authentic and consistent, allow the merged consumer to invoke only the existing SDK materialization seam and bind the exact output path/hash/schema/state. Only then may `EXECUTE_OR_CLASSIFY_REUSED_RTC_STEGVERSE-EGRESS-007` advance.

If no authentic resident execution is observable, do not synthesize evidence. Classify the exact missing state transition in the resident execution/event path instead.

## Completion boundary

This Goal remains ACTIVE. The source delivery chain through SDK return materialization is now connected and validated, but runtime execution through that chain is not yet observed. Transport success and communication completion remain false until their independent terminal predicates are authentically satisfied.
