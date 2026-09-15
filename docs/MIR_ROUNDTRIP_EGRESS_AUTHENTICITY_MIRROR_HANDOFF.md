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
Reusable egress source merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / CHECKED_OUT / PROTOCOL RECONCILED / FIRST IMPLEMENTATION CONTRADICTION IDENTIFIED`

## Defining protocol sources

This Goal is governed by the already-defined protocol, not by downstream handoff inference:

- `StegVerse-Labs/.github/docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`
- `StegVerse-Labs/Site/docs/INTERLOCK_INTR_CONNECTION_GUIDE.md`
- `StegVerse-Labs/Site/docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
- `StegVerse-Labs/StegOS/docs/UNIVERSAL_INTERLOCK_PROTOCOL_MIRROR_HANDOFF.md`

## Correct transport semantics

The documented path is:

```text
data event
-> MIR destination profile selected/substituted
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node intr_outbox / event materialization
-> Interlock/InTr admission
-> profile-defined MIR mirror destination materialization
-> MIR mirror destination state transition
-> destination evidence
-> governed return
```

`INGRESS_ADMITTED` is an evidence boundary. It proves transport admission only; it does not by itself prove the downstream transition. It does **not** create an architectural gap requiring a scheduler, dispatcher, resident executor, always-on application receiver, second user-operated device, or second transport plane.

The Universal Interlock contract explicitly permits bounded event-ephemeral materialization when the destination receiver is not already resident. A data event creates the transport intent; the platform must queue the exact packet or materialize bounded event-ephemeral execution as required by the installed profile.

## Endpoint substitution semantics

For this Goal:

```text
endpoint substitution = destination-profile substitution
```

The MIR mirror endpoint is StegVerse-owned and known. It is not an undiscovered external endpoint. The substituted destination profile is the mechanism that binds the governed transport to that known MIR mirror endpoint.

Therefore the prior predicate wording `authentic_external_mir_endpoint_substitution_observed` is not used as an endpoint-discovery concept. The relevant states are:

```text
MIR_MIRROR_ENDPOINT_KNOWN = true
MIR_DESTINATION_PROFILE_BOUND = runtime/source dependent
MIR_MIRROR_DESTINATION_CALLED = runtime evidence
MIR_MIRROR_FAR_SIDE_TRANSITION_OBSERVED = runtime evidence
```

## First actual implementation contradiction

The first contradiction appears **before any authentic signal can be correctly addressed**.

The defining MIR guide requires a designated/registered MIR connection profile before InTr materialization. However, the current canonical SDK completion builder emits only:

```json
{
  "final_stegverse_transition_surface": "LLM_ADAPTER",
  "transport": "INTERLOCK_INTR",
  "far_side_transition_required": true
}
```

It carries no destination/connection profile.

The current reusable LLM Adapter `RTC-STEGVERSE-EGRESS-007` implementation then constructs a generic InTr handoff containing `protocol = InTr` but no MIR destination profile. Therefore the documented MIR destination-profile substitution cannot be represented end-to-end on the current SDK -> LLM Adapter -> InTr egress contract.

This is the first protocol contradiction. It precedes questions about resident execution or missing runtime receipts.

```text
first failing documented transition:
MIR_DESTINATION_PROFILE_SELECTED_OR_SUBSTITUTED

classification:
IMPLEMENTATION_CONTRACT_INCOMPLETE

missing contract:
manifest completion.egress must preserve a designated InTr destination profile,
and RTC-STEGVERSE-EGRESS-007 must carry that exact profile into the canonical InTr handoff.
```

## What is not missing

Do not classify any of the following as the next condition:

- MIR endpoint discovery;
- independent post-InTr executor;
- scheduler;
- dispatcher;
- always-on receiver;
- resident-receiver prerequisite;
- alternate carrier;
- second runtime plane.

## Existing validated source truth

The prior source chain remains valid for the transitions it actually implements:

- SDK exact Publisher-return materialization merged in SDK PR #245 as `d7f57428cb817c5f308b7cd545bfac29ca0a817c`.
- Publisher reverse-owner routing merged in `.github` PR #1902 as `bf8a726da8688bcfbf625b82a388ae8c79080666`.
- SDK-owned reverse return ingress/materialization merged in `.github` PR #1905 as `61d064229939d714bd85ba15fd7a6355f37d0647`.
- Reusable final StegVerse-side LLM Adapter egress source merged as `7c7c43a0171360ce7ed4cc2873b29686147845ae`.

Those source merges do not establish an authentic MIR signal because the destination-profile binding required by the defining protocol is absent from the southbound contract.

## Reused downstream chain after repair

After destination-profile propagation is repaired, the intended existing chain remains:

```text
stegverse.sdk.publisher-return-binding/v1
-> RTC-STEGVERSE-EGRESS-007 carrying exact MIR destination profile
-> RTC-INTERLOCK-INTR-TRANSPORT-008
-> profile-defined MIR mirror destination materialization/state transition
-> MIR mirror destination evidence
-> governed return
-> durable return record
-> final allowed transport-exit transition
-> SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED=true
```

No additional runtime plane is authorized.

## Runtime predicates not established

```text
authentic predecessor SDK return input observed: false
MIR destination profile bound through SDK -> LLM Adapter -> InTr egress: false
final StegVerse-side egress transition observed: false
authentic Interlock/InTr egress observed: false
MIR mirror destination called: false
MIR mirror far-side transition observed: false
governed return record durably recorded: false
final allowed transport-exit transition observed: false
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED: false
communication_complete: false
```

## Authority boundaries

- GitHub Actions runtime authority: `NONE`.
- TV/TVC retains credential authority where required.
- SDK owns manifested ingress and caller-return assembly only.
- LLM Adapter owns manifest-bound protocol/framing and final StegVerse-side transition only.
- Interlock/InTr owns governed admission and transport state transitions.
- Destination profile selection does not create governance or credential authority.
- MIR owns MIR-native semantics.
- Site is documentation/coordination only.

## README review

The Site `README.md` remains adequate. This reconciliation corrects a task-specific protocol interpretation and identifies a cross-repository contract omission; no Site README byte change is required.

## Next bounded transition

Repair only the first documented contradiction:

```text
REPAIR_AND_VALIDATE_MIR_DESTINATION_PROFILE_BINDING_IN_EXISTING_SDK_TO_INTR_EGRESS_CONTRACT
```

The repair must reuse the existing SDK manifest/completion contract, existing `stegverse.sdk.publisher-return-binding/v1`, existing LLM Adapter `RTC-STEGVERSE-EGRESS-007`, and existing Universal InTr handoff. It must add/preserve a designated destination-profile field without creating another transport, endpoint-discovery layer, scheduler, dispatcher, or runtime plane.

Once exact profile propagation is source-validated, the next runtime action is to submit the governed event through that existing profile and inspect the resulting InTr admission and MIR mirror destination-transition evidence.

## Completion boundary

This Goal remains ACTIVE. No qualifying signal is claimed sent in this reconciliation. The first reason is now concrete and protocol-grounded: the current southbound SDK/LLM Adapter handoff cannot represent the MIR destination-profile substitution required by the documented protocol.
