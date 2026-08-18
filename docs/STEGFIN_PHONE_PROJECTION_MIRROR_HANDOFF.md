# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T21:44:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388
originating_session_goal: make the current-phone USER_ONLY wallet handoff continue after Safari proves no injected EIP-1193 provider, without Render, hosted wallet authority, or NON-TV/TVC credentials
repository: StegVerse-Labs/Site
branch: main
canonical_issue: #388
canonical_task_owner: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-PUBLISH
publication_claim: SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817 / CLAIMED_FOR_VALIDATION
publication_claim_created_at: 2026-08-17T19:54:00-05:00
publication_claim_release_condition: exact corrected public participant proof, then transfer to StegFin #81/current phone/USER_ONLY
released_integration_claim: SITE-STEGFIN-WALLET-BROWSER-WEBAUTHN-PROJECTION-388-20260817 / MERGED_INTO_CANONICAL_WORKSTREAM
source_owner: StegVerse-Labs/stegfin-governance#81
source_pr: #83
source_merge: 39cd7b144523063fe0c3046453e9920a6ad2dde6
source_bootstrap_blob: dc1a86bc564146cdaa645620c8fc698e45029440
source_ui_blob: 114b3c39052d5b1622407080407259a0040a1369
Site_projection_pr: #390
Site_projection_merge: 8c5882b2ff3a17c847d48376b856db32c0331832
publication_observer: scripts/check_stegfin_public_wallet_transport.py
publication_observer_extension: dab5cc136da9f01a6b15a822065da33959f4e5e2
publication_receipt: receipts/stegfin-ios-local-wallet-transport-388-validation.json
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

## Current-phone evidence

The current phone successfully opened the StegVerse participant in the MetaMask Mobile local wallet browser and reached `READY_TO_RUN_ON_DEVICE`. A fresh Verify/PREPARE then failed closed with `user-verifying platform authenticator unavailable`. That proved the local-wallet-browser transport is reachable and exposed the upstream compatibility defect now corrected by StegFin #81 PR #83.

The released correction preserves `userVerification: 'required'`, keeps the actual `navigator.credentials.create()` / `navigator.credentials.get()` ceremony authoritative, and treats `isUserVerifyingPlatformAuthenticatorAvailable()` only as advisory. No signature, broadcast, settlement, candidate transfer, or authority effect was produced by the prior failed current-phone attempt.

## Exact Site projection — COMPLETE

```text
source: StegVerse-Labs/stegfin-governance/ui/stegid-device-wallet-bootstrap.js
source merge: 39cd7b144523063fe0c3046453e9920a6ad2dde6
source blob: dc1a86bc564146cdaa645620c8fc698e45029440
destination: assets/stegfin-phone/stegid-device-wallet-bootstrap.js
destination blob: dc1a86bc564146cdaa645620c8fc698e45029440
projection PR: #390
projection final head: 14753722beeaa27ccd16fcda60f7883ae7d4fcaa
projection merge: 8c5882b2ff3a17c847d48376b856db32c0331832
integration task: data/tasks/SITE-STEGFIN-WALLET-BROWSER-WEBAUTHN-PROJECTION-388.json
integration claim: RELEASED / MERGED_INTO_CANONICAL_WORKSTREAM
```

### Validation evidence for PR #390

```text
Check StegFin Phone Projection run 32092420729: SUCCESS
Site Handoff Orchestrator run 32092420660: SUCCESS
Site Bootstrap Validate run 32092420772: SUCCESS
Ecosystem Heartbeat Orchestration run 32092420704: SUCCESS
```

The projection validator requires the exact corrected bootstrap blob, advisory UVPAA behavior, real WebAuthn create/get ceremonies, `userVerification: 'required'`, TV/TVC-only credential authority, no forbidden credential path, and unchanged USER_ONLY signing/broadcast.

## Publication proof automation — ACTIVE

Canonical observer: `scripts/check_stegfin_public_wallet_transport.py`.

The observer is bound to the existing credential-clean Site validation lane. It now verifies all three public surfaces:

```text
https://stegverse.org/stegfin-trade.html
https://stegverse.org/assets/stegfin-phone/wallet-user-handoff-ui.js
https://stegverse.org/assets/stegfin-phone/stegid-device-wallet-bootstrap.js
```

It requires:

```text
wallet UI Git blob: 114b3c39052d5b1622407080407259a0040a1369
corrected bootstrap Git blob: dc1a86bc564146cdaa645620c8fc698e45029440
platformAuthenticatorProbe present
UVPAA advisory marker present
navigator.credentials.create/get present
userVerification: 'required'
old unconditional user-verifying-platform-authenticator-unavailable precheck absent
TV/TVC credential authority
no GitHub token
no Render
no WalletConnect/provider/private-key path
```

Observer extension commit: `dab5cc136da9f01a6b15a822065da33959f4e5e2`.
Receipt binding: `receipts/stegfin-ios-local-wallet-transport-388-validation.json` at schema `v4`.

Publication remains fail-closed until a directly inspected main-push validation step returns `VERIFIED_PUBLICATION` for both exact blobs. Source merge, Site merge, workflow PASS, visual reachability, or a third-party deployment bot status does not substitute for that proof.

## Authority and collision boundaries

```text
no second publication observer
no second scheduler/heartbeat
no Render/Vercel/Cloudflare production authority
no NON-TV/TVC secret/token
no GitHub token runtime authority
no Safari candidate transfer through deeplink or hosted service
no automatic network switch
no automatic signing
no automatic broadcast
no settlement inference from transaction submission
```

Healer #16 is `CLOSED_NOT_PLANNED`. Healer #17 is `CLOSED_DUPLICATE`; its duplicate target is disabled. Site #388 remains the single publication-proof owner.

## Installed wallet-browser transition

```text
fresh current-device WebAuthn/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY handoff action
-> Safari lacks injected provider: fail closed; no wallet action
-> Open StegVerse in local wallet browser
-> navigation carries participant location only
-> no Safari candidate/calldata/hash/key/seed/signature/StegID capability transfer
-> NEW Verify/PREPARE inside wallet browser
-> UVPAA probe is advisory
-> actual WebAuthn ceremony with userVerification='required' determines HUMAN_CONTINUITY
-> fresh PREPARE only after successful ceremony
-> require injected EIP-1193 provider + Base 0x2105 + exact governed account
-> exact fresh candidate revalidation before eth_sendTransaction
-> wallet independently confirms/rejects
-> returned hash is SUBMITTED_NOT_SETTLED until receipt
-> USER_ONLY remains sole signing/broadcast authority
```

## Current completion state

```text
source WebAuthn compatibility correction: COMPLETE / MERGED
Site exact bootstrap projection: COMPLETE / VALIDATED / MERGED
Site projection integration claim: RELEASED
publication observer source: COMPLETE
publication observer corrected-bootstrap extension: COMPLETE
exact public corrected bootstrap observation: PENDING
current-phone MetaMask fresh WebAuthn/PREPARE: PENDING
governed injected provider observation: PENDING
USER_ONLY wallet review: PENDING
signature/broadcast/settlement: NOT EXECUTED
```

## Cross-repository continuation

```text
StegVerse-Labs/stegfin-governance#81 / PR #83 / merge 39cd7b144523063fe0c3046453e9920a6ad2dde6
-> StegVerse-Labs/Site#388 / PR #390 / merge 8c5882b2ff3a17c847d48376b856db32c0331832
-> canonical Site #388 public observer proves exact UI + corrected bootstrap blobs
-> StegVerse-Labs/stegfin-governance#81 + current phone + USER_ONLY
-> MetaMask local wallet browser NEW Verify/PREPARE
-> governed injected provider proof
-> USER_ONLY wallet review
```

Publisher is not pertinent until a transaction/release publication contract exists. `admissibility-wiki` and `stegguardian-wiki` require no compatibility-only doctrine update. `master-records` becomes pertinent only when actual USER_ONLY transaction/settlement evidence exists.

## Machine-owned work that must not be duplicated

```text
sovereign local model live activation: StegVerse-Labs/.github#60 + SHWP-DURABLE-RUNTIME-ACTIVATION + StegVerse-Labs/TVC/tasks/TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002.json
site publication validation: Site #388 active validation claim + scripts/check_stegfin_public_wallet_transport.py + .github/workflows/validate.yml
wallet signing/broadcast: USER_ONLY
```

## Exact next actions

1. Inspect the next main-push `Site Bootstrap Validate` execution after observer extension `dab5cc136da9f01a6b15a822065da33959f4e5e2`.
2. Accept publication only on direct `VERIFIED_PUBLICATION` evidence for both exact blobs.
3. Release the Site publication claim and propagate completion to StegFin #81 only after that proof.
4. Current phone then opens the corrected participant in MetaMask local wallet browser and performs a NEW Verify/PREPARE.
5. If the real WebAuthn ceremony fails, record the concrete ceremony error and do not weaken HUMAN_CONTINUITY.
6. If PREPARE succeeds, require governed injected EIP-1193 provider/Base/account proof and stop at USER_ONLY review unless the user explicitly signs/broadcasts.

## Completion accounting

```text
required developed product/control/observer files: 6
implemented: 6/6
scaffolding_or_stubs: 0
missing_required_files: 0
source compatibility validation: COMPLETE
Site projection validation: 4/4 PASS
repository integration: COMPLETE
publication automation: COMPLETE / EXECUTION PENDING
current-phone activation: PENDING
session consolidation: original model goal transferred; source fix durable; Site integration durable; publication/live proof canonicalized
```

MERGED ORIGINAL LOCAL-MODEL GOAL INTO: `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md` + machine-owned activation chain.

MERGED SOURCE COMPATIBILITY INTO: `StegVerse-Labs/stegfin-governance#81` / PR #83 / merge `39cd7b144523063fe0c3046453e9920a6ad2dde6`.

MERGED SITE INTEGRATION INTO: `StegVerse-Labs/Site#388` / PR #390 / merge `8c5882b2ff3a17c847d48376b856db32c0331832`.

CANONICAL CONTINUATION: `StegVerse-Labs/Site#388` + this handoff + `scripts/check_stegfin_public_wallet_transport.py` + `receipts/stegfin-ios-local-wallet-transport-388-validation.json` until exact public proof, then `StegVerse-Labs/stegfin-governance#81` + current phone + USER_ONLY.
