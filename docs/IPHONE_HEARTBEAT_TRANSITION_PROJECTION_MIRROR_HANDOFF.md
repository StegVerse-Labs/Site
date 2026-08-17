# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-17T13:20:00-05:00`

## Active goal and ownership

```text
goal_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-001
originating_goal: eliminate the original-session HB29->HB30 initiation deadlock by projecting the canonical non-authorizing transition capsule to the permitted CURRENT_USER_IPHONE without another machine, Render, GitHub token, or NON-TV/TVC secret/token
repository: StegVerse-Labs/Site
branch: feat/iphone-heartbeat-transition-projection-358-r1
canonical_issue: StegVerse-Labs/Site#358
canonical_source_issue: StegVerse-Labs/.github#209
parent_task: SHWP-DURABLE-RUNTIME-ACTIVATION / G18
role: CLAIMED_FOR_INTEGRATION
claim_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-358-R1-20260817
claim_created_at: 2026-08-17T13:20:00-05:00
claim_release_condition: exact projection merged and credential-clean deterministic validation passes; physical iPhone execution then transfers to .github#209/G18
credential_authority: TV/TVC
github_token_runtime_authority: NONE
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
```

## Supersession

PR #363 / branch `feat/iphone-heartbeat-transition-projection-358` is superseded unmerged because Site `main` advanced while its original Actions check suite retained a pre-admission merge snapshot. R1 is reconstructed from current `main` and preserves the same narrow capability without carrying stale base state.

## Authority and collision boundary

Site owns public transport/materialization only. It does not own heartbeat transition authority, G18 claim/fence/lease, WorkerCoordinator authority, TV/TVC route/credential authority, local-model authority, HIL/StegOS authority, or StegFin wallet/signing/broadcast authority. Publication alone is not HB30 activation.

## Canonical source contract

```text
source owner: StegVerse-Labs/.github#209
contract: management/SHWP_IPHONE_TRANSITION_CAPSULE_CONTRACT.json
receipt schema: schemas/iphone_heartbeat_transition_receipt.schema.json
verifier/materializer: scripts/verify_iphone_heartbeat_transition_receipt.py
legacy blob: d18d57d83cf19b7799cde1a1b4487e496eca7f76
legacy epoch/generation: 29/29
successor epoch/generation: 30/30
physical execution surface: CURRENT_USER_IPHONE
credential_requirement: NONE
credential_authority: TV/TVC
authority_effect: NONE
```

## R1 required surfaces

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
.github/workflows/validate.yml validator binding
data/session-work-claims.json admission record
this handoff
```

The browser must fail closed unless it is executing at `https://stegverse.org` on an iPhone in a secure context with WebCrypto. It emits only a locally retained portable receipt and performs no automatic network/API/provider/wallet action.

## Continuation

```text
.github#209 source contract
-> Site#358 browser projection
-> CURRENT_USER_IPHONE portable receipt
-> .github independent verifier/materializer
-> HB30 carrier state with immutable HB29
-> independent WorkerCoordinator observation
-> G18 release
-> .github#60 sovereign inference
```

## Execution ownership

### MANUAL / SESSION-STARTABLE

- R1 Site projection source integration and credential-clean validation only.

### WORKER-OWNED / DO NOT COMPETE

- `SHWP-DURABLE-RUNTIME-ACTIVATION / G18`: HB30 materialization/continuity.
- WorkerCoordinator: independent worker observation.
- `.github#60`: sovereign same-execution inference after carrier release.

### ESCALATED / AUTHORITY-OWNED

- TV/TVC: credential and route authority.
- USER_ONLY: StegFin signing/broadcast.

### COMPLETED / SUPERSEDED

- PR #363 branch: superseded unmerged by R1 current-main reconstruction.
- local model/runtime source: COMPLETE_RELEASED.
- StegFin pre-sign trade readiness: COMPLETE_ACTIVATED_AT_PRE_SIGN_BOUNDARY.

## Progress

```text
developed files: 1/6
validation: 0/3
integration: 0/2
physical iPhone receipt: pending after source release
HB30 activation: not claimed
```
