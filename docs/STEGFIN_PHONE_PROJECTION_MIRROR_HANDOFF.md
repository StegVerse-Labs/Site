# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-15T17:10:00-05:00

## Canonical scope

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
active_hardening_goal: SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING
parent_goal: STEGFIN-PHONE-DIRECT-ROUTE-011
originating_goal: expose the StegVerse phone-sovereign preparation path on the participant-facing Site without Render or non-TV/TVC credentials, and keep that projection bound to the currently released phone carrier
repository: StegVerse-Labs/Site
canonical_branch: main
hardening_branch: fix/stegfin-phone-bounded-inventory-projection-261
canonical_intake_issue: StegVerse-Labs/Site#261
canonical_live_activation_issue: StegVerse-Labs/stegfin-governance#60
original_projection_pr: #276
original_projection_merge: 8b5319705dcf02c8edc8dd1612e9787cf70386a1
released_projection_claim: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
active_hardening_claim: SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815
hardening_claim_state: CLAIMED_FOR_IMPLEMENTATION
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
GitHub token runtime authority: NONE
Render production runtime: PROHIBITED
wallet signing authority: USER_ONLY
broadcast authority: USER_ONLY
```

`SITE_MIRROR_HANDOFF.md` remains the canonical repository parent. `docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md` remains authoritative for Site mutation admission. This handoff is bounded to participant-facing projection only and creates no new StegFin, StegID, TV/TVC, wallet, provider, settlement, signing, broadcast, or Master Records authority.

## Upstream source of truth

The original Site projection was correctly released through PR #276, but it copied the first released phone carrier blob. During subsequent live-executability review, StegFin task `STEGFIN-PHONE-DIRECT-ROUTE-011` found that the carrier's prior Inventory N logic attempted block-0 historical ERC-20 Transfer-log discovery. That was not a suitable bounded prerequisite for the authorized iPhone. The upstream carrier was hardened and released before actual phone activation.

```text
StegFin handoff: StegVerse-Labs/stegfin-governance/docs/STEGFIN_PHONE_DIRECT_ROUTE_MIRROR_HANDOFF.md
StegFin live activation observer: StegVerse-Labs/stegfin-governance#60
StegFin hardening issue: StegVerse-Labs/stegfin-governance#61 CLOSED_COMPLETED
StegFin hardening PR: #62
StegFin hardening merge: e19f64ca53699cc626cf05524ff8398544696067
StegFin hardening task: STEGFIN-PHONE-DIRECT-ROUTE-011 COMPLETE_RELEASED
StegID current-phone bootstrap merge: 6a61dd291f7b66db31f1bb348975d8f829fca249
TVC credential-free direct-route merge: a00e52e3cde60c08969e22cf11aeba3971172108
```

The old projected route blob `87c39b623724c4c7f637f3747d7f8b965a6bad3a` is superseded for the active phone path by exact hardened upstream blob `31ed79cb56e8d2366e6d70f22e28c70162c88fd8`.

## Installed participant path

Canonical participant entry remains unchanged:

```text
https://stegverse.org/stegfin-trade.html
```

No second Site participant surface is authorized or required.

Execution chain:

```text
stegfin-trade.html
-> exact hardened phone-direct-route.js
-> exact StegID current-phone bootstrap
-> exact device-wallet identity/capability guard
-> exact StegFin operator app
-> user gesture on this phone
-> non-exportable browser-local P-256 device possession
-> platform WebAuthn HUMAN_CONTINUITY
-> DEVICE_ADMITTED
-> OBSERVE + PREPARE only
-> bounded current-block Inventory N:
   -> native ETH gas reserve
   -> USDC sell balance
   -> WETH buy/current-position balance
   -> no historical Transfer-log scan
   -> no unknown-token enumeration
   -> no exhaustive wallet-discovery claim
-> fail closed if USDC < 12_500_000 atomic
-> TV/TVC ROUTE_ADMITTED / credential_requirement=NONE
-> pinned Uniswap V3 quote / exact allowance
-> exact approval OR swap candidate
-> exact candidate gas-reserve sufficiency
-> <=50 bps slippage
-> <=$1 gas
-> read-only eth_call simulation
-> unsigned wallet handoff
-> WALLET_HANDOFF_READY
-> STOP
-> USER_ONLY review/sign/broadcast
```

The Site is a static projection/delivery surface. It does not execute the trade on a server. The current phone executes the browser-local preparation path after the participant gesture.

## Exact projected upstream blobs

```text
assets/stegfin-phone/phone-direct-route.js             31ed79cb56e8d2366e6d70f22e28c70162c88fd8
assets/stegfin-phone/stegid-device-wallet-bootstrap.js 01df37b655f1dae8650c9102ffbd85f72432c47f
assets/stegfin-phone/device-wallet-identity.js          0f18f416dee3d2707ac47964a6b24fe918d6ef68
assets/stegfin-phone/app.js                             ade469ac61df37da46bef1376cfdbb10d3c9b5f1
assets/stegfin-phone/styles.css                         3a91c67d6088f75a93955a260985ce686eb5698f
```

The dedicated validator recomputes Git blob identities and fails on drift. The phone-route validator additionally rejects `eth_getLogs`, `discoverContracts`, `discoveryChunk`, `transferTopic`, and an exhaustive `discovery_complete` claim from the active carrier.

## Bounded Inventory N contract

```text
inventory_scope: BOUNDED_TRADE_RELEVANT_ASSETS
scope_assets:
  - ETH_GAS_RESERVE
  - USDC_SELL_ASSET
  - WETH_BUY_ASSET
trade_relevant_scope_complete: true
unknown_asset_enumeration_performed: false
exhaustive_wallet_asset_discovery_claimed: false
historical_transfer_log_scan_allowed: false
minimum_usdc_atomic: 12500000
native_gas_reserve_required: true
candidate_gas_reserve_sufficiency_required: true
```

This is intentionally narrower and more truthful than attempting to reconstruct the wallet's entire asset history before one bounded validation transition.

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

## Prior release and current hardening evidence

Prior projection release remains valid historical evidence:

```text
PR #276 merge: 8b5319705dcf02c8edc8dd1612e9787cf70386a1
Check StegFin Phone Projection: run 31910836065 SUCCESS
Ecosystem Heartbeat Orchestration: run 31910836030 SUCCESS
Site Handoff Orchestrator: run 31910836202 SUCCESS
Site Bootstrap Validate: run 31910836064 SUCCESS
GitHub Pages exact build: 1153781444
```

Current hardening source evidence:

```text
StegFin PR #62 merge: e19f64ca53699cc626cf05524ff8398544696067
StegFin phone source blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
Site hardening claim: SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815
Site projected hardened blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
Site hardening validator: scripts/check_stegfin_phone_projection.py
hardening merge/publication evidence: PENDING
```

No live phone execution is inferred from source or publication validation.

## Collision and claim disposition

Released original projection:

```yaml
task_id: SITE-STEGFIN-PHONE-PROJECTION-261
claim_id: SITE-STEGFIN-PHONE-PROJECTION-261-20260815
state: MERGED_INTO_CANONICAL_WORKSTREAM
```

Active noncompeting refresh:

```yaml
task_id: SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING
claim_id: SITE-STEGFIN-PHONE-PROJECTION-261-HARDENING-20260815
role: IMPLEMENTATION
state: CLAIMED_FOR_IMPLEMENTATION
branch: fix/stegfin-phone-bounded-inventory-projection-261
collision_scope:
  - assets/stegfin-phone/phone-direct-route.js
  - scripts/check_stegfin_phone_projection.py
  - docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
  - data/session-work-claims.json
release_condition: exact hardened upstream blob projected; validation and Site orchestration pass; PR merged; public build reflects merge
```

PR #277's duplicate `/stegfin-phone/` implementation was closed unmerged after detecting that canonical PR #276 had already provided the participant surface. Do not reopen it.

Do not duplicate the upstream phone carrier, StegID device bootstrap, TVC route, G18 runtime activation, MCP exact-artifact worker, provider route, signer, or broadcaster.

## Discoverability decision

The canonical participant entry remains `stegfin-trade.html`. No functional or authority requirement requires creating another participant path or rewriting unrelated Site surfaces.

## Live activation boundary

After this hardening refresh is merged and publicly rebuilt, the remaining live step is participant-owned and directly executable from the current phone:

```text
open https://stegverse.org/stegfin-trade.html
-> select "Verify this phone and prepare wallet handoff"
-> complete platform WebAuthn/device verification
-> phone observes bounded current-block Inventory N
-> carrier persists precise hash-bound BLOCKED evidence or WALLET_HANDOFF_READY
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

Issue `StegVerse-Labs/stegfin-governance#60` remains open until actual phone evidence is observed. `WALLET_HANDOFF_READY` is not signing permission; review/sign/broadcast remains USER_ONLY.

## Completion accounting

```text
required developed projection surfaces: 8
complete developed projection surfaces: 8
scaffolding/stubs: 0
missing required files: 0
original source validation: 3/3 PASS
hardening source projection: IMPLEMENTED
hardening validation: PENDING PR checks
Site hardening integration: 1/3 (claim + source update complete; validation/merge/publication pending)
participant PREPARE execution: 0/1 pending current-phone gesture after public hardening refresh
terminal phone receipt: 0/1 pending current-phone execution
```

## Session consolidation / archive condition

The prior Site projection workstream is released. This session currently owns only the bounded hardening refresh above. Once the exact hardened source is validated, merged, publicly rebuilt, the claim is released, Site #261 is reconciled, and StegFin #60 imports the refreshed public evidence condition, no Site source implementation role remains.

```text
MERGED INTO after hardening release:
- StegVerse-Labs/stegfin-governance#60
- StegVerse-Labs/Site#261
- StegVerse-Labs/Site/docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
```
