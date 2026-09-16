# MIR round-trip egress authenticity mirror handoff

Updated: 2026-09-16
Goal Task ID: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Predecessor Goal Task ID: `MIR-SDK-RETURN-ASSEMBLY-CONTINUITY-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/.github#1891`
Canonical registry: `StegVerse-Labs/.github/data/canonical-task-records/MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001.json`
Canonical route-duplication binding: `data/mir-roundtrip-egress-sv002-route-binding.v1.json`
SDK return materialization merge: `StegVerse-org/StegVerse-SDK@d7f57428cb817c5f308b7cd545bfac29ca0a817c`
Publisher return carrier-routing merge: `StegVerse-Labs/.github@bf8a726da8688bcfbf625b82a388ae8c79080666`
SDK-owned return ingress/materialization source merge: `StegVerse-Labs/.github@61d064229939d714bd85ba15fd7a6355f37d0647`
SDK destination-profile propagation merge: `StegVerse-org/StegVerse-SDK@4bf374bed1dba745099f2d0f6a0a970b687f02b0`
LLM Adapter destination-profile propagation merge: `StegVerse-org/LLM-adapter@b106b87a974a219e394b9eb5f3629814f3ec1239`
Status: `ACTIVE / CHECKED_OUT / PROVEN SV002 ROUTE DUPLICATION BOUND / MIR-SPECIFIC EVIDENCE NEXT`

## Execution-order correction

The governing instruction is now explicit and canonical:

```text
DUPLICATE THE PROVEN STEGVERSE-002 ROUTE FIRST
-> THEN ADD ONLY THE MIR-SPECIFIC BINDINGS AND NEW EVIDENCE REQUIREMENTS
```

The previously successful SV002 lane is not an unproven prerequisite to be re-established before this task may proceed. It is the validated reusable substrate.

Canonical proven mechanics:

```text
registered StegVerse Node
-> Interlock
-> InTr materialization
-> bounded invocation lease
-> EVENT_EPHEMERAL runtime
-> execution-time runtime identity
-> authority-owned continuation
-> independent Master Records reconstruction
```

Historical SV002 identities retained as evidence of that successful lane are recorded in `docs/STEGBROWSER_SV002_VALIDATED_LANE_RETEST.md` and in the route-duplication binding. Those historical identifiers do not grant present authority and are not copied as current runtime identity.

The generic Node/Interlock/InTr/lease/runtime mechanics MUST NOT be re-proved before applying the current MIR bindings. Fresh evidence is required only for the current invocation and the MIR-specific transition/result.

## Defining protocol sources

This Goal is governed by the already-defined protocol, not by downstream handoff inference:

- `StegVerse-Labs/.github/docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`
- `StegVerse-Labs/Site/docs/INTERLOCK_INTR_CONNECTION_GUIDE.md`
- `StegVerse-Labs/Site/docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
- `StegVerse-Labs/StegOS/docs/UNIVERSAL_INTERLOCK_PROTOCOL_MIRROR_HANDOFF.md`
- `StegVerse-Labs/Site/data/mir-roundtrip-egress-sv002-route-binding.v1.json`

## Correct transport semantics

```text
proven SV002 route mechanics
-> current Goal/COSV invocation binding
-> MIR destination profile selected/substituted
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> existing registered StegOS Node / event materialization semantics
-> Interlock/InTr admission
-> profile-defined MIR mirror destination materialization
-> MIR mirror destination state transition
-> destination evidence
-> Master Records reconstruction of the current final exit transition
```

That establishes the one-way duplication target. Only after that exact one-way result is observed do the additional round-trip requirements apply:

```text
governed return
-> return record durably recorded
-> final allowed transport-exit transition observed
-> SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED
-> communication_complete
```

`INGRESS_ADMITTED` is an evidence boundary. It proves transport admission only; it does not by itself prove the downstream transition. It does not create an architectural gap requiring a scheduler, dispatcher, resident executor, always-on application receiver, second user-operated device, or second transport plane.

## Endpoint substitution semantics

For this Goal:

```text
endpoint substitution = destination-profile substitution
```

The MIR mirror endpoint is StegVerse-owned and known. Canonical MIR counterpart profile:

```text
StegVerse-Labs/StegOS/config/external_counterpart_profiles/mir.json
profile_id = MIR
```

The profile is bound by `StegVerse-Labs/StegOS/stegos/mir_node_mirror.py`, which defines `EXTERNAL_SYSTEM_PROFILE = "MIR"`, `NODE_LABEL = "MIR NODE MIRROR"`, and the MIR mirror receipt/return contract.

## Source repair already complete

The complete SDK egress contract and reusable LLM Adapter final-transition handoff now preserve the designated InTr destination profile.

SDK merge:

```text
4bf374bed1dba745099f2d0f6a0a970b687f02b0
```

LLM Adapter merge:

```text
b106b87a974a219e394b9eb5f3629814f3ec1239
```

Source invariant:

```text
completion.egress.destination_profile = MIR
-> stegverse.sdk.publisher-return-binding/v1.egress.destination_profile = MIR
-> RTC-STEGVERSE-EGRESS-007 destination_profile = MIR
-> stegverse.llm-adapter.southbound-intr-egress-handoff/v1.destination_profile = MIR
```

Source validation does not establish current runtime admission or the new MIR transition.

## Duplicate-first binding

`data/mir-roundtrip-egress-sv002-route-binding.v1.json` now freezes the required order:

1. preserve the proven SV002 route mechanics;
2. do not re-prove generic route mechanics as a gate;
3. bind the current Goal/COSV and `destination_profile=MIR`;
4. execute through the existing `RTC-STEGVERSE-EGRESS-007 -> RTC-INTERLOCK-INTR-TRANSPORT-008 -> RTC-FARSIDE-FINAL-009` path;
5. retain fresh evidence for the current MIR-specific invocation only;
6. have Master Records reconstruct the current final exit transition;
7. only then add the governed-return and round-trip-completion requirements.

## Execution-surface invariant

There is no required iPhone-local, browser-local, remote-device, attached-device, or user-operated execution surface for this transition, and none is expected to appear later.

Do not introduce or investigate:

- iPhone-local `/intr/materialization` control as a prerequisite;
- browser-local execution authority;
- remote-device execution authority;
- attached-device execution authority;
- user-operated execution authority;
- a scheduler or dispatcher replacement;
- a resident-receiver prerequisite;
- another runtime or transport plane.

GitHub Actions runtime authority remains `NONE` and is not a substitute execution plane.

## Fresh predicates still required

The successful SV002 lane is established historical evidence for reusable mechanics. It does not prove this new MIR-bound event. The remaining fresh predicates are intentionally narrow:

```text
current Goal/COSV binding observed: false
MIR destination profile binding observed: false
final StegVerse-side egress transition observed: false
authentic Interlock/InTr egress observed: false
MIR mirror far-side transition observed: false
MIR destination evidence retained: false
Master Records reconstructs current final exit transition: false
```

Only after the one-way duplication above succeeds do these additional requirements become completion work:

```text
governed return received: false
return record durably recorded: false
final allowed transport-exit transition observed: false
SUCCESSFUL_DATA_TRANSPORT_ROUND_TRIP_IDENTIFIED: false
communication_complete: false
```

## Authority boundaries

- Historical SV002 receipts prove the prior successful lane only; they grant no present authority.
- GitHub Actions runtime authority: `NONE`.
- TV/TVC retains credential authority where required.
- SDK owns manifested ingress and caller-return assembly only.
- LLM Adapter owns manifest-bound protocol/framing and final StegVerse-side transition only.
- Interlock/InTr owns governed admission and transport state transitions.
- Destination profile selection does not create governance or credential authority.
- MIR owns MIR-native semantics.
- Master Records owns observed-reality custody/reconstruction, not transport authority.
- Site is documentation/coordination and route-binding source only.

## README review

A task-specific README is maintained under `docs/mir-roundtrip-egress-authenticity/README.md`. Site root README semantics remain unchanged by this duplicate-first correction.

## Next bounded transition

```text
USE data/mir-roundtrip-egress-sv002-route-binding.v1.json
-> DUPLICATE_PROVEN_SV002_ROUTE_MECHANICS
-> APPLY_CURRENT_GOAL_COSV_AND_MIR_DESTINATION_PROFILE_ONLY
-> EXECUTE_REUSED_RTC_STEGVERSE_EGRESS_007
-> OBSERVE_AUTHENTIC_RTC_INTERLOCK_INTR_TRANSPORT_008
-> OBSERVE_AUTHENTIC_RTC_FARSIDE_FINAL_009
-> RETAIN_MIR_DESTINATION_EVIDENCE
-> MASTER_RECORDS_RECONSTRUCT_CURRENT_FINAL_EXIT_TRANSITION
```

Do not insert a generic A1-A4 re-proving gate ahead of that sequence. Any fresh proof obligation must be scoped to the current MIR-bound invocation or to a genuinely new requirement added after duplication.

## Completion boundary

This Goal remains ACTIVE. The proven route is now canonically bound as the reusable substrate and the additional requirements are sequenced after duplication. No new MIR-specific runtime transition, far-side receipt, Master Records reconstruction, governed return, or completed round trip is claimed until authentic evidence exists.
