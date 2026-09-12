# MIR Connection and Round-Trip Communication Technical Guide

Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Global lifecycle contract: `StegVerse-Labs/.github/docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`

## 1. Purpose

This document defines the StegVerse technical architecture and operating procedure for establishing, transporting, receiving, correlating, processing, evidencing, presenting, returning, and completing bidirectional communication with MIR.

It is an architecture and operations document. It is not a test plan and no experiment defines the architecture.

## 2. Single permitted communication medium

For StegVerse <-> MIR communication, the only valid communication medium is the designated Universal Interlock/InTr transport protocol.

```text
StegVerse <-> MIR communication medium = DESIGNATED INTERLOCK / INTR TRANSPORT ONLY
```

The following cannot satisfy delivery, receipt, evaluation, return, connection, or round-trip predicates:

- email or Gmail;
- shared documents or Google Docs;
- PDFs or manually exchanged files;
- direct web forms;
- direct provider/API calls outside the designated InTr path;
- ad hoc sockets, hosted relays, or second runtimes;
- any out-of-band human or machine transfer.

A source-native request, MIR-native response, JSON object, signed payload, evidence package, or presentation artifact may be carried as payload through the designated Interlock/InTr path. Payload representation is not a second transport.

If an authenticated external operation is required by an installed transport profile, TV/TVC remains credential authority. Credential brokerage does not create another communication medium.

## 3. Canonical southbound lifecycle

`SOUTH` means the complete governed communication path moving toward ecosystem egress. It is not a separate processor, authority, runtime, or transport.

The complete lifecycle is:

```text
initiating entity
-> canonical SDK manifested ingress
-> admitted manifest
-> manifest-declared processing capability + bound route
-> governed processing / required internal transitions
-> designated MIR Interlock/InTr round trip when declared
-> MIR-native return + exact correlation
-> returned governed processing / reconciliation declared by manifest
-> canonical receipts/custody
-> replay/reconstruction/evidence stages when declared
-> Publisher presentation/evidence stage when presentation or evaluator evidence is declared
-> Publisher output returned to SDK
-> SDK return assembly bound to original request + initiating entity
-> applicable caller-path egress adapter
-> final StegVerse-side state transition
-> designated Interlock/InTr egress
-> far-side Interlock/InTr state transition
-> initiating entity receives manifested result/evidence projection
```

The communication is not complete merely because governance completed, Publisher rendered a package, SDK assembled a response, an adapter emitted bytes, or local Interlock/InTr egress was staged. The terminal communication transition is the authentic far-side Interlock/InTr transition bound to the same manifest/request lineage and applicable caller-side consequence.

## 4. Complete-manifest invariant

The manifest describes the complete required communication lifecycle, not merely the first processing call.

When presentation, report, or evaluator evidence is required, Publisher is an explicit manifest stage. Publisher is not post-hoc or out-of-band rendering.

The complete manifest preserves the relationship among:

- original initiating entity;
- original request/manifest identity;
- `processing.capability` and `processing.route_id`;
- all required governed internal transitions;
- designated Interlock/InTr counterparty/evaluator round trips;
- canonical custody requirements;
- replay/reconstruction requirements;
- evidence expectations;
- Publisher presentation/evidence requirements;
- SDK return projection and original-initiator binding;
- applicable final StegVerse-side egress transition;
- Interlock/InTr egress;
- far-side Interlock/InTr terminal transition.

Publisher consumes authentic retained evidence and prepares the presentation/report/evaluator package required by the manifest. Publisher does not invent evidence and does not gain governance, processing-selection, transport, or caller-routing authority.

## 5. Authority roles

### Task Registry

Work-intent and coordination truth only.

### WorkerCoordinator

Execution claim/fence authority.

### StegVerse

Owns StegVerse governance decisions, manifested processing requests, local transition evidence, and StegVerse analysis/reconstruction required by the manifest.

### MIR

Owns MIR-native historical/accounting semantics and MIR-native output.

### Interlock/InTr

Owns governed ingress/egress and transition admission. It is the exclusive StegVerse <-> MIR communication seam and the egress seam to the initiating side where applicable.

Interlock/InTr is not governance, MIR historical, Publisher, processor-selection, credential, or evidence authority.

### Registered StegOS Node

Provides write-once `intr_outbox` continuity for applicable materializations. Counterparty payloads cannot self-assert Node identity.

### TV/TVC

Owns non-exportable credential custody for authenticated operations required by installed profiles.

### Master Records

Owns observed-reality custody and reconstruction.

### SDK

Owns canonical manifested processing ingress and caller-return assembly. SDK binds Publisher output to the original request and initiating entity before southbound egress.

### Publisher

Owns only the manifest-declared presentation/evidence assembly stage. It consumes authentic retained evidence and produces the required package; it does not determine processing, governance, transport, or truth.

### LLM Adapter

For framework paths that use it, LLM Adapter is the final StegVerse-side transition surface before Interlock/InTr egress. It performs manifest-bound protocol/framing transformation only.

### Site, Heartbeat, GitHub Actions

Site documents/projects state only. Heartbeat observes only. GitHub Actions validate source/evidence only. None is an alternate communication or runtime authority.

## 6. System-wide manifest-driven processing invariant

Source identity, MIR response class, provider identity, framework identity, adapter identity, transport identity, model identity, file type, interface identity, or prior-result identity may contribute provenance/policy evidence but cannot select processing semantics.

```text
admitted manifest
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

This invariant remains in force throughout the complete southbound lifecycle.

## 7. Outbound MIR sequence

```text
manifest-declared MIR-bound payload
-> exact-byte/canonical-object commitment
-> designated MIR connection profile
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node intr_outbox
-> materialization trigger
-> authentic MIR-facing InTr ingress receipt
-> MIR-owned processing/evaluation
```

No state may be inferred from out-of-band movement or provider reachability.

## 8. Connection profile discovery and admission

Before initiating MIR-bound or MIR-return transport, the initiating side resolves the exact installed profile and the receiving side advertises or otherwise authoritatively registers that profile.

Where the current local InTr surface is used:

```text
GET /intr/profile
POST /intr/materialization
```

Unavailable or mismatched profiles fail closed as `BLOCKED_PROFILE_UNAVAILABLE` or `FAIL_CLOSED`. There is no alternate-channel fallback.

## 9. Payload construction

At minimum the outbound binding retains:

```json
{
  "connection_id": "stable request/connection identity",
  "revision": 1,
  "request_class": "source-native or manifested class",
  "request_sha256": "sha256:<64 lowercase hex>",
  "expected_response_class": "MIR-native response class",
  "connection_profile": "registered MIR InTr profile"
}
```

The exact payload is retained or content-addressed, its digest is recomputed locally, source semantics are preserved, stale/conflicting identities are rejected, and local Node/Interlock identity comes only from registered local state.

## 10. MIR-native return

A MIR result exists only when MIR-native downstream evidence is observed after authentic MIR-facing admission.

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

The MIR response remains MIR-native and is carried back only through the designated return profile.

## 11. Return transport and StegVerse ingress

Before returned MIR data may enter StegVerse processing:

1. validate response-to/original-request relationship;
2. retain and recompute exact return hash;
3. build/validate designated return InTr transport/materialization;
4. stage applicable write-once outbox continuity;
5. emit return materialization;
6. validate authentic StegVerse-facing InTr ingress receipt;
7. construct/validate canonical `stegverse.ingress-manifest.v1` for the processing requested by the complete manifest.

`INGRESS_ADMITTED` proves transport admission only. It does not select a processor.

## 12. Returned processing, custody, replay, and reconstruction

After return admission:

```text
MIR-native payload
-> SDK manifested ingress
-> processing.capability + processing.route_id
-> installed manifest-selected processor
-> canonical receipts/custody
-> declared reconciliation/comparison/delta
-> declared replay/reconstruction/evidence stages
```

Any delta is StegVerse analysis of preserved MIR evidence, not a rewrite of MIR's artifact.

## 13. Publisher stage

Publisher is part of the same complete manifest when presentation/report/evaluator evidence is required.

Publisher receives the authentic retained evidence basis only after the prior required governed stages have produced their evidence. Publisher then prepares the requested presentation/report/evaluator evidence package while preserving source distinctions and evidence provenance.

Publisher output does not automatically start a new processing cycle. A new processing cycle exists only when a new admitted manifest explicitly requests one.

## 14. SDK return assembly

Publisher output returns to SDK as the presentation/evidence product of the same manifested communication lifecycle.

SDK must bind:

- Publisher package identity/digest or retained reference;
- original manifest/request identity;
- original initiating entity identity/correlation;
- requested caller projection;
- applicable evidence/custody references;
- egress route/adapter required by the complete manifest.

SDK return assembly is not terminal communication completion.

## 15. Framework egress and LLM Adapter

For external-framework paths using the LLM Adapter:

```text
Publisher
-> SDK return assembly
-> LLM Adapter final StegVerse-side state transition
-> designated Interlock/InTr egress
-> far-side Interlock/InTr transition
-> external framework receives result
```

LLM Adapter may translate only protocol/framing required by the manifest. It may not change evidence semantics, select/substitute processing, claim evidence authority, or mark communication complete before the far-side transition.

For initiating entities that do not use LLM Adapter, the applicable manifest-bound egress surface occupies the analogous last StegVerse-side position.

## 16. Completion states

Useful states include:

| State | Meaning |
|---|---|
| `WAITING_FOR_RESPONSE_PACKET` | Outbound request exists; MIR return not yet evidenced |
| `PACKET_ACCEPTED` | Exact payload retained and hash-bound |
| `OUTBOX_STAGED` | Materialization persisted into registered outbox continuity |
| `CONNECTION_INITIATED` | Designated InTr materialization emitted |
| `INGRESS_ADMITTED` | Authentic matching InTr ingress receipt validated |
| `AWAITING_DOWNSTREAM_RECEIPT` | Transport admitted; required processing result not yet evidenced |
| `GOVERNED_PROCESSING_COMPLETE` | Applicable processing stages complete; presentation/egress may remain |
| `PUBLISHER_STAGE_COMPLETE` | Manifest-required presentation/evidence package assembled |
| `SDK_RETURN_ASSEMBLED` | Publisher/result package bound to original request/initiator |
| `STEGVERSE_EGRESS_TRANSITION_COMPLETE` | Applicable final StegVerse-side transition observed |
| `INTR_EGRESS_ADMITTED` | Authentic local Interlock/InTr egress admission observed |
| `ROUNDTRIP_VERIFIED` | MIR outbound/return correlation and required processing verified |
| `COMMUNICATION_COMPLETE` | Authentic far-side Interlock/InTr transition and required caller consequence observed |
| `BLOCKED_PROFILE_UNAVAILABLE` | Required designated profile unavailable |
| `FAIL_CLOSED` | Binding/hash/identity/authority/continuity/credential/receipt/semantic check failed |

`ROUNDTRIP_VERIFIED` and `COMMUNICATION_COMPLETE` are distinct when the complete manifest includes Publisher/caller-return/egress stages after MIR/governance processing.

## 17. Evidence model

### Source evidence

Implementation, schemas, deterministic tests, source review, CI. Source evidence does not prove runtime communication.

### MIR transport evidence

Exact payload digest, outbox/materialization identities, authentic MIR-facing and StegVerse-facing InTr receipts.

### MIR downstream evidence

MIR-native evaluation/accounting output produced after authentic transport admission.

### StegVerse processing evidence

SDK manifest receipt, capability/route resolution, processor receipts, custody, declared delta/replay/reconstruction evidence.

### Publisher evidence

Manifest-bound package identity, input evidence references, presentation/report/evaluator artifact references, and provenance showing no evidence invention.

### Southbound egress evidence

SDK original-initiator binding, applicable egress adapter transition, final StegVerse-side transition, Interlock/InTr egress receipt, far-side transition receipt, and caller-side consequence where required.

## 18. Retry and fail-closed behavior

Exact retry is allowed only where the installed profile explicitly permits idempotent retry and exact payload/profile/destination/operation/continuity bindings are unchanged.

Changed payloads receive new content identity and revision/epoch. Stale responses fail correlation unless the profile explicitly permits late reconciliation.

Digest, profile, receipt, credential, semantic, Publisher-package, initiator-binding, egress-route, or far-side transition mismatch fails closed.

There is no fallback to email, documents, files, direct API calls, or alternate transports.

## 19. Current evidence correction

A prior Google Doc/PDF/Gmail attempt was outside the designated Interlock/InTr protocol and has zero qualifying effect on MIR runtime predicates.

Current qualifying runtime state:

```text
outbound designated InTr materialization: NOT OBSERVED
MIR-facing authentic InTr ingress receipt: NOT OBSERVED
MIR evaluation over admitted payload: NOT OBSERVED
MIR designated return materialization: NOT OBSERVED
StegVerse-facing authentic return InTr ingress: NOT OBSERVED
canonical SDK manifested return processing: NOT OBSERVED
Publisher manifest stage runtime completion: NOT OBSERVED
Publisher -> SDK -> initiator binding: NOT OBSERVED
final StegVerse-side egress transition: NOT OBSERVED
far-side Interlock/InTr transition: NOT OBSERVED
roundtrip verified: FALSE
communication complete: FALSE
```

## 20. Completion rule

This guide is not complete until at least one authentic end-to-end MIR communication lifecycle is observed through the designated Interlock/InTr protocol and all applicable complete-manifest stages are evidenced:

1. outbound MIR InTr materialization and MIR-facing ingress;
2. MIR evaluation;
3. designated MIR return InTr transport;
4. StegVerse return ingress;
5. SDK manifested processing with manifest-selected route;
6. declared custody/delta/replay/reconstruction stages;
7. manifest-declared Publisher stage where required;
8. Publisher output returned to SDK and bound to original initiator;
9. applicable final StegVerse-side egress transition;
10. designated Interlock/InTr egress;
11. authentic far-side Interlock/InTr terminal transition and caller consequence;
12. guide reconciliation to observed runtime behavior.

No source merge, CI result, report rendering, SDK assembly, adapter emission, local egress staging, email, document, file, provider reachability, or other out-of-band evidence may substitute for the required authentic transitions.
