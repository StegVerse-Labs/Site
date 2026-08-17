# StegFin iOS First-Passkey Projection Mirror Handoff

Updated: 2026-08-17

## Active goal

```text
goal_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
source_goal: STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018
source_issue: StegVerse-Labs/stegfin-governance#79
site_issue: StegVerse-Labs/Site#380
repository: StegVerse-Labs/Site
branch: claim/stegfin-ios-first-passkey-prepare-380
canonical_parent: docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md
claim: data/session-work-claims.json#SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
implementation_claim: CLAIMED_FOR_INTEGRATION
validation_claim: SITE_CANONICAL_GATES
claim_created: 2026-08-17T13:37:00-05:00
claim_release_condition: exact source projection + Site validation + merge + exact Pages build + claim release
```

## Source evidence and defect

Current-phone evidence showed a successful iOS passkey creation ceremony (`Done`) followed by the published participant rendering the platform/user-agent `NotAllowedError` text. Source inspection established that first-time admission executed `navigator.credentials.create()` and then immediately executed `navigator.credentials.get()` from one original button gesture.

The released StegFin correction makes the successful first platform credential creation with `userVerification='required'` the initial HUMAN_CONTINUITY ceremony and returns before any second WebAuthn operation. Existing credentials still require a fresh `navigator.credentials.get()` assertion on each later PREPARE gesture.

## Exact projection

```text
source: StegVerse-Labs/stegfin-governance/ui/stegid-device-wallet-bootstrap.js
source blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
destination: assets/stegfin-phone/stegid-device-wallet-bootstrap.js
expected destination blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
source issue: #79
source PR: #80
```

## Authority boundaries

- TV/TVC is the sole credential authority.
- Phone-route credential requirement remains `NONE`.
- NON-TV/TVC secrets/tokens are prohibited.
- GitHub-token runtime authority is `NONE`.
- Render/Vercel/Cloudflare/GitHub-hosted production execution is prohibited.
- Site is static transport/materialization only.
- Wallet review/signing and broadcast remain `USER_ONLY`.
- No stale/expired candidate becomes current authority through this projection.
- This task does not modify sovereign heartbeat, local-model/runtime, route admission, settlement, or Master Records authority.

## Claim reconciliation performed before mutation

`data/session-work-claims.json` had retained Site #298 as active after its product scope was already closed/completed. The exact release evidence was already durable in Site #298 comment `5313605823`: PR #309 merge `1f5ab3acde796d2787edf0493c19e193ca72eda4`, Pages build `1156543676` built from that merge, and all required Site gates successful. The current #268 continuation explicitly records its next token-remediation candidate as UNCLAIMED. The #380 claim therefore terminalizes #298 to `MERGED_INTO_CANONICAL_WORKSTREAM` and admits a distinct nonoverlapping StegFin projection surface.

## Validation requirements

```text
python scripts/check_stegfin_phone_projection.py
python scripts/check_session_work_claims.py
python scripts/site_handoff_orchestrator.py
Site Bootstrap Validate
Ecosystem Heartbeat Orchestration
```

The canonical StegFin phone validator now requires the exact corrected bootstrap blob, both `CREDENTIAL_CREATION` and `CREDENTIAL_ASSERTION` proof markers, creation-before-assertion control flow, no forbidden credential/wallet middleware markers, terminal Site #298 claim state, and the active/released #380 claim.

Hosted Site validation is publication/source evidence only. It grants no wallet, route, runtime, or live phone authority.

## Current state

```text
source_fix: RELEASED
site_claim: CLAIMED_FOR_INTEGRATION
exact_projection: INSTALLED_ON_BRANCH
canonical_validator: UPDATED_ON_BRANCH
canonical_phone_handoff: UPDATED_ON_BRANCH
site_merge: PENDING
pages_publication: PENDING
current_phone_validation: PENDING
wallet_signature_or_broadcast: USER_ONLY_NOT_AUTHORIZED_BY_THIS_TASK
```

## Next executable action

Open the Site PR from the admitted branch, inspect required Site gates, correct any branch-level validation defect without weakening authority boundaries, merge only after the strongest available validation, verify Pages built from the exact merge, terminalize the #380 claim, then transfer live observation to StegFin #79/#77. On the current phone, reload the participant and perform one fresh Verify/PREPARE gesture; only a newly generated candidate may proceed to the USER_ONLY wallet boundary.

## Archive condition

This Site integration task becomes archive-safe after merge, exact Pages publication, and claim release. Current-phone execution remains a separate live-observation requirement owned by StegFin #79/#77 + current phone + USER_ONLY.
