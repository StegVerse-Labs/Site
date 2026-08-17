# StegFin iOS First-Passkey Projection Mirror Handoff

Updated: 2026-08-17

## Canonical released state

```text
goal_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
source_goal: STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018
source_issue: StegVerse-Labs/stegfin-governance#79
site_issue: StegVerse-Labs/Site#380
repository: StegVerse-Labs/Site
source_pr: StegVerse-Labs/stegfin-governance#80
source_merge: f5ff9b1aa2fad545cf9fd676c785438f306dda7a
site_pr: StegVerse-Labs/Site#384
site_merge: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
pages_build: 1157682910 BUILT
pages_commit: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
source_bootstrap_blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
site_claim_state: COMPLETE_RELEASED_PRODUCT
site_execution_responsibility: NONE
continuation_owner: StegVerse-Labs/stegfin-governance#79 -> #77 + current phone + USER_ONLY
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
render_required: false
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

Live repository state, exact Site validation, Pages build evidence, current-phone observations and StegFin task state supersede older chat claims.

## Defect and released correction

The originating current-phone observation showed a successful iOS platform passkey creation ceremony followed by an immediate WebAuthn `NotAllowedError`. Source inspection established that first-time admission executed `navigator.credentials.create()` and then immediately executed `navigator.credentials.get()` from the same original user gesture.

The released correction preserves fail-closed behavior:

```text
first-time/no stored WebAuthn credential
-> navigator.credentials.create
-> platform authenticator required
-> residentKey required
-> userVerification required
-> public-key credential + rawId required
-> persist bounded credential identifier metadata
-> return HUMAN_CONTINUITY with ceremony=CREDENTIAL_CREATION
-> no immediate second WebAuthn operation

later PREPARE with stored credential
-> explicit new user gesture
-> navigator.credentials.get
-> userVerification required
-> return HUMAN_CONTINUITY with ceremony=CREDENTIAL_ASSERTION
```

The exact corrected source blob `9cac39a990a956f16fcde3681cbcc7d47b2fc704` is now published through Site. This correction is not a retry, downgrade, cached signing authority, or stale-candidate reauthorization.

## Release validation

The fresh-current-main Site projection was reconstructed only after B26 released the shared claim registry. Site #298's stale registry entry was terminalized from its already-recorded completed merge/Pages evidence.

Exact pre-merge validation for Site PR #384:

```text
Check StegFin Phone Projection: 32066238396 SUCCESS
Site Handoff Orchestrator: 32066238185 SUCCESS
Ecosystem Heartbeat Orchestration: 32066237444 SUCCESS
Site Bootstrap Validate: 32066238690 SUCCESS
```

Exact publication evidence:

```text
Site PR #384 merge: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
Pages build: 1157682910
Pages state: BUILT
Pages commit: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
canonical participant: https://stegverse.org/stegfin-trade.html
```

Publication and hosted validation do not grant wallet, signing, broadcast, route, runtime, settlement, or model-output authority.

## Authority boundaries

- TV/TVC is the sole credential authority.
- Phone route credential requirement remains `NONE`.
- NON-TV/TVC secrets/tokens remain prohibited.
- GitHub-token runtime authority is `NONE`.
- No Render/Vercel/Cloudflare/GitHub-hosted production execution is used.
- Site is static transport/materialization only.
- Wallet review, signature and broadcast remain `USER_ONLY`.
- A stale/expired wallet candidate is not made valid by this release.
- Sovereign heartbeat, model/runtime, TVC route admission, settlement and Master Records authority remain with their canonical owners.

## Current live continuation

Site execution is complete. The next executable evidence must come from the current phone:

```text
1 reload the canonical participant
2 perform a fresh Verify this phone and prepare wallet handoff gesture
3 first-time/reset-state path: one successful passkey creation must continue without immediate second-ceremony NotAllowedError
4 later PREPARE path: a fresh platform assertion must still be required
5 only a newly generated unexpired WALLET_HANDOFF_READY candidate may be presented at the USER_ONLY wallet boundary
```

If no fresh candidate is produced, do not sign or broadcast anything. If a fresh candidate is produced, wallet confirmation remains a separate explicit USER_ONLY act.

## Post-candidate continuation

```text
USER_ONLY wallet review/sign/broadcast
-> transaction hash is SUBMITTED_NOT_SETTLED
-> independent credential-free Base receipt observation
-> successful receipt invalidates predecessor authority and requires fresh successor PREPARE
-> fresh exit candidate
-> USER_ONLY exit sign/broadcast
-> settled round trip
-> realized P&L / Master Records reconstruction / production sizing
```

## Archive state for Site integration

```text
developed product/control files: 5/5
scaffolding or stubs: 0
missing required files: 0
Site validation: 4/4 canonical pre-merge gates PASS
Site integration: exact projection + merge + Pages = COMPLETE
Site #380 claim: READY_FOR_TERMINAL_REGISTRY_RELEASE
current-phone proof: PENDING outside Site execution authority
```

MERGED INTO: `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018.json` -> StegFin #79/#77 + current phone + USER_ONLY.
