# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

<!-- STEGGATE_FOUR_APP_SITE_STATUS_BEGIN -->
## StegGate four-public-application execution status

Canonical progress handoff: `docs/STEGGATE_FOUR_APP_MIRROR_HANDOFF.md`
Machine status: `data/steggate-four-app-status.json`
Parent goal: `StegVerse-Labs/Site#239`

```text
execution_progress: 37% (11/30 verified gates)
fully_functional_public_apps: 0/4
goal_complete: false
orchestration_state: COMPLETE
archive_ready_for_four_app_goal: false
status_timestamp: 2026-08-09T17:35:00-05:00
```

Status checks must read the dedicated four-app handoff and machine status, then current heartbeat/orchestration state, before reporting progress. Product completion is never inferred from orchestration completion.
<!-- STEGGATE_FOUR_APP_SITE_STATUS_END -->

## Mandatory orchestration entry

Every ChatGPT session or automation touching this repository must invoke the repository orchestration files before beginning new work. The incoming request is a candidate workload, not automatic execution authority.

Required entry sequence:

```text
1. Read data/site-orchestration-state.json.
2. Read data/ecosystem-heartbeat-state.json.
3. Run scripts/site_handoff_orchestrator.py.
4. Run scripts/check_ecosystem_heartbeat_orchestration.py.
5. Continue only the workload admitted by the orchestration result.
6. Preserve active ownership and claimed paths.
7. Update orchestration state and this handoff before task closure.
```

Sessions must not independently reinterpret this handoff while bypassing the repository orchestrator.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat / Ecosystem Node request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, synchronized human/governed projections, downstream propagation, and playable governed service surfaces
Primary surface: ecosystem-chat.html
Usage surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Playable service surface: ecosystem-music.html
Participant-facing HIL surface: humans-as-interoperability-layer.html
Result: ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT
Compatibility Result: ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION
Manual user action required for routine repository work: false
```

`ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION` is retained as the stable compatibility class consumed by existing Site validators. The more specific current blocker is the absent authorized real-provider configuration and persistent endpoint; neither marker grants activation authority.

## Current live task sequence

```text
current work task sequence 0001
state: RUNNING
priority: FIRST_SEAMLESS_HIL_USER_EXPERIENCE
heartbeat model: transition-driven and health-relative
parallel work admitted: HIL upload surface; heartbeat/orchestration integration; Cloudflare deployment verification
exclusive barrier: no non-parallel HIL activation task begins until all active parallel tasks close
```

The live working state is carried by `data/ecosystem-heartbeat-state.json`. Time-based watchdogs detect silence only; they do not claim progress. Meaningful governed orchestration transitions advance repository and ecosystem heartbeat counters.

When the active sequence closes, the state must read:

```text
end of current work task sequence 0001, no tasks running
```

Only then may a queued exclusive task begin.

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

## Active workload ownership

```text
HIL upload surface: owned by separate active session; parallel-safe with heartbeat/orchestration work
Heartbeat/orchestration contract: PR #98, branch goal/hil-heartbeat-orchestration
Canonical upstream browser binding: PR #95
StegVerse-owned endpoint publication and activation path: Site issue #24
Cloudflare Workers deployment verification: current session; parallel-safe, evidence-only, no activation authority
Semantic shorthand command layer for Ecosystem Chat/VACC: Site issue #396, PR #397, branch feat/vacc-semantic-shorthand-396; bounded local discovery only, no provider or adjudicative authority
Superseded broad activation tracker: Site issue #16 closed in favor of issue #24 and this handoff
```

No new branch may claim an active workload unless the existing owner is completed, explicitly superseded, or declared stale by the orchestrator.

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

Sensitive fields remain subject to role-based disclosure and redaction policies. Human-readable, formatted governed, and raw machine-readable output resolve to the same canonical records. Raw records are exportable and replayable.

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
Playable StegMusic partial Ecosystem Chat surface
Three locally generated StegDJ tracks
Normal audio controls and trait refinement
Always-visible playback, preference, projection, and royalty indicators
Conversation / Governed music play / Split / Raw JSONL music projections
Visible rights/source posture
Persistent local music event stream and prototype contribution-value panel
StegMusic JSON session export
Health-relative heartbeat orchestration contract
Repository and ecosystem heartbeat state
Parallel-safe / exclusive / dependency-blocked workload classification
Cloudflare Workers GitHub deployment path established for the Site repository
Shared semantic shorthand router with bounded `/disability`, `/help`, `/evidence`, `/timeline`, `/compare`, `/explain`, and `/visualize` discovery
VACC semantic command interception before coordinated-provider runtime gating
Ecosystem Chat semantic command interception before generic route classification
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
Heartbeat orchestration validator: PASS observed on PR #98 run 30213685708
Site Bootstrap Validate: PASS observed on PR #98 run 30213685712
Site handoff orchestrator: duplicate ownership repair in progress
StegMusic static playable-slice verifier: IMPLEMENTED
StegMusic browser audio execution: NOT YET OBSERVED IN CI OR DEPLOYED PREVIEW
Browser execution test: NOT YET OBSERVED IN CI
Accessibility interaction test: NOT YET OBSERVED IN CI
Cryptographic canonical hash: NOT YET IMPLEMENTED; browser fixtures use preview-only markers
Gateway-origin canonical events: NOT YET IMPLEMENTED
Semantic shorthand static and Node regression validators: IMPLEMENTED; fresh exact-head hosted PASS pending
Semantic shorthand public VACC/Ecosystem Chat behavior: NOT YET OBSERVED AFTER MERGE
Cloudflare repository clone: OBSERVED SUCCESS
Cloudflare Wrangler deployment: OBSERVED SUCCESS
Cloudflare workers.dev trigger: OBSERVED at https://site.rigelrandolph.workers.dev
Cloudflare deployment version: cb589190-bb71-46fb-84ea-bf767902ba89
Cloudflare live route content and HIL behavior: NOT YET VERIFIED
Cloudflare deployment is hosting evidence only; authority effect: NONE
Authority effect: NONE
```

## Cloudflare deployment observation — 2026-07-29

```text
Provider: Cloudflare Workers & Pages
Source repository: StegVerse-Labs/Site
Deployment command: npx wrangler deploy
Root directory: /
Observed result: SUCCESS
Observed workers.dev route: https://site.rigelrandolph.workers.dev
Observed version ID: cb589190-bb71-46fb-84ea-bf767902ba89
workers_dev: enabled by default
preview_urls: enabled by default
Live browser verification: PENDING
HIL upload verification: PENDING
Custom domain binding: NOT OBSERVED
R2/D1/KV/Queue/Durable Object bindings: NOT OBSERVED
MCP endpoint: NOT OBSERVED
Activation authority: false
Publication authority: false
Custody authority: false
```

The Cloudflare deployment establishes that the repository can be cloned and deployed through Wrangler. It does not establish that the expected Site content is served, that the HIL page is reachable, that uploads complete, that evidence is durably stored, that an MCP endpoint exists, or that any activation gate has passed.

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
Cloudflare Workers repository deployment: VERIFIED AS DEPLOYMENT EVENT ONLY
Cloudflare live content and route behavior: NOT VERIFIED
Real governed provider response: NOT VERIFIED
Provider-usage persistence from real provider use: NOT VERIFIED
Provider-usage custody: NOT VERIFIED
Provider-usage reconstruction: NOT VERIFIED
Adapter immutable zero-blocker VERIFIED receipt: NOT OBSERVED
Site ACTIVATION_COMPLETE: NOT OBSERVED
Downstream verified ingestion: NOT OBSERVED
Playable StegMusic generated-audio source: IMPLEMENTED ON FEATURE BRANCH; DEPLOYMENT NOT YET OBSERVED
Commercial music source: NOT IMPLEMENTED
Public-domain verified source: NOT IMPLEMENTED
```

## Remaining work

Destination `StegVerse-Labs/Site`:

```text
Open and verify the Cloudflare workers.dev route
Identify the exact deployed landing page and HIL route
Verify static assets, navigation, and expected Site content
Capture the first exact HIL upload request/response failure through Cloudflare Observability
Determine whether Site should remain a Worker deployment or use a distinct static/full-stack deployment contract
Explicitly configure workers_dev and preview_urls posture
Define custom-domain route only after live content verification
Keep Cloudflare as a replaceable execution-substrate adapter rather than the StegVerse authority layer
Observe and preserve passing heartbeat orchestration and canonical Site validation
Complete HIL upload surface without conflicting with PR #98 paths
Add browser behavior tests for all three modes and bidirectional selection
Implement runtime role selection and emitted redaction receipts
Accept canonical events from the governed gateway instead of constructing them from DOM messages
Render attachments and generated artifacts from canonical artifact_refs
Add locale-aware multilingual renderer selection
Add direct StegMusic service launcher inside ecosystem-chat.html
Observe StegMusic browser audio on deployed preview
Add StegMusic interaction, persistence, accessibility, reset, revocation, and tester-isolation tests
Add captured-versus-derived inspection and downstream projection permission controls
Complete semantic shorthand discovery for Ecosystem Chat and VACC, validate `/disability` and ambiguity-preserving command behavior, then observe deployed behavior
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
Custody music interaction, derivation, reuse, rights, and value-lineage records after authorization
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

## Machine-owned continuation

```text
1. Verify the Cloudflare workers.dev route and identify the correct HIL URL.
2. Record live content, route, and upload observations without treating deployment as activation.
3. Keep PR #98 limited to heartbeat/orchestration files and parallel-safe with the upload session.
4. Close or supersede duplicate workload owners before admitting new work.
5. StegVerse-org/LLM-adapter issue #18 owns the remaining live-provider and persistent-endpoint path.
6. Reuse the canonical StegDeploy runtime and governed provider broker.
7. Supply authorized provider configuration only through an authorized runtime environment.
8. Produce the secret-free provider readiness status.
9. When readiness is READY, execute one governed request through the verified gateway and custody path.
10. Retain the first exact provider, persistence, custody, reconstruction, or activation-receipt failure.
11. Site imports and validates the first zero-blocker immutable VERIFIED receipt automatically.
12. Site recomputes activation and propagation state.
13. Publisher and both wiki consumers ingest the Site projection automatically.
14. Release readiness remains fail-closed until downstream verified evidence exists.
15. In parallel, deploy and browser-test the generated-audio StegMusic service slice.
16. Add one verified lawful non-generated source before invited external testing.
17. Complete Site#396 semantic shorthand validation, merge only after exact-head gates pass, observe deployed VACC/Ecosystem Chat behavior, then propagate the released interaction contract downstream.
```

No browser credential, copy/paste, workflow dispatch, artifact download, image build, node installation, node start, screenshot confirmation, receipt construction, blocker transcription, or manual publication task is assigned to the user. Opening the newly deployed route for live verification is the current explicit user-performed observation already in progress and does not grant activation authority.

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
Cloudflare deployment success != live content verification
workers.dev route != custom production domain
hosting provider availability != StegVerse authority
portable-node supervision != heartbeat authority
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
browser-generated audio != licensed catalog
prototype contribution estimate != payable royalty
music rights label != license grant
semantic shorthand recognition != committed intent
semantic topic discovery != execution authority
```

## Current blocker and next executable step

```text
Immediate observation blocker: the deployed workers.dev route has not yet been opened and mapped to the expected Site/HIL path
Primary activation blocker: no repository evidence establishes an authorized real-provider HTTPS endpoint, explicit hostname allowlist, credential, model, and bounded cost policy in a persistent authorized runtime environment
Owner of Cloudflare live verification: current Site deployment session
Owner of activation blocker: StegVerse-org/LLM-adapter issue #18
Next Site step: verify the deployed route, identify the HIL URL, record the first exact upload behavior, finish parallel HIL upload and heartbeat/orchestration integration, complete Site#396 exact-head semantic shorthand validation, then add runtime gateway canonical-event envelope consumption and browser correlation tests
Next adapter step: produce the secret-free provider readiness status; when READY, execute one real governed provider request through the verified transition custody and reconstruction path
Manual user action required for routine repository work: false
```

## Release posture

No tag or release is authorized. Remaining conditions are verified live Cloudflare route content, passing CI/browser verification, gateway-origin canonical records, runtime redaction receipts, authorized real-provider execution, provider-usage persistence and custody, provider-usage reconstruction, persistent endpoint verification, immutable zero-blocker activation receipt publication, Site activation completion, verified downstream ingestion, StegMusic browser verification, at least one verified lawful non-generated music source for invited testing, and exact-head validation/deployment evidence for the semantic shorthand command layer.

## Archive readiness

This handoff, repository orchestration state, heartbeat state, active PRs, issues, validators, workflows, receipts, Cloudflare deployment observations, and repository history preserve all continuation state without requiring conversation context.
