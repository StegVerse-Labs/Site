# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-16T22:03:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
originating_session_goal: make the current-phone StegFin path trade-ready through fresh current-device StegID PREPARE evidence while preserving TV/TVC-only credentials and USER_ONLY signing/broadcast
repository: StegVerse-Labs/Site
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
claim_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
product_state: COMPLETE_RELEASED_PRODUCT
site_execution_responsibility: NONE
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
render_production_runtime_allowed: false
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

The Site freshness projection is complete. No active Site product claim remains for this goal. Site is static transport/materialization only and does not own StegID, TV/TVC, route admission, wallet contact, signing, broadcast, settlement, or a hosted production runtime.

## Source and exact projected blobs

```text
source repository: StegVerse-Labs/stegfin-governance
source task: STEGFIN-PHONE-STEGID-FRESHNESS-016
source PR #75 merge: b0973b0c99fde2e8860952a0167a56a6e8890aa2
stegid-device-wallet-bootstrap.js: 403d164b21a1c6e812d31f7ab45635baab59b73c
device-wallet-identity.js: 1180d8ee929c161978d095c91514cbc3d873d3fd
evidence-export.js: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
```

The published path requires current WebAuthn HUMAN_CONTINUITY, DEVICE_POSSESSION, identity continuity, receipt linkage, PREPARE-only authority, a five-minute minimum remaining-validity margin, stale terminal clearing, and fail-closed rejection of expired or near-expiry evidence. SIGN and BROADCAST are never granted by the PREPARE capability.

## Product release evidence

```text
Site issue: #292
product PR: #293
product merge: 1ef161a9e4b72579408a22057e5eccb8300c34a6
Check StegFin Phone Projection: 31988094522 SUCCESS
Site Handoff Orchestrator: 31988094681 SUCCESS
Ecosystem Heartbeat Orchestration: 31988094498 SUCCESS
Site Bootstrap Validate: 31988094546 SUCCESS
Pages build: 1156068305 BUILT
Pages product commit: 1ef161a9e4b72579408a22057e5eccb8300c34a6
```

Release reconciliation:

```text
PR: #297
merge: e9be3d220c09f51150a5983c0f048991531c5bc2
release Site Handoff Orchestrator: 31989781149 SUCCESS
release Ecosystem Heartbeat Orchestration: 31989781188 SUCCESS
release Site Bootstrap Validate: 31989781119 SUCCESS
release receipt: receipts/stegfin-phone-stegid-freshness-292-release.json
release receipt state: COMPLETE_RELEASED_PRODUCT
```

The failed/unmerged release attempt PR #296 is superseded. It failed because its branch had no admitted active Site claim; the gate was preserved rather than weakened.

## Live current-phone proof

A new current-phone packet was produced from the exact published freshness path while its StegID receipts were current. Canonical retained evidence:

```text
repository: StegVerse-Labs/stegfin-governance
path: receipts/phone-live/STEGFIN-PHONE-LIVE-EVIDENCE-20260816T2150-0500.json
commit: 53fc6263fa1e4f2e690389f16351b97a5ff9c880
terminal state: WALLET_HANDOFF_READY
identity continuity: IDENTITY_CONTINUITY_VALID
device admission: DEVICE_ADMITTED
validation steps: DEVICE_POSSESSION + HUMAN_CONTINUITY + IDENTITY_CONTINUITY
wallet capability: OBSERVE + PREPARE only
issued_at: 2026-08-17T02:50:19.726Z
expires_at: 2026-08-17T03:50:19.726Z
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_used: false
hosted_runtime_required: false
signed: false
broadcast: false
```

StegFin issue #60 is CLOSED_COMPLETED from this evidence. Evidence-reconciliation issue #68 is also CLOSED_COMPLETED.

## Participant and wallet boundary

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

The current unsigned handoff is an exact ERC-20 approval candidate for 12,500,000 atomic USDC to Base SwapRouter02 `0x2626664c2603336E57B271c5C0b26F421741e481`. Unlimited allowance is false. The Site never signs or broadcasts it.

If USER_ONLY submits and confirms that approval, the next StegFin transition must begin a fresh PREPARE cycle, re-observe allowance and current chain state, obtain a fresh quote/simulation, and construct a new swap candidate. The existing quote is not authority for a later swap.

## Canonical continuation

```text
StegFin live task state: StegVerse-Labs/stegfin-governance/task-state/STEGFIN-PHONE-DIRECT-ROUTE-010.json
StegFin live evidence: StegVerse-Labs/stegfin-governance/receipts/phone-live/STEGFIN-PHONE-LIVE-EVIDENCE-20260816T2150-0500.json
sovereign Base continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
Site pre-work collision enforcement: SITE-PREWORK-CLAIM-GATE-MACHINE-001
wallet review/sign/broadcast: USER_ONLY
```

MERGED INTO: `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-PHONE-DIRECT-ROUTE-010.json` for any continuation beyond the unsigned wallet handoff. No Site execution responsibility remains.

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

```yaml
- task_id: SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
  state: COMPLETE_RELEASED
  manual_execution_allowed: false
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816
  collision_scope: no mutable Site scope remains
  release_condition: SATISFIED
  next_executable_action: NONE_SITE
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: SITE-PREWORK-CLAIM-GATE-OPERATIONS
  execution_owner: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  state: MACHINE_OWNED
  manual_execution_allowed: false
  worker_registry_ref: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  collision_scope: future Site mutation admission only
  release_condition: stronger canonical collision-control owner imports this authority
  next_executable_action: enforce future Site pre-work admission
```

### AUTHORITY-OWNED

```yaml
- task_id: STEGFIN-NEXT-WALLET-TRANSITION
  execution_owner: USER_ONLY for sign/broadcast; StegFin for any subsequent PREPARE after observed chain confirmation
  state: USER_AUTHORITY_BOUNDARY
  manual_execution_allowed: false from Site
  worker_registry_ref: StegVerse-Labs/stegfin-governance/task-state/STEGFIN-PHONE-DIRECT-ROUTE-010.json
  collision_scope: exact approval signature/broadcast and any later fresh PREPARE
  release_condition: user explicitly signs/broadcasts or declines; repository/runtime cannot substitute
  next_executable_action: no Site action
```

## Completion and archive condition

```text
developed product/control files: 6/6
scaffolding or stubs: 0
missing required product files: 0
validation: 7/7 recorded product/release gates
integration: 6/6 source + exact import + product merge + Pages + release reconciliation + fresh live proof
goal activation: 100% through WALLET_HANDOFF_READY
Site session-specific work transferred: 100%
```
