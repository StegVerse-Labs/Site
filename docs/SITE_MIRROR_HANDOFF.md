# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat / Ecosystem Node request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, synchronized human/governed projections, and downstream propagation path
Primary surface: ecosystem-chat.html
Usage surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Result: ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT
Manual user action required for routine repository work: false
```

## Required vertical slice

```text
real request
-> canonical governed event stream
-> synchronized conversation / governed-record / split renderers
-> governed real-provider response
-> provider usage persistence
-> authenticated provider-usage Master-Records custody
-> transition custody
-> reconstruction PASS for both chains
-> immutable adapter VERIFIED receipt with zero blockers
-> automatic Site acquisition and validation
-> Site ACTIVATION_COMPLETE
-> hash-bound downstream propagation
-> verified downstream ingestion
```

## Authoritative owners

```text
Runtime gateway, canonical event creation, canonical StegDeploy runtime, provider broker, portable-node runtime, and activation evidence: StegVerse-org/LLM-adapter
Custody and reconstruction: master-records/orchestration
Site activation and renderer projection: StegVerse-Labs/Site
Publication projection: GCAT-BCAT-Engine/Publisher
Admissibility projection: StegVerse-Labs/admissibility-wiki
Guardian projection: StegVerse-002/stegguardian-wiki
```

## Ecosystem Node synchronized dual-view requirement

The Ecosystem Node must expose three modes:

```text
conversation
governed
split
```

All modes are synchronized projections of one authoritative structure:

```text
Canonical governed event stream
├── Conversation renderer
├── Governed-record renderer
└── Split-view correlation layer
```

Neither visible pane is the source of truth. View switching must not create, remove, reorder, or mutate events. Governance may be hidden from the human-facing projection without being disabled. Correlation must use stable `event_id` values, never text matching.

Minimum canonical event:

```json
{
  "event_id": "stable-unique-id",
  "parent_event_id": null,
  "timestamp": "RFC3339",
  "actor": {},
  "event_type": "message|decision|execution|receipt|policy|evidence",
  "human_projection": {},
  "governed_projection": {},
  "policy_refs": [],
  "evidence_refs": [],
  "artifact_refs": [],
  "continuity_refs": [],
  "hash": ""
}
```

Sensitive fields must remain subject to role-based disclosure and redaction policies. Human-readable, formatted governed, and raw machine-readable output must resolve to the same canonical records. Raw records must be exportable and replayable. The design must remain extensible to technical, legal, executive, audit, and multilingual renderers.

## Initial implementation completed

Branch:

```text
feature/ecosystem-node-dual-view
```

Files changed:

```text
ecosystem-chat.html
assets/ecosystem-node-views.js
docs/ECOSYSTEM_NODE_CANONICAL_EVENT_CONTRACT.md
scripts/check_ecosystem_node_dual_view.py
docs/SITE_MIRROR_HANDOFF.md
```

Implemented behavior:

```text
Conversation, Governed record, and Split controls
One in-memory canonical event stream used by all renderers
Stable event_id correlation across panes
Governance-only decision records without conversation entries
Formatted governed inspection
Raw JSONL inspection
JSON export
JSONL export
Immutable browser event objects
Parent, evidence, artifact, policy, and continuity reference fields
Explicit preview-only authority boundary
Future disclosure, redaction, role, legal, executive, audit, and multilingual extension contract
```

## Verification status

```text
Static contract verifier added: scripts/check_ecosystem_node_dual_view.py
Required mode markers present: VERIFIED BY SOURCE INSPECTION
Required canonical fields present: VERIFIED BY SOURCE INSPECTION
Stable-ID correlation implementation present: VERIFIED BY SOURCE INSPECTION
JSON and JSONL export implementation present: VERIFIED BY SOURCE INSPECTION
Browser execution test: NOT YET OBSERVED IN CI
Accessibility interaction test: NOT YET OBSERVED IN CI
Replay validator against exported records: NOT YET IMPLEMENTED
Cryptographic canonical hash: NOT YET IMPLEMENTED; browser fixture uses non-cryptographic fnv1a32 marker
Role-based redaction engine: CONTRACTED, NOT YET IMPLEMENTED
Gateway-origin canonical events: NOT YET IMPLEMENTED
Authority effect: NONE
```

## Current verified evidence posture

```text
Canonical provider-neutral StegDeploy runtime: IMPLEMENTED and MERGED
Canonical image build and publication: VERIFIED
Published image digest: sha256:71a77c2b10762fa070f01ad2f2314b9f7989f62821e972f75f2a0991b237936e
Canonical package anonymous pull compatibility: NOT VERIFIED
Portable-node health-bound advertisement: IMPLEMENTED and MERGED
Site portable-node discovery and local runtime binding: VERIFIED
Governed gateway request with deterministic provider fallback: VERIFIED
Local transition persistence: VERIFIED
Authenticated transition custody: VERIFIED
Transition reconstruction: VERIFIED
Real governed provider response: NOT VERIFIED
Provider-usage persistence from real provider use: NOT VERIFIED
Provider-usage custody: NOT VERIFIED
Provider-usage reconstruction: NOT VERIFIED
Adapter immutable zero-blocker VERIFIED receipt: NOT OBSERVED
Site ACTIVATION_COMPLETE: NOT OBSERVED
Downstream verified ingestion: NOT OBSERVED
```

Custody and reconstruction were previously verified through `master-records/orchestration` Runtime Evidence Validation run `29865690620`, merge `421da84784888e3dc9bb98a7b2b47a1518f0eee0`, with authenticated custody `RECORDED` and reconstruction `PASS`. Provider execution remained disabled during that run.

## Remaining work

Destination `StegVerse-Labs/Site`:

```text
Run the static dual-view verifier in CI
Add browser behavior tests for all three modes and bidirectional selection
Add replay validation for JSON/JSONL exports
Implement role-based field disclosure and explicit redaction receipts
Replace preview fnv1a32 marker with validated upstream cryptographic hashes
Accept canonical events from the governed gateway instead of constructing them from DOM messages
Render attachments and generated artifacts from canonical artifact_refs
Add locale-aware multilingual renderer selection
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical governed events before rendering
Provide stable event and transition identifiers
Populate model/provider, delegation, policy, evidence, artifact, continuity, receipt, signature, quarantine, refusal, override, and recovery fields
Sign and hash canonical records
Expose replayable JSON or JSONL stream through the governed endpoint
Complete authorized real-provider and persistent endpoint activation path owned by issue #18
```

Destination `master-records/orchestration`:

```text
Custody canonical event streams and exports
Validate chain references, signatures, duplicate IDs, and replay reconstruction
Return reconstruction and disclosure-policy verification receipts
```

Downstream destinations after verified Site activation:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Next construction step

```text
1. Add the static checker to Site validation workflow.
2. Add browser tests that submit one message, switch through conversation/governed/split, and assert stable-ID bidirectional highlighting without event-count mutation.
3. Define the gateway canonical-event response envelope and adapt Site to consume it.
4. Retain browser-local event construction only as explicitly marked preview fallback.
5. Add export replay validation and role-based redaction fixtures.
6. Continue the authorized real-provider activation path through StegVerse-org/LLM-adapter issue #18.
```

## Authority boundary

```text
Site display != execution
view switching != event mutation
human projection != canonical record
formatted record != separate record
raw export != custody
browser hash marker != cryptographic proof
provider readiness != provider authorization
provider output != authority
local persistence != custody
submission != custody
pending status != activation
container publication != live deployment
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
```

## Current blocker

```text
Blocker: no repository evidence establishes an authorized real-provider HTTPS endpoint, explicit hostname allowlist, credential, model, and bounded cost policy in a persistent authorized runtime environment
Owner: StegVerse-org/LLM-adapter issue #18
Next step: produce the secret-free provider readiness status from the authorized runtime; when READY, execute one real governed provider request through the already-verified transition custody and reconstruction path and retain the first exact downstream failure
Manual user action required for routine repository work: false
```

## Release posture

No tag or release is authorized. The synchronized interface shell is an initial construction slice, not full activation. Remaining release conditions include CI/browser verification, gateway-origin canonical records, replay and redaction validation, authorized real-provider execution, provider-usage persistence and custody, provider-usage reconstruction, persistent endpoint verification, immutable zero-blocker activation receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This handoff, the feature branch, canonical mapping contract, static verifier, adapter issue #18, prior custody evidence, activation receipt paths, Site machine-readable state, and repository history preserve the continuation state without requiring this conversation.
