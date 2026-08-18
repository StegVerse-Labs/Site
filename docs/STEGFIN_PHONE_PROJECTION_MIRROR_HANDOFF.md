# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T19:50:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
branch: main
claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
claim_state: BLOCKED_PENDING_PUBLICATION_PROOF_AND_CURRENT_PHONE_PROOF
product_state: SOURCE_AND_SITE_MERGED_PUBLICATION_PROOF_REQUIRED
site_execution_responsibility: STATIC_PARTICIPANT_PROJECTION_ONLY
source_owner: StegVerse-Labs/stegfin-governance#81
source_task: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019
source_merge: 78b648b8414f8ca9f93f396bb20e96d049607227
site_issue: StegVerse-Labs/Site#388
site_pull_request: StegVerse-Labs/Site#389
site_merge: ec8b5136ff9281ea37e861281f9428c7c283fbe4
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

## Released predecessor and convergence

`SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` remains complete/released and is not restarted. Its release enabled a fresh phone PREPARE that reached `WALLET_HANDOFF_READY`. The subsequent live phone observation established the narrower current blocker: Safari exposes no injected EIP-1193 provider.

The local-model/runtime goal is independently complete/released in `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`. Its remaining live activation is MACHINE_OWNED by the sovereign heartbeat -> TV/TVC -> LLM-adapter -> Master Records chain and must not be duplicated here.

## Current iOS local wallet-browser implementation

Upstream source release:

```text
StegFin issue: #81
StegFin PR: #82
StegFin merge: 78b648b8414f8ca9f93f396bb20e96d049607227
upstream UI: ui/wallet-user-handoff-ui.js
upstream UI blob: 114b3c39052d5b1622407080407259a0040a1369
```

Site integration:

```text
Site issue: #388
Site PR: #389
Site merge: ec8b5136ff9281ea37e861281f9428c7c283fbe4
Site UI: assets/stegfin-phone/wallet-user-handoff-ui.js
Site UI blob: 114b3c39052d5b1622407080407259a0040a1369
validator: scripts/check_stegfin_user_wallet_handoff_projection.py
validation observation receipt: receipts/stegfin-ios-local-wallet-transport-388-validation.json
```

Installed transition:

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY tap: Hand exact candidate to wallet
-> if injected EIP-1193 provider exists: require Base 0x2105 + exact governed account + fresh candidate validation
-> if Safari has no injected provider: fail closed; no wallet action occurs
-> expose explicit Open StegVerse in local wallet browser control
-> explicit user tap opens the same StegVerse participant in a compatible wallet browser
-> DO NOT transfer the Safari retained candidate, calldata, candidate hash, signature, key, seed, or StegID capability material
-> perform a NEW phone verification/PREPARE inside the wallet-browser context
-> require injected EIP-1193 provider there before any eth_sendTransaction request
-> wallet independently displays/confirms or rejects
-> returned transaction hash is SUBMITTED_NOT_SETTLED
-> credential-free Base receipt observation
-> successful receipt invalidates predecessor quote/simulation/candidate authority
-> explicit fresh successor PREPARE
-> successor again stops at WALLET_HANDOFF_READY / USER_ONLY
```

## Authority boundaries

```text
credential authority: TV/TVC
credential requirement: NONE
NON-TV/TVC secret/token: PROHIBITED
GitHub runtime credential authority: NONE
Render/Vercel/Cloudflare production runtime authority: NONE
WalletConnect / MetaMask Connect relay transaction authority: NOT INSTALLED
provider API key: NOT INSTALLED
automatic network switching: PROHIBITED
automatic signing: PROHIBITED
automatic broadcast: PROHIBITED
wallet signing: USER_ONLY
broadcast: USER_ONLY
stale candidate/quote/simulation reuse: PROHIBITED
```

The local-wallet-browser navigation carries only the StegVerse participant location. It is not transaction authority and cannot make the Safari candidate signable in the second browser context.

## Validation state

Static and repository-integration predicates directly established:

```text
exact source/UI blob identity: PASS
no-injected-wallet fail-closed predicate present: PASS
wallet-browser continuation only after exact failure: PASS
wallet-browser onclick carries no transaction_request/candidate_sha256/eth_sendTransaction/private_key/seed/signature: PASS by installed validator contract + exact source inspection
fresh PREPARE instruction in wallet-browser context: PASS
no automatic network switch/sign/broadcast: PASS by exact source inspection
Site merge to main: COMPLETE at ec8b5136ff9281ea37e861281f9428c7c283fbe4
```

Canonical GitHub-hosted PR-head runs were directly inspected before merge and all terminated without observable validator steps:

```text
Check StegFin Phone Projection: 32083442727 FAILURE / zero exposed steps
Site Handoff Orchestrator: 32083442734 FAILURE / zero exposed steps
Site Bootstrap Validate: 32083442769 FAILURE / zero exposed steps
Ecosystem Heartbeat Orchestration: 32083442854 FAILURE / zero exposed steps
```

Individual reruns were requested and did not produce a successful observable validation cycle. No PASS is inferred from those runs and no GitHub-token workaround is authorized.

PR #389 was subsequently merged as repository integration only. That merge does **not** satisfy the publication or activation release condition. Pages build status for merge `ec8b5136ff9281ea37e861281f9428c7c283fbe4` has not yet been directly proven through an available deployment surface in this session.

## Active ownership and blocker

```yaml
site_publication_proof:
  task_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-PUBLISH
  owner: StegVerse-Labs/Site#388
  state: BLOCKED
  durable_evidence: receipts/stegfin-ios-local-wallet-transport-388-validation.json + this handoff
  release_condition: prove the published participant serves UI blob 114b3c39052d5b1622407080407259a0040a1369 from Site merge ec8b5136ff9281ea37e861281f9428c7c283fbe4, or obtain an exact Pages build receipt for that merge
  next_executable_action: observe exact Pages/live participant publication without introducing credentials or hosted runtime authority

human_authority_and_live_observation:
  task_id: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019-LIVE
  owner: StegVerse-Labs/stegfin-governance#77 + #81 + current phone + USER_ONLY
  state: BLOCKED_ON_PUBLICATION_PROOF
  release_condition: published participant exposes the local-wallet-browser continuation and the wallet-browser context reaches fresh PREPARE with an injected governed wallet provider
  next_executable_action: after publication proof, current phone reloads the participant, reproduces the Safari fail-closed state, uses Open StegVerse in local wallet browser, then runs NEW Verify/PREPARE there

machine_owned:
  site_prework_claim_gate: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  sovereign_heartbeat_runtime: StegVerse-Labs/.github#12 + #60
  sovereign_base_continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
  sovereign_local_model_live_activation: StegVerse-Labs/.github#60 + StegVerse-Labs/TVC/tasks/TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002.json
```

## Cross-repository propagation

```text
source: StegVerse-Labs/stegfin-governance#81 / task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json
Site integration: StegVerse-Labs/Site#388 / merge ec8b5136ff9281ea37e861281f9428c7c283fbe4
post-publication return: update StegVerse-Labs/stegfin-governance#81 + task-state to SOURCE_AND_SITE_RELEASED_CURRENT_PHONE_PROOF_REQUIRED
Publisher: no transaction/publication contract requires propagation yet
admissibility-wiki: no doctrine change required from compatibility integration alone
stegguardian-wiki: no guardian contract change required from compatibility integration alone
master-records: receives live transaction/settlement continuity only if/when USER_ONLY transaction evidence exists; none exists now
```

## Completion accounting

```text
required product/control files: 4
implemented: 4/4
scaffolding or stubs: 0
missing required files: 0
static validation predicates: 6/6 established
hosted canonical validation cycle: 0/4 successful; runner/startup failure retained explicitly
repository integration: source merge + Site merge = COMPLETE
publication proof: PENDING
current-phone wallet-browser proof: PENDING
wallet signature/broadcast: NOT EXECUTED / USER_ONLY
goal activation: NOT COMPLETE
session consolidation: all unique state is durable, but this session still owns publication-proof observation until it is transferred or completed
```

MERGED PREDECESSOR: `SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` remains released.

MERGED ORIGINAL LOCAL-MODEL GOAL INTO: `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md` + machine-owned activation chain.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + this handoff for publication proof, then `StegVerse-Labs/stegfin-governance#81` + `task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json` + current phone/USER_ONLY for live proof.
