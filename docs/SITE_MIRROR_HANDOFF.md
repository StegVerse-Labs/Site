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

The Ecosystem Node exposes three modes:

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

Sensitive fields remain subject to role-based disclosure and redaction policies. Human-readable, formatted governed, and raw machine-readable output resolve to the same canonical records. Raw records are exportable and replayable. The design remains extensible to technical, legal, executive, audit, and multilingual renderers.

## Files changed

```text
ecosystem-chat.html
assets/ecosystem-node-views.js
docs/ECOSYSTEM_NODE_CANONICAL_EVENT_CONTRACT.md
data/ecosystem-node-canonical-events.fixture.json
scripts/check_ecosystem_node_dual_view.py
scripts/check_ecosystem_node_replay_and_disclosure.py
scripts/check_ecosystem_chat_application.py
docs/SITE_MIRROR_HANDOFF.md
```

## Implemented behavior

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
Replay fixture preserving order and canonical IDs across JSON and JSONL
Role-based disclosure fixture with fail-closed public redaction
Canonical application-validation binding
Explicit preview-only authority boundary
```

## Verification status

```text
Static contract verifier: BOUND INTO CANONICAL APPLICATION VALIDATION
Required mode markers: VERIFIED BY SOURCE INSPECTION
Required canonical fields: VERIFIED BY SOURCE INSPECTION
Stable-ID correlation implementation: VERIFIED BY SOURCE INSPECTION
JSON and JSONL export implementation: VERIFIED BY SOURCE INSPECTION
Replay validator against canonical JSON/JSONL fixture: IMPLEMENTED AND BOUND INTO APPLICATION VALIDATION
Duplicate event ID rejection fixture behavior: IMPLEMENTED
Unresolved parent/evidence/continuity reference rejection: IMPLEMENTED
Role-based public redaction fixture: IMPLEMENTED
Browser execution test: NOT YET OBSERVED IN CI
Accessibility interaction test: NOT YET OBSERVED IN CI
Cryptographic canonical hash: NOT YET IMPLEMENTED; browser fixture uses non-cryptographic fnv1a32 marker
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
Observe the restored canonical application validation in CI
Add browser behavior tests for all three modes and bidirectional selection
Implement runtime role selection and emitted redaction receipts
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

## Provider readiness boundary

The governed provider requires every configuration gate to pass before any network call:

```text
STEGVERSE_PROVIDER_ENABLED=true
STEGVERSE_PROVIDER_ENDPOINT uses HTTPS
endpoint hostname exists
STEGVERSE_PROVIDER_ALLOWED_HOSTS is non-empty
endpoint hostname is explicitly included in STEGVERSE_PROVIDER_ALLOWED_HOSTS
STEGVERSE_PROVIDER_TOKEN is configured
STEGVERSE_PROVIDER_MODEL is configured
cost, quota, input, and output limits pass
```

An empty hostname allowlist is fail-closed. Readiness status is configuration evidence only and grants no execution or activation authority.

## Verified activation receipt gates

The immutable adapter receipt is accepted only when:

```text
state = VERIFIED
blockers = []
canonical receipt hash valid
gateway health OK
durable storage
governed provider enabled
real provider use
local usage remains non-custodial
provider-usage custody RECORDED
provider-usage reconstructability PASS
transition custody RECORDED
transition reconstructability PASS
all authority flags false
```

Invalid, conflicting, stale, simulated, or authority-escalating evidence is rejected.

## Site-local completion and downstream propagation

Until all activation gates pass:

```text
data/ecosystem-chat-activation-propagation.json
state: PENDING_ACTIVATION_EVIDENCE
```

After machine-verified completion:

```text
state: READY_FOR_DOWNSTREAM_INGESTION
```

A propagation packet is not custody, activation authority, publication authority, execution authority, admissibility, or release authority.

## Machine-owned continuation

```text
1. StegVerse-org/LLM-adapter issue #18 owns the remaining live-provider and persistent-endpoint path.
2. Reuse the canonical StegDeploy runtime and governed provider broker.
3. Supply authorized provider configuration only through an authorized runtime environment.
4. Produce the secret-free provider readiness status.
5. When readiness is READY, execute one governed request through the verified gateway and custody path.
6. Retain the first exact provider, persistence, custody, reconstruction, or activation-receipt failure.
7. Site imports and validates the first zero-blocker immutable VERIFIED receipt automatically.
8. Site recomputes activation and propagation state.
9. Publisher and both wiki consumers ingest the Site projection automatically.
10. Release readiness remains fail-closed until downstream verified evidence exists.
```

No browser credential, copy/paste, workflow dispatch, artifact download, image build, node installation, node start, screenshot confirmation, receipt construction, blocker transcription, or manual publication task is assigned to the user.

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
usage retrieval != authority
usage measurement != admissibility
local persistence != custody
submission != custody
pending status != activation
CI execution != runtime heartbeat
container publication != live deployment
portable-node supervision != heartbeat authority
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
```

## Browser-local ChatGPT session continuation

The Site includes an operator-local convenience surface:

```text
chat-session-launcher.html
docs/CHATGPT_SESSION_LAUNCHER.md
scripts/check_chat_session_launcher.py
```

It stores a validated `https://chatgpt.com/c/<conversation-id>` URL in browser local storage only and does not inject prompts, transmit the private identifier, authenticate ChatGPT, grant Site execution authority, create custody, or produce activation evidence.

## Current blocker and next executable step

```text
Blocker: no repository evidence establishes an authorized real-provider HTTPS endpoint, explicit hostname allowlist, credential, model, and bounded cost policy in a persistent authorized runtime environment
Owner: StegVerse-org/LLM-adapter issue #18
Next Site step: observe the restored ST-017 run, then add runtime gateway canonical-event envelope consumption and browser correlation tests
Next adapter step: produce the secret-free provider readiness status; when READY, execute one real governed provider request through the verified transition custody and reconstruction path
Manual user action required for routine repository work: false
```

## Release posture

No tag or release is authorized. Remaining conditions are passing CI/browser verification, gateway-origin canonical records, runtime redaction receipts, authorized real-provider execution, provider-usage persistence and custody, provider-usage reconstruction, persistent endpoint verification, immutable zero-blocker activation receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This handoff, the feature branch, canonical mapping contract, replay/disclosure fixture and verifier, adapter issue #18, prior custody evidence, activation receipt paths, Site machine-readable state, and repository history preserve all continuation state without requiring conversation context.
