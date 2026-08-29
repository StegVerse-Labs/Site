# Evaluator Review Interlock + InTr Connector Mirror Handoff

Updated: 2026-08-29

## Source of truth

```text
repository: StegVerse-Labs/Site
issue: #634
branch: feat/evaluator-review-intr-connector-634
claim: SITE-EVALUATOR-REVIEW-INTR-CONNECTOR-634-20260829
parent_handoff: docs/EVALUATOR_REVIEW_UI_MIRROR_HANDOFF.md
sdk_source_authority: StegVerse-org/StegVerse-SDK
production_governance_owner: StegVerse-Labs/StegCore
credential_authority: TV/TVC
transport: InTr
admission_boundary: Interlock Connector
authority_effect: NONE
activation_effect: false
```

## Goal

Correct the evaluator-review browser/runtime boundary so browser-to-SDK/demo/test interactions use the established StegVerse Interlock Connector + InTr transport architecture instead of growing `window.StegVerseEvaluatorReviewBridge` into a second transport subsystem.

## Architectural rule

```text
browser UI
  -> bounded evaluator-review Interlock request
  -> runtime-provisioned Interlock Connector
  -> InTr transport + canonical hop receipt
  -> governed runtime / SDK ingress
  -> canonical StegCore production evaluator where applicable
  -> governed result / receipt
  -> InTr return path
  -> Interlock response
  -> Site validation + presentation
```

Site remains transport-neutral and non-authorizing. It does not open a provider/runtime endpoint, hold runtime credentials, mint InTr receipts, grant approval/freeze/execution authority, reinterpret StegCore dispositions, or create custody/replay/reconstruction evidence.

## Implemented Site source

```text
assets/evaluator-review.js
  - replaces direct StegVerseEvaluatorReviewBridge lookup with StegVerseInterlockConnector
  - builds stegverse.evaluator_review.interlock_request.v1
  - maps review actions to bounded Interlock operations
  - requires opaque admitted authority_ref from the runtime connector
  - validates stegverse.evaluator_review.interlock_response.v1
  - validates canonical stegverse.intr.hop_receipt/v1 evidence
  - rejects unverified/not-received transport
  - rejects authority transfer
  - rejects plaintext-secret transport
  - rejects test/revision/manifest-hash binding mismatch
  - preserves static PUBLIC_READ fallback only

tests/evaluator-review-intr.test.cjs
  - deterministic request binding
  - valid InTr receipt acceptance
  - manifest mismatch rejection
  - authority-transfer rejection
  - unverified-boundary rejection

docs/EVALUATOR_REVIEW_API_CONTRACT.md
  - canonical Interlock/InTr browser contract
```

## Deliberate non-implementation

The Site code does not implement `fetch()` to a runtime endpoint for evaluator actions. Transport belongs to the injected canonical Interlock Connector. This prevents a new Site-specific bridge protocol from becoming a parallel transport/control plane.

## Receiving-side dependency

A corresponding governed runtime/SDK ingress must admit `EVALUATOR_REVIEW` Interlock requests, consume the InTr transport envelope, bind the exact review/test revision+hash, invoke the existing SDK/client contract and canonical StegCore production evaluator where applicable, and return canonical review/result projection plus InTr receipt evidence.

The SDK may not become credential authority or a parallel evaluator. TV/TVC and StegCore boundaries remain unchanged.

## Current completion gates

```text
pre-work collision check: COMPLETE / no open conflicting Site or SDK issue found
Site issue/claim: COMPLETE
Site branch: COMPLETE
browser Interlock request adapter: IMPLEMENTED
InTr receipt validation: IMPLEMENTED
legacy ad-hoc bridge transport dependency: REMOVED FROM evaluator-review.js
static public-read fallback: PRESERVED
deterministic source tests: IMPLEMENTED / CI NOT YET OBSERVED
API contract: UPDATED
Site merge: PENDING
public observation of corrected source: PENDING
runtime Interlock Connector provisioning: NOT CLAIMED
live InTr browser->runtime receipt: NOT OBSERVED
SDK/runtime receiving ingress: PENDING / SEPARATE LINKED LANE
approval/freeze/execution: NOT CLAIMED
activation: NOT CLAIMED
```

## Non-claims

Source implementation, validation, merge, or public observation cannot establish a live InTr event. A live browser-originated governed operation requires an actual provisioned Interlock Connector and directly inspectable InTr receipt chain.


## Manifest / receipt report requirement — 2026-08-29

The fully documented evaluator UI report MUST include transport evidence as part of the same manifest/receipt report presented to the reviewer.

Required report schema:

```text
stegverse.evaluator_review.manifest_receipt_report.v1
```

Required transport fields:

```text
transport.status
transport.ingress_receipt
transport.egress_receipt
transport.operation
transport.decision
transport.authority_effect
```

A real governed round trip is not report-complete unless both ingress and egress receipts are present, individually validated, and bound to the same test id, revision, manifest hash, and operation. A single generic receipt cannot satisfy this requirement.

Before authentic runtime evidence exists, the UI must state:

```text
transport.status=NOT_OBSERVED
transport.ingress_receipt=null
transport.egress_receipt=null
```

The report also carries the manifest, execution projection, and results projection so the reviewer can export one complete manifest/receipt record. Site presents and validates this evidence; it does not mint the receipts or assume custody authority.

Implemented surfaces:
- `evaluator-review.html`: dedicated Manifest / Receipt Report section with ingress and egress panels plus copy/export.
- `assets/evaluator-review.js`: distinct ingress/egress validation and report composition.
- `tests/evaluator-review-ui.test.cjs`: deterministic two-receipt validation, missing-egress rejection, static NOT_OBSERVED report.
- `scripts/check_evaluator_review_ui.py`: static acceptance for report presence and dual-receipt contract.
