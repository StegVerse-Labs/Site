# MIR round-trip egress authenticity mirror handoff

Updated: 2026-09-14
Goal Task ID: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Predecessor Goal Task ID: `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/.github#1891`
Canonical registry: `StegVerse-Labs/.github/data/canonical-task-records/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
SDK return predecessor merge: `StegVerse-org/StegVerse-SDK@b4927ed277c4993662f9e7e4ffd717f677ad5459`
SDK return materialization issue: `StegVerse-org/StegVerse-SDK#244`
SDK return materialization PR: `StegVerse-org/StegVerse-SDK#245`
SDK return materialization source merge: `StegVerse-org/StegVerse-SDK@d7f57428cb817c5f308b7cd545bfac29ca0a817c`
Publisher return carrier routing issue: `StegVerse-Labs/.github#1900`
Publisher return carrier routing PR: `StegVerse-Labs/.github#1902`
Publisher return carrier routing source merge: `StegVerse-Labs/.github@bf8a726da8688bcfbf625b82a388ae8c79080666`
Canonical registry reconciliation merge: `StegVerse-Labs/.github@767daab404b189df6518b4ccff0e0241d8a31b86`
Reusable egress source merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / CHECKED_OUT / SDK RETURN MATERIALIZATION SOURCE REPAIRED / PUBLISHER MIR RETURN CARRIER ROUTING REPAIRED / AUTHENTIC SDK RETURN INPUT STILL NOT OBSERVED`

## State-transition invariant

Every process step is a state transition. Owner routing, observation, exact-byte retention/materialization, egress framing, Interlock/InTr admission, governed transport transitions, far-side arrival, return receipt, durable return recording, final allowed transport-exit transition, and downstream reconstruction are distinct state transitions. Evidence for one transition must not promote another, and a downstream failure must not rewrite a completed upstream state.

## Coordination truth

The exhausted parent `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001` is `INACTIVE / CHECKED_IN` at Goal Prompt Count `20/20` and must not consume further execution prompts. Remaining downstream work is owned by this successor.

The predecessor `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001` completed source/build-test continuity and emitted the stable `stegverse.sdk.publisher-return-binding/v1` contract. That source/build-test completion does not prove live SDK runtime assembly, final egress, Interlock/InTr admission, far-side receipt, return-record durability, final transport exit, authentic MIR substitution, release/deployment, or communication completion.

## Reused downstream chain

```text
stegverse.sdk.publisher-return-binding/v1
-> RTC-STEGVERSE-EGRESS-007
-> RTC-INTERLOCK-INTR-TRANSPORT-008
-> RTC-FARSIDE-FINAL-009
-> governed return receipt and durable record
-> final allowed transport-exit transition
-> SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED=true
-> post-transport downstream domains as required
```

Do not create a MIR-specific transport, scheduler, dispatcher, listener, credential authority, governance engine, custody implementation, or second runtime plane.

## Stable input contract

The next component consumes exact canonical bytes of `stegverse.sdk.publisher-return-binding/v1` with:

- `communication_state = READY_FOR_FINAL_STEGVERSE_EGRESS_TRANSITION`;
- `sdk_return_binding_observed = true` for the SDK assembly transition represented by that artifact;
- manifest-declared final StegVerse surface `LLM_ADAPTER`;
- transport `INTERLOCK_INTR`;
- `far_side_transition_required = true`;
- `authority_effect = NONE`;
- `communication_complete = false`;
- exact continuity to the original manifest, response/correlation binding, retained packet hash, Publisher return bytes, and SDK downstream completion capsule.

## Current truth

Established:

- SDK return source/build-test merge `b4927ed277c4993662f9e7e4ffd717f677ad5459`;
- reusable LLM Adapter `RTC-STEGVERSE-EGRESS-007` source merge `7c7c43a0171360ce7ed4cc2873b29686147845ae`;
- SDK PR #245 exact-head source validation passed and the exact-byte materialization/export/retention seam merged as `d7f57428cb817c5f308b7cd545bfac29ca0a817c`;
- Publisher reverse-carrier routing defect was identified in `.github#1900`: every Publisher artifact return was previously hard-coded to `StegVerse-Labs/continuity-vault-kit`;
- `.github#1902` repaired only that existing-carrier transition: verified `stegverse.publisher.mir-roundtrip-binding/v1` returns now route to `StegVerse-org/StegVerse-SDK`, while ordinary returns continue to the KV owner;
- owner selection occurs only after canonical Publisher return verification and fails closed on authority expansion, missing observed Publisher transition, or any prematurely promoted downstream predicate;
- exact-head `6577517bff986048a801bae59c811c949037c854` passed organization control-plane validation, Heartbeat validation, and the full deterministic repository suite before squash merge `bf8a726da8688bcfbf625b82a388ae8c79080666`;
- the same validation pass exposed and repaired a pre-existing read-only GADI compatibility regression (`SOURCE_SCHEMA` alias plus returned deterministic `observation_ref`) without granting runtime or transport authority;
- canonical registry reconciliation merged as `767daab404b189df6518b4ccff0e0241d8a31b86`.

The routing repair is source/build evidence only. It does not itself prove an authentic same-execution MIR Publisher return traversed the resident carrier after the repair.

The merged SDK materialization repair remains the only allowed exact-byte retention surface for the next SDK transition. It accepts only caller-supplied original manifest, authentic manifest receipt ID, exact Publisher return bytes, and the original SDK downstream completion capsule where MIR continuity requires it. It does not infer runtime provenance or synthesize MIR provenance.

First missing runtime predicate remains:

```text
owner: StegVerse-org/StegVerse-SDK / existing authorized runtime-carrier chain
required_artifact: exact predecessor-produced stegverse.sdk.publisher-return-binding/v1 bytes
required_state: READY_FOR_FINAL_STEGVERSE_EGRESS_TRANSITION
required_binding: sdk_return_binding_observed=true with original manifest/correlation/retained-packet/Publisher continuity intact
materialization_surface: stegverse-materialize-sdk-return / publisher_return_materialization.py
carrier_source_repair_merged: true
carrier_source_repair_merge: bf8a726da8688bcfbf625b82a388ae8c79080666
authentic_predecessor_input_observed: false
```

Not established for this successor:

```text
live exact SDK return input consumed by RTC-STEGVERSE-EGRESS-007: false
final StegVerse-side egress transition observed: false
authentic Interlock/InTr egress admission observed: false
far-side final transition/caller receipt observed: false
governed return record durably recorded: false
final allowed transport-exit transition observed: false
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED: false
authentic external MIR endpoint substitution observed: false
communication_complete: false
```

## Transport terminal boundary

Transport is not complete merely because the request reached the far side. The governed return leg must be received and durably recorded, followed by the final allowed Interlock/InTr state transition that exits the transport lane.

Only when all are true:

```text
RETURN_RECORD_RECEIVED = true
RETURN_RECORD_DURABLY_RECORDED = true
FINAL_ALLOWED_TRANSPORT_EXIT_TRANSITION_OBSERVED = true
```

may the system set:

```text
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED = true
```

That transition closes the transport subproblem. Master Records ingress, reconstruction, mirroring, reconciliation, persistence, projection, measurement, or another downstream action occurs after the transport boundary and cannot retroactively convert successful transport into transport failure.

## Preserved authority and evidence boundaries

- KV preferred custody remains optional and does not become an egress prerequisite.
- No live KV/provider installation, writeback, readback, or runtime claim is made.
- No Master Records custody claim is made.
- No final egress claim is inferred from source or CI.
- GitHub Actions remains validation/evidence transport only with runtime authority `NONE`.
- Publisher return routing selects only the verified next owner and grants no downstream authority.
- The SDK materialization surface has exact-byte retention authority only; it does not grant runtime provenance or downstream transition authority.
- Interlock/InTr owns governed admission and state transitions.
- TV/TVC remains credential authority where required.
- LLM Adapter owns protocol/framing and the applicable final StegVerse-side framework transition only.
- MIR owns external MIR semantics/provenance.
- No authentic external MIR endpoint substitution is claimed from source/build evidence.

## README review

The Site `README.md` remains adequate for this bounded reconciliation. Its existing authority boundary states that Site is a public mirror, not transition, credential, receipt-generation, or runtime authority. The carrier routing repair changes no Site runtime behavior, so no README byte change is required.

## Next bounded transition

Continue only `OBSERVE_OR_MATERIALIZE_AUTHENTIC_PREDECESSOR_SDK_RETURN_INPUT_THROUGH_EXISTING_AUTHORIZED_CARRIER`.

Inspect the authorized resident/carrier outputs after merged carrier repair `bf8a726da8688bcfbf625b82a388ae8c79080666` for an authentic same-execution MIR Publisher return addressed to `StegVerse-org/StegVerse-SDK`. Require the original admitted manifest, authentic manifest receipt ID, exact Publisher artifact-return bytes, and original SDK downstream completion capsule to be present and continuity-valid. If they are present, invoke only the merged `stegverse-materialize-sdk-return` surface and bind the resulting exact output path/hash/schema/state. Do not reconstruct equivalent inputs, invent a receipt ID, infer a capsule, or synthesize authentic MIR provenance.

Only after authentic predecessor-produced exact SDK return bytes become observable may `EXECUTE_OR_CLASSIFY_REUSED_RTC_STEGVERSE_EGRESS_007` advance. Each later transition remains independently evidenced.

## Completion boundary

This goal remains ACTIVE. Source routing is repaired and validated, but authentic runtime delivery through the repaired carrier is not yet observed. `SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED` and `communication_complete` both remain false until their exact state-transition predicates are authentically satisfied.
