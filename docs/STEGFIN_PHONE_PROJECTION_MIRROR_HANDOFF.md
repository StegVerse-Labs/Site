# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-16T21:30:00-05:00

## Authority and released goal

```text
goal_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
originating_session_goal: make the current-phone StegFin path genuinely trade-ready while preserving TV/TVC-only credentials, rejecting stale PREPARE authority, and keeping signing/broadcast USER_ONLY
repository: StegVerse-Labs/Site
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
claim_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
claim_state: COMPLETE_RELEASED_PRODUCT
source_task: StegVerse-Labs/stegfin-governance/STEGFIN-PHONE-STEGID-FRESHNESS-016
source_merge: StegFin PR #75 b0973b0c99fde2e8860952a0167a56a6e8890aa2
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

The stale-PREPARE correction is now released on the canonical participant surface. Site does not recreate StegID, TV/TVC, the direct carrier, transaction construction, RPC policy, wallet authority, or any hosted production runtime. Live observation returns to `StegVerse-Labs/stegfin-governance#68/#60`.

## Source and Site release evidence

```text
StegFin task: STEGFIN-PHONE-STEGID-FRESHNESS-016
StegFin PR #75 merge: b0973b0c99fde2e8860952a0167a56a6e8890aa2
upstream bootstrap blob: 403d164b21a1c6e812d31f7ab45635baab59b73c
upstream identity/freshness blob: 1180d8ee929c161978d095c91514cbc3d873d3fd
upstream evidence-export blob: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
Site issue: #292
Site PR #293 merge: 1ef161a9e4b72579408a22057e5eccb8300c34a6
Check StegFin Phone Projection: 31988094522 SUCCESS
Site Handoff Orchestrator: 31988094681 SUCCESS
Ecosystem Heartbeat Orchestration: 31988094498 SUCCESS
Site Bootstrap Validate: 31988094546 SUCCESS
Pages build: 1156068305 BUILT from exact merge 1ef161a9e4b72579408a22057e5eccb8300c34a6
release receipt: receipts/stegfin-phone-stegid-freshness-292-release.json
```

Exact installed participant blobs:

```text
assets/stegfin-phone/stegid-device-wallet-bootstrap.js = 403d164b21a1c6e812d31f7ab45635baab59b73c
assets/stegfin-phone/device-wallet-identity.js = 1180d8ee929c161978d095c91514cbc3d873d3fd
assets/stegfin-phone/evidence-export.js = 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
```

## Released behavior

```text
wallet capability decisions carry expires_at
legacy/missing/expired/near-expiry capability state is never accepted for PREPARE
five-minute minimum remaining validity is enforced before and after direct-route preparation
stale localStorage WALLET_HANDOFF_READY is cleared before renewal
stale IndexedDB latest-terminal is deleted before renewal and on post-carrier freshness failure
fresh renewal requires current platform WebAuthn HUMAN_CONTINUITY + DEVICE_POSSESSION
identity/device/capability receipt linkage is checked
only fresh identity-bound terminal evidence may be durably retained
canonical evidence export rejects expired identity/device/capability evidence
SIGN/BROADCAST are never granted by the PREPARE capability
credential_authority remains TV/TVC
credential_requirement remains NONE
non_tv_tvc_secret_or_token_used remains false
wallet signing remains USER_ONLY
broadcast remains USER_ONLY
```

## Preserved predecessor lineage

```text
SITE-STEGFIN-PHONE-PROJECTION-261
STEGFIN-PHONE-DIRECT-ROUTE-011
STEGFIN-PHONE-RPC-RESILIENCE-012
TASK-2026-0004
Site#282
COMPLETE_INSTALLED
31ed79cb56e8d2366e6d70f22e28c70162c88fd8
290b567eca2cc9f83e7438a80682ebaf8006ad76
bcba49976a52024a233f998ce290ec4ab42618ff
STEGFIN-PHONE-WALLET-REVIEW-014
433ef5e5db9f9f7af2c7c7df4ba01acc89125403
SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
```

Released predecessor chain:

```text
original phone projection: PR #276
bounded Inventory N hardening: PR #278
hardening reconciliation: PR #279
RPC resilience: PR #281
source readiness projection: PR #283
sanitized StegID evidence: PR #285
USER_ONLY wallet review: PR #288
evidence-export product: PR #290
release reconciliation: PR #291
freshness source: StegFin PR #75
freshness Site product: PR #293
```

## Participant evidence contract

Canonical participant URL:

```text
https://stegverse.org/stegfin-trade.html
```

Executable order remains:

```text
rpc-resilience.js
phone-direct-route.js
stegid-device-wallet-bootstrap.js
device-wallet-identity.js
app.js
evidence-export.js
```

A valid current-phone export must be a currently unexpired, hash-bound terminal `WALLET_HANDOFF_READY` packet and directly carry:

```text
identity_continuity.decision = IDENTITY_CONTINUITY_VALID
identity_continuity.expires_at > current time
device_admission.decision = DEVICE_ADMITTED
device_admission.expires_at > current time
device_admission.validation_steps includes DEVICE_POSSESSION
device_admission.validation_steps includes HUMAN_CONTINUITY
device_admission.validation_steps includes IDENTITY_CONTINUITY
wallet_capability.decision = ALLOW_DEVICE_WALLET_CAPABILITY
wallet_capability.expires_at > current time
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

Copy canonical evidence / Share canonical evidence remain browser-local evidence transport only. The Site path does not contact a wallet, sign, broadcast, settle, or mint execution authority.

## Validation contract

Canonical validator:

```text
python scripts/check_stegfin_phone_projection.py
```

It preserves exact Git-blob identity for all seven participant assets, five-minute PREPARE freshness, stale terminal clearing, receipt linkage, `COMPLETE_INSTALLED` source readiness, bounded Inventory N, RPC resilience, TV/TVC/NONE authority, no NON-TV/TVC secret/token, USER_ONLY wallet review, and USER_ONLY signing/broadcast.

## Canonical continuation

```text
Site product implementation: COMPLETE_RELEASED_PRODUCT
Site release receipt: receipts/stegfin-phone-stegid-freshness-292-release.json
current-phone evidence reconciliation: StegVerse-Labs/stegfin-governance#68
live phone activation observer: StegVerse-Labs/stegfin-governance#60
sovereign Base continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
Site pre-work collision enforcement: SITE-PREWORK-CLAIM-GATE-MACHINE-001
wallet sign/broadcast: USER_ONLY
```

The next authority-bound sequence is:

```text
current phone reloads canonical participant surface
-> Verify this phone and prepare wallet handoff
-> stale/near-expiry capability cannot survive
-> current platform WebAuthn HUMAN_CONTINUITY
-> current DEVICE_POSSESSION
-> fresh identity/device/PREPARE receipts with unexpired expires_at
-> bounded Base inventory + TV/TVC ROUTE_ADMITTED
-> quote / allowance / simulation
-> unsigned WALLET_HANDOFF_READY or precise BLOCKED
-> evidence exporter independently verifies unexpired admission
-> exact canonical JSON retained by StegFin #68/#60
-> STOP before USER_ONLY signing/broadcast
```

MERGED INTO: `StegVerse-Labs/stegfin-governance#68/#60` for remaining live current-phone observation.

## Execution ownership and collision partition

### COMPLETED / SUPERSEDED

```yaml
- task_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
  state: COMPLETE_RELEASED_PRODUCT
  release_evidence: PR #293 + Pages 1156068305 + receipts/stegfin-phone-stegid-freshness-292-release.json
  mutable_site_scope_remaining: false
  next_executable_action: NONE_SITE_PRODUCT
- task_id: STEGFIN-PHONE-STEGID-FRESHNESS-016
  repository: StegVerse-Labs/stegfin-governance
  state: COMPLETE_RELEASED_SOURCE
  source_merge: b0973b0c99fde2e8860952a0167a56a6e8890aa2
  next_executable_action: NONE_SOURCE
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: SITE-PREWORK-CLAIM-GATE-OPERATIONS
  execution_owner: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  state: MACHINE_OWNED
  manual_execution_allowed: false
  worker_registry_ref: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  collision_scope: future Site mutation admission only
  next_executable_action: enforce future Site pre-work admission
```

### ESCALATED / AUTHORITY-OWNED

```yaml
- task_id: CURRENT-PHONE-FRESH-PREPARE
  execution_owner: current phone + StegVerse-Labs/stegfin-governance#68/#60
  state: AUTHORITY_BOUNDARY
  manual_execution_allowed: false from repository lane
  collision_scope: actual platform WebAuthn/device-possession gesture and resulting terminal evidence
  release_condition: newly issued unexpired PREPARE evidence plus terminal BLOCKED or WALLET_HANDOFF_READY is directly retained
  next_executable_action: current phone performs the user-presence Verify/prepare gesture on the released Site surface
```

## Completion and archive condition

```text
developed product/control files: 6/6
scaffolding or stubs: 0
missing required product files: 0
validation: 5/5 (exact source blobs + four PR-head gates)
integration: 4/5 (source release + Site import + PR merge + exact Pages publication complete; fresh current-phone proof remains authority-bound)
Site product goal activation: 100% COMPLETE_RELEASED_PRODUCT
session consolidation: Site implementation transfers to StegFin #68/#60 after claim release; the conversation remains useful only for fresh current-phone evidence reconciliation until that proof is retained
```
