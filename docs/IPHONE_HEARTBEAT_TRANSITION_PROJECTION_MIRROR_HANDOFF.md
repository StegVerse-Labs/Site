# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-17T13:10:00-05:00`

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
claim_created_at: 2026-08-17T13:10:00-05:00
claim_release_condition: exact Site projection merged and deterministic credential-clean validation passes; physical iPhone execution then transfers to .github#209/G18
credential_authority: TV/TVC
github_token_runtime_authority: NONE
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
```

## Authority and collision boundary

Site owns only public transport/materialization of the exact browser capsule. It does not own or acquire heartbeat state-transition authority, G18 claim/fence/lease authority, WorkerCoordinator authority, TV/TVC route or credential authority, model/runtime authority, custody authority, or StegFin wallet/signing/broadcast authority.

Do not modify active StegOS/HIL/StegFin product paths or `data/session-work-claims.json`. Site issue #358 is the durable coordination/claim surface for this non-overlapping projection lane because the canonical claim registry is itself currently owned by existing admission/product claims.

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

## Required Site surfaces

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
this handoff
```

The browser capsule must fail closed unless all of these are true:
- `location.origin` is HTTPS `stegverse.org` or `www.stegverse.org`;
- `navigator.userAgent` contains `iPhone`;
- `window.isSecureContext === true`;
- `crypto.subtle.digest` is available.

It must derive exactly one portable receipt with immutable seed HB29/29, exact successor HB30/30, all authority flags non-authorizing, and SHA-256 over canonical JSON excluding `receipt_sha256`. It may offer local copy/share/download convenience but may not transmit the receipt automatically or contact a credentialed endpoint.

## Validation

Required deterministic validator:

```text
python3 scripts/check_iphone_heartbeat_transition_projection.py
```

The canonical credential-clean Site validation workflow may invoke that validator, but hosted validation is source evidence only and cannot satisfy physical execution, materialization, or HB30 activation.

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

## Incomplete work

- exact browser HTML: pending
- exact browser JavaScript: pending
- deterministic projection validator: pending
- credential-clean canonical validation binding: pending if needed
- PR validation: pending
- merge/release: pending
- physical iPhone receipt: current-iPhone carrier boundary after source release
- HB30 materialization: `.github` verifier/materializer / G18
- WorkerCoordinator observation: machine-owned

## Session consolidation state

This is a distinct support role for the original sovereign-heartbeat activation goal. It must close after the Site projection is merged and transferred. It must not remain open merely to observe subsequent G18 or WorkerCoordinator execution.

## Progress

```text
developed files: 1/4
validation: 0/1
integration: 0/1
source projection activation: 25%
product HB30 activation: not claimed
archive dependency: this Site source lane must be released or durably blocked before the current session can close under the user's original-goal activation rule
```
