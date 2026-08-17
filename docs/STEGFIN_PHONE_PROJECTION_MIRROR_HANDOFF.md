# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T15:31:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
originating_session_goal: correct the current-phone iOS first-passkey PREPARE double-ceremony failure while preserving TV/TVC-only credentials and USER_ONLY signing/broadcast
repository: StegVerse-Labs/Site
canonical_parent_handoff: docs/SITE_MIRROR_HANDOFF.md
prework_authority: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md + data/session-work-claims.json
claim_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
claim_state: CLAIMED_FOR_INTEGRATION
product_state: SOURCE_PROJECTED_VALIDATION_PENDING
source_owner: StegVerse-Labs/stegfin-governance#79 (StegFin #79)
parent_live_owner: StegVerse-Labs/stegfin-governance#77 + current phone + USER_ONLY
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

Site remains static transport/materialization only. It does not own wallet keys, signatures, broadcast, settlement, TV/TVC credential authority, model/runtime authority, sovereign heartbeat authority, or a hosted production runtime.

## Released predecessor chain

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
current StegID bootstrap blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
freshness identity blob: 1180d8ee929c161978d095c91514cbc3d873d3fd
freshness evidence-export blob: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
StegFin PR #75: freshness source release b0973b0c99fde2e8860952a0167a56a6e8890aa2
USER_ONLY wallet review: RELEASED
Copy canonical evidence: RELEASED
Share canonical evidence: RELEASED
unexpired StegID evidence: REQUIRED BEFORE PREPARE
```

The historical current-phone evidence from `StegVerse-Labs/stegfin-governance/receipts/phone-live/STEGFIN-PHONE-LIVE-EVIDENCE-20260816T2150-0500.json` proved PREPARE -> WALLET_HANDOFF_READY, but its StegID evidence expired at `2026-08-17T03:50:19.726Z`. It is evidence only and must not be signed or reused as transaction authority.

## USER_ONLY wallet handoff release

```text
StegFin task: STEGFIN-USER-ONLY-WALLET-HANDOFF-017
StegFin issue: #77
StegFin source PR: #78
StegFin source merge: 7c71636ef3e682443f561f3f1162673b42e12036
wallet-user-handoff.js source blob: c9c0688ab58e1a196bd777c45fa6f33fa7b9601b
wallet-user-handoff-ui.js source blob: 83a36d6b622c45be35d1af14d96f7ff92e71ced3
Site issue: #301
Site product PR: #302
Site product merge: 4e876834ad8822dd55db3cafb60152390c60a086
Pages build: 1156335357 BUILT
Pages product commit: 4e876834ad8822dd55db3cafb60152390c60a086
Site release PR: #303
Site release merge: 2338dd8a2f3bca64ede3bad2ba18cc762cd1aba6
validator hardening PR: #304
validator hardening merge: 7529e4534bf3749141bff1921d92ede2a22144cb
claim release commit: 7a48e735b4ff434a8571809ae942ef537811d1f3
release receipt: receipts/stegfin-user-wallet-handoff-301-release.json
validator release receipt: receipts/stegfin-user-wallet-handoff-301-validator-release.json
```

## Current-phone iOS first-passkey correction

Current-phone evidence on 2026-08-17 directly showed the iOS platform passkey creation ceremony completing with `Done`, followed by the published participant rendering the WebAuthn `NotAllowedError` text. Source inspection proved the first-time bootstrap immediately performed a second `navigator.credentials.get()` after successful `navigator.credentials.create()`.

Canonical source correction:

```text
StegFin child task: STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018
StegFin issue: #79 (StegFin #79)
source PR: #80
source merge: f5ff9b1aa2fad545cf9fd676c785438f306dda7a
released source bootstrap blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
Site issue: #380
Site claim: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
```

Required behavior now projected into Site:

```text
first-time/no stored WebAuthn credential
-> navigator.credentials.create
-> platform authenticator required
-> residentKey required
-> userVerification required
-> public-key credential + rawId required
-> persist credential identifier metadata
-> return HUMAN_CONTINUITY with ceremony=CREDENTIAL_CREATION
-> DO NOT perform an immediate second WebAuthn operation

later PREPARE with stored credential
-> explicit new user gesture
-> navigator.credentials.get
-> userVerification required
-> return HUMAN_CONTINUITY with ceremony=CREDENTIAL_ASSERTION
```

This is not a retry, downgrade, bypass, or cached signing authority. Cancellation/failure of either required ceremony remains fail-closed. It does not revive the expired historical wallet candidate. A new current-device PREPARE must still create a fresh wallet candidate before any USER_ONLY wallet action.

## Validation evidence

Historical predecessor release evidence remains:

```text
product Check StegFin Phone Projection: 31999164165 SUCCESS
product Site Handoff Orchestrator: 31999164164 SUCCESS
product Ecosystem Heartbeat Orchestration: 31999164196 SUCCESS
product Site Bootstrap Validate: 31999164179 SUCCESS
release Site Handoff Orchestrator: 31999296401 SUCCESS
release Ecosystem Heartbeat Orchestration: 31999296406 SUCCESS
release Site Bootstrap Validate: 31999296433 SUCCESS
validator PR Check StegFin Phone Projection: 32003248523 SUCCESS
validator PR Site Handoff Orchestrator: 32003248512 SUCCESS
validator PR Ecosystem Heartbeat Orchestration: 32003248521 SUCCESS
validator PR Site Bootstrap Validate: 32003248538 SUCCESS
post-claim-release main Check StegFin Phone Projection: 32003358306 SUCCESS
post-claim-release main Ecosystem Heartbeat Orchestration: 32003358246 SUCCESS
post-claim-release main Site Bootstrap Validate: 32003358251 SUCCESS
```

The current #380 projection requires fresh Site gates against bootstrap blob `9cac39a990a956f16fcde3681cbcc7d47b2fc704`, merge, exact Pages build, and current-phone proof. None of those later states may be inferred from this handoff alone.

## Published transition after #380 release

Canonical participant URL remains:

```text
https://stegverse.org/stegfin-trade.html
```

After exact publication, required live continuation is:

```text
reload current participant
-> explicit Verify this phone and prepare wallet handoff
-> current-device WebAuthn/device-possession/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY tap: Hand exact candidate to wallet
-> require already-injected EIP-1193 wallet on Base 0x2105 and exact governed account
-> exact candidate/freshness revalidation before wallet request
-> wallet independently confirms or rejects eth_sendTransaction
-> rejection: no transaction authority transferred
-> returned tx hash: SUBMITTED_NOT_SETTLED
-> credential-free Base eth_getTransactionReceipt observation
-> failed receipt: CHAIN_RECEIPT_FAILED; successor disabled
-> successful receipt: CONFIRMED_REPREPARE_REQUIRED
-> remove stale handoff and prohibit old quote/simulation/candidate reuse
-> explicit tap: Verify phone and prepare successor
-> current-device user verification/PREPARE renews
-> re-observe allowance + bounded inventory + fresh quote + fresh simulation
-> fresh successor transaction candidate
-> WALLET_HANDOFF_READY
-> STOP at USER_ONLY again
```

A transaction hash is not settlement. A successful Base receipt is required before predecessor authority is invalidated and successor PREPARE becomes eligible.

## Wallet compatibility boundary

Only an already-injected EIP-1193 provider is supported. The released path does not install WalletConnect, a relay, hosted wallet middleware, provider API keys, automatic chain switching, automatic signing or automatic broadcast. If the current phone browser lacks `window.ethereum`, it fails closed. That observation belongs to StegFin #77 as a live compatibility result and, if needed, must be transferred to a named non-hosted StegVerse wallet-compatibility owner. No NON-TV/TVC credential or token may be introduced as a workaround.

## Ownership and continuation

```yaml
active_site_task:
  task_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
  state: CLAIMED_FOR_INTEGRATION
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
  manual_execution_allowed: true
  collision_scope: bootstrap projection + validator + this handoff + scoped claim records only
  release_condition: exact source projection + Site gates PASS + merge + exact Pages built evidence + claim release
  next_executable_action: validate branch, merge, verify Pages, release claim

machine_owned_do_not_compete:
  site_claim_gate: SITE-PREWORK-CLAIM-GATE-MACHINE-001
  sovereign_heartbeat: StegVerse-Labs/.github#12 and #60
  sovereign_base: StegVerse-Labs/.github/tasks/TASK-2026-0005.json

human_authority_and_live_observation:
  owner: StegVerse-Labs/stegfin-governance#77 + #79 + current phone + USER_ONLY
  state: WAITING_FOR_SITE_380_PUBLICATION
  next_executable_action: after publication, reload participant and run NEW Verify/PREPARE; exercise wallet handoff only if a fresh candidate is produced and the user explicitly chooses
```

MERGED INTO after release: `StegVerse-Labs/stegfin-governance#79` -> `#77` + current phone + USER_ONLY.

## Completion and archive condition

```text
developed product/control files for #380: 4/4 projected/updated on claim branch
scaffolding or stubs: 0
missing required product files: 0
validation: pending fresh Site gates
integration: source projection installed; merge/Pages/current-phone proof outstanding
Site goal activation: not complete until exact Pages publication
chat-specific Site archive dependency: active until claim released or transferred
```

The prior #301 Site product remains complete/released. #380 is a bounded current defect correction and does not reopen Site wallet authority.
