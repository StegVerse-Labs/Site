# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T20:35:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
branch: main
claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
claim_state: CLAIMED_FOR_VALIDATION
product_state: SOURCE_AND_SITE_MERGED_PUBLICATION_OBSERVER_INSTALLED
site_execution_responsibility: STATIC_PARTICIPANT_PROJECTION + CREDENTIAL_FREE_PUBLICATION_OBSERVATION_ONLY
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

Site is transport/materialization and publication observation only. Site never owns wallet keys, signatures, broadcast, settlement, TV/TVC credential authority, sovereign model/runtime authority, or current-phone activation.

## Converged and completed predecessor goals

`SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` is complete/released and is not restarted. Its release enabled the current phone to reach a fresh `WALLET_HANDOFF_READY` state.

The session's original local-model/runtime objective is also complete/released in `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`: the descriptive runtime-selection step has been superseded by executable discovery/launch/inference/proof and formally developed local reference models. Remaining live model activation is MACHINE_OWNED by sovereign heartbeat -> TV/TVC -> LLM-adapter -> Master Records and must not be duplicated in Site.

## Installed iOS wallet transport

Upstream release:

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
validation receipt: receipts/stegfin-ios-local-wallet-transport-388-validation.json
publication observer: scripts/check_stegfin_public_wallet_transport.py
publication observer install: 64173cabc8a7b5cb72437b26c7f90f2970215f0e
validation receipt update: 0d263423c7616a4f4405e2981b7c903ef905fc1d
```

Installed transition:

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY Hand exact candidate to wallet
-> if injected EIP-1193 provider exists: exact chain/account/freshness validation
-> if Safari has no provider: fail closed; no wallet action occurs
-> expose Open StegVerse in local wallet browser
-> open only the StegVerse participant location
-> DO NOT transfer Safari candidate/calldata/hash/key/seed/signature/StegID capability
-> NEW phone verification/PREPARE inside wallet-browser context
-> require injected EIP-1193 provider there
-> require Base 0x2105 + exact governed account
-> exact fresh candidate validation before eth_sendTransaction
-> wallet independently confirms or rejects
-> returned tx hash remains SUBMITTED_NOT_SETTLED until Base receipt
-> successful receipt invalidates predecessor quote/simulation/candidate
-> explicit fresh successor PREPARE
-> successor again stops at WALLET_HANDOFF_READY / USER_ONLY
```

## Authority boundary

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

The wallet-browser navigation is not transaction authority and cannot make the Safari candidate signable in the second context.

## Validation evidence

Established directly:

```text
exact source/Site UI blob identity: PASS
no-injected-wallet fail-closed predicate: PASS
wallet-browser continuation bound to exact failure: PASS
wallet-browser navigation excludes transaction request/candidate/key/seed/signature: PASS by validator/source inspection
fresh PREPARE requirement: PASS
no auto network switch/sign/broadcast: PASS
source merge: COMPLETE
Site merge: COMPLETE
credential-free publication observer: INSTALLED
```

GitHub-hosted PR-head observation remains non-PASS evidence:

```text
Check StegFin Phone Projection: 32083442727 FAILURE / zero exposed steps
Site Handoff Orchestrator: 32083442734 FAILURE / zero exposed steps
Site Bootstrap Validate: 32083442769 FAILURE / zero exposed steps
Ecosystem Heartbeat Orchestration: 32083442854 FAILURE / zero exposed steps
```

No validator failure and no validator PASS is inferred from those zero-step runs. No token workaround is authorized.

## Publication observer automation

`script: scripts/check_stegfin_public_wallet_transport.py`

Trigger: execute from any networked StegVerse-owned observer with ordinary public HTTPS reachability.

Inputs:

```text
https://stegverse.org/stegfin-trade.html
https://stegverse.org/assets/stegfin-phone/wallet-user-handoff-ui.js
expected Site merge: ec8b5136ff9281ea37e861281f9428c7c283fbe4
expected UI blob: 114b3c39052d5b1622407080407259a0040a1369
```

Deterministic outputs:

```text
VERIFIED_PUBLICATION or BLOCKED
stegfin-public-wallet-transport.report.json
observed HTTP/TLS state
observed UI Git blob SHA
required public-page and compatibility markers
credential_requirement NONE
github_token_required false
authority_effect false
```

The observer fails closed if HTTP/TLS, exact blob identity, or required participant markers are absent. It does not sign, broadcast, switch networks, create wallet authority, use a GitHub token, or create a hosted production dependency.

## Active claims

```yaml
site_publication_validation:
  task_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-PUBLISH
  owner: StegVerse-Labs/Site#388
  claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
  role: CLAIMED_FOR_VALIDATION
  claim_created_at: 2026-08-17T19:54:00-05:00
  claimed_surfaces:
    - docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
    - data/session-work-claims.json
    - receipts/stegfin-ios-local-wallet-transport-388-validation.json
    - scripts/check_stegfin_public_wallet_transport.py
  release_condition: publication observer returns VERIFIED_PUBLICATION for exact UI blob and result is propagated to StegFin #81
  next_action: execute the credential-free publication observer from a networked StegVerse observer

human_authority_live_proof:
  task_id: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019-LIVE
  owner: StegVerse-Labs/stegfin-governance#77 + #81 + current phone + USER_ONLY
  state: BLOCKED_ON_PUBLICATION_PROOF
  release_condition: published participant -> Safari fail-closed -> local wallet-browser reopen -> NEW PREPARE -> governed injected provider -> USER_ONLY wallet review
  next_action: only after VERIFIED_PUBLICATION, perform the current-phone sequence

machine_owned_do_not_compete:
  site_prework_claim_gate: data/session-work-claims.json#SITE-PREWORK-CLAIM-GATE-MACHINE-001
  sovereign_heartbeat_runtime: StegVerse-Labs/.github#12 + #60
  sovereign_base_continuation: StegVerse-Labs/.github/tasks/TASK-2026-0005.json
  sovereign_local_model_live_activation: StegVerse-Labs/.github#60 + StegVerse-Labs/TVC/tasks/TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002.json
```

## Cross-repository propagation

```text
source authority: StegVerse-Labs/stegfin-governance#81
Site integration/publication proof: StegVerse-Labs/Site#388 + this handoff + publication observer
post-publication return: governance #81 + task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json
Publisher: not pertinent until a transaction/release publication contract exists
admissibility-wiki: no compatibility-only doctrine change required
stegguardian-wiki: no compatibility-only guardian contract change required
master-records: only after live USER_ONLY transaction/settlement evidence exists
```

## Validation commands

```text
python3 scripts/check_stegfin_user_wallet_handoff_projection.py
python3 scripts/check_stegfin_public_wallet_transport.py
```

## Completion accounting

```text
required developed product/control/observer files: 5
implemented: 5/5
scaffolding or stubs: 0
missing required files: 0
static/repository validation predicates: 7/7
credential-free publication observer installation: COMPLETE
publication observer execution: PENDING
current-phone wallet-browser proof: PENDING
wallet signature/broadcast: NOT EXECUTED / USER_ONLY
repository integration: COMPLETE
goal activation: NOT COMPLETE
session consolidation: all unique requirements are durable; this session retains distinct publication/live-validation responsibility until observer execution or explicit transfer
```

MERGED PREDECESSOR: `SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380`.

MERGED ORIGINAL LOCAL-MODEL GOAL INTO: `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md` + machine-owned activation chain.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + this handoff + `scripts/check_stegfin_public_wallet_transport.py` until publication proof, then `StegVerse-Labs/stegfin-governance#81` + `task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json` + current phone/USER_ONLY.
