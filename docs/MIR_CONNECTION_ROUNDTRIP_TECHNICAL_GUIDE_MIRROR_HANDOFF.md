# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Site PR: `StegVerse-Labs/Site#1278`
Merged commit: `383dadb8cfa5b86012ecfbf7ea6026a8ce80b4e3`
Status: `SOURCE COMPLETE / MERGED; RUNTIME VERIFICATION SEPARATE`

## Goal

Maintain an independent technical document describing the process, techniques, state model, authority boundaries, transport bindings, response correlation, evidence requirements, and failure/retry behavior used to establish and verify bidirectional StegVerse <-> MIR communication.

This goal is independent of any individual MIR test or experiment. Tests may instantiate the architecture, but they do not define it.

## Canonical architecture

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
- Universal Interlock/InTr: transport/admission/transition coordination according to the installed profile; not governance or historical authority.
- TV/TVC: credential custody and bounded provider-operation brokerage when authenticated provider operations are required.
- Site: documentation, projection, packet intake/initiation surfaces only.
- Heartbeat: observability/carrier only.
- GitHub Actions: source validation/evidence transport only; runtime authority `NONE`.

## Merged implementation evidence

PR #1278 merged the standalone guide, this handoff, and the exact Site pre-work claim at commit `383dadb8cfa5b86012ecfbf7ea6026a8ce80b4e3`.

Exact validated PR head: `ee3cf14289d0204a5e3f489331b1db936502e5ad`.

Validation results:

- Site Handoff Orchestrator run `34707793691`: `SUCCESS`.
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority run `34707793605`: `SUCCESS`.
- Ecosystem Heartbeat Orchestration run `34707793607`: `SUCCESS`.

The earlier Bootstrap failure was caused by a missing required Site pre-work claim. The claim was added and the repaired exact head passed all three gates. No transport, runtime, authority, or credential semantics were weakened to obtain the pass.

## Discoverability

The primary guide is on Site `main` and is indexed by `docs/MIR_CONNECTION_DOCUMENTATION_INDEX.md`, which also points to the generic Interlock/InTr guide and the MIR-specific return handoff.

## Completion boundary

The documentation task is source-complete when the standalone guide is merged, validated, and discoverable from Site documentation. That boundary is now satisfied.

This completion does **not** claim:

- a live MIR connection has executed;
- an authentic MIR provider session has occurred;
- a packet has completed an end-to-end round trip;
- an SDK delta or reconstruction has been observed.

Those are runtime predicates owned by their respective execution tasks.

## Next use

Future MIR tests, integrations, and provider operations should reference `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md` as the normative connection procedure. Test-specific documents may add packet classes, fixtures, response classes, or acceptance criteria, but must not redefine the underlying transport, authority, credential, correlation, retry, or evidence model.
