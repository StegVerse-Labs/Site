# MIR Connection and Round-Trip Communication Technical Guide

Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`

## 1. Purpose

This document defines the StegVerse technical architecture and operating procedure for establishing, transporting, receiving, correlating, verifying, retrying, and evidencing bidirectional communication with MIR.

It is an architecture and operations document. It is not a test plan and no experiment defines the architecture.

## 2. Single permitted communication medium

For StegVerse <-> MIR communication, the only valid communication medium is the designated Universal Interlock/InTr transport protocol.

```text
StegVerse <-> MIR communication medium = DESIGNATED INTERLOCK / INTR TRANSPORT ONLY
```

The following are not valid StegVerse <-> MIR communication channels and cannot satisfy delivery, receipt, evaluation, return, connection, or round-trip predicates:

- email or Gmail;
- shared documents or Google Docs;
- PDFs or manually exchanged files;
- direct web forms;
- direct provider/API calls outside the designated InTr path;
- ad hoc sockets, hosted relays, or second runtimes;
- any out-of-band human or machine transfer.

A source-native request, MIR-native response, JSON object, signed payload, or other artifact may be carried as the payload of the designated Interlock/InTr transport. Its representation is payload semantics, not a second transport.

If an authenticated external operation is required as part of the installed MIR transport profile, TV/TVC remains credential authority. Credential brokerage does not create another communication medium.

## 3. Authority boundaries

### StegVerse

StegVerse owns StegVerse governance decisions, manifested processing requests, local state-transition evidence, comparison/delta computation when requested, and StegVerse-side reconstruction.

### MIR

MIR owns MIR-native historical/accounting semantics and MIR-native output. StegVerse preserves MIR output without rewriting it into a StegVerse verdict.

### Universal Interlock/InTr

Universal Interlock/InTr is the exclusive StegVerse <-> MIR transport/admission/transition seam. It carries the request and return payloads through registered profiles and binds transport/materialization continuity.

InTr is not governance authority, MIR historical authority, credential authority, or processor-selection authority.

### Registered StegOS Node

The registered Node provides write-once `intr_outbox` continuity for outbound and return materializations. Counterparty payloads cannot self-assert Node identity.

### TV/TVC

TV/TVC owns non-exportable credential custody for any authenticated operation required by the designated transport profile. No raw MIR credential is exposed to Site, SDK, GitHub Actions, documents, or payloads.

### SDK

The SDK is the canonical StegVerse manifested processing ingress after the MIR return has been admitted through the designated return transport. The admitted manifest selects processing through `processing.capability` + `processing.route_id` bound to an installed admissible route.

### Site, Heartbeat, GitHub Actions

Site documents/projects state only. Heartbeat observes only. GitHub Actions validate source/evidence only. None of them is an alternate MIR communication channel or runtime authority.

## 4. Canonical outbound and return sequence

```text
StegVerse source-native request/artifact
-> exact-byte/canonical-object commitment
-> designated MIR connection profile
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node write-once intr_outbox
-> materialization trigger
-> authentic MIR-facing InTr ingress receipt
-> MIR-owned processing/evaluation
-> MIR-native response payload
-> designated MIR return profile
-> exact response binding/correlation
-> canonical return transport/materialization
-> registered StegOS Node return intr_outbox continuity
-> authentic StegVerse-facing InTr ingress receipt
-> StegVerse canonical SDK manifest ingress
-> admitted stegverse.ingress-manifest.v1
-> processing.capability + processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
-> canonical receipts/custody
-> requested comparison/delta/reconstruction when applicable
```

No step may be replaced by email, file sharing, shared-document exchange, direct API invocation, or another transport.

## 5. Connection profile discovery and admission

Before initiating a MIR-bound or MIR-return connection, the initiating side must resolve the exact installed profile and the receiving side must advertise or otherwise authoritatively register that profile.

Where the current local InTr surface is used, profile discovery and materialization are represented by:

```text
GET /intr/profile
POST /intr/materialization
```

The adapter fails closed with `BLOCKED_PROFILE_UNAVAILABLE` when the required profile cannot be authoritatively resolved.

The existence of Universal InTr does not imply that every MIR request or response class is installed. Each bounded operation requires an installed profile.

## 6. Payload construction

Before staging the outbound payload, the initiating side binds at minimum:

```json
{
  "connection_id": "stable request/connection identity",
  "revision": 1,
  "request_class": "source-native or manifested class",
  "request_sha256": "sha256:<64 lowercase hex>",
  "expected_response_class": "MIR-native response class",
  "connection_profile": "registered MIR InTr profile",
  "authority_boundary": {
    "stegverse_governance": "STEGVERSE",
    "mir_history_or_accounting": "MIR",
    "credential_authority": "TV/TVC"
  }
}
```

Required outbound checks:

1. retain exact payload bytes or canonical object;
2. recompute the request digest locally;
3. reject unsupported request classes;
4. reject stale/conflicting connection identities;
5. reject profile mismatch;
6. bind Node/Interlock identity from registered local state, never from the payload;
7. preserve source semantics;
8. construct or validate canonical InTr transport/materialization objects;
9. stage a write-once outbox entry;
10. emit materialization only after all checks pass.

## 7. Outbound transport states

`PACKET_ACCEPTED` means the exact payload is retained and hash-bound.

`OUTBOX_STAGED` means canonical materialization is persisted into registered Node continuity.

`CONNECTION_INITIATED` means the materialization trigger was emitted through the designated profile.

`INGRESS_ADMITTED` requires an authentic matching MIR-facing InTr ingress receipt bound to the exact payload/materialization/transport identity.

None of these states may be inferred from out-of-band delivery or provider reachability.

## 8. MIR processing boundary

Once the exact payload has been authentically admitted through the designated MIR InTr profile, MIR performs MIR-owned evaluation/accounting according to MIR semantics.

StegVerse must not claim MIR processing merely because the outbound transport was staged or admitted. A MIR result exists only when MIR-native downstream evidence is observed through the designated connection.

The connection remains `AWAITING_DOWNSTREAM_RECEIPT` until that evidence exists.

## 9. MIR-native return payload

The MIR return remains MIR-native. It is carried back only through the designated MIR Interlock/InTr return profile.

A normal return binding includes:

```json
{
  "response_to": "original connection/request identifier",
  "revision": 1,
  "response_class": "expected MIR-native class",
  "artifact_sha256": "sha256:<64 lowercase hex>",
  "return_profile": "registered MIR return profile"
}
```

The return is not trusted merely because it contains fields such as `approved`, `verified`, `connected`, `receipt`, `ALLOW`, or similar. Exact source, response, transport, and hash bindings must validate.

## 10. Return transport and StegVerse ingress

Before the return may enter StegVerse processing:

1. validate the MIR-native response against the original `connection_id`/`response_to` relationship;
2. retain and recompute the exact response hash;
3. build/validate the designated return InTr transport and materialization;
4. stage the return in registered Node write-once outbox continuity;
5. emit the return materialization trigger;
6. validate the authentic StegVerse-facing InTr ingress receipt;
7. only then construct/validate canonical `stegverse.ingress-manifest.v1` for requested StegVerse processing.

`INGRESS_ADMITTED` proves transport admission only. It does not select a processor.

## 11. System-wide manifest-driven processing invariant

After return transport admission, the MIR payload is processed according to the same StegVerse invariant as every other admitted input:

```text
admitted payload
-> canonical SDK manifest ingress
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

MIR identity, response class, provider identity, adapter identity, transport identity, file type, or prior result may contribute provenance/policy evidence, but none may independently select processing semantics.

For one test, a manifest may request evidence reconciliation, comparison/delta, governance, or another installed capability. That is a property of the admitted manifest, not of MIR identity.

## 12. Round-trip verification

A round trip is verified only when the complete designated transport chain is evidenced.

Required correlation evidence includes:

- outbound connection/request identity;
- outbound exact payload digest;
- outbound Node outbox/materialization identity;
- authentic MIR-facing InTr ingress receipt;
- MIR-native evaluation/result identity;
- `response_to` binding;
- exact MIR return payload digest;
- return Node outbox/materialization identity;
- authentic StegVerse-facing InTr ingress receipt;
- canonical SDK manifest receipt for requested StegVerse processing;
- manifest-declared capability/route resolution;
- applicable downstream processor receipt;
- comparison/delta/reconstruction evidence when the manifest requests it.

## 13. Delta and reconstruction

When the admitted manifest requests comparison/reconciliation, the processor may classify:

- exact matches;
- missing entries;
- additional entries;
- reordered entries;
- changed fields/content;
- unsupported or semantically non-representable fields;
- unverifiable fields.

The MIR-native artifact remains intact. The delta is StegVerse analysis of returned evidence, not a rewrite of MIR's artifact.

Where supported, reconstruction retains enough exact commitments and receipts to reproduce the communication sequence from the original outbound payload through the return consequence.

## 14. Credential handling

Any authenticated operation used by the installed MIR transport profile must use TV/TVC bounded credential brokerage.

Rules:

- credentials remain non-exportable;
- no plaintext credential is placed in payloads, GitHub, Site, SDK, or logs;
- endpoint/method/operation must match the registered profile;
- unsupported operations fail closed;
- credential success does not itself prove MIR communication or round-trip completion.

## 15. State model

| State | Meaning |
|---|---|
| `WAITING_FOR_RESPONSE_PACKET` | Outbound request exists; MIR return not yet evidenced |
| `PACKET_ACCEPTED` | Exact outbound payload retained and hash-bound |
| `OUTBOX_STAGED` | Canonical outbound materialization persisted into registered Node outbox |
| `CONNECTION_INITIATED` | Designated InTr materialization trigger emitted |
| `INGRESS_ADMITTED` | Authentic matching InTr ingress receipt validated |
| `AWAITING_DOWNSTREAM_RECEIPT` | Transport admitted; MIR or downstream result not yet evidenced |
| `CONNECTION_ESTABLISHED` | Profile-required downstream relationship/result receipt observed |
| `ROUNDTRIP_VERIFIED` | Outbound and return InTr legs plus required correlation and downstream predicates validated |
| `BLOCKED_PROFILE_UNAVAILABLE` | Required designated profile unavailable |
| `FAIL_CLOSED` | Binding, hash, identity, authority, continuity, credential, receipt, or semantic check failed |

A UI or report must not jump from payload creation or out-of-band delivery to connection establishment or round-trip verification.

## 16. Evidence classes

### Source evidence

Implementation, tests, schemas, source review, CI. Source evidence does not prove live MIR communication.

### Transport evidence

Exact payload digest, Node outbox entry, materialization identity, trigger identity, authentic outbound/return InTr ingress receipts.

### MIR downstream evidence

MIR-native evaluation/accounting result produced after designated transport admission.

### StegVerse downstream evidence

SDK manifest ingress receipt, manifest capability/route resolution, selected processor receipt, and requested custody/delta/reconstruction artifacts.

Only the designated InTr transport chain can satisfy the transport portions of the evidence model.

## 17. Retry and fail-closed behavior

An exact retry may reuse a connection identity only when the registered profile permits idempotent retry and the payload digest, profile, destination, operation identity, and continuity linkage are unchanged.

A changed payload receives a new content identity and successor revision/epoch.

A stale response fails correlation unless the installed profile explicitly supports late-response reconciliation.

Digest mismatch, profile mismatch, receipt mismatch, credential mismatch, or semantic mismatch fails closed.

There is no fallback to email, shared documents, files, direct API calls, or any alternate transport when the designated InTr profile is unavailable. The correct state is `BLOCKED_PROFILE_UNAVAILABLE` or `FAIL_CLOSED`.

## 18. Adding or changing a MIR profile

A MIR connection profile is ready only when:

- request/response semantics are documented;
- exact payload hashes and correlation fields are defined;
- direction/profile identity is registered;
- Node identity cannot be supplied by counterparty payload;
- Universal InTr transport/materialization objects are reused;
- registered Node write-once outbox is used;
- authentic InTr ingress evidence is required;
- stale/retry semantics are defined;
- TV/TVC handles credentials when needed;
- canonical SDK manifest ingress follows return admission before any StegVerse processor selection;
- no alternate communication medium is present;
- source validation is not represented as runtime proof.

## 19. Current evidence correction

A prior attempt transmitted a validation packet through Google Doc/PDF/Gmail. That was outside the designated Interlock/InTr protocol and therefore has zero qualifying effect on MIR connection/runtime predicates.

It may remain archived as evidence of an incorrect attempted method, but it MUST NOT be cited as proving outbound MIR delivery, MIR receipt, MIR evaluation, MIR return, or round-trip progress.

The frozen packet content/hash may be reused only if the exact payload is submitted through the designated Interlock/InTr profile and authentic transport receipts bind that exact payload.

Current qualifying runtime state:

```text
outbound designated InTr materialization: NOT OBSERVED
MIR-facing authentic InTr ingress receipt: NOT OBSERVED
MIR evaluation over admitted payload: NOT OBSERVED
MIR designated return materialization: NOT OBSERVED
StegVerse-facing authentic return InTr ingress: NOT OBSERVED
canonical SDK manifested return processing: NOT OBSERVED
roundtrip verified: FALSE
```

## 20. Completion rule

This guide is not complete until at least one authentic end-to-end MIR round trip is observed through the designated Interlock/InTr protocol, including both transport legs, MIR-owned evaluation, exact return correlation, canonical SDK manifest ingress, manifest-selected processing where requested, and reconciliation of the guide against the observed runtime behavior.

No email, external document, shared file, direct provider operation, or other out-of-band evidence can satisfy that requirement.
