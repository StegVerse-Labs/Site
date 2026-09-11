# Interlock / InTr response-packet connection guide

Goal Task ID: `SITE-INTERLOCK-INTR-CONNECTION-DOCS-001`

## Contents

- [Purpose](#purpose)
- [Core rule](#core-rule)
- [Connection sequence](#connection-sequence)
- [Response packet responsibilities](#response-packet-responsibilities)
- [Adapter responsibilities](#adapter-responsibilities)
- [Connection state model](#connection-state-model)
- [Installed-profile discovery](#installed-profile-discovery)
- [HIL as the reference implementation](#hil-as-the-reference-implementation)
- [Shared-document and external-system use](#shared-document-and-external-system-use)
- [Authority boundaries](#authority-boundaries)
- [Failure and retry](#failure-and-retry)
- [Implementation checklist](#implementation-checklist)

## Purpose

Site is the public documentation and user-facing initiation surface for StegVerse Interlock / InTr connections. A counterparty or external system should be able to understand the same sequence that HIL already demonstrates:

```text
response packet submitted
-> exact packet accepted and content-bound
-> receiving adapter validates the packet class/profile
-> adapter builds or reuses stegverse.universal-intr-transport/v1
-> adapter builds or reuses stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node stages a write-once stegOS node outbox entry
-> InTr materialization trigger is emitted
-> installed/advertised InTr ingress validates the exact request
-> ingress receipt is retained
-> downstream receiver completes its own bounded transition
-> connection is established only when authentic downstream evidence says so
```

The response packet is therefore the **start of connection initiation**. It is not itself a governance decision, transition authorization, credential, admission receipt, or proof that the connection completed.

## Core rule

A response packet may request or continue a connection, but it must never be allowed to self-assert the receiving Node, Interlock, governance decision, or successful connection state.

```text
counterparty response packet != StegOS Node outbox origin
packet accepted != ingress admitted
InTr ingress admitted != downstream transition executed
transport receipt != governance authority
connection established != historical/governance authority transfer
```

The receiving Site/StegOS adapter is responsible for turning a valid response packet into the existing Universal InTr transport path. No counterparty packet is allowed to mint a fake `STEGOS_NODE_OUTBOX` origin.

## Connection sequence

### 1. An initial request establishes the expected connection profile

The initiating side records enough information to bind the later response:

- connection/request identifier;
- expected counterparty or participant class;
- response packet class;
- exact response fields or artifact class expected;
- desired InTr destination/profile;
- authority boundary;
- replay/retry policy.

### 2. The counterparty returns a response packet

The response packet may be a JSON object, document, binary artifact, signed response, or another manifested class. The source-native artifact remains the counterparty's object.

At minimum, the receiving adapter must be able to bind:

- the exact bytes or canonical object hash;
- the request/connection identifier being answered;
- the declared response class;
- the intended connection profile;
- the source/counterparty identity reference where the profile requires one;
- any source-native proof or signature without rewriting its meaning.

### 3. Site accepts the packet into local preflight

Site may display `PACKET_ACCEPTED` only after it can retain the exact packet or an exact content-addressed reference and recompute the expected digest. This state grants no transport, governance, or execution authority.

### 4. The receiving adapter binds the response to Universal InTr

The profile adapter constructs or reuses:

- `stegverse.universal-intr-transport/v1`;
- `stegverse.universal-intr-materialization-request/v1`;
- `stegos.node_intr_outbox_entry.v1`;
- `stegos.node_intr_materialization_trigger.v1`.

The adapter must preserve the response-packet digest through those objects. It must also bind the registered Node / Interlock locally rather than accepting those values from the counterparty.

### 5. The registered Node stages the request

A validated request is persisted to the Node's write-once `intr_outbox`. At this point Site may display `OUTBOX_STAGED`.

The outbox is durable continuity. It does not mean the ingress or receiver has accepted the request.

### 6. Submission initiates the connection attempt

The Node/adapter emits the materialization trigger to the currently installed/advertised InTr ingress. The existing device-local profile is discoverable at `/intr/profile`, and the current materialization route is `/intr/materialization` when that profile is active.

The connection attempt is event-triggered. An always-on application receiver or second user-operated device is not required by the Universal InTr profile.

### 7. Ingress returns an authentic receipt

`INGRESS_ADMITTED` may be displayed only when the ingress returns a receipt that is cryptographically/structurally bound to the exact Node outbox entry, materialization request, transport identity, and payload hash.

Ingress admission is still transport admission only. It does not prove a downstream consequence executed.

### 8. The downstream receiver finishes its own bounded work

A connection reaches `CONNECTION_ESTABLISHED` only when the applicable connection profile produces its required authentic receiver/downstream receipt or equivalent retained state transition evidence.

For profiles whose purpose is a persistent relationship rather than one transaction, the connection-specific adapter defines the durable relationship receipt and reconnection semantics.

## Response packet responsibilities

The response packet should carry source-owned facts, not StegVerse authority claims. A portable response packet normally includes or references:

```json
{
  "response_to": "connection/request identifier",
  "response_class": "source-native class",
  "connection_profile": "profile expected by the receiver",
  "payload_ref": "content-addressed or local retained reference",
  "payload_sha256": "sha256:<64 lowercase hex>",
  "counterparty_ref": "opaque/source-native identity reference",
  "source_proof": null
}
```

This is documentation-level metadata, not a replacement transport schema. The canonical transport remains `stegverse.universal-intr-transport/v1`.

A response packet must not be accepted as authoritative merely because it contains fields named `node_id`, `interlock_id`, `ALLOW`, `admitted`, `connected`, `receipt`, `credential`, or similar. Those states are established only by the systems that own them.

## Adapter responsibilities

Each connection profile needs a bounded adapter. The adapter is the point where source-native packet semantics are mapped into the existing InTr transport without erasing source ownership.

The adapter must:

1. validate the response packet against the expected request/connection;
2. hash the exact packet/artifact;
3. reject packet substitution, stale request identifiers, profile mismatch, or unsupported payload class;
4. read the local registered Node/Interlock identity rather than trusting the packet to supply it;
5. build or validate the canonical Universal InTr transport intent;
6. build or validate the canonical materialization request;
7. persist a write-once Node outbox entry;
8. emit the materialization trigger to an installed/advertised profile;
9. retain the exact ingress response/receipt;
10. wait for profile-specific downstream evidence before reporting `CONNECTION_ESTABLISHED`.

The adapter may be provider- or system-specific. InTr is not.

## Connection state model

| State | Meaning | Authority implication |
|---|---|---|
| `WAITING_FOR_RESPONSE_PACKET` | Initial request exists; no response packet retained | None |
| `PACKET_ACCEPTED` | Exact response packet/artifact retained and hash-bound | None |
| `OUTBOX_STAGED` | Canonical request persisted to registered Node `intr_outbox` | None |
| `CONNECTION_INITIATED` | Trigger emitted to the selected installed/advertised InTr ingress | None |
| `INGRESS_ADMITTED` | Authentic ingress receipt validated for the exact request | Transport admission only |
| `AWAITING_DOWNSTREAM_RECEIPT` | Ingress admitted; profile-specific receiver completion not yet observed | None beyond observed ingress admission |
| `CONNECTION_ESTABLISHED` | Profile-required downstream/relationship receipt observed and validated | Only the authority defined by that profile; never a blanket transfer |
| `BLOCKED_PROFILE_UNAVAILABLE` | Requested profile is not installed/advertised | None |
| `FAIL_CLOSED` | Packet, hash, profile, binding, receipt, or continuity check failed | None |

UI and documentation must not skip directly from `PACKET_ACCEPTED` to `CONNECTION_ESTABLISHED`.

## Installed-profile discovery

Site's device-local Universal InTr ingress publishes a discovery document at:

```text
GET /intr/profile
```

Current profile semantics include:

```text
schema = stegverse.universal-intr-profiled-ingress/v1
protocol = InTr
materialization_path = /intr/materialization
runtime_owner = REGISTERED_STEGVERSE_NODE
event_triggered = true
always_on_application_receiver_required = false
second_user_device_required = false
credential_authority = TV/TVC
execution_authority = NONE
```

The discovery response advertises its currently supported profiles. A connection adapter must fail closed with `BLOCKED_PROFILE_UNAVAILABLE` if the target profile is not advertised. Documentation must not imply that the existence of `/intr/profile` means every external system/profile is already implemented.

## HIL as the reference implementation

HIL is the concrete working reference for this pattern.

The HIL flow:

```text
participant response PDF selected
-> exact PDF hash + provenance retained
-> HIL adapter builds stegverse.universal-intr-transport/v1
-> HIL adapter builds stegverse.universal-intr-materialization-request/v1
-> packet is staged into registered Node intr_outbox
-> HIL InTr sync discovers device-local /intr/profile
-> trigger is POSTed to /intr/materialization
-> stegverse.hil-intr-materialization-ingress/v1 receipt is validated
-> later HIL custody/TVC steps remain separately evidenced
```

Relevant implementation surfaces:

- `humans-as-interoperability-layer.html`
- `hil-receipt.html`
- `stegos-node/stegos-node-impl.js`
- `stegos-node/hil-intr-sync.js`
- `intr-service-worker.js`
- `docs/HIL_SITE_MIRROR_HANDOFF.md`

The general Interlock/InTr documentation should remain aligned with this proven sequence rather than inventing a second transport.

## Shared-document and external-system use

A shared document can be the response artifact and interoperability carrier. The document provider does not need to become the governance or historical authority.

Example:

```text
external system sees shared request/document state
-> external system produces response artifact or exact revision
-> response packet references/hash-binds that artifact
-> receiving Site adapter accepts exact response packet
-> registered Node stages Universal InTr request
-> trigger initiates the connection attempt
-> receiving profile admits or fails closed
-> downstream systems retain their own governance/history/provenance according to role
```

The same pattern applies to MIR, SDK evaluators, KV adapters, social/provider adapters, or another system once an appropriate profile adapter exists. The connection docs describe the reusable InTr seam; they do not make every profile active merely by documenting it.

## Authority boundaries

The following invariants are mandatory:

```text
Site documentation/projection authority = NONE
response packet authority = NONE unless independently defined by source system and separately verified
Universal InTr transport authority = transport/admission only
Heartbeat authority = NONE_CARRIER_ONLY
credential authority = TV/TVC
Interlock/InTr transition authority = governed by the installed profile and current admission path
GitHub Actions runtime authority = NONE
```

A response packet must never mint a WorkerCoordinator claim/fence, credential, Node registration, governance verdict, or historical-custody assertion.

## Failure and retry

Exact-packet transport retry is allowed when the profile permits it. Blind consequence retry is not.

A retry must preserve:

- packet/payload hash;
- request/operation identity where the profile requires continuity;
- destination/profile identity;
- prior transport receipt linkage;
- authority boundaries.

A changed response packet creates a new packet identity and, where applicable, a successor connection/review epoch. It is never silently substituted into the old attempt.

## Implementation checklist

A new Site connection adapter is ready for use only when all applicable items are evidenced:

- [ ] public Site documentation names the connection profile and response packet class;
- [ ] exact response packet/artifact digest is retained;
- [ ] packet cannot self-assert Node/Interlock identity;
- [ ] adapter reuses `stegverse.universal-intr-transport/v1`;
- [ ] adapter reuses `stegverse.universal-intr-materialization-request/v1`;
- [ ] registered Node outbox is write-once for the materialization identity;
- [ ] `/intr/profile` advertises the target profile before connection initiation;
- [ ] trigger is bound to the exact outbox entry;
- [ ] ingress receipt is validated before `INGRESS_ADMITTED` is shown;
- [ ] downstream evidence is required before `CONNECTION_ESTABLISHED` is shown;
- [ ] exact-packet retry is defined;
- [ ] packet mutation fails closed;
- [ ] no Site, Heartbeat, CI, packet, or transport artifact is promoted into governance/credential authority.
