# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-15T19:55:00-05:00

## Canonical scope

```text
goal_id: SITE-STEGFIN-PHONE-PROJECTION-261
completed_goal: TASK-2026-0004
capability: site-stegfin-phone-rpc-resilience-projection-v1
parent_phone_task: STEGFIN-PHONE-DIRECT-ROUTE-011
originating_goal: expose the phone-sovereign StegFin PREPARE path on the canonical Site surface, preserve TV/TVC credential authority, remove the single-public-RPC fragility, and introduce no hosted production execution authority
repository: StegVerse-Labs/Site
canonical_branch: main
release_pr: #281
release_merge: 19db08571c679c3143b4c2f2b380497eb8630cd4
superseded_unmerged_pr: #280
canonical_intake_issue: StegVerse-Labs/Site#261
canonical_live_activation_issue: StegVerse-Labs/stegfin-governance#60
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
GitHub token runtime authority: NONE
Render production runtime: PROHIBITED
wallet signing authority: USER_ONLY
broadcast authority: USER_ONLY
```

`SITE_MIRROR_HANDOFF.md` remains the repository parent and `docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md` remains authoritative for mutation admission. This scoped handoff creates no provider, credential, wallet, signing, broadcast, settlement, execution, publication, or Master Records authority.

## Released predecessor work

```text
original projection: Site PR #276 -> 8b5319705dcf02c8edc8dd1612e9787cf70386a1
bounded Inventory N task: STEGFIN-PHONE-DIRECT-ROUTE-011
bounded Inventory N hardening: StegFin PR #62 -> e19f64ca53699cc626cf05524ff8398544696067
Site hardening projection: PR #278 -> 264c75f84361567bdc1126e0fdb13c7a7a90de1c
Site hardening metadata reconciliation: PR #279 -> 99f510d7e1d2026d09df0a4997cd7c2c3d5e9f9f
released hardened phone-direct-route.js blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
```

All predecessor Site claims are terminal `MERGED_INTO_CANONICAL_WORKSTREAM`.

## Released RPC resilience projection

Canonical upstream source:

```text
StegVerse-Labs/stegfin-governance/task-state/STEGFIN-PHONE-RPC-RESILIENCE-012.json
StegVerse-Labs/stegfin-governance/ui/rpc-resilience.js
StegFin PR #66 merge: bcba49976a52024a233f998ce290ec4ab42618ff
exact released blob: 290b567eca2cc9f83e7438a80682ebaf8006ad76
source claim: COMPLETE_RELEASED_SOURCE
```

Site release:

```text
assets/stegfin-phone/rpc-resilience.js 290b567eca2cc9f83e7438a80682ebaf8006ad76
Site PR #281 merge: 19db08571c679c3143b4c2f2b380497eb8630cd4
Check StegFin Phone Projection: 31918210506 SUCCESS
Site Handoff Orchestrator: 31918210541 SUCCESS
Ecosystem Heartbeat Orchestration: 31918210505 SUCCESS
Site Bootstrap Validate: 31918210534 SUCCESS
Pages build: 1153990519 BUILT from exact merge 19db08571c679c3143b4c2f2b380497eb8630cd4
claim: SITE-STEGFIN-PHONE-RPC-RESILIENCE-0004-20260815 RELEASED_IMPLEMENTATION / MERGED_INTO_CANONICAL_WORKSTREAM
```

The asset wraps only Base JSON-RPC POSTs directed to the existing primary `https://mainnet.base.org`. It uses two credential-free endpoints, bounded attempts/backoff, explicit `eth_chainId == 0x2105` verification before fallback use, `credentials: omit`, local bounded evidence, and fail-closed termination when all endpoints fail. It carries no token, provider secret, signing authority, broadcast authority, or hosted-runtime authority.

This public-RPC resilience layer is an immediate availability bridge. It is not classified as sovereign infrastructure and does not supersede the machine-owned StegVerse Base RPC activation chain.

## Installed participant order

The canonical participant URL remains:

```text
https://stegverse.org/stegfin-trade.html
```

Released local script order:

```text
stegfin-trade.html
-> assets/stegfin-phone/rpc-resilience.js
-> assets/stegfin-phone/phone-direct-route.js
-> assets/stegfin-phone/stegid-device-wallet-bootstrap.js
-> assets/stegfin-phone/device-wallet-identity.js
-> assets/stegfin-phone/app.js
```

Loading resilience before `phone-direct-route.js` ensures the phone carrier's Base calls traverse the bounded credential-free retry/failover policy. All executable scripts remain local Site assets; no remote executable script is introduced.

## Phone execution contract

```text
user gesture on current phone
-> browser-local non-exportable device possession
-> platform WebAuthn HUMAN_CONTINUITY
-> DEVICE_ADMITTED
-> OBSERVE + PREPARE only
-> bounded current-block Inventory N:
   ETH_GAS_RESERVE
   USDC_SELL_ASSET
   WETH_BUY_ASSET
-> resilient credential-free Base observation
-> fail closed if transport/chain identity/inventory evidence unavailable
-> TV/TVC ROUTE_ADMITTED / credential_requirement=NONE
-> pinned Uniswap V3 quote / exact allowance
-> exact approval OR swap candidate
-> exact gas-reserve sufficiency
-> <=50 bps slippage
-> <=$1 transaction gas
-> read-only eth_call simulation
-> unsigned wallet handoff
-> WALLET_HANDOFF_READY
-> STOP
-> USER_ONLY review/sign/broadcast
```

No historical transfer-log scan, unknown-token enumeration, automatic signing, or automatic broadcast is authorized.

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
automatic_signing: false
automatic_broadcast: false
```

The Site is a static delivery/projection surface. GitHub-hosted validation proves source integrity only and is not production execution authority.

## Claim disposition

```text
task_id: TASK-2026-0004
claim_id: SITE-STEGFIN-PHONE-RPC-RESILIENCE-0004-20260815
role: RELEASED_IMPLEMENTATION
state: MERGED_INTO_CANONICAL_WORKSTREAM
release_merge: 19db08571c679c3143b4c2f2b380497eb8630cd4
publication_evidence: Pages build 1153990519 BUILT
next_owner: StegVerse-Labs/stegfin-governance#60
```

PR #280 was closed unmerged after the repository orchestrator proved that the original `fix/` branch class did not map to its parent handoff workload. The source was preserved unchanged on the claim-admitted branch and released through PR #281 after all four repository gates passed.

## Cross-repository continuation

```text
upstream resilience source: StegVerse-Labs/stegfin-governance/STEGFIN-PHONE-RPC-RESILIENCE-012 COMPLETE_RELEASED_SOURCE
Site projection: TASK-2026-0004 COMPLETE_RELEASED_SITE_PROJECTION
long-term sovereign Base runtime: StegVerse-Labs/.github/tasks/TASK-2026-0005.json MACHINE_OWNED_REAL_ENDPOINT_PENDING
TVC exact sovereign route admission: TVC-SOVEREIGN-BASE-RPC-ROUTE-003 COMPLETE_RELEASED_SOURCE
current-phone terminal observer: StegVerse-Labs/stegfin-governance#60
wallet sign/broadcast: USER_ONLY
```

The sovereign Base route and the immediate public failover are intentionally distinct. The latter reduces current-phone availability risk while the former removes permanent reliance on third-party public RPC transport after a real synchronized StegVerse Base endpoint is observed and admitted.

## Completion accounting

For `TASK-2026-0004`:

```text
required developed source surfaces: 5
complete developed source surfaces: 5
scaffolding/stubs: 0
missing required files: 0
exact upstream asset identity: PASS
repository validation gates: 4/4 PASS
merge: COMPLETE
public Pages lineage: COMPLETE
Site implementation claim: RELEASED
StegFin #60 propagation: NEXT CANONICAL OBSERVER
developed-files: 100%
validation: 5/5 release evidence classes complete
integration: 4/5 completed locally; final live-observer propagation is cross-repository
Site source goal activation: 100%
```

## Session consolidation / archive condition

No Site source implementation remains in this lane. Continuation is durably transferred to:

```text
MERGED INTO:
- StegVerse-Labs/stegfin-governance#60 for current-phone PREPARE and terminal BLOCKED/WALLET_HANDOFF_READY evidence
- StegVerse-Labs/.github/tasks/TASK-2026-0005.json for real synchronized StegVerse Base endpoint activation
- StegVerse-Labs/TVC/tasks/TVC-SOVEREIGN-BASE-RPC-ROUTE-003.json for exact sovereign route admission contract
```

Live phone `WALLET_HANDOFF_READY` is not inferred from source completion. Signing and broadcast remain USER_ONLY. This Site handoff is sufficient to continue the released projection without the originating chat history.
