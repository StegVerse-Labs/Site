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
\n\n## Operational egress timing correction — 2026-08-29\nIngress receipt state is `RECEIVED` at the governed runtime. Egress receipt returned with the response is `FORWARDED` unless a separately observed destination acknowledgement exists. The UI must not invent future receipt evidence.\n

## Bounded live transport observation projection — 2026-08-29

Canonical evidence owner:
`StegVerse-Labs/.github#440`

Merged evidence:
`StegVerse-Labs/.github@4c92ebb54def8afd29a18c955240ecd8892423ce`

Observed in bounded live execution:

```text
browser -> shared Gateway -> InTr -> sovereign evaluator runtime -> egress: OBSERVED_BOUNDED_LIVE_EXECUTION
authentic ingress receipt: OBSERVED_BOUNDED_LIVE_EXECUTION
authentic egress receipt: OBSERVED_BOUNDED_LIVE_EXECUTION

ingress receipt:
  EVAL-IN-ec786d5f45f0de7e24bf0d09
  DEVICE_SYSTEM -> STEGOS_ECOSYSTEM
  RECEIVED
  sha256:47349944c04dec1ea0c1fabfbf7eb1b2c1a02fae7bca5cebac822607944ad984

egress receipt:
  EVAL-OUT-097598820e03794bd150594c
  STEGOS_ECOSYSTEM -> DEVICE_SYSTEM
  FORWARDED
  prior = ingress receipt hash
  sha256:14b15dd4f65e2be0ec0b045daf8a3b57c6d15453a739544057cccb19ecd04615
```

The proof harness used a bounded Chromium execution environment and does not establish the production public route.

Still distinct and NOT OBSERVED:

```text
public production Gateway/WebPKI route: NOT OBSERVED
public deployed Site UI receiving this receipt pair from production: NOT OBSERVED
resident sovereign production-host activation: NOT OBSERVED
review/freeze/test execution authority: NOT OBSERVED
```

No Site authority or behavior is promoted by this evidence projection.


## Interaction-surface independence invariant — 2026-08-29

This evaluator lane must preserve the existing StegVerse architectural rule that presentation and interaction surfaces are replaceable projections, not sources of canonical authority.

For this lane:

```text
instruction_origin:
  canonical repository/path/revision/hash that defines the permitted action

interaction_surface:
  the currently rendered projection surface (for example stegverse.org, a native client,
  StegOS, a local/offline UI, or another admitted device/node surface)

browser_network_origin:
  optional web-only transport/security observation
  MUST NOT be treated as canonical provenance or authority
```

The causal sequence is:

```text
canonical instruction/source-of-truth
-> admissible projection onto an interaction surface
-> user/device interaction observed at that surface
-> Interlock instantiated according to the canonical instruction
-> InTr transport
-> receiving subsystem evaluates under its own canonical authority
```

Required invariants:

- `stegverse.org` is one replaceable interaction surface, not an architectural dependency.
- No hostname, browser, operating system, device class, app store, hosting provider, or third-party platform may be required to establish StegVerse authority, provenance, admissibility, or continuity.
- A surface may contribute observed context or transport-security evidence, but interaction on that surface does not make the surface the source of truth.
- Web `Origin` is a network-security fact only and is optional outside browser transports.
- The same canonical instruction must remain projectable through other admitted surfaces without changing governance semantics.
- Third-party presentation/transport mechanisms remain replaceable and must not acquire canonical authority merely by carrying or rendering the interaction.

This section narrows terminology for the current evaluator work; it does not create a new architectural doctrine or supersede existing ecosystem-wide sovereignty/platform-independence rules.


## Receipt-bound Gateway runtime projection — 2026-08-29

Issue #660 removes the remaining normal-path dependency on manually injecting a Site runtime endpoint.

The Site mirror now carries a blocked-by-default non-authorizing projection:

```text
data/evaluator-review/runtime-projection.json
schema: stegverse.site.evaluator_intr_runtime_projection/v1
state: BLOCKED
active: false
endpoint: null
```

The intended activation chain is:

```text
live sovereign shared Gateway
-> Gateway node advertisement + evaluator readiness
-> independent observer validates HTTPS route, advertisement digest, receiver liveness and authority boundary
-> projector emits fresh digest-bound Site runtime projection
-> Site connector validates projection
-> connector becomes available
-> exact manifest bootstrap/hash
-> READ_REVIEW Interlock + InTr round trip
```

Site cannot populate or widen the route from repository state. An absent, stale, malformed, authority-drifted, non-HTTPS, or non-ready projection leaves transport `NOT_PROVISIONED` and preserves static public read.

The projected hostname is an observed route fact, not an architectural dependency or source of authority. Other interaction surfaces may provide their own admitted connector/runtime projection without using this Site file.

Source implementation on this branch does not claim live Gateway observation or activate the blocked projection.
