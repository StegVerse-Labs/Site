# StegFin USER_ONLY Wallet Handoff Projection Mirror Handoff

Updated: 2026-08-17T00:43:00-05:00

This is a **bounded subordinate handoff**, not a competing phone authority. Canonical parent remains `docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md`; on release this task merges back into that parent and no second Site product authority survives.

## Active goal and ownership

```text
goal_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301
originating_goal: remove ChatGPT/session dependence after WALLET_HANDOFF_READY by projecting exact USER_ONLY wallet handoff + post-confirmation successor PREPARE continuity
repository: StegVerse-Labs/Site
branch: claim/stegfin-user-wallet-handoff-301
source_repository: StegVerse-Labs/stegfin-governance
source_task: STEGFIN-USER-ONLY-WALLET-HANDOFF-017
source_issue: StegVerse-Labs/stegfin-governance#77
source_pr: StegVerse-Labs/stegfin-governance#78
source_merge: 7c71636ef3e682443f561f3f1162673b42e12036
site_issue: 301
claim_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301-20260817
claim_state: CLAIMED_FOR_IMPLEMENTATION
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
hosted_runtime_required: false
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

## Exact source projection

```text
assets/stegfin-phone/wallet-user-handoff.js
  source blob: c9c0688ab58e1a196bd777c45fa6f33fa7b9601b
assets/stegfin-phone/wallet-user-handoff-ui.js
  source blob: 83a36d6b622c45be35d1af14d96f7ff92e71ced3
```

The participant loads both assets after the already released PREPARE, wallet-review and evidence-export stack. No existing phone-direct-route, RPC, StegID, quote, allowance, gas or simulation implementation is forked.

## Executable transition

```text
fresh current-device WebAuthn/device-possession/PREPARE
-> WALLET_HANDOFF_READY exact unsigned candidate
-> explicit tap: Hand exact candidate to wallet
-> require already-injected EIP-1193 provider on Base 0x2105 and exact governed account
-> exact candidate hash revalidation immediately before wallet contact
-> wallet independently displays/confirms or rejects eth_sendTransaction
-> rejection: USER_DECLINED_OR_WALLET_REJECTED; no transaction effect claimed
-> returned tx hash: SUBMITTED_NOT_SETTLED
-> credential-free resilient Base eth_getTransactionReceipt observation
-> failed receipt: CHAIN_RECEIPT_FAILED; no successor enabled
-> successful receipt: CONFIRMED_REPREPARE_REQUIRED
-> remove stale WALLET_HANDOFF_READY; stale quote/simulation/candidate reuse=false
-> explicit tap: Verify phone and prepare successor
-> remove cached StegID capability to force a new current-device user-verification/PREPARE gesture
-> re-observe allowance/inventory + fresh quote/simulation
-> fresh successor candidate
-> WALLET_HANDOFF_READY
-> STOP at USER_ONLY again
```

A submitted transaction hash is not settlement. Chain receipt success is required before predecessor authority is invalidated and successor PREPARE is offered.

## Wallet compatibility boundary

The released source intentionally supports only an **already-injected EIP-1193 provider**. It does not install WalletConnect, a relay, a hosted wallet middleware, a wallet API key, automatic chain switching, or a wallet-specific deep link. If the current iPhone browser does not expose `window.ethereum`, the control fails closed and current-phone evidence must drive a separate wallet-compatibility implementation task rather than bypass governance.

## Validation

Canonical predecessor validator remains:

```text
python3 scripts/check_stegfin_phone_projection.py
```

Task-specific validator installed here:

```text
python3 scripts/check_stegfin_user_wallet_handoff_projection.py
```

The `Check StegFin Phone Projection` validation-only workflow executes both. Task-specific validation requires exact upstream Git blob identity, fresh PREPARE checks, exact Base/wallet binding, explicit USER_ONLY invocation before `eth_sendTransaction`, no automatic network switching, no WalletConnect/hosted relay, receipt observation, `SUBMITTED_NOT_SETTLED`, stale-authority invalidation, a separate successor user gesture, forced fresh StegID capability, and unchanged TV/TVC/NONE + USER_ONLY boundaries.

## Active claim / collision partition

```yaml
task_id: SITE-STEGFIN-USER-WALLET-HANDOFF-301
claimant: chatgpt-session-stegfin-user-wallet-handoff-20260817
role: IMPLEMENTATION
state: CLAIMED_FOR_IMPLEMENTATION
claimed_paths:
  - data/session-work-claims.json
  - assets/stegfin-phone/wallet-user-handoff.js
  - assets/stegfin-phone/wallet-user-handoff-ui.js
  - stegfin-trade.html
  - scripts/check_stegfin_user_wallet_handoff_projection.py
  - .github/workflows/check-stegfin-phone-projection.yml
  - docs/STEGFIN_USER_ONLY_WALLET_HANDOFF_PROJECTION_MIRROR_HANDOFF.md
  - receipts/stegfin-user-wallet-handoff-301-release.json
collision_boundary:
  - exact projection only
  - no modification of direct trade construction/RPC/StegID/quote/allowance/gas/simulation semantics
  - no automatic signing/broadcast
  - no NON-TV/TVC secret/token
  - no Render/Vercel/Cloudflare/GitHub-hosted production authority
release_condition: exact source projection + final-head Site gates PASS + merge + exact Pages build + terminal claim release + live continuation transferred to StegFin #77/current phone
```

Site pre-work collision enforcement remains machine-owned by `SITE-PREWORK-CLAIM-GATE-MACHINE-001` and may block this branch if its claim ceases to resolve uniquely.

## Completed work

```text
StegFin source PR #78: MERGED @ 7c71636ef3e682443f561f3f1162673b42e12036
Site issue #301: OPEN
Site claim: CREATED
exact runtime asset projection: INSTALLED / blob c9c0688ab58e1a196bd777c45fa6f33fa7b9601b
exact UI asset projection: INSTALLED / blob 83a36d6b622c45be35d1af14d96f7ff92e71ced3
participant load order: INSTALLED
new task-specific validator: INSTALLED
validation workflow integration: INSTALLED
```

## Incomplete work / next executable action

```text
1 open Site PR from claim/stegfin-user-wallet-handoff-301
2 inspect final-head Check StegFin Phone Projection, Site Handoff Orchestrator, Ecosystem Heartbeat Orchestration and Site Bootstrap Validate
3 repair only within this claim if any gate fails
4 merge after positive evidence
5 verify exact GitHub Pages build from merged lineage
6 create release receipt and terminalize Site claim
7 merge this bounded handoff back into docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
8 current phone reloads page and runs a NEW fresh PREPARE
9 test whether this iPhone browser exposes an injected EIP-1193 wallet; no transaction occurs unless user explicitly taps and independently confirms in wallet
```

## Archive condition

This session is not archive-safe until Site publication is complete and current-phone continuation is durably owned with enough executable state to proceed without chat memory. A live approval or swap signature is never an archive requirement because it is USER_ONLY, but the installed path to request, observe and continue from that user action must be proven usable or fail closed with a durable wallet-compatibility owner.

Developed files: 6/8; validation: 2/6; integration: 2/5; goal activation: 0% until exact public Pages publication; session consolidation: ACTIVE_UNIQUE_SUPPORT.
