# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T00:48:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301
originating_session_goal: make the current-phone StegFin path continue beyond WALLET_HANDOFF_READY without chat memory while preserving TV/TVC-only credentials and USER_ONLY signing/broadcast
repository: StegVerse-Labs/Site
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
active_claim_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301-20260817
active_claim_state: CLAIMED_FOR_IMPLEMENTATION
bounded_subordinate_handoff: docs/STEGFIN_USER_ONLY_WALLET_HANDOFF_PROJECTION_MIRROR_HANDOFF.md
source_task: StegVerse-Labs/stegfin-governance/STEGFIN-USER-ONLY-WALLET-HANDOFF-017
source_issue: StegVerse-Labs/stegfin-governance#77
source_pr: StegVerse-Labs/stegfin-governance#78
source_merge: 7c71636ef3e682443f561f3f1162673b42e12036
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

The previously released Site freshness projection remains canonical and unchanged. The active task adds only the missing USER_ONLY wallet handoff and post-confirmation successor PREPARE continuation. Site remains static transport/materialization: it does not own wallet keys, signatures, broadcast authority, settlement authority, TV/TVC credential authority, or a hosted production runtime.

## Released predecessor chain retained intact

The current participant is cumulative. The following predecessor identities are preserved as validation invariants and are not reimplemented by task 301:

```text
SITE-STEGFIN-PHONE-PROJECTION-261
STEGFIN-PHONE-DIRECT-ROUTE-011
STEGFIN-PHONE-RPC-RESILIENCE-012
SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
STEGFIN-PHONE-STEGID-FRESHNESS-016
TASK-2026-0004
Site#282
source trade contract: COMPLETE_INSTALLED
phone direct-route blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
RPC resilience blob: 290b567eca2cc9f83e7438a80682ebaf8006ad76
StegFin RPC resilience source merge: bcba49976a52024a233f998ce290ec4ab42618ff
STEGFIN-PHONE-WALLET-REVIEW-014
USER_ONLY wallet review app blob: 433ef5e5db9f9f7af2c7c7df4ba01acc89125403
freshness bootstrap blob: 403d164b21a1c6e812d31f7ab45635baab59b73c
freshness identity blob: 1180d8ee929c161978d095c91514cbc3d873d3fd
freshness evidence-export blob: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
StegFin PR #75: freshness source release b0973b0c99fde2e8860952a0167a56a6e8890aa2
Copy canonical evidence: released browser-local evidence transport
Share canonical evidence: released browser-local evidence transport
unexpired StegID evidence: required before PREPARE and export
```

These compatibility markers are retained because `scripts/check_stegfin_phone_projection.py` is the predecessor regression gate. They document released provenance; they do not reactivate any old claim or hosted authority.

## Freshness release evidence

```text
Site freshness issue: #292 CLOSED_COMPLETED
freshness product PR: #293
freshness product merge: 1ef161a9e4b72579408a22057e5eccb8300c34a6
Check StegFin Phone Projection: 31988094522 SUCCESS
Site Handoff Orchestrator: 31988094681 SUCCESS
Ecosystem Heartbeat Orchestration: 31988094498 SUCCESS
Site Bootstrap Validate: 31988094546 SUCCESS
Pages build: 1156068305 BUILT
freshness release PR: #297
freshness release merge: e9be3d220c09f51150a5983c0f048991531c5bc2
freshness release receipt: receipts/stegfin-phone-stegid-freshness-292-release.json
freshness release receipt state: COMPLETE_RELEASED_PRODUCT
```

The failed/unmerged freshness release attempt PR #296 is superseded. It failed because its branch had no admitted active Site claim; the Site pre-work gate was preserved rather than weakened.

## Retained current-phone proof

The last completed pretrade proof remains canonical evidence, but it is now historical because its PREPARE capability has expired and must not be signed or reused as transaction authority:

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

StegFin #60 and #68 are CLOSED_COMPLETED only for the prior PREPARE -> WALLET_HANDOFF_READY activation predicates. They do not prove wallet-transfer compatibility or successor PREPARE.

## Active USER_ONLY successor projection

Released source authority:

```text
StegFin task: STEGFIN-USER-ONLY-WALLET-HANDOFF-017
StegFin issue: #77
StegFin PR: #78
StegFin source merge: 7c71636ef3e682443f561f3f1162673b42e12036
wallet-user-handoff.js source blob: c9c0688ab58e1a196bd777c45fa6f33fa7b9601b
wallet-user-handoff-ui.js source blob: 83a36d6b622c45be35d1af14d96f7ff92e71ced3
Site issue: #301
Site product PR: #302
Site claim: SITE-STEGFIN-USER-WALLET-HANDOFF-301-20260817
```

Canonical participant URL remains:

```text
https://stegverse.org/stegfin-trade.html
```

The predecessor defer stack remains exactly:

```text
rpc-resilience.js
phone-direct-route.js
stegid-device-wallet-bootstrap.js
device-wallet-identity.js
app.js
evidence-export.js
```

After those defer scripts execute, a local DOMContentLoaded loader appends, in order:

```text
wallet-user-handoff.js
wallet-user-handoff-ui.js
```

Both new assets are same-origin Site projections of the exact released StegFin blobs. No remote executable script is introduced.

## Required end-to-end transition

```text
fresh current-device WebAuthn/device-possession/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY tap: Hand exact candidate to wallet
-> already-injected EIP-1193 wallet on Base 0x2105 + exact governed account
-> exact candidate/freshness revalidation immediately before wallet request
-> wallet independently displays/confirms or rejects eth_sendTransaction
-> rejection: no transaction authority transferred
-> returned transaction hash: SUBMITTED_NOT_SETTLED
-> credential-free resilient Base eth_getTransactionReceipt observation
-> successful receipt: CONFIRMED_REPREPARE_REQUIRED
-> remove prior WALLET_HANDOFF_READY and prohibit stale quote/simulation/candidate reuse
-> explicit USER_ONLY-adjacent user-presence tap: Verify phone and prepare successor
-> remove cached StegID capability so platform WebAuthn/PREPARE must renew
-> re-observe allowance and bounded inventory
-> fresh quote + fresh simulation
-> fresh successor transaction candidate
-> WALLET_HANDOFF_READY
-> STOP at USER_ONLY again
```

A transaction hash is not settlement. A successful Base receipt is required before the predecessor candidate is invalidated and successor PREPARE is enabled.

## Wallet compatibility boundary

The source supports only an already-injected EIP-1193 provider. It deliberately does **not** add WalletConnect, a relay, hosted wallet middleware, provider API keys, automatic network switching, automatic signing, or automatic broadcast. If the current iPhone browser does not expose `window.ethereum`, the new control fails closed with no wallet action. That observation, if encountered, becomes the evidence for a separate wallet-compatibility task rather than a reason to bypass governance.

## Validation contract

Predecessor regression gate:

```text
python3 scripts/check_stegfin_phone_projection.py
```

New exact successor gate:

```text
python3 scripts/check_stegfin_user_wallet_handoff_projection.py
```

Repository release gates:

```text
Check StegFin Phone Projection
Site Handoff Orchestrator
Ecosystem Heartbeat Orchestration
Site Bootstrap Validate
exact GitHub Pages publication from the merged product lineage
```

The task-specific gate proves exact source blob identity; current PREPARE freshness; exact Base/wallet binding; explicit user action before `eth_sendTransaction`; no automatic network switching; no WalletConnect/hosted relay; receipt observation; `SUBMITTED_NOT_SETTLED`; stale quote/simulation/candidate invalidation after successful receipt; a distinct successor user gesture; forced fresh StegID capability; TV/TVC/NONE; no NON-TV/TVC secret/token; and USER_ONLY signing/broadcast.

## Canonical continuation and ownership

```yaml
manual_session_claim:
  task_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301
  execution_owner: claim/stegfin-user-wallet-handoff-301
  state: CLAIMED_FOR_IMPLEMENTATION
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-USER-WALLET-HANDOFF-301-20260817
  collision_scope: exact wallet-handoff source projection + validator/workflow + this handoff + release bookkeeping only
  release_condition: final-head Site gates PASS + product PR merged + exact Pages publication + claim terminalized
  next_executable_action: inspect/repair PR #302 within claim scope, merge, publish, release claim, transfer live proof to StegFin #77/current phone

machine_owned_do_not_compete:
  task_id: SITE-PREWORK-CLAIM-GATE-OPERATIONS
  execution_owner: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  state: MACHINE_OWNED
  collision_scope: Site admission/orchestration only

human_authority:
  wallet_signature_and_broadcast: USER_ONLY
```

Sovereign Base continuation remains `StegVerse-Labs/.github/tasks/TASK-2026-0005.json`; this Site task does not duplicate that machine owner.

## Completion and archive condition

```text
developed product/control files: 7/8
scaffolding or stubs: 0
missing required product files: 1 release receipt pending publication
validation: predecessor source/projection history retained; task-specific/final-head Site gates pending
integration: source merge + exact Site import + participant loader installed; product merge + Pages + release reconciliation + live compatibility proof pending
goal activation: 0% for wallet-transfer continuity until exact public Pages publication
session consolidation: ACTIVE_UNIQUE_SUPPORT until Site release is terminal and StegFin #77/current phone owns the remaining live compatibility/user-authority proof
```

MERGED INTO: `StegVerse-Labs/stegfin-governance#77` only after Site release and current-phone continuation ownership are durable.
