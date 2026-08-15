# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-15T16:49:00-05:00

## Canonical scope

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
parent_goal: STEGFIN-PHONE-DIRECT-ROUTE-010
originating_goal: If trading cannot begin now, expose the already-released StegVerse phone-sovereign preparation path on the participant-facing Site without Render or non-TV/TVC credentials.
repository: StegVerse-Labs/Site
branch: feat/stegfin-phone-participant-projection-20260815
canonical_intake_issue: StegVerse-Labs/Site#261
canonical_live_activation_issue: StegVerse-Labs/stegfin-governance#60
prework_claim: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
claim_state: CLAIMED_FOR_IMPLEMENTATION
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
GitHub token runtime authority: NONE
Render production runtime: PROHIBITED
wallet signing authority: USER_ONLY
broadcast authority: USER_ONLY
```

`SITE_MIRROR_HANDOFF.md` remains the canonical repository parent. `docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md` remains authoritative for Site mutation admission. This handoff is bounded to the participant-facing projection of the released phone route and creates no new StegFin, StegID, TV/TVC, wallet, provider, settlement, signing, broadcast, or Master Records authority.

## Upstream source of truth

```text
StegFin handoff: StegVerse-Labs/stegfin-governance/docs/STEGFIN_PHONE_DIRECT_ROUTE_MIRROR_HANDOFF.md
StegFin issue: StegVerse-Labs/stegfin-governance#60
StegFin source merge: 06c9c01d9253dcd39ce1206bdc2326fb4722c017
StegID current-phone bootstrap merge: 6a61dd291f7b66db31f1bb348975d8f829fca249
TVC credential-free direct-route merge: a00e52e3cde60c08969e22cf11aeba3971172108
```

The upstream phone carrier is already source-complete and statically validated. It executes preparation in the current browser on the current phone. Site only publishes the exact released executable assets plus a participant-facing HTTPS entry point.

## Exact copied upstream blobs

```text
assets/stegfin-phone/phone-direct-route.js            87c39b623724c4c7f637f3747d7f8b965a6bad3a
assets/stegfin-phone/stegid-device-wallet-bootstrap.js 01df37b655f1dae8650c9102ffbd85f72432c47f
assets/stegfin-phone/device-wallet-identity.js         0f18f416dee3d2707ac47964a6b24fe918d6ef68
assets/stegfin-phone/app.js                            ade469ac61df37da46bef1376cfdbb10d3c9b5f1
assets/stegfin-phone/styles.css                        3a91c67d6088f75a93955a260985ce686eb5698f
```

The projection validator computes Git blob identities locally and fails if any copied production asset drifts from those upstream values.

## Participant path

```text
stegfin-trade.html
-> exact phone-direct-route.js
-> exact StegID current-phone bootstrap
-> exact device-wallet identity/capability guard
-> exact StegFin operator app
-> user gesture on this phone
-> non-exportable browser-local P-256 device possession
-> platform WebAuthn HUMAN_CONTINUITY
-> DEVICE_ADMITTED
-> OBSERVE + PREPARE only
-> TV/TVC ROUTE_ADMITTED / credential_requirement=NONE
-> credential-free Base JSON-RPC observation
-> pinned Uniswap V3 quote / exact allowance
-> exact approval OR swap candidate
-> <=50 bps slippage
-> <=$1 gas estimate
-> read-only eth_call simulation
-> unsigned wallet handoff
-> WALLET_HANDOFF_READY
-> STOP
-> USER_ONLY review/sign/broadcast
```

The Site is a projection and HTTPS delivery surface. It does not execute the trade on a server. The current phone executes the browser-local preparation path after the participant gesture.

## Authority invariants

```text
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
provider_secret_required: false
provider_secret_export_allowed: false
GitHub token runtime authority: NONE
hosted runtime authority: NONE
Render production runtime: PROHIBITED
Vercel production runtime: PROHIBITED
Cloudflare production runtime: PROHIBITED
GitHub Actions production runtime: PROHIBITED
wallet signing authority: USER_ONLY
broadcast authority: USER_ONLY
automatic signing: false
automatic broadcast: false
settlement authority created by Site: false
Master Records authority created by Site: false
```

Static Site publication does not convert the web host into a StegVerse production execution runtime. All effect-capable wallet operations remain outside Site and outside ChatGPT.

## Current claim and collision partition

```yaml
task_id: SITE-STEGFIN-PHONE-PROJECTION-261
claim_id: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
role: IMPLEMENTATION
state: CLAIMED_FOR_IMPLEMENTATION
branch: feat/stegfin-phone-participant-projection-20260815
claimed_paths:
  - data/session-work-claims.json
  - stegfinco.html
  - stegfin-trade.html
  - assets/stegfin-phone/
  - docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
  - scripts/check_stegfin_phone_projection.py
  - .github/workflows/check-stegfin-phone-projection.yml
release_condition: validated merge to main, otherwise bounded expiration with exact BLOCKED evidence
```

Do not duplicate the upstream phone carrier, StegID device bootstrap, TVC route, G18 runtime activation, MCP exact-artifact worker, provider route, signer, or broadcaster. The existing Site machine pre-work gate owns orchestration admission only and does not conflict with this bounded product projection.

## Validation commands

```text
python3 scripts/check_session_work_claims.py
python3 scripts/check_stegfin_phone_projection.py
```

The dedicated workflow must use `permissions: {}` and anonymous checkout with no GitHub credential token. Hosted validation proves source/projection predicates only; it cannot produce current-phone WebAuthn, current wallet state, `WALLET_HANDOFF_READY`, signing, broadcast, or production runtime activation.

## Completion accounting — current branch

```text
required developed projection surfaces: 8
complete developed projection surfaces before workflow/link completion: 7
scaffolding/stubs: 0
missing source functionality: 0
validation implementation: installed
validation execution: pending
Site source integration: in progress
live phone PREPARE: pending participant gesture
WALLET_HANDOFF_READY: pending live phone execution
```

Required developed surfaces are: five exact mirrored upstream assets, `stegfin-trade.html`, deterministic projection validator, and validation workflow. The existing `stegfinco.html` link is an integration/discoverability obligation and is not counted as a new executable source surface.

## Integration and propagation obligations

1. Validate the exact copied asset hashes and authority invariants.
2. Expose the new participant entry from `stegfinco.html` without copying any wallet/provider/credential authority into the parent page.
3. Merge only after Site claim/orchestration validation passes.
4. Release the Site implementation claim with merge evidence.
5. Update Site #261 to the merged participant path.
6. Update StegFin #60 that the phone execution entry is available; issue #60 remains open until actual phone PREPARE plus terminal `BLOCKED` or `WALLET_HANDOFF_READY` evidence exists.

No Publisher, admissibility-wiki, stegguardian-wiki, or Master Records propagation is required merely to expose this bounded participant preparation entry.

## Live release condition

Source/projected availability is complete only after merged-main publication is verified. Trade readiness remains live-state dependent:

```text
current phone performs WebAuthn/device possession
AND valid StegID PREPARE capability is retained
AND direct carrier persists either:
  WALLET_HANDOFF_READY
OR
  precise hash-bound BLOCKED receipt
```

A successful terminal receipt must preserve:

```text
credential_authority=TV/TVC
credential_requirement=NONE
non_tv_tvc_secret_or_token_used=false
provider_secret_required=false
hosted_runtime_required=false
signed=false
broadcast=false
```

## Archive condition

This session is not archive-ready while the Site projection claim is active. After validated merge, claim release, canonical issue reconciliation, and verified participant-path availability, the source/integration role is complete. If the only remaining boundary is actual platform WebAuthn/current-phone execution, that boundary belongs to the phone participant and StegFin issue #60 rather than to a competing ChatGPT execution lane.
