# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Reusable Task Component Model merge: `StegVerse-Labs/.github@b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`
Goal Task component profile: `StegVerse-Labs/.github/data/goal-task-transport-profiles/MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001.json`
Task Registry/component reconciliation merge: `StegVerse-Labs/.github@9f3814ebdd490229a1a939b2634e5f9be55989c2`
Site component reconciliation merge: `StegVerse-Labs/Site@d2ba5ca7809ef50dce6e1d3d0ce3c1cf49f4d0f3`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / REUSABLE COMPONENT COMPOSITION MERGED + VALIDATED / AUTHENTIC MIR RUNTIME PENDING`

## Canonical reusable composition

The Goal Task identity and COSV remain unchanged. The canonical decomposition score is `28`, requiring reuse/componentization before any additional task-specific orchestration.

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

For this goal, `RTC-INTERLOCK-INTR-TRANSPORT-008` is required three times: StegVerse -> MIR outbound, MIR -> StegVerse return, and final StegVerse -> original initiator egress. `RTC-ROUNDTRIP-003` is required once for the MIR historical/accounting request-response cycle.

## Reuse and supersession

Reuse the existing implementations and owners:

- manifest intake / processing selection: StegVerse SDK;
- MIR round trip: `RTC-ROUNDTRIP-003` + Interlock/InTr transport;
- evidence custody/reconstruction: Master Records;
- Publisher projection: Publisher;
- SDK return assembly: merged `RTC-SDK-RETURN-006` implementation;
- framework final StegVerse-side egress: merged LLM Adapter `RTC-STEGVERSE-EGRESS-007` implementation;
- packet movement/state transition: Interlock/InTr;
- credentials/provider session: TV/TVC.

Do not extend MIR-specific Publisher-to-SDK assembly, MIR-specific generic framework egress, or duplicate InTr materialization/transport code. Historical evidence remains preserved.

`callback_correlation` remains a candidate reusable family only. No new Goal Task or duplicate correlation subsystem is created; exact response-to/original-request correlation remains parameterized evidence inside `RTC-ROUNDTRIP-003` until a canonical standalone component exists.

## Authority invariants

- Task Registry: coordination only.
- WorkerCoordinator: claim/fence authority.
- Interlock/InTr: governed transition/admission authority.
- TV/TVC: credential/provider authority.
- KV/SKAP Vault: sole user-verification authority.
- StegOS devices: interchangeable transport/execution nodes, not user verifiers.
- Master Records: observed-reality custody/reconstruction.
- HeartBeat: synchronization/timing/freshness/liveness/state correlation/observability only.
- GitHub: source/evidence coordination only; runtime authority `NONE`.

No device-local user verification is required or permitted.

## Processing invariant

Source/provider/framework/adapter/device/transport identity must not select processing semantics.

```text
admitted manifest
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

## Canonical runtime truth

The generic StegOS canonical runtime lane has already been authentically proven as an application-neutral `EVENT_EPHEMERAL` lifecycle and does not require a participant/developer second machine. That proof does not prove MIR runtime visitation.

The current MIR outbound blocker is narrower and remains under existing TV/TVC authority. Canonical TVC state reports:

```text
TVC-CAPABILITY-RUNTIME-002: ACTIVE_VALIDATION_OBSERVER_HTTPS_PATH_OPTIONAL_FOR_STEGFIN_WHEN_LOCAL_UNIX_BROKER_AVAILABLE
primary_runtime_bound: false
primary_runtime_service_installed_observed: false
blocked_by: TV_TVC_AUTHORITY_OWNED_HTTPS_RUNTIME_ACTIVATION_AND_OBSERVATION
```

TVC already contains validated primary-runtime binder, service-delivery, provider-operation broker, and non-secret observer source. Do not create another MIR runtime, credential route, provider broker, relay, or observer to bypass that authority-owned boundary.

## Runtime evidence state

```text
qualifying outbound MIR transport observed: false
qualifying MIR ingress receipt observed: false
qualifying MIR evaluation observed: false
qualifying MIR return transport observed: false
qualifying StegVerse return ingress observed: false
Master Records runtime custody/readback observed: false
Publisher runtime execution observed: false
SDK runtime return binding observed: false
final StegVerse-side runtime egress transition observed: false
Interlock/InTr final egress observed: false
far-side Interlock/InTr final transition observed: false
roundtrip verified: false
```

Source construction, component reuse, CI, static compatibility, or merge status do not satisfy those predicates.

## Remaining Goal Task-specific predicates

1. authentic StegVerse outbound InTr materialization to MIR;
2. authentic MIR-facing ingress receipt;
3. authentic MIR historical/accounting evaluation over the admitted payload;
4. authentic MIR-native return through designated InTr;
5. exact response-to/original-request correlation;
6. authentic StegVerse return InTr ingress;
7. canonical SDK manifest admission and manifest-selected processing receipt;
8. Master Records custody/readback/reconstruction when requested;
9. authentic Publisher execution when declared;
10. authentic SDK runtime return binding;
11. authentic final StegVerse-side egress transition;
12. authentic Interlock/InTr final egress;
13. authentic far-side final transition/caller receipt;
14. technical guide reconciled against exact observed runtime behavior.

## Communication invariant

The designated Universal Interlock/InTr protocol is the only qualifying StegVerse <-> MIR communication medium. Email, shared documents, generic direct provider/API calls, or other out-of-band channels cannot satisfy runtime/evaluation/return predicates. TV/TVC credential brokerage may support authenticated operations but does not create an alternate communication path.

## Current source state

- Reusable Task Component Model: merged.
- Goal Task component profile/task record: merged at `9f3814ebdd490229a1a939b2634e5f9be55989c2`.
- Site component reconciliation: merged at `d2ba5ca7809ef50dce6e1d3d0ce3c1cf49f4d0f3`.
- SDK complete-manifest contract: merged.
- SDK return binding (`RTC-SDK-RETURN-006`): merged.
- LLM Adapter framework egress (`RTC-STEGVERSE-EGRESS-007`): merged.
- Generic canonical runtime lane: authentically proven application-neutral lifecycle exists.
- TVC provider-operation/binder/service-delivery/observer: source implemented and validated; authentic primary runtime binding remains unobserved.

## Next admissible work

1. Stop adding task-specific MIR transport/runtime machinery.
2. Observe the existing TV/TVC authority-owned primary provider-operation boundary when it becomes live and require the canonical non-secret READY receipt.
3. Only after that observation, execute the first MIR-specific reusable runtime composition: outbound `RTC-INTERLOCK-INTR-TRANSPORT-008` within `RTC-ROUNDTRIP-003`, using existing TV/TVC credential custody.
4. Retain authentic outbound, MIR-facing evaluation, and MIR-native return evidence before advancing to the return transport occurrence.
5. Continue component-by-component without inferring later receipts from earlier components.
6. Reconcile the guide only against exact observed runtime evidence.

## Completion boundary

This Goal Task remains `ACTIVE`. It must not become `COMPLETE` from source construction, CI, merge state, or architecture reconciliation. Completion requires the authentic end-to-end runtime evidence listed above.
