# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T19:12:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
branch: claim/stegfin-ios-local-wallet-transport-388-r1
claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
claim_state: CLAIMED_FOR_INTEGRATION
product_state: IMPLEMENTED_PENDING_VALIDATION_RELEASE
site_execution_responsibility: STATIC_PARTICIPANT_PROJECTION_ONLY
source_owner: StegVerse-Labs/stegfin-governance#81
source_task: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019
source_merge: 78b648b8414f8ca9f93f396bb20e96d049607227
parent_live_owner: StegVerse-Labs/stegfin-governance#77 + #81 + current phone + USER_ONLY
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

Site remains static transport/materialization only. It does not own wallet keys, signatures, broadcast, settlement, TV/TVC credential authority, model/runtime authority, sovereign heartbeat authority, or live current-phone activation.

## Superseded/released predecessor

The iOS first-passkey correction `SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` is complete and remains released evidence:

```text
StegFin source issue: #79
source PR: #80
source merge: f5ff9b1aa2fad545cf9fd676c785438f306dda7a
released source/bootstrap blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
Site issue: #380 CLOSED_COMPLETED
Site PR: #384
Site merge: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
Pages build: 1157682910 BUILT
Site claim release commit: 9456df6b3a6bcff0fd6d2e2bcc2c55fb76e42811
```

That correction enabled the fresh PREPARE that later reached `WALLET_HANDOFF_READY`. Current-phone proof then identified a new, narrower boundary: Safari exposes no injected EIP-1193 wallet.

## Current iOS local wallet-browser projection

Upstream StegFin source released through PR #82 / merge `78b648b8414f8ca9f93f396bb20e96d049607227`.

```text
upstream source UI: StegVerse-Labs/stegfin-governance/ui/wallet-user-handoff-ui.js
upstream source blob: 114b3c39052d5b1622407080407259a0040a1369
Site projected UI: assets/stegfin-phone/wallet-user-handoff-ui.js
Site projected blob: 114b3c39052d5b1622407080407259a0040a1369
Site projection commit: 8272b5235b120e26da766f60205cc205b5d7710d
validator: scripts/check_stegfin_user_wallet_handoff_projection.py
validator update commit: a9ed87ac2b42f83b591e96d8fa7ef7ebc502015e
Site issue: #388
```

Required participant transition:

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY tap: Hand exact candidate to wallet
-> Safari has no injected EIP-1193 provider
-> fail closed; no wallet action occurs
-> expose explicit Open StegVerse in local wallet browser control
-> explicit user tap opens the same StegVerse participant in a compatible local wallet browser
-> DO NOT transfer the Safari retained candidate, calldata, candidate hash, signature, key, seed, or StegID capability material
-> perform a NEW phone verification/PREPARE inside the wallet browser
-> require injected EIP-1193 provider there
-> require Base 0x2105 and exact governed account
-> exact candidate/freshness revalidation immediately before any eth_sendTransaction request
-> wallet independently displays/confirms or rejects
-> returned transaction hash is SUBMITTED_NOT_SETTLED
-> credential-free Base receipt observation
-> successful receipt requires a fresh successor PREPARE
-> successor again stops at WALLET_HANDOFF_READY / USER_ONLY
```

The local-wallet-browser navigation is not transaction authority. It carries the StegVerse participant location, not the retained candidate. This prevents the Safari origin's current candidate from becoming a stale or cross-context authority artifact.

## Authority boundaries

```text
credential authority: TV/TVC
credential requirement: NONE
NON-TV/TVC secret/token: PROHIBITED
GitHub runtime credential authority: NONE
Render/Vercel/Cloudflare production runtime authority: NONE
WalletConnect / MetaMask Connect relay: NOT INSTALLED
Infura/provider API key: NOT INSTALLED
automatic network switching: PROHIBITED
automatic signing: PROHIBITED
automatic broadcast: PROHIBITED
wallet signing: USER_ONLY
broadcast: USER_ONLY
stale candidate/quote/simulation reuse: PROHIBITED
```

The unchanged wallet handoff runtime still requires an injected provider, exact Base chain and governed account and calls `eth_sendTransaction` only from an explicit USER_ONLY action. The Site compatibility projection only creates the route into a wallet browser where that same runtime may become satisfiable after a fresh PREPARE.

## Active claim and collision partition

```yaml
active_site_integration:
  task_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
  claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
  owner: StegVerse-Labs/Site#388
  branch: claim/stegfin-ios-local-wallet-transport-388-r1
  state: CLAIMED_FOR_INTEGRATION
  claimed_paths:
    - assets/stegfin-phone/wallet-user-handoff-ui.js
    - scripts/check_stegfin_user_wallet_handoff_projection.py
    - docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
    - data/session-work-claims.json
  collision_scope: exact StegFin participant wallet-compatibility projection and validators
  release_condition: exact source projection + canonical Site validation + merge + exact Pages build + claim release + propagation to StegFin #81
  next_executable_action: open Site PR, inspect all canonical gates, merge only on evidence, verify exact Pages build, release claim

human_authority_and_live_observation:
  owner: StegVerse-Labs/stegfin-governance#77 + #81 + current phone + USER_ONLY
  state: BLOCKED_ON_SITE_COMPATIBILITY_RELEASE
  release_condition: published participant exposes local-wallet-browser continuation and the wallet-browser context reaches a fresh injected-provider PREPARE
  next_executable_action: current-phone retest only after exact Site publication is proven

machine_owned:
  site_prework_claim_gate: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  sovereign_heartbeat_runtime: StegVerse-Labs/.github#12 + #60
  sovereign_base_continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
```

The Site pre-work claim gate owns orchestration admission only and does not own this product integration. Prior StegFin Site claims are terminal `MERGED_INTO_CANONICAL_WORKSTREAM`; #388 is the sole active owner for these exact participant/validator surfaces.

## Validation requirements

```text
1. exact UI blob == 114b3c39052d5b1622407080407259a0040a1369
2. validator requires exact no-injected-wallet fail-closed predicate
3. local-wallet-browser onclick contains no transaction_request, candidate_sha256, eth_sendTransaction, private_key, seed or signature
4. validator preserves no wallet_switchEthereumChain / WalletConnect / walletconnect / render.com / api_key / github_token conditions
5. Check StegFin Phone Projection = SUCCESS
6. Site Handoff Orchestrator = SUCCESS
7. Ecosystem Heartbeat Orchestration = SUCCESS
8. Site Bootstrap Validate = SUCCESS
9. exact GitHub Pages build = BUILT from the merge commit
10. current-phone proof remains separate and does not become true from publication alone
```

No workflow success, Pages publication or current-phone activation is claimed until directly observed.

## Local model/runtime convergence

The user's adjacent local-model/runtime goal is not open work here. Formal model development plus executable local-runtime discovery/launch/inference/proof are already canonical and released in `StegVerse-002/micro-node-runtime`. Site must not duplicate that authority. Remaining live model activation is machine-owned by the sovereign heartbeat -> TVC -> LLM-adapter -> Master Records chain.

## Cross-repository propagation

```text
source: StegVerse-Labs/stegfin-governance#81 / task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json
destination: StegVerse-Labs/Site#388 / this canonical handoff
post-release return: update StegVerse-Labs/stegfin-governance#81 and task-state to SOURCE_AND_SITE_RELEASED_CURRENT_PHONE_PROOF_REQUIRED
Publisher: verify pertinence after release; no propagation currently claimed
admissibility-wiki: verify pertinence after release; no propagation currently claimed
stegguardian-wiki: verify pertinence after release; no propagation currently claimed
master-records: live transaction/settlement evidence only if/when produced; no settlement currently exists
```

## Completion accounting

```text
Site #388 required product/control files: 4
implemented: 4/4 (UI projection, validator, canonical handoff, claim registry)
scaffolding or stubs: 0
missing required source/integration files: 0
validation: 2/5 release layers currently established (exact blob/static contract; PR/workflow and Pages gates pending)
integration: source -> Site projection complete; merge/publication/claim-release pending
goal activation: current-phone wallet transport NOT YET ACTIVATED
session consolidation: unique #388 integration remains active in this session
```

MERGED PREDECESSOR: `SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` remains released and is not restarted.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + `data/session-work-claims.json#SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817` + this handoff until Site release, then returns to `StegVerse-Labs/stegfin-governance#81` for current-phone proof.
