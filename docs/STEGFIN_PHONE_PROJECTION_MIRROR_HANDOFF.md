# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-16T16:33:00-05:00

## Canonical scope

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
active_goal: SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
originating_session_goal: make StegFin trade-ready on the current phone, preserve TV/TVC-only credentials, externalize exact current-phone proof, and keep wallet signing/broadcast USER_ONLY
repository: StegVerse-Labs/Site
branch: claim/stegfin-phone-evidence-export-289
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
active_implementation_claim: SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289-20260816
active_validation_claim: SAME_BOUNDED_CLAIM_PR_HEAD_VALIDATION
claim_created_at: 2026-08-16T16:33:00-05:00
claim_release_condition: exact upstream evidence-export blob projected, all four Site PR gates PASS, PR merged, exact Pages build proves publication, claim terminalized, and release evidence propagated to StegFin #68/#60
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
GitHub token runtime authority: NONE
Render production runtime: PROHIBITED
wallet signing authority: USER_ONLY
broadcast authority: USER_ONLY
```

This handoff is the canonical StegFin phone projection handoff. It supersedes its earlier `NONE_SITE_IMPLEMENTATION` continuation state only for the bounded evidence-export projection introduced by Site #289. It does not create a second participant surface or transfer StegID, TV/TVC, wallet, route, settlement, publication, or Master Records authority.

## Completed predecessor releases

```text
original phone projection: Site PR #276 -> 8b5319705dcf02c8edc8dd1612e9787cf70386a1
bounded Inventory N hardening: Site PR #278 -> 264c75f84361567bdc1126e0fdb13c7a7a90de1c
hardening reconciliation: Site PR #279 -> 99f510d7e1d2026d09df0a4997cd7c2c3d5e9f9f
RPC resilience: Site PR #281 -> 19db08571c679c3143b4c2f2b380497eb8630cd4; Pages 1153990519 BUILT
source readiness: Site PR #283 -> 5941fd49647b9304d8220fcaf7155989feed89b1; Pages 1154089848 BUILT
sanitized StegID evidence: Site PR #285 -> 0e9921305cbe31eb2b00cf26baa7bba3e52de4bd; Pages 1154410266 BUILT
USER_ONLY wallet review: Site PR #288 -> abe63f6af052c460d102818e8dd16ccda90b72c6; Pages 1154455062 BUILT
phone-direct-route.js blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
rpc-resilience.js blob: 290b567eca2cc9f83e7438a80682ebaf8006ad76
device-wallet-identity.js blob: efc2c9c21d369bbc3d6817599f74496f918d721b
app.js blob: 433ef5e5db9f9f7af2c7c7df4ba01acc89125403
source trade contract: COMPLETE_INSTALLED
```

These predecessors remain terminal `MERGED_INTO_CANONICAL_WORKSTREAM` in `data/session-work-claims.json`.

## Active exact phone evidence export projection

Canonical source is `StegVerse-Labs/stegfin-governance#73`, released through StegFin PR #74 at merge `0917f5283514a54db1c520f44126a78cfc6428d7`. Exact released source:

```text
ui/evidence-export.js blob: d545063b7024b60de702ece85bd23eac6096c8bb
Site issue: #289
Site branch: claim/stegfin-phone-evidence-export-289
Site target: assets/stegfin-phone/evidence-export.js
participant page: stegfin-trade.html
```

The exporter is evidence transport only. It unlocks `Copy canonical evidence` and `Share canonical evidence` only when the exact JSON already rendered in `#evidence` is a fresh hash-bound terminal `WALLET_HANDOFF_READY` packet proving all of the following:

```text
identity_continuity.decision = IDENTITY_CONTINUITY_VALID
device_admission.decision = DEVICE_ADMITTED
device_admission.validation_steps includes DEVICE_POSSESSION
device_admission.validation_steps includes HUMAN_CONTINUITY
device_admission.validation_steps includes IDENTITY_CONTINUITY
wallet_capability.granted_capabilities includes PREPARE
wallet_capability.granted_capabilities excludes SIGN and BROADCAST
credential_authority = TV/TVC
credential_requirement = NONE
non_tv_tvc_secret_or_token_used = false
hosted_runtime_required = false
signed = false
broadcast = false
evidence_sha256 present
receipt_sha256 present
```

The export path adds no `fetch`, XHR, WebSocket, provider call, GitHub call, wallet call, signature request, broadcast request, or settlement action. Clipboard and Web Share are user-invoked browser-local transport only.

## Installed participant order

Canonical participant URL:

```text
https://stegverse.org/stegfin-trade.html
```

Exact local executable order for this projection:

```text
stegfin-trade.html
-> assets/stegfin-phone/rpc-resilience.js
-> assets/stegfin-phone/phone-direct-route.js
-> assets/stegfin-phone/stegid-device-wallet-bootstrap.js
-> assets/stegfin-phone/device-wallet-identity.js
-> assets/stegfin-phone/app.js
-> assets/stegfin-phone/evidence-export.js
```

No remote executable script is authorized.

## Phone execution and evidence contract

```text
current-phone user gesture
-> browser-local device possession
-> platform WebAuthn HUMAN_CONTINUITY
-> DEVICE_ADMITTED
-> OBSERVE + PREPARE only
-> bounded current-block ETH/USDC/WETH inventory
-> credential-free admitted Base observation
-> TV/TVC ROUTE_ADMITTED / credential_requirement=NONE
-> pinned quote, exact allowance, bounded gas and read-only simulation
-> unsigned WALLET_HANDOFF_READY
-> sanitized hash-bound StegID admission evidence retained
-> USER_ONLY wallet review available
-> Copy canonical evidence or Share canonical evidence
-> exact JSON supplied to StegFin #68/#60
-> observer validates hashes/predicates and retains durable evidence
-> STOP before USER_ONLY signing/broadcast
```

Historical phone receipts are not rewritten. A fresh current-phone PREPARE is required after the exact Site exporter is published.

## Authoritative files

```text
data/session-work-claims.json
assets/stegfin-phone/evidence-export.js
stegfin-trade.html
scripts/check_stegfin_phone_projection.py
docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
```

## Validation

Required PR-head gates:

```text
Check StegFin Phone Projection
Site Handoff Orchestrator
Ecosystem Heartbeat Orchestration
Site Bootstrap Validate
```

Focused local validator:

```text
python scripts/check_stegfin_phone_projection.py
python scripts/check_session_work_claims.py
```

The projection validator requires exact Git blob identity for seven StegFin assets, exact script order, TV/TVC/NONE credential semantics, no NON-TV/TVC token path, no hosted runtime authority, sanitized StegID PREPARE evidence, USER_ONLY wallet review, exact canonical JSON evidence export, and no network/wallet authority inside the exporter.

## Cross-repository continuation

```text
StegFin source evidence exporter: StegVerse-Labs/stegfin-governance#73 / PR #74 COMPLETE_RELEASED_SOURCE
Site projection/publication: StegVerse-Labs/Site#289 ACTIVE
current-phone evidence reconciliation: StegVerse-Labs/stegfin-governance#68
current-phone live activation observer: StegVerse-Labs/stegfin-governance#60
long-term sovereign Base runtime: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
wallet sign/broadcast: USER_ONLY
```

MERGED INTO: `StegVerse-Labs/stegfin-governance#68` and `#60` after Site #289 publishes the exact exporter and a fresh current-phone packet is produced.

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

```yaml
- task_id: SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
  execution_owner: claim/stegfin-phone-evidence-export-289
  claim_state: CLAIMED_FOR_IMPLEMENTATION
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289-20260816
  manual_execution_allowed: true
  collision_scope: exact static Site projection only; no trade/StegID/route/wallet semantic mutation
  release_condition: all Site gates PASS + merge + exact Pages build + claim release + #68/#60 propagation
  next_executable_action: validate PR head, merge only after gates pass, then prove exact Pages publication
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: SITE-PREWORK-CLAIM-GATE-OPERATIONS
  execution_owner: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  claim_state: MACHINE_OWNED
  worker_registry_ref: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  manual_execution_allowed: false
  collision_scope: claim admission/orchestration only
  release_condition: stronger organization-level collision owner imports this contract
  next_executable_action: evaluate this branch claim and fail closed on collision
```

### ESCALATED / AUTHORITY-OWNED

```yaml
- task_id: CURRENT-PHONE-WEBAUTHN-PREPARE-EVIDENCE
  execution_owner: current phone + StegFin #68/#60
  claim_state: AUTHORITY_BOUNDARY
  worker_registry_ref: StegVerse-Labs/stegfin-governance#68/#60
  manual_execution_allowed: false
  collision_scope: user-presence/WebAuthn and resulting exact terminal phone receipt only
  release_condition: fresh exact canonical JSON retained and validated by #68/#60
  next_executable_action: after Site publication, current phone performs Verify/prepare and exports exact JSON
```

### COMPLETED / SUPERSEDED

```yaml
- task_id: PRIOR-SITE-STEGFIN-PROJECTIONS
  execution_owner: none_source_complete
  claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
  worker_registry_ref: data/session-work-claims.json
  manual_execution_allowed: false
  collision_scope: released predecessor Site phone projection tasks
  release_condition: already satisfied by PRs #276/#278/#279/#281/#283/#285/#288
  next_executable_action: NONE
```

## Incomplete work and archive condition

Site #289 remains incomplete until its exact branch passes all four gates, merges, Pages builds that merge lineage, the claim is terminalized, and release evidence is posted to #68/#60. Only then does the remaining current-phone WebAuthn/PREPARE observation move wholly to those canonical observers.

```text
developed files: 5/5
scaffolding/stubs: 0
missing required files: 0
static validation: pending PR-head execution
integration: 2/4 (source released; Site asset/page installed; merge/Pages pending)
goal activation: pending publication + fresh current-phone evidence
session consolidation: durable continuation locations identified; active Site implementation still owned here
```
