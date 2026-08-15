# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-15T17:01:00-05:00

## Canonical scope

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
parent_goal: STEGFIN-PHONE-DIRECT-ROUTE-010
originating_goal: If trading cannot begin now, expose the already-released StegVerse phone-sovereign preparation path on the participant-facing Site without Render or non-TV/TVC credentials.
repository: StegVerse-Labs/Site
canonical_branch: main
canonical_intake_issue: StegVerse-Labs/Site#261
canonical_live_activation_issue: StegVerse-Labs/stegfin-governance#60
pull_request: #276
merge_commit: 8b5319705dcf02c8edc8dd1612e9787cf70386a1
prework_claim: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
implementation_state: COMPLETE_VALIDATED_MERGED_RELEASED
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

## Installed participant path

Canonical participant entry:

```text
https://stegverse.org/stegfin-trade.html
```

Execution chain:

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

The Site is a static projection/delivery surface. It does not execute the trade on a server. The current phone executes the browser-local preparation path after the participant gesture.

## Exact copied upstream blobs

```text
assets/stegfin-phone/phone-direct-route.js             87c39b623724c4c7f637f3747d7f8b965a6bad3a
assets/stegfin-phone/stegid-device-wallet-bootstrap.js 01df37b655f1dae8650c9102ffbd85f72432c47f
assets/stegfin-phone/device-wallet-identity.js          0f18f416dee3d2707ac47964a6b24fe918d6ef68
assets/stegfin-phone/app.js                             ade469ac61df37da46bef1376cfdbb10d3c9b5f1
assets/stegfin-phone/styles.css                         3a91c67d6088f75a93955a260985ce686eb5698f
```

The dedicated validator recomputes Git blob identities and fails on drift.

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

The public Site host delivers static files only and is not the sovereign production execution runtime for this path.

## Validation and publication evidence

```text
PR #276 merge: 8b5319705dcf02c8edc8dd1612e9787cf70386a1
Check StegFin Phone Projection: run 31910836065 SUCCESS
Ecosystem Heartbeat Orchestration: run 31910836030 SUCCESS
Site Handoff Orchestrator: run 31910836202 SUCCESS
Site Bootstrap Validate: run 31910836064 SUCCESS
Site pre-work claim validator: PASS
exact upstream asset blob validation: PASS
no-token/non-authorizing workflow guard: PASS
GitHub Pages status: built
GitHub Pages source: main:/
GitHub Pages CNAME: stegverse.org
GitHub Pages exact build: 1153781444
GitHub Pages build commit: 8b5319705dcf02c8edc8dd1612e9787cf70386a1
```

This is publication evidence for the participant entry. It is not evidence that the phone has executed WebAuthn, observed current wallet state, produced `WALLET_HANDOFF_READY`, signed, broadcast, or settled anything.

## Collision and claim disposition

```yaml
task_id: SITE-STEGFIN-PHONE-PROJECTION-261
claim_id: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
role: RELEASED_IMPLEMENTATION
state: MERGED_INTO_CANONICAL_WORKSTREAM
release_evidence:
  - PR #276 merge 8b5319705dcf02c8edc8dd1612e9787cf70386a1
  - validation runs 31910836065, 31910836030, 31910836202, 31910836064 SUCCESS
  - Pages build 1153781444 built from exact merge
next_owner: StegVerse-Labs/stegfin-governance#60 phone participant activation lane
```

Do not duplicate the upstream phone carrier, StegID device bootstrap, TVC route, G18 runtime activation, MCP exact-artifact worker, provider route, signer, or broadcaster.

## Discoverability decision

The earlier branch handoff listed a `stegfinco.html` link as an optional discoverability integration. That mutation is **explicitly superseded** by the independently addressable participant entry `stegfin-trade.html`, because no functional or authority requirement requires rewriting the existing StegFinCo landing page. This minimizes mutable Site surface while still providing the exact current-phone entry. Site #261 and StegFin #60 now durably record the canonical URL.

## Live activation boundary

Source, validation, merge and publication are complete. The remaining live step is participant-owned and directly executable now from the current phone:

```text
open https://stegverse.org/stegfin-trade.html
-> select "Verify this phone and prepare wallet handoff"
-> complete platform WebAuthn/device verification
-> carrier persists either precise hash-bound BLOCKED evidence or WALLET_HANDOFF_READY
```

Successful terminal evidence must preserve:

```text
credential_authority=TV/TVC
credential_requirement=NONE
non_tv_tvc_secret_or_token_used=false
provider_secret_required=false
hosted_runtime_required=false
signed=false
broadcast=false
```

Issue `StegVerse-Labs/stegfin-governance#60` remains open until that actual phone evidence is observed. A `WALLET_HANDOFF_READY` receipt is not signing permission; review/sign/broadcast remains USER_ONLY.

## Completion accounting

```text
required developed projection surfaces: 8
complete developed projection surfaces: 8
scaffolding/stubs: 0
missing required files: 0
source validation: 3/3 PASS
Site integration: 3/3 COMPLETE
publication: 1/1 BUILT FROM EXACT MERGE
Site implementation claim: RELEASED
participant PREPARE execution: 0/1 pending current-phone gesture
terminal phone receipt: 0/1 pending current-phone execution
```

## Session consolidation / archive condition

This Site implementation no longer requires a ChatGPT execution lane. The unique Site projection requirement is installed, validated, merged, published, claim-released and transferred to the canonical phone activation observation surface. If this conversation remains active, it may only process actual phone evidence supplied by the participant; it must not create a competing phone, G18, TVC, MCP, provider, wallet, signing, or broadcast execution lane.

```text
MERGED INTO: StegVerse-Labs/stegfin-governance#60
MERGED INTO: StegVerse-Labs/Site#261
MERGED INTO: StegVerse-Labs/Site/docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
```
