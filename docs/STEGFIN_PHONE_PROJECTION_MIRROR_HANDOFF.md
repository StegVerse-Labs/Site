# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-16T21:15:00-05:00

## Active goal and authority

```text
goal_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
originating_session_goal: make the current-phone StegFin path genuinely trade-ready while preserving TV/TVC-only credentials, rejecting stale PREPARE authority, and keeping signing/broadcast USER_ONLY
repository: StegVerse-Labs/Site
branch: claim/stegfin-phone-stegid-freshness-292
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
claim_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
claim_state: CLAIMED_FOR_IMPLEMENTATION
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

This is the canonical Site continuation for the stale-PREPARE defect detected from the current phone. It does not recreate StegID, TV/TVC, the direct carrier, transaction construction, RPC policy, wallet authority, or any hosted runtime. It projects the exact released StegFin freshness source and then returns live observation to `StegVerse-Labs/stegfin-governance#68/#60`.

## Directly observed reason for this task

A new current-phone `WALLET_HANDOFF_READY` packet was produced with structurally valid `DEVICE_POSSESSION`, `HUMAN_CONTINUITY`, `IDENTITY_CONTINUITY`, and PREPARE evidence, but the embedded identity/device receipts had already expired. StegFin therefore corrected the source path so stale or near-expiry admission cannot be retained/exported as current authority.

Released upstream correction:

```text
StegFin task: STEGFIN-PHONE-STEGID-FRESHNESS-016
StegFin PR #75 merge: b0973b0c99fde2e8860952a0167a56a6e8890aa2
stegid-device-wallet-bootstrap.js blob: 403d164b21a1c6e812d31f7ab45635baab59b73c
device-wallet-identity.js blob: 1180d8ee929c161978d095c91514cbc3d873d3fd
evidence-export.js blob: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
```

## Installed branch projection

The active Site branch now carries those exact source blobs at:

```text
assets/stegfin-phone/stegid-device-wallet-bootstrap.js
assets/stegfin-phone/device-wallet-identity.js
assets/stegfin-phone/evidence-export.js
```

Required behavior now projected into Site:

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

The following predecessor assets remain unchanged and authoritative:

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

## Released predecessor chain

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
active exact freshness projection: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
```

## Participant evidence contract

Canonical participant URL remains:

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

The exact Site validator is:

```text
python scripts/check_stegfin_phone_projection.py
```

It must prove:

```text
exact Git blob identity for all seven participant assets
403d164b21a1c6e812d31f7ab45635baab59b73c exact bootstrap projection
1180d8ee929c161978d095c91514cbc3d873d3fd exact identity/freshness projection
29ddb120fe6d1bd7c5118b41c4ef061d2db90a58 exact expiry-aware evidence exporter
five-minute minimum PREPARE-validity margin
stale terminal clearing
receipt-linkage verification
source trade contract COMPLETE_INSTALLED
bounded Inventory N preserved
RPC resilience preserved
TV/TVC credential authority preserved
credential_requirement NONE preserved
NON-TV/TVC secret/token prohibited
Render/Vercel/Cloudflare/GitHub-hosted production authority absent
USER_ONLY wallet review preserved
signing/broadcast remain USER_ONLY
```

Repository release gates remain:

```text
Check StegFin Phone Projection
Site Handoff Orchestrator
Ecosystem Heartbeat Orchestration
Site Bootstrap Validate
exact Pages publication from the merged commit lineage
```

## Canonical continuation

```text
active Site implementation claim: data/session-work-claims.json#SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
source authority: StegVerse-Labs/stegfin-governance task STEGFIN-PHONE-STEGID-FRESHNESS-016
current-phone evidence reconciliation: StegVerse-Labs/stegfin-governance#68
live phone activation observer: StegVerse-Labs/stegfin-governance#60
sovereign Base continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
Site pre-work collision enforcement: SITE-PREWORK-CLAIM-GATE-MACHINE-001
wallet sign/broadcast: USER_ONLY
```

After Site merge + exact Pages publication:

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

MERGED INTO: `StegVerse-Labs/stegfin-governance#68/#60` only after source + Site publication and a new unexpired current-phone packet is retained.

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

```yaml
- task_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
  execution_owner: claim/stegfin-phone-stegid-freshness-292
  state: CLAIMED_FOR_IMPLEMENTATION
  manual_execution_allowed: true
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
  collision_scope: exact three-asset freshness projection + Site projection validator + this handoff + claim bookkeeping only
  release_condition: Site validation/orchestration gates PASS + PR merged + exact Pages publication verified + claim terminalized
  next_executable_action: run/inspect PR-head gates, repair only within claim scope, merge after positive evidence, verify exact Pages build, then release claim
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: SITE-PREWORK-CLAIM-GATE-OPERATIONS
  execution_owner: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  state: MACHINE_OWNED
  manual_execution_allowed: false
  worker_registry_ref: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  collision_scope: Site admission/orchestration only
  release_condition: stronger canonical collision-control owner imports this authority
  next_executable_action: enforce the active freshness claim and block overlapping Site mutations
```

### ESCALATED / AUTHORITY-OWNED

```yaml
- task_id: CURRENT-PHONE-FRESH-PREPARE
  execution_owner: current phone + StegVerse-Labs/stegfin-governance#68/#60
  state: AUTHORITY_BOUNDARY
  manual_execution_allowed: false from repository lane
  worker_registry_ref: StegVerse-Labs/stegfin-governance#68/#60
  collision_scope: actual platform WebAuthn/device-possession gesture and resulting terminal evidence
  release_condition: newly issued unexpired PREPARE evidence plus terminal BLOCKED or WALLET_HANDOFF_READY is directly retained
  next_executable_action: only after exact Site publication, perform the current-phone Verify/prepare gesture
```

### COMPLETED / SUPERSEDED

```yaml
- task_id: SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
  state: COMPLETE_RELEASED
  next_executable_action: NONE
- task_id: STEGFIN-PHONE-STEGID-FRESHNESS-016
  repository: StegVerse-Labs/stegfin-governance
  state: COMPLETE_RELEASED_SOURCE
  source_merge: b0973b0c99fde2e8860952a0167a56a6e8890aa2
  next_executable_action: exact Site projection only
```

## Completion and archive condition

```text
developed product/control files: 6/6
scaffolding or stubs: 0
missing required product files: 0
validation: 3/5 before final-head rerun (exact upstream blobs + Handoff Orchestrator + Ecosystem Heartbeat proven; projection rerun + Site Bootstrap pending)
integration: 2/5 (source release + Site branch import complete; PR merge + Pages publication + live phone proof pending)
Site goal activation: 0% until exact public publication is verified
session consolidation: local-model/runtime source goal already complete/released; sovereign activation remains machine-owned; current session retains distinct Site propagation/live-proof support until this claim is released and #68/#60 receive fresh evidence
```
