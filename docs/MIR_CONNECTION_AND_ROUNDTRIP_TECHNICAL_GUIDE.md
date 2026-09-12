# MIR Connection and Round-Trip Communication Technical Guide

Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`

## 1. Purpose

This document defines the StegVerse technical architecture and operating procedure for establishing, transporting, receiving, correlating, verifying, retrying, and evidencing bidirectional communication with MIR.

It is an architecture and operations document. It is **not** a test plan, experiment protocol, evaluator-specific contract, or record of any particular MIR run. A test may instantiate this architecture, but no test or experiment defines the architecture.

The core design rule is:

> MIR communication must reuse StegVerse's existing bounded adapter + Universal Interlock/InTr + registered Node transport model. A MIR-specific payload, document, API operation, or response class may be added, but a second transport/runtime must not be created merely because the counterparty is MIR.

## 2. System roles and authority boundaries

### 2.1 StegVerse

StegVerse owns StegVerse governance decisions, manifested-request commitments, local state-transition evidence, comparison/delta computation, and StegVerse-side reconstruction.

A MIR response cannot create or replace a StegVerse governance decision unless an independently governed StegVerse process consumes it and makes a new governed transition.

### 2.2 MIR

MIR owns MIR-native historical/accounting semantics and source-native MIR output. StegVerse must retain MIR output without rewriting it into a StegVerse verdict.

MIR historical/accounting output is evidence received from MIR. It is not StegVerse governance authority.

### 2.3 Universal Interlock / InTr

Universal Interlock/InTr provides the reusable connection seam and transition/admission mechanism. It carries manifested transport intent, materialization identity, registered Node outbox continuity, ingress admission, and connection-state evidence according to the installed profile.

InTr does not become MIR historical authority, StegVerse governance authority, or TV/TVC credential authority.

### 2.4 Registered StegOS Node

The registered Node provides the local write-once `intr_outbox` origin used to stage a materialization request. Counterparty packets are never allowed to self-assert the Node identity or mint a Node-origin claim.

### 2.5 TV / TVC

TV/TVC owns credential custody and bounded provider-operation brokerage where an authenticated MIR provider operation is required.

MIR credentials are referenced through the TV/TVC non-exportable vault/broker path. SDK, Site, InTr, GitHub Actions, or counterparty documents do not receive raw provider credentials.

### 2.6 Site

Site may document the connection, collect or observe a source-native packet/artifact, perform packet preflight, invoke the bounded adapter, and project connection state.

Site does not gain governance, credential, historical, or runtime authority merely by handling the packet.

### 2.7 Heartbeat and GitHub Actions

Heartbeat is observability/timing/carrier only. GitHub Actions validate source/package shape and may transport evidence, but have runtime authority `NONE`.

## 3. Canonical connection model

The canonical connection model is:

```text
source-owned request or artifact
-> exact-byte/canonical-object commitment
-> bounded connection-profile adapter
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node write-once intr_outbox
-> materialization trigger
-> advertised Universal InTr ingress
-> authentic ingress receipt
-> downstream MIR- or StegVerse-owned processing
-> source-native response artifact
-> exact response correlation
-> bounded return adapter
-> Universal InTr return materialization
-> destination receiver
-> downstream receipt / comparison evidence
```

No state should be skipped merely because both ends are reachable.

## 4. Connection establishment and profile discovery

Before initiating a MIR-bound or MIR-return connection, the initiating adapter must identify the expected connection profile and the receiving side must advertise or otherwise expose the profile it can admit.

For the device-local Site ingress, profile discovery uses:

```text
GET /intr/profile
```

The current Universal InTr materialization route is:

```text
POST /intr/materialization
```

An adapter must fail closed with `BLOCKED_PROFILE_UNAVAILABLE` when the required profile is not advertised or otherwise authoritatively registered.

The existence of Universal InTr does not imply every MIR operation or response class is installed. Connection-profile availability is checked independently for each bounded operation.

## 5. Carrier choices

MIR communication may use different **source-native carriers** while preserving the same StegVerse connection architecture.

### 5.1 Shared-document or source-native artifact carrier

A shared document, exact revision, file, JSON object, signed artifact, or other source-native object may serve as the interoperability carrier when its exact content can be retained or content-addressed.

This is appropriate where the complete communication object contains structured history or information that would be distorted by flattening it into an unrelated API event vocabulary.

The carrier must provide or permit StegVerse to retain:

- exact bytes or canonical object representation;
- a stable revision/content identity where applicable;
- SHA-256 or equivalent committed digest;
- originating request/connection identifier;
- expected response class/profile;
- source-native proof/signature if one exists.

The document provider is a carrier/provider. It does not thereby become governance or historical authority.

### 5.2 Authenticated MIR provider operation

Where MIR exposes a native authenticated provider operation whose semantics exactly match the intended action, StegVerse may use the TV/TVC provider-operation broker.

The provider operation must remain bounded by the registered MIR provider profile, expected endpoint/path/method, exact request/body commitments, operation allowlist, and non-exportable credential custody.

An authenticated MIR API operation is **not** a requirement for shared-document exchange unless the applicable MIR operation itself requires it.

### 5.3 Do not force semantic translation

If an exact StegVerse history object cannot be represented without semantic loss in a MIR fixed event vocabulary, the exact object remains the carrier. Only MIR-native events whose published semantics actually match the intended event may be submitted as MIR events.

Transport convenience must never override semantic fidelity.

## 6. Outbound packet/request construction

Before a MIR-bound packet is staged, the initiating side records the response contract.

A connection request should bind at least:

```json
{
  "connection_id": "stable request/connection identity",
  "revision": 1,
  "request_class": "source-native or manifested class",
  "request_sha256": "sha256:<64 lowercase hex>",
  "expected_response_class": "MIR-native response class",
  "connection_profile": "registered profile identifier",
  "authority_boundary": {
    "stegverse_governance": "STEGVERSE",
    "mir_history_or_accounting": "MIR",
    "credential_authority": "TV/TVC"
  },
  "retry_policy": "profile-defined"
}
```

The actual source-native request/artifact remains authoritative for its content. The wrapper exists to bind identity, expected response, transport profile, and digest.

### 6.1 Required outbound checks

The adapter must:

1. retain the exact packet/artifact or an exact content-addressed reference;
2. recompute the request digest locally;
3. reject unsupported request classes;
4. reject stale or conflicting connection identifiers;
5. reject profile mismatch;
6. bind local Node/Interlock identity from the registered local state, not from the packet;
7. preserve the original source semantics unchanged;
8. build or validate the canonical Universal InTr objects;
9. stage a write-once outbox entry;
10. emit the materialization trigger only after the above checks pass.

## 7. Node outbox and Universal InTr materialization

The bounded adapter constructs or reuses:

- `stegverse.universal-intr-transport/v1`;
- `stegverse.universal-intr-materialization-request/v1`;
- `stegos.node_intr_outbox_entry.v1`;
- `stegos.node_intr_materialization_trigger.v1`.

The exact request/artifact digest must remain bound through the materialization chain.

The registered Node stages the request in write-once `intr_outbox` continuity. This state is `OUTBOX_STAGED`; it does **not** mean MIR or another receiver has accepted or processed the request.

After trigger emission, the state becomes `CONNECTION_INITIATED`. Only an authentic matching ingress receipt permits `INGRESS_ADMITTED`.

## 8. MIR processing boundary

Once a MIR-bound object has crossed the StegVerse transport/admission boundary, MIR performs MIR-owned work according to its own semantics and systems.

StegVerse must not claim:

- that MIR processed the request merely because transport was admitted;
- that a MIR result exists before a source-native result is observed;
- that a StegVerse-generated fixture is a MIR result;
- that MIR's historical/accounting output is a StegVerse governance verdict.

The connection remains `AWAITING_DOWNSTREAM_RECEIPT` until the required MIR-native downstream evidence is observed.

## 9. MIR source-native response

A MIR response may be a document revision, JSON response, signed object, exported artifact, provider-native result, or another source-owned representation.

The source-native response is retained byte-for-byte or by an exact content-addressed reference.

A normal MIR response binding includes:

```json
{
  "response_to": "original connection/request identifier",
  "revision": 1,
  "response_class": "expected MIR-native class",
  "artifact_sha256": "sha256:<64 lowercase hex>",
  "connection_profile": "expected return profile",
  "source_proof": null
}
```

The response is not trusted merely because it contains fields such as `approved`, `verified`, `connected`, `receipt`, `node_id`, `ALLOW`, or similar. Source-owned claims remain source-owned and are evaluated only according to the registered profile.

## 10. Return correlation and adapter binding

Before a MIR response is accepted for a StegVerse destination, the return adapter must bind it to the original connection.

At minimum it validates:

- the expected original connection/request identifier in `response_to`;
- a valid revision/epoch;
- the exact original request or manifested-run digest where required;
- the expected MIR response class;
- exact returned artifact bytes/content reference;
- recomputed returned artifact SHA-256;
- the intended return connection profile;
- absence of unauthorized authority-bearing fields.

The existing MIR accounting-return implementation demonstrates this pattern by preserving the source-native MIR artifact, binding it to the original request, wrapping only the transport metadata, and reusing an existing evaluator-read-review Universal InTr profile rather than inventing another MIR transport.

The same technique applies to other MIR response classes with their own bounded profile adapters.

## 11. Return transport and destination ingress

After successful response binding, the return adapter:

1. constructs/reuses canonical Universal InTr transport intent;
2. constructs/reuses the canonical materialization request;
3. stages the exact response digest into registered Node `intr_outbox` continuity;
4. emits the materialization trigger;
5. validates an authentic ingress receipt bound to the exact outbox/materialization/transport/payload identity;
6. waits for destination-specific downstream evidence.

`INGRESS_ADMITTED` proves transport admission only.

The destination's own bounded receipt is required before the relevant connection leg can be considered complete.

## 12. Round-trip correlation and verification

A round trip is verified only when the return can be correlated to the exact outbound request and the destination has observed the applicable downstream result.

### 12.1 Correlation predicates

The verifier should be able to prove:

- outbound connection/request identity;
- outbound exact content digest;
- outbound materialization/outbox identity;
- outbound ingress/admission receipt where applicable;
- MIR-native downstream artifact identity;
- `response_to` linkage to the outbound request;
- returned artifact digest;
- return materialization/outbox identity;
- return ingress receipt;
- destination downstream receipt;
- any comparison/delta output required by the application profile.

### 12.2 Delta verification

When the application requires MIR to account for or transform an input history, StegVerse may compute an explicit comparison between the original committed object and MIR's returned accounting.

A useful delta representation distinguishes:

- exact matches;
- missing entries;
- additional entries;
- reordered entries;
- changed fields/content;
- unverifiable fields.

The delta is StegVerse analysis of MIR-returned evidence. It is not a rewrite of MIR's artifact.

### 12.3 Reconstruction

Where supported, StegVerse may retain enough commitments and receipts to reconstruct the communication sequence from the original request through the returned downstream consequence.

Reconstruction success is evidence about continuity and reproducibility. It does not retroactively promote transport into governance authority.

## 13. Credential handling through TV/TVC

Authenticated provider operations use the TV/TVC bounded provider broker.

Required rules:

- credential material remains non-exportable;
- request references the registered secret/vault location rather than containing plaintext credentials;
- endpoint/path/method must match the registered MIR provider profile;
- operation must be allowlisted;
- request/test/revision/body/idempotency commitments are validated where the profile requires them;
- unsupported MIR operations fail closed;
- GitHub Actions, Site, SDK, InTr, and counterparty packets have no raw credential access.

A provider-operation receipt proves only what the provider/TVC receipt actually demonstrates. It does not automatically prove the complete shared-document round trip.

## 14. Connection state model

The reusable state vocabulary is:

| State | Meaning |
|---|---|
| `WAITING_FOR_RESPONSE_PACKET` | Request/connection exists; expected counterparty response not yet retained |
| `PACKET_ACCEPTED` | Exact source-native packet/artifact retained and hash-bound |
| `OUTBOX_STAGED` | Canonical materialization persisted into registered Node write-once outbox |
| `CONNECTION_INITIATED` | Materialization trigger emitted to selected advertised ingress |
| `INGRESS_ADMITTED` | Authentic ingress receipt validated for exact request |
| `AWAITING_DOWNSTREAM_RECEIPT` | Transport admitted; required source/destination processing result not yet evidenced |
| `CONNECTION_ESTABLISHED` | Profile-required downstream or durable relationship receipt observed and validated |
| `ROUNDTRIP_VERIFIED` | Outbound and return legs plus required correlation/comparison predicates validated |
| `BLOCKED_PROFILE_UNAVAILABLE` | Required bounded profile not installed/advertised |
| `FAIL_CLOSED` | Binding, hash, identity, authority, continuity, receipt, credential, or semantic check failed |

A UI or report must not jump directly from packet acceptance to connection establishment or round-trip verification.

## 15. Evidence model

A useful evidence package separates evidence classes instead of collapsing them into one success flag.

### 15.1 Source evidence

- adapter/profile implementation;
- deterministic tests;
- schema validation;
- source review;
- CI results.

Source evidence does not prove live MIR communication.

### 15.2 Transport evidence

- exact packet digest;
- Node outbox entry;
- materialization identity;
- trigger identity;
- authentic InTr ingress receipt.

Transport evidence does not prove MIR processing or destination consequence.

### 15.3 Provider/downstream evidence

- MIR-native response/result artifact;
- provider-use/result receipt where applicable;
- destination-specific receiver receipt.

### 15.4 Round-trip evidence

- outbound and inbound correlation chain;
- `response_to` linkage;
- exact digest continuity;
- destination downstream consequence;
- delta/reconstruction output when required.

## 16. Retry, replay and fail-closed behavior

### 16.1 Exact-packet retry

A transport retry may reuse the same packet identity only where the profile explicitly permits idempotent retry and the exact packet digest, destination/profile identity, operation identity, and continuity linkage are unchanged.

### 16.2 Mutated packet

A changed packet/artifact receives a new content identity and normally a successor revision/connection epoch. It must not silently replace an earlier committed packet.

### 16.3 Stale response

A response to a superseded request/revision must be retained as source evidence if appropriate but must fail correlation with the active request unless the profile explicitly supports late-response reconciliation.

### 16.4 Digest mismatch

Any request or response digest mismatch fails closed before materialization/admission.

### 16.5 Profile mismatch

A packet for one MIR connection profile cannot be admitted through another merely because its JSON/document shape can be parsed.

### 16.6 Ingress receipt mismatch

An ingress receipt must be bound to the exact outbox entry, materialization request, transport identity, and payload hash. Receipt mismatch fails closed.

### 16.7 Provider/authentication failure

Credential, endpoint, method, operation, idempotency, lease, or provider-profile mismatch fails closed in TV/TVC. No alternate plaintext-credential path may be introduced as a fallback.

## 17. Adding a new MIR connection profile

A new MIR connection/response type is ready only when all applicable items are satisfied:

- [ ] source-native request/response semantics are documented;
- [ ] profile ID and direction are declared;
- [ ] request and expected response classes are declared;
- [ ] exact-byte/canonical-object hashing is defined;
- [ ] response correlation fields are defined;
- [ ] local Node/Interlock identity cannot be supplied by the counterparty packet;
- [ ] Universal InTr transport/materialization objects are reused;
- [ ] registered Node write-once outbox is used;
- [ ] target ingress/profile can be discovered or authoritatively resolved;
- [ ] packet mutation fails closed;
- [ ] stale-response behavior is defined;
- [ ] retry/idempotency behavior is defined;
- [ ] source-native MIR artifact is preserved without semantic rewriting;
- [ ] credential requirements, if any, route through TV/TVC;
- [ ] authentic ingress evidence is required before `INGRESS_ADMITTED`;
- [ ] authentic downstream evidence is required before `CONNECTION_ESTABLISHED`;
- [ ] both legs plus correlation evidence are required before `ROUNDTRIP_VERIFIED`;
- [ ] CI/source validation is not represented as runtime proof.

## 18. Illustrative connection sequence

The following sequence is illustrative and does not define any specific experiment:

```text
1. StegVerse application creates source-owned request R.
2. Adapter retains R exactly and computes H(R).
3. Adapter records connection C and expected MIR response class M.
4. Adapter builds canonical Universal InTr transport/materialization objects.
5. Registered Node writes immutable outbox entry O1.
6. Trigger T1 is emitted; ingress returns receipt I1.
7. MIR observes/receives the source-native request through the agreed carrier.
8. MIR performs MIR-owned work and emits source-native artifact A.
9. Return adapter retains A exactly and computes H(A).
10. Adapter verifies A.response_to == C and response class == M.
11. Adapter builds the canonical return materialization.
12. Registered Node writes immutable outbox entry O2.
13. Trigger T2 is emitted; destination ingress returns receipt I2.
14. Destination performs its bounded work and emits receipt D.
15. Verifier correlates C, H(R), O1/I1, A/H(A), O2/I2 and D.
16. Application-specific comparison/reconstruction runs if required.
17. State may become ROUNDTRIP_VERIFIED only if all required predicates pass.
```

## 19. Relationship to existing StegVerse documentation

This guide specializes, but does not replace, the generic Site `INTERLOCK_INTR_CONNECTION_GUIDE.md`.

Implementation-specific MIR return adapters or provider profiles may define narrower packet classes, bindings, and operations. Those implementation documents must remain consistent with this architecture.

Tests and experiments may cite this guide. This guide must not depend on any test or experiment to define its normative behavior.

## 20. Operational principle

The connection is trustworthy because each system proves only the state it owns:

```text
source owns source artifact
registered Node owns outbox continuity
InTr owns transport/admission evidence
TV/TVC owns credential brokerage
MIR owns MIR-native historical/accounting output
StegVerse owns StegVerse governance and comparison
application receiver owns downstream consequence
round-trip verifier correlates these independent proofs
```

That separation is the round-trip technique. The transport can be reused across counterparties because authority is never inferred merely from message movement.