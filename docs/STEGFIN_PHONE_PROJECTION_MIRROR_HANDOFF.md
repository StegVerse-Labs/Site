# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T20:45:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
branch: main
claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
claim_state: CLAIMED_FOR_VALIDATION
product_state: SOURCE_AND_SITE_MERGED_AUTOMATED_PUBLICATION_PROOF_PENDING
site_execution_responsibility: STATIC_PARTICIPANT_PROJECTION + CREDENTIAL_FREE_PUBLICATION_OBSERVATION_ONLY
source_owner: StegVerse-Labs/stegfin-governance#81
source_task: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019
source_merge: 78b648b8414f8ca9f93f396bb20e96d049607227
site_issue: StegVerse-Labs/Site#388
site_pull_request: StegVerse-Labs/Site#389
site_merge: ec8b5136ff9281ea37e861281f9428c7c283fbe4
publication_observer: scripts/check_stegfin_public_wallet_transport.py
publication_observer_install: 64173cabc8a7b5cb72437b26c7f90f2970215f0e
publication_execution_lane: .github/workflows/validate.yml
publication_execution_binding: 6c1551a4ae5456f0e46d2c2c80cc7c382a97f54b
publication_receipt: receipts/stegfin-ios-local-wallet-transport-388-validation.json
publication_receipt_binding: a7705025ccf10cb0eac8f5caf1590085b39c18e4
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

## Converged goals

`SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380` is complete/released and is not restarted.

The session's original local-model/runtime objective is complete/released in `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`: the descriptive runtime-selection step has been superseded by executable local discovery/launch/inference/proof and formally developed local reference models. Remaining live model activation is MACHINE_OWNED by sovereign heartbeat -> TV/TVC -> LLM-adapter -> Master Records and must not be duplicated here.

A proposed fallback publication observer in `StegVerse-Labs/StegVerse-Healer#16` was superseded before implementation once the canonical Site validation lane gained an exact publication-observer binding. Healer #16 is closed `not_planned`; its branch must not merge. This prevents duplicate publication observers and a second scheduler surface.

## Installed wallet-browser transition

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY Hand exact candidate to wallet
-> injected provider exists: exact Base/account/freshness validation
-> Safari lacks provider: fail closed; no wallet action
-> expose Open StegVerse in local wallet browser
-> navigation carries only participant location
-> no Safari candidate/calldata/hash/key/seed/signature/StegID capability transfer
-> NEW phone verification/PREPARE inside wallet browser
-> require injected EIP-1193 provider + Base 0x2105 + exact governed account
-> exact candidate revalidation before eth_sendTransaction
-> wallet independently confirms/rejects
-> returned hash is SUBMITTED_NOT_SETTLED until receipt
-> fresh successor PREPARE after successful receipt
-> USER_ONLY remains sole signing/broadcast authority
```

Exact upstream and Site UI blob: `114b3c39052d5b1622407080407259a0040a1369`.

## Publication proof automation

The canonical observer is `scripts/check_stegfin_public_wallet_transport.py`. It checks public HTTPS for:

```text
https://stegverse.org/stegfin-trade.html
https://stegverse.org/assets/stegfin-phone/wallet-user-handoff-ui.js
```

It computes the Git blob SHA of the public UI, requires exact blob `114b3c39052d5b1622407080407259a0040a1369`, validates required participant and wallet-browser markers, and emits only `VERIFIED_PUBLICATION` or `BLOCKED`. It sets `authority_effect=false`, requires no GitHub token, and grants no runtime/wallet/publication authority.

The observer is now bound into the existing canonical Site validation lane rather than a new workflow. On a `push` to `main`, `.github/workflows/validate.yml` runs a bounded six-attempt public observation window with 20-second spacing and an ephemeral `/tmp` report. No artifact custody or repository writeback is introduced. The workflow already has `permissions: {}`, refuses credential-bearing environments, and fetches source anonymously.

```text
observer source commit: 64173cabc8a7b5cb72437b26c7f90f2970215f0e
claim execution-surface update: 1669813c5535cc852898aae1bce3cab6273c0cd8
workflow binding commit: 6c1551a4ae5456f0e46d2c2c80cc7c382a97f54b
receipt binding commit: a7705025ccf10cb0eac8f5caf1590085b39c18e4
observer state: BOUND_EXECUTION_PENDING
```

Publication is not claimed until a directly inspected execution produces `VERIFIED_PUBLICATION` with the exact public UI blob.

## Validation evidence

```text
exact source/Site UI blob identity: PASS
no-injected-wallet fail-closed predicate: PASS
wallet-browser continuation bound to exact failure: PASS
navigation excludes transaction/candidate/key/seed/signature material: PASS
fresh wallet-browser PREPARE requirement: PASS
no automatic network switch/sign/broadcast: PASS
source merge: COMPLETE
Site merge: COMPLETE
credential-free publication observer source: COMPLETE
canonical validation-lane binding: COMPLETE
live publication observer execution: PENDING
current-phone wallet-browser proof: PENDING
```

Historical PR-head runs that exposed zero validator steps remain non-PASS evidence and are not reclassified. A later user-observed Site validation run did execute and identified the now-repaired claim-schema defect; no PASS is inferred from that failed run.

## Active ownership

```yaml
site_publication_validation:
  task_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-PUBLISH
  owner: StegVerse-Labs/Site#388
  claim_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817
  role: CLAIMED_FOR_VALIDATION
  claimed_surfaces:
    - docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
    - data/session-work-claims.json
    - receipts/stegfin-ios-local-wallet-transport-388-validation.json
    - scripts/check_stegfin_public_wallet_transport.py
    - .github/workflows/validate.yml
  release_condition: directly inspected main-push validation produces VERIFIED_PUBLICATION for exact UI blob and result is propagated to StegFin #81
  next_action: inspect the main-push Site Bootstrap Validate execution created after the automated observer binding

human_authority_live_proof:
  task_id: STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019-LIVE
  owner: StegVerse-Labs/stegfin-governance#77 + #81 + current phone + USER_ONLY
  state: BLOCKED_ON_PUBLICATION_PROOF
  release_condition: published participant -> Safari fail-closed -> local wallet-browser reopen -> NEW PREPARE -> governed injected provider -> USER_ONLY wallet review

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
superseded fallback: StegVerse-Labs/StegVerse-Healer#16 CLOSED_NOT_PLANNED
post-publication return: StegVerse-Labs/stegfin-governance#81 + task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json
Publisher: not pertinent until a transaction/release publication contract exists
admissibility-wiki: no compatibility-only doctrine change required
stegguardian-wiki: no compatibility-only guardian contract change required
master-records: only after live USER_ONLY transaction/settlement evidence exists
```

## Completion accounting

```text
required developed product/control/observer files: 5
implemented: 5/5
scaffolding or stubs: 0
missing required files: 0
static/repository validation predicates: 9/9
publication automation binding: COMPLETE
publication observer execution: PENDING
current-phone wallet-browser proof: PENDING
repository integration: COMPLETE
goal activation: NOT COMPLETE
session consolidation: original model goal transferred; Site implementation merged; duplicate Healer fallback superseded; publication validation remains this session's distinct role
```

MERGED PREDECESSOR: `SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380`.

MERGED ORIGINAL LOCAL-MODEL GOAL INTO: `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md` + machine-owned activation chain.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + this handoff + `scripts/check_stegfin_public_wallet_transport.py` + `.github/workflows/validate.yml` until publication proof, then `StegVerse-Labs/stegfin-governance#81` + `task-state/STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-019.json` + current phone/USER_ONLY.
