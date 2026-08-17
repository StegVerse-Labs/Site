# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-17T13:25:00-05:00`

## Goal and release state

```text
goal_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-001
originating_goal: eliminate the original-session HB29->HB30 initiation deadlock by projecting the canonical non-authorizing transition capsule to the permitted CURRENT_USER_IPHONE without another machine, Render, GitHub token, or NON-TV/TVC secret/token
repository: StegVerse-Labs/Site
canonical_branch: main
canonical_issue: StegVerse-Labs/Site#358
canonical_source_issue: StegVerse-Labs/.github#209
parent_task: SHWP-DURABLE-RUNTIME-ACTIVATION / G18
claim_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-358-R1-20260817
claim_state: COMPLETE_RELEASED / MERGED_INTO_CANONICAL_WORKSTREAM
Site_PR: #368
final_head: 0b1f7f741fe71057bea93241ad74b5b72f1cc20d
merge: 37c8ac81b8b00e22310b8f03687f4b9f42581d31
credential_authority: TV/TVC
github_token_runtime_authority: NONE
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
authority_effect: NONE
```

## Released Site surfaces

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
.github/workflows/validate.yml credential-clean validator binding
data/session-work-claims.json coordination/admission record
this handoff
```

The browser capsule fails closed unless execution is at `https://stegverse.org` on an iPhone in a secure context with WebCrypto. It constructs the exact `.github#209` portable receipt with immutable HB29/29 seed, HB30/30 successor, TV/TVC/NONE credential semantics, all authority flags non-authorizing, and SHA-256 over canonical JSON excluding `receipt_sha256`. Receipt retention and copy/share/file-save are user-initiated/local only. The capsule contains no automatic network/API/provider/wallet operation.

## Exact validation evidence

PR #368 exact merge-checkout was current main `96423f16cf6d3f440630d322cc5d5c196e4fa672` plus final head `0b1f7f741fe71057bea93241ad74b5b72f1cc20d`.

```text
Site Bootstrap Validate: 32054685239 SUCCESS
Bootstrap job: 95462000602 SUCCESS
IPHONE_HB30_PROJECTION_PASS
SESSION_WORK_CLAIMS_PASS
SITE_HANDOFF_ORCHESTRATION_PASS
ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS
ECOSYSTEM_CHAT_APPLICATION_PASS
ST-017 sandbox PASS
StegFin projection PASS / USER_ONLY signing+broadcast
Site Handoff Orchestrator: 32054685374 SUCCESS
Ecosystem Heartbeat Orchestration: 32054685170 SUCCESS
Check StegFin Phone Projection: 32054685244 SUCCESS
workflow census observed in exact merge-checkout: 101 total / canonical 3 / migration-required 98 / placeholders 0
```

Hosted validation is source evidence only. It does not constitute physical iPhone execution, HB30 materialization, WorkerCoordinator observation, sovereign inference, wallet signature, broadcast, or settlement.

## Authority and collision boundary

Site owns only public transport/materialization. It does not own heartbeat transition authority, G18 claim/fence/lease, WorkerCoordinator authority, TV/TVC route/credential authority, local-model authority, HIL/StegOS authority, or StegFin wallet/signing/broadcast authority. Publication alone is not HB30 activation.

PR #363 / branch `feat/iphone-heartbeat-transition-projection-358` is superseded unmerged. PR #368 is the canonical current-main release.

## Canonical continuation

```text
StegVerse-Labs/.github#209 source contract
-> released Site browser capsule at /heartbeat-transition/
-> CURRENT_USER_IPHONE portable receipt
-> .github independent verifier/materializer
-> HB30 carrier state with immutable HB29
-> independent WorkerCoordinator observation
-> G18 release
-> .github#60 sovereign same-execution inference
```

The next physical step is deliberately outside Site authority: the permitted CURRENT_USER_IPHONE executes the published capsule. The portable receipt must then be independently accepted by the `.github` verifier/materializer before HB30 can be claimed.

## Execution ownership

### MANUAL / SESSION-STARTABLE

- Site source projection: COMPLETE_RELEASED; no further Site implementation is startable under this claim.

### WORKER-OWNED / DO NOT COMPETE

- `SHWP-DURABLE-RUNTIME-ACTIVATION / G18`: receipt acceptance/HB30 continuity.
- WorkerCoordinator: independent HB30+ observation.
- `.github#60`: sovereign same-execution inference after carrier release.

### ESCALATED / AUTHORITY-OWNED

- TV/TVC: credential and route authority.
- USER_ONLY: StegFin signing/broadcast.

### COMPLETED / SUPERSEDED

- Site #358 projection source: COMPLETE_RELEASED.
- PR #363: superseded unmerged.
- local model/runtime source: COMPLETE_RELEASED.
- StegFin pre-sign trade readiness: COMPLETE_ACTIVATED_AT_PRE_SIGN_BOUNDARY.

## Progress

```text
developed files: 6/6
validation: 4/4 required exact-head lanes PASS
integration: 2/2 source projection + canonical G18 transfer complete
Site projection release: 100%
physical iPhone receipt: not yet observed
HB30 activation: not yet observed
WorkerCoordinator observation: not yet observed
sovereign same-execution inference: not yet observed
```
