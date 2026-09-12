# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Status: `ACTIVE / HANDOFF ESTABLISHED; TECHNICAL GUIDE IN PROGRESS`

## Goal

Create an independent technical document describing the process, techniques, state model, authority boundaries, transport bindings, response correlation, evidence requirements, and failure/retry behavior used to establish and verify bidirectional StegVerse <-> MIR communication.

This goal is independent of any individual MIR test or experiment. Existing test/experiment artifacts may be cited as implementation examples, but they do not define the architecture and are not prerequisites for the guide's validity.

## Architectural baseline

Reuse the existing StegVerse connection architecture rather than inventing MIR-specific transport:

```text
source-native request/artifact
-> exact-byte/hash commitment
-> bounded profile adapter
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node write-once intr_outbox
-> /intr/materialization
-> advertised/admitted InTr ingress
-> source-native downstream processing
-> source-native response artifact
-> exact response binding/correlation
-> Universal InTr return path
-> destination receiver
-> round-trip comparison/evidence
```

Shared documents may act as the interoperability carrier when they preserve exact revision/content commitments. An API is an optional provider-specific surface, not a prerequisite for a shared-document exchange.

## Authority invariants

- MIR historical/accounting authority: MIR only.
- StegVerse governance authority: StegVerse only.
- Universal Interlock/InTr: transport/admission/transition coordination according to the installed profile; it does not become governance or historical authority.
- TV/TVC: credential custody and bounded provider-operation brokerage when authenticated provider operations are required.
- Site: documentation, projection, packet intake/initiation surfaces; no governance or credential authority.
- Heartbeat: observability/carrier only.
- GitHub Actions: source validation/evidence transport only; runtime authority NONE.

## Existing source material to reconcile

- `docs/INTERLOCK_INTR_CONNECTION_GUIDE.md`
- `docs/MIR_INTR_SDK_RETURN_PROFILE_MIRROR_HANDOFF.md`
- `assets/mir-accounting-return-v1.js`
- `intr-service-worker.js`
- TVC MIR provider profile/broker implementation in `StegVerse-Labs/TVC`
- MIR public API/changelog semantics where provider-native operations are discussed

## Required guide sections

1. Purpose and non-test scope.
2. Component/authority model.
3. Connection establishment and profile discovery.
4. Carrier choices: shared document/source-native artifact vs authenticated provider operation.
5. Outbound packet/request construction and immutable content binding.
6. Registered Node outbox and Universal InTr materialization.
7. MIR processing boundary.
8. MIR source-native response construction/observation.
9. Return correlation and adapter binding.
10. Receiver ingress and downstream completion.
11. Round-trip verification and delta/reconstruction concepts.
12. Credential handling through TV/TVC.
13. State machine and evidence model.
14. Retry, replay, stale response, mutation and fail-closed behavior.
15. Implementation/operations checklist.
16. Example sequence that is explicitly illustrative, not experiment-defining.

## Completion boundary

This task is complete only when the standalone guide is merged and discoverable from Site documentation/README. Completion of the guide does not claim that a live MIR round trip has executed.

## Next action

Create `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`, cross-link it from the general connection guide/README, validate internal consistency with the existing MIR return adapter and TVC boundaries, then merge after repository validation.