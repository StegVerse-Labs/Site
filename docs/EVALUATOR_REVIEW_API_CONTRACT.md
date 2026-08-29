# Evaluator Review API Contract

## Purpose

The evaluator review page is a non-authorizing client over the published StegVerse SDK evaluator-manifest lane. It may render public review data without credentials. Master Records remains custody/reconstruction authority where applicable; this client cannot mint or replace that custody.

Consequential interaction does **not** use a Site-specific transport bridge. A StegVerse runtime may provision the canonical `window.StegVerseInterlockConnector`; that connector owns Interlock admission and InTr transport. Site only constructs bounded evaluator-review requests, validates returned bindings/transport receipts, and renders the governed review projection.

```text
TV/TVC = credential/secret/token authority
SDK = evaluator-neutral manifest/demo/test client contract
StegCore = production manifold-governance evaluator
Site = non-authorizing browser presentation/client
Interlock Connector = admission boundary
InTr = transport + hop receipt
Master Records = custody/replay/reconstruction where applicable
GitHub = source/provenance only
```

## Public read model

When no Interlock Connector is provisioned, the UI may read the static same-origin JSON projection. Static projection is evidence presentation only and grants no write, approval, freeze, execution, credential, or transport authority.

## Runtime connector

The runtime MAY inject:

```js
window.StegVerseInterlockConnector = {
  authorityRef() { return "opaque-admitted-authority-ref"; },
  async transact(interlockRequest) { /* canonical Interlock + InTr */ }
}
```

Site must not implement its own provider/runtime `fetch()` transport for consequential evaluator actions. Missing connector capability fails closed.

## Browser request contract

Schema:

```text
stegverse.evaluator_review.interlock_request.v1
```

Shape:

```json
{
  "schema_version": "stegverse.evaluator_review.interlock_request.v1",
  "request_class": "EVALUATOR_REVIEW",
  "operation": "READ_REVIEW | COMMENT | REQUEST_CHANGES | APPROVE | FREEZE | EXECUTE",
  "authority_ref": "opaque admitted authority reference",
  "transport": "InTr",
  "payload": {},
  "bindings": {
    "test_id": "...",
    "revision": 4,
    "manifest_hash": "sha256 hex"
  },
  "authority_transfer": false
}
```

The browser binding is exact where an operation is revision-sensitive. The request expresses intent only; it does not grant authority and does not itself prove transport.

## Runtime response contract

Schema:

```text
stegverse.evaluator_review.interlock_response.v1
```

Required semantic shape:

```json
{
  "schema_version": "stegverse.evaluator_review.interlock_response.v1",
  "operation": "APPROVE",
  "decision": "ALLOW_BOUNDED_CONTEXT",
  "authority_effect": "NONE",
  "authority_transfer": false,
  "bindings": {
    "test_id": "...",
    "revision": 4,
    "manifest_hash": "sha256 hex"
  },
  "transport_receipts": {
    "ingress": {},
    "egress": {}
  },
  "review": {}
}
```

Site rejects operation, test, revision, or manifest-hash binding mismatches. Site also rejects any response that asserts authority transfer or a Site authority effect.

## Canonical InTr receipt requirements

Every completed governed round trip must return two distinct transport receipts under `transport_receipts`: `ingress` and `egress`. A single generic receipt is insufficient. Both receipts must use:

```text
stegverse.intr.hop_receipt/v1
boundary_verification=VERIFIED
transition_state=RECEIVED
authority_transfer=false
secret_plaintext_present=false
payload_hash=<64 lowercase hex>
receipt_hash=<64 lowercase hex>
```

For ingress the canonical adjacent browser/runtime boundary is `DEVICE_SYSTEM -> STEGOS_ECOSYSTEM`. For egress it is `STEGOS_ECOSYSTEM -> DEVICE_SYSTEM`. These roles mirror `StegOS/stegos/universal_intr_transport.py`; Site does not define an alternate role vocabulary.

The browser does not mint this receipt. The runtime Interlock/InTr path returns it after transport/admission. Source, CI, merge, or public deployment cannot substitute for a real receipt.

## Operations

The existing UI operations map to bounded Interlock operations:

```text
loadReview      -> READ_REVIEW
comment         -> COMMENT
requestChanges  -> REQUEST_CHANGES
approve         -> APPROVE
freeze          -> FREEZE
execute         -> EXECUTE
```

`COMMENT`, `REQUEST_CHANGES`, `APPROVE`, `FREEZE`, and `EXECUTE` must fail closed without the provisioned connector. `READ_REVIEW` may fall back to static public projection when no connector is available.

## Required governance invariants

- approval binds reviewer identity + exact revision + exact manifest SHA-256 + timestamp;
- evaluator identity is never a governance decision input;
- expected observation is never a governance decision input;
- any manifest mutation invalidates approvals for freeze readiness;
- freeze is unavailable unless all required approvals match the current revision/hash, no blocking change request remains, and canonical validation is PASS;
- frozen artifact is immutable for execution; amendment creates a new draft/version;
- Site never generates canonical freeze receipts, execution receipts, custody receipts, replay evidence, reconstruction evidence, or InTr receipts;
- TV/TVC remains the only credential/secret/token authority;
- SDK remains a client of canonical StegCore production governance and may not create a parallel evaluator;
- replay/reconstruction never re-executes the original consequence;
- Interlock/InTr transports admitted requests and evidence but never transfers governance authority to Site.

## Access modes

```text
PUBLIC_READ
INVITED_REVIEWER
AUTHENTICATED_APPROVER
```

The governed runtime/Interlock path, not static Site JavaScript, determines authenticated identity, admitted authority reference, and permitted action. Missing connector capability must be rendered as unavailable rather than simulated.

## Hashing

The client computes a deterministic review SHA-256 over canonicalized JSON for comparison and approval confirmation. A hash is labeled FROZEN only when the canonical review model reports state `FROZEN` and supplies the canonical frozen hash.


## Manifest / receipt report

The UI report schema is:

```text
stegverse.evaluator_review.manifest_receipt_report.v1
```

The report binds the displayed manifest, exact test id/revision/manifest hash, execution/result projection, and transport evidence into one user-reviewable object. It MUST expose ingress and egress receipts separately.

Static/public projection uses:

```text
transport.status=NOT_OBSERVED
transport.ingress_receipt=null
transport.egress_receipt=null
```

After an authenticated governed round trip has passed browser validation:

```text
transport.status=OBSERVED
transport.ingress_receipt=<verified receipt>
transport.egress_receipt=<verified receipt>
```

The report is evidence presentation. Site still does not mint either transport receipt or custody evidence.
\n\nOperational note: the response may carry an egress `FORWARDED` receipt because that event is established before the browser receives the response. A later destination acknowledgement, if implemented, is stronger delivery evidence and must remain distinct rather than being retroactively inferred.\n

## Browser connector adapter

`assets/evaluator-intr-connector.js` is the browser Interlock Connector carrier adapter. It is inert unless `window.__STEGVERSE_EVALUATOR_INTR_CONFIG__` explicitly provisions `mode=REMOTE_INTR` and an endpoint. It sends the canonical evaluator Interlock request with `X-StegVerse-Transport: InTr`, an opaque authority reference, and the SHA-256 of the exact request body. It omits browser credentials and does not grant authority. The evaluator UI itself remains transport-neutral and calls only `StegVerseInterlockConnector.transact(...)`.

For `READ_REVIEW`, the UI first loads the public projection, computes the exact manifest hash, and binds the InTr request to that test id/version/hash. The sovereign runtime must reject a mismatch instead of returning an unbound newer/different projection.
