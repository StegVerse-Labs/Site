# MIR connection documentation index

This index is the stable Site documentation entry point for StegVerse <-> MIR connection and round-trip communication.

## Normative architecture and operations guide

- [`MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`](MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md) — independent technical procedure for connection establishment, carrier choice, outbound binding, Universal Interlock/InTr materialization, registered Node continuity, MIR processing boundaries, source-native return preservation, round-trip correlation, retry/replay, credential isolation, and evidence states.

## Reusable transport reference

- [`INTERLOCK_INTR_CONNECTION_GUIDE.md`](INTERLOCK_INTR_CONNECTION_GUIDE.md) — generic response-packet-to-connection pattern reused by MIR and other external systems.

## MIR return implementation reference

- [`MIR_INTR_SDK_RETURN_PROFILE_MIRROR_HANDOFF.md`](MIR_INTR_SDK_RETURN_PROFILE_MIRROR_HANDOFF.md) — implementation-specific MIR historical-accounting return binding into the existing SDK evaluator/read-review Universal InTr profile.

## Standalone guide handoff

- [`MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md`](MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md) — coordination/evidence record for the independent technical guide.

## Authority boundary

```text
MIR historical/accounting authority = MIR
StegVerse governance authority = STEGVERSE
Universal Interlock/InTr = transport/admission/transition coordination only
TV/TVC = credential custody and bounded provider-operation brokerage
Heartbeat = observability/carrier only
GitHub Actions runtime authority = NONE
```

Tests and experiments may instantiate the architecture described by the normative guide, but they do not define or supersede it.
