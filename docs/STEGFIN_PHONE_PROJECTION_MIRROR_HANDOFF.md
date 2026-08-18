# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T21:28:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
canonical_issue: #388
integration_branch: fix/stegfin-wallet-browser-webauthn-projection-388
integration_task: SITE-STEGFIN-WALLET-BROWSER-WEBAUTHN-PROJECTION-388
integration_claim: CLAIMED_FOR_INTEGRATION
publication_claim: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817 / CLAIMED_FOR_VALIDATION
source_owner: StegVerse-Labs/stegfin-governance#81
source_pr: #83
source_merge: 39cd7b144523063fe0c3046453e9920a6ad2dde6
source_bootstrap_blob: dc1a86bc564146cdaa645620c8fc698e45029440
source_ui_blob: 114b3c39052d5b1622407080407259a0040a1369
publication_observer: scripts/check_stegfin_public_wallet_transport.py
publication_execution_lane: .github/workflows/validate.yml
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

Site is a static participant projection and publication-observation surface only. It does not own wallet keys, signatures, broadcast, settlement, TV/TVC credential authority, sovereign model/runtime authority, or current-phone activation.

## Original session goal — transferred / complete at source scope

The descriptive local-model/runtime goal is complete and released in `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`. Executable discovery, local launch, real inference, proof, formal local language-model development, visual-evidence model development, and visual runtime are released there. Live activation remains MACHINE_OWNED by the resident sovereign heartbeat -> TV/TVC -> LLM-adapter/consumer -> Master Records chain. Do not duplicate that work here.

## Current-phone evidence that changed this Site task

The current phone successfully opened the StegVerse participant in the MetaMask Mobile local wallet browser and reached `READY_TO_RUN_ON_DEVICE`. A fresh Verify/PREPARE then failed closed with `user-verifying platform authenticator unavailable`. That observation proved the wallet-browser transport itself was reachable but exposed an upstream compatibility defect: the old bootstrap treated `PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable() == false` as a pre-ceremony authority decision.

StegFin #81 PR #83 corrected that behavior and merged at `39cd7b144523063fe0c3046453e9920a6ad2dde6`. The correction preserves `userVerification: 'required'`, keeps the actual `navigator.credentials.create()` / `navigator.credentials.get()` ceremony authoritative, and treats UVPAA only as an advisory probe. The exact released bootstrap Git blob is `dc1a86bc564146cdaa645620c8fc698e45029440`.

No signature, broadcast, settlement, candidate transfer, or authority effect was produced by the failed current-phone attempt.

## Exact Site projection

```text
source: StegVerse-Labs/stegfin-governance/ui/stegid-device-wallet-bootstrap.js
source merge: 39cd7b144523063fe0c3046453e9920a6ad2dde6
source blob: dc1a86bc564146cdaa645620c8fc698e45029440
destination: assets/stegfin-phone/stegid-device-wallet-bootstrap.js
projection commit: a6e2c0b6893ef17f646aa5430c44ab69cc2fd78a
validator: scripts/check_stegfin_phone_projection.py
validator commit: 53aeef115459013c79bcb772d1569cabc40164c1
claim record: data/tasks/SITE-STEGFIN-WALLET-BROWSER-WEBAUTHN-PROJECTION-388.json
claim commit: 0165e3f941bfdeb3ed362e0fffcde851bf99df67
```

The projection is exact: the destination blob is `dc1a86bc564146cdaa645620c8fc698e45029440`.

## Validator contract

`check_stegfin_phone_projection.py` now requires:

```text
exact upstream bootstrap blob dc1a86bc564146cdaa645620c8fc698e45029440
platformAuthenticatorProbe present
UVPAA described and enforced as advisory only
userVerification: 'required'
real navigator.credentials.create() ceremony
real navigator.credentials.get() ceremony
CREDENTIAL_CREATION returns HUMAN_CONTINUITY before later assertion path
absence of the old unconditional `user-verifying platform authenticator unavailable` pre-ceremony failure
TV/TVC credential authority
credential_requirement NONE
no NON-TV/TVC secret/token
no GitHub runtime credential
no WalletConnect/provider key/private key path
USER_ONLY signing/broadcast unchanged
```

## Installed wallet-browser transition

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY Hand exact candidate to wallet
-> Safari has no injected provider: fail closed; no wallet action
-> Open StegVerse in local wallet browser
-> navigation carries participant location only
-> no Safari candidate/calldata/hash/key/seed/signature/StegID capability transfer
-> NEW Verify/PREPARE inside local wallet browser
-> UVPAA probe is advisory
-> actual WebAuthn ceremony with userVerification='required' determines HUMAN_CONTINUITY
-> fresh PREPARE only after successful ceremony
-> require injected EIP-1193 provider + Base 0x2105 + exact governed account
-> exact candidate revalidation before eth_sendTransaction
-> wallet independently confirms/rejects
-> returned hash remains SUBMITTED_NOT_SETTLED until receipt
-> USER_ONLY remains sole signing/broadcast authority
```

## Publication proof ownership

The existing Site #388 publication-validation claim remains canonical and separate from this integration claim. It owns:

```text
docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
data/session-work-claims.json
receipts/stegfin-ios-local-wallet-transport-388-validation.json
scripts/check_stegfin_public_wallet_transport.py
.github/workflows/validate.yml
```

This integration branch does not create a second observer or scheduler and does not modify that active observer surface. The publication owner must accept the new bootstrap projection only after merge and then prove the corrected public participant before the phone retest. The existing wallet UI publication predicate remains exact UI blob `114b3c39052d5b1622407080407259a0040a1369`; the corrected bootstrap must additionally be present in the published participant before current-phone continuation is considered unblocked.

## Collision and authority boundaries

```text
no second publication observer
no second scheduler/heartbeat
no Render/Vercel/Cloudflare production authority
no NON-TV/TVC secret/token
no GitHub token runtime authority
no candidate transfer through deeplink or hosted service
no automatic network switch
no automatic signing
no automatic broadcast
no settlement inference from tx submission
```

Healer #16 is `CLOSED_NOT_PLANNED`. Healer #17 is `CLOSED_DUPLICATE`, and its duplicate target is disabled. Site #388 is the single publication owner.

## Validation evidence

```text
StegFin #81 PR #83 merge: COMPLETE
exact source bootstrap blob identified: PASS
exact Site bootstrap projection on integration branch: PASS
projection validator updated for advisory-UVPAA contract: IMPLEMENTED
branch validation execution: PENDING
integration PR: #390 OPEN
merge to Site main: PENDING
public corrected bootstrap observation: PENDING
current-phone MetaMask browser fresh Verify/PREPARE: PENDING
signature/broadcast/settlement: NOT EXECUTED / USER_ONLY
```

## Released projection anchors retained for validator continuity

These anchors describe already-released predecessor capabilities and are retained so the canonical projection validator proves that the new compatibility fix did not erase prior product lineage:

```text
STEGFIN-PHONE-DIRECT-ROUTE-011
STEGFIN-PHONE-RPC-RESILIENCE-012
SITE-STEGFIN-PHONE-PROJECTION-261
SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
STEGFIN-PHONE-STEGID-FRESHNESS-016
TASK-2026-0004
Site#282
COMPLETE_INSTALLED
31ed79cb56e8d2366e6d70f22e28c70162c88fd8
290b567eca2cc9f83e7438a80682ebaf8006ad76
bcba49976a52024a233f998ce290ec4ab42618ff
STEGFIN-PHONE-WALLET-REVIEW-014
433ef5e5db9f9f7af2c7c7df4ba01acc89125403
1180d8ee929c161978d095c91514cbc3d873d3fd
29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
StegFin PR #75
USER_ONLY wallet review
Copy canonical evidence
unexpired
SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
StegFin #79
CREDENTIAL_CREATION
CREDENTIAL_ASSERTION
```

## Cross-repository continuation

```text
StegVerse-Labs/stegfin-governance#81 / PR #83 / merge 39cd7b144523063fe0c3046453e9920a6ad2dde6
-> StegVerse-Labs/Site#388 / fix/stegfin-wallet-browser-webauthn-projection-388
-> exact bootstrap projection dc1a86bc564146cdaa645620c8fc698e45029440
-> Site projection validation
-> merge to main
-> canonical Site #388 publication validation
-> current phone MetaMask browser NEW Verify/PREPARE
-> governed injected provider proof
-> USER_ONLY wallet review
```

Publisher is not pertinent until a transaction/release publication contract exists. `admissibility-wiki` and `stegguardian-wiki` do not require a compatibility-only doctrine update. `master-records` becomes pertinent only when actual USER_ONLY transaction/settlement evidence exists.

## Machine-owned work that must not be duplicated

```text
sovereign local model live activation: StegVerse-Labs/.github#60 + SHWP-DURABLE-RUNTIME-ACTIVATION + StegVerse-Labs/TVC/tasks/TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002.json
site publication validation: StegVerse-Labs/Site#388 active validation claim
wallet signing/broadcast: USER_ONLY
```

## Exact next actions

1. Execute `python scripts/check_stegfin_phone_projection.py` against this branch through the strongest available validation surface.
2. Repair only branch-local projection/validator defects if found.
3. Inspect Site PR #390 validation jobs and logs; do not infer PASS from PR state.
4. Merge only after adequate validation and current branch freshness.
5. Return to the existing Site #388 publication-validation owner to prove the corrected bootstrap is publicly served.
6. After publication proof, current phone repeats MetaMask-browser fresh Verify/PREPARE. Signing and broadcast remain USER_ONLY.

## Completion accounting

```text
required integration files: 4
implemented: 4/4
scaffolding_or_stubs: 0
missing_required_files: 0
source projection: PASS
branch validation: ACTIVE
integration: 1/2 (PR open; merge pending)
publication: PENDING
current-phone proof: PENDING
session consolidation: original local-model goal durable; wallet compatibility source durable; Site integration active; publication/live proof remain canonical continuation
```

MERGED ORIGINAL LOCAL-MODEL GOAL INTO: `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md` + machine-owned activation chain.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + this handoff + `data/tasks/SITE-STEGFIN-WALLET-BROWSER-WEBAUTHN-PROJECTION-388.json` for Site integration, then existing Site #388 publication validation, then `StegVerse-Labs/stegfin-governance#81` + current phone + USER_ONLY.
