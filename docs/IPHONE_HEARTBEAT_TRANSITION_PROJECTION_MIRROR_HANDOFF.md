# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-17T13:18:00-05:00`

## Active goal and goal ID

```text
goal_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-001
originating_goal: eliminate the original-session HB29->HB30 initiation deadlock by projecting the canonical non-authorizing transition capsule to the permitted CURRENT_USER_IPHONE without another machine, Render, GitHub token, or NON-TV/TVC secret/token
repository: StegVerse-Labs/Site
branch: feat/iphone-heartbeat-transition-projection-358
canonical_issue: StegVerse-Labs/Site#358
canonical_source_issue: StegVerse-Labs/.github#209
parent_task: SHWP-DURABLE-RUNTIME-ACTIVATION / G18
role: CLAIMED_FOR_INTEGRATION
claim_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-358-20260817
claim_created_at: 2026-08-17T13:10:00-05:00
claim_registry_admission_commit: 8a3beffe58021adc7af0ffae11278f1306869daf
claim_release_condition: exact Site projection merged and deterministic credential-clean validation passes; physical iPhone execution then transfers to .github#209/G18
credential_authority: TV/TVC
github_token_runtime_authority: NONE
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
```

## Authority and collision boundary

Site owns only public transport/materialization of the exact browser capsule. It does not own or acquire heartbeat state-transition authority, G18 claim/fence/lease authority, WorkerCoordinator authority, TV/TVC route or credential authority, model/runtime authority, custody authority, or StegFin wallet/signing/broadcast authority.

The only shared active-claim surface changed is `data/session-work-claims.json`, and only to register this branch with the existing pre-work admission system after the first PR validation correctly failed closed because the branch had no active claim. No existing active claim body, state, branch, ownership surface, or authority was changed.

Publication alone is not HB30 activation. A browser-generated receipt alone is not canonical carrier state. Only the independent `.github` verifier/materializer may accept the physical receipt, and WorkerCoordinator must still independently observe HB30+.

## Canonical source contract

Source owner: `StegVerse-Labs/.github`.

```text
contract: management/SHWP_IPHONE_TRANSITION_CAPSULE_CONTRACT.json
schema: schemas/iphone_heartbeat_transition_receipt.schema.json
verifier/materializer: scripts/verify_iphone_heartbeat_transition_receipt.py
legacy source: control/heartbeat-state.json
legacy blob: d18d57d83cf19b7799cde1a1b4487e496eca7f76
legacy epoch/generation: 29/29
successor epoch/generation: 30/30
physical execution surface: CURRENT_USER_IPHONE
physical transport: STEGVERSE_BROWSER_CAPSULE
authority_effect: NONE
credential_requirement: NONE
credential_authority: TV/TVC
```

## Implemented Site surfaces

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
.github/workflows/validate.yml (credential-clean validator binding only)
data/session-work-claims.json (coordination/admission record only)
this handoff
```

The browser capsule fails closed unless all of these are true:
- `location.origin === https://stegverse.org`;
- `navigator.userAgent` contains `iPhone`;
- `window.isSecureContext === true`;
- `crypto.subtle.digest` is available.

It derives exactly one portable receipt with immutable seed HB29/29, exact successor HB30/30, all authority flags non-authorizing, and SHA-256 over canonical JSON excluding `receipt_sha256`. It persists the receipt only in browser-local storage and exposes user-initiated copy/share/file-save controls. It performs no automatic network/API request and carries no repository/provider/wallet credential material.

## Validation

Required deterministic validator:

```text
python3 scripts/check_iphone_heartbeat_transition_projection.py
```

The existing credential-clean Site Bootstrap validation invokes that validator. Hosted validation is source evidence only and cannot satisfy physical execution, materialization, or HB30 activation.

Initial PR #363 validation correctly failed closed at pre-work admission because the branch was not yet in `data/session-work-claims.json`. The admission defect was repaired in commit `8a3beffe58021adc7af0ffae11278f1306869daf`. Attempts to rerun the original check suite continued to use its immutable pre-admission merge snapshot, so PR #363 was closed/reopened against current `main` and this follow-on synchronize commit requests a fresh check suite against the admitted current head rather than treating stale reruns as evidence.

## Integration and propagation

```text
StegVerse-Labs/.github#209 portable contract
-> StegVerse-Labs/Site#358 exact public browser capsule
-> CURRENT_USER_IPHONE physical receipt
-> .github canonical verifier/materializer
-> HB30 carrier state
-> independent WorkerCoordinator observation
-> G18 release
-> .github#60 sovereign inference continuation
```

No Site/Publisher/admissibility/stegguardian propagation is authorized merely from source validation or publication.

## Current incomplete work

- fresh exact-head deterministic PR validation: pending
- merge/release: pending
- physical iPhone receipt: current-iPhone carrier boundary after source release
- HB30 materialization: `.github` verifier/materializer / G18
- WorkerCoordinator observation: machine-owned

## Session consolidation state

This is a distinct support role for the original sovereign-heartbeat activation goal. It must close after the Site projection is merged and transferred. It must not remain open merely to observe subsequent G18 or WorkerCoordinator execution.

## Progress

```text
developed files: 6/6
validation: 0/1 pending fresh exact-head workflow evidence after claim admission
integration: 0/1 pending merge
source projection activation: 85%
product HB30 activation: not claimed
archive dependency: this Site source lane must be released or durably blocked before the current session can close under the user's original-goal activation rule
```
