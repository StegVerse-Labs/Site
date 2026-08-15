# StegFin Phone Participant Surface Mirror Handoff

Updated: 2026-08-15T17:02:00-05:00

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
originating_goal: expose the released sole-phone StegVerse trade-preparation carrier on StegVerse itself so the authorized iPhone can produce current-device PREPARE and WALLET_HANDOFF_READY evidence
repository: StegVerse-Labs/Site
branch: feat/stegfin-phone-participant-surface-261
canonical_issue: #261
canonical_owner: Site participant-surface integration lane
active_implementation_claim: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
active_validation_claim: same bounded claim; no separate validator claimant
claim_created_at: 2026-08-15T17:01:00-05:00
claim_release_condition: exact upstream assets projected + source manifest and validator PASS + PR merged + Site #261 reconciled
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
render_required: false
hosted_runtime_required: false
```

## Source of truth

Read this with:

1. `data/session-work-claims.json` claim `SITE-STEGFIN-PHONE-PROJECTION-261-20260815`;
2. `StegVerse-Labs/stegfin-governance/docs/STEGFIN_PHONE_DIRECT_ROUTE_MIRROR_HANDOFF.md`;
3. `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-PHONE-DIRECT-ROUTE-011.json`;
4. `StegVerse-Labs/stegfin-governance/issues/60`;
5. `StegVerse-Labs/Site/issues/261`;
6. `stegfin-phone/source-manifest.json` after installation.

Live repository state and exact source blobs supersede chat descriptions.

## Collision state

Site's pre-work registry was inspected before mutation. `SITE-PREWORK-CLAIM-GATE-MACHINE-001` owns orchestration admission only. Historical HIL post-submit and workflow-minimization claims are released/merged. The new claim uses the distinct dependency surface `site:stegfin-phone-participant-surface` and does not alter HIL, Site #67/#81, workflow-minimization, TV/TVC, or machine pre-work ownership.

## Canonical upstream release

```text
StegFin hardening task: STEGFIN-PHONE-DIRECT-ROUTE-011
StegFin PR: #62
merge: e19f64ca53699cc626cf05524ff8398544696067
source issue: #61 CLOSED_COMPLETED
live terminal observer: StegFin #60 OPEN
phone source blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
StegID bootstrap blob: 01df37b655f1dae8650c9102ffbd85f72432c47f
identity gate blob: 0f18f416dee3d2707ac47964a6b24fe918d6ef68
operator app blob: ade469ac61df37da46bef1376cfdbb10d3c9b5f1
operator HTML blob: 8cff3f6efae7261822559ca0c7ba1b44c4cd5ce2
styles blob: 3a91c67d6088f75a93955a260985ce686eb5698f
```

The corrected phone source performs bounded current-block Inventory N observation only for native ETH gas reserve, USDC sell balance, and WETH buy/current-position balance. It no longer performs block-0 historical `eth_getLogs` discovery and explicitly does not claim exhaustive wallet-asset enumeration.

## Participant path

```text
stegverse.org/stegfin-phone/
-> user gesture on this authorized phone
-> non-exportable StegID device key
-> platform WebAuthn user verification
-> current-device DEVICE_ADMITTED
-> OBSERVE + PREPARE wallet capability only
-> bounded Base ETH/USDC/WETH Inventory N
-> TV/TVC ROUTE_ADMITTED / credential_requirement NONE
-> direct pinned Uniswap V3 eth_call quote
-> exact allowance
-> exact approval or swap candidate
-> exact native gas-reserve sufficiency + <=$1 gas
-> read-only eth_call simulation
-> unsigned wallet handoff
-> WALLET_HANDOFF_READY
-> STOP
-> USER_ONLY signing/broadcast
```

Failures persist a local hash-bound `BLOCKED` receipt. Site projects browser source only. It does not receive provider, credential, wallet, route, signing, broadcast, settlement, or trade authority.

## Authoritative Site files

```text
stegfin-phone/index.html
stegfin-phone/phone-direct-route.js
stegfin-phone/stegid-device-wallet-bootstrap.js
stegfin-phone/device-wallet-identity.js
stegfin-phone/app.js
stegfin-phone/styles.css
stegfin-phone/source-manifest.json
scripts/check_stegfin_phone_participant_surface.py
data/session-work-claims.json
docs/STEGFIN_PHONE_PARTICIPANT_SURFACE_MIRROR_HANDOFF.md
```

## Validation

The validator must prove:
- exact upstream source manifest and release commit;
- exact local file SHA-1 blobs after projection;
- no active `eth_getLogs` historical inventory path;
- bounded ETH/USDC/WETH Inventory N markers;
- current-device StegID/WebAuthn + PREPARE-only capability;
- TV/TVC credential authority and `credential_requirement=NONE`;
- no GitHub/provider/wallet secret input;
- no Render/Vercel/Cloudflare hosted production dependency;
- `WALLET_HANDOFF_READY` remains unsigned/unbroadcast and USER_ONLY thereafter.

Hosted GitHub validation is non-authorizing. If anonymous private checkout prevents it from running, that is not product/runtime failure and must not be bypassed by adding a non-TV/TVC credential.

## Remaining work

1. Materialize exact released browser assets and source manifest on this branch.
2. Install and execute the strongest available deterministic/static Site validation.
3. Open/merge the Site PR when validation and claim checks allow it.
4. Reconcile Site #261 and release the implementation claim.
5. Actual device-local WebAuthn and live Base preparation require an explicit user gesture on the authorized phone; StegFin #60 owns terminal observation. Signing and broadcast remain USER_ONLY.

## Completion accounting

```text
developed files: 2/10 (claim registry + handoff)
scaffolding_or_stubs: 0
missing required files: 8
validation: 0/2 (claim/source validator + exact projection validation)
integration: 1/3 (claim admitted; source projection + merged public surface pending)
goal_activation: 20%
session_consolidation: active until participant surface is merged/transferred
```
