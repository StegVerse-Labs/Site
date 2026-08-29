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
  "intr_receipt": {},
  "review": {}
}
```

Site rejects operation, test, revision, or manifest-hash binding mismatches. Site also rejects any response that asserts authority transfer or a Site authority effect.

## Canonical InTr receipt requirements

Returned transport evidence must use:

```text
stegverse.intr.hop_receipt/v1
boundary_verification=VERIFIED
transition_state=RECEIVED
authority_transfer=false
secret_plaintext_present=false
payload_hash=<64 lowercase hex>
receipt_hash=<64 lowercase hex>
```

Where source/destination roles are supplied for this browser-origin hop, Site accepts `from_role=SITE` and a governed destination role of `INTERLOCK`, `SDK`, or `STEGVERSE_RUNTIME`.

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
