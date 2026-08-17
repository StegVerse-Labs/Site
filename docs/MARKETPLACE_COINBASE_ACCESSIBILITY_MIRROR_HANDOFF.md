# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Workflow-cleanup claim: `SITE-MARKETPLACE-COINBASE-ACTIVATION-CONTROLLER-TOKEN-RETIREMENT-20260817`
- Goal: project the verified Publisher paper chain into a public StegVerse accessibility state without granting live or financial authority, while keeping continuation credential-clean and StegVerse-owned.

## Authoritative files

- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/marketplace-coinbase-accessibility-status.json`
- `.github/workflows/import-marketplace-coinbase-accessibility.yml`
- `scripts/advance_marketplace_coinbase_activation.py`
- `data/marketplace-coinbase-activation-tasks.json`
- this handoff

## Current product state

```text
SITE_MARKETPLACE_COINBASE_PAPER_ACCESSIBILITY_ACTIVATED_AND_MACHINE_PERSISTED
paper_trading_accessible: true
live_trading_accessible: false
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
financial_authority: NOT_GRANTED
```

The Site projection is display and continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified upstream

- Publisher repository: `GCAT-BCAT-Engine/Publisher`
- Publisher status path: `data/marketplace-coinbase-release-evidence-status.json`
- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher machine persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`

## Completed product evidence

- initial Site projection activation commit: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine-owned importer persistence commit: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- projection tests: commit `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- workflow validation binding: commit `04dab58eafc6d47779f1196486c1384d5fe1ed3a`
- projection digest: `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`

Deterministic production contract:

```text
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
historical result: 4 passed in 0.03s
```

The tests verify the committed projection digest, paper-only state, valid Publisher acceptance, authority-escalation rejection after re-signing, and tampered-status rejection.

## Exact evidence bindings

- intent: `intent-marketplace-release-73a0543ddb27`
- packet: `sha256:ae990ce837cac3077a80c966b4e2d960f4158065dcec9c7fdc4da8b8f26ea89b`
- sequence 1: `sha256:f6f41875a5e066fc348cac68691c1d4fb77f3559282eb4ede26a398c87ee7e64`
- acknowledgement: `sha256:c76c0decad6b82f9356a58598ef5e217f92802dc657e9f5ed95cae9b8f77f0a3`
- sequence 2: `sha256:805000ab776b00863f5962514bcb8f843ccaa27ab9e0ac7821b92499b2e347f1`
- Publisher projection: `sha256:4ab30925412757058f3f752fad1d7e452e95dcddf3d2e272ecd9605cee97e8d9`
- publication receipt: `sha256:0dc495cf5f7de0b4610d5b4fc7732f3ddb888543fbe6c9a55ef07ad7f175d240`

## Credential-clean controller retirement

The former standalone `.github/workflows/advance-marketplace-coinbase-activation.yml` is being retired under the workflow-cleanup claim because it consumed or depended on:

```text
secrets.MARKETPLACE_COINBASE_EVIDENCE_TOKEN
github.token
contents: write
issues: write
actions/checkout
actions/setup-python
repository commit/push writeback
actions/upload-artifact
```

Those GitHub-hosted mechanics are not required to preserve the already-bound Site product state and conflict with the current governing boundary that NON-TV/TVC secrets/tokens must not be used and GitHub Actions must not become production/runtime/control-plane authority.

The retained deterministic observation surface is:

```text
scripts/advance_marketplace_coinbase_activation.py
data/marketplace-coinbase-activation-tasks.json
```

Its v3 contract is credential-clean and fail-closed:

```text
credential_requirement: NONE
github_token_allowed: false
non_tv_tvc_secret_or_token_allowed: false
anonymous_public_observation_only: true
continuation_mode: STEGVERSE_OWNED_OBSERVATION_ONLY
publication_authority: false
release_authority: false
execution_authority: false
live_authority: false
financial_authority: false
```

The observer refuses `STEGVERSE_CROSS_REPO_READ_TOKEN`, `MARKETPLACE_COINBASE_EVIDENCE_TOKEN`, `GITHUB_TOKEN`, `GH_TOKEN`, and `STEGVERSE_GITHUB_TOKEN`; it sends no Authorization header. If an upstream evidence path is not anonymously observable, it records `BLOCKED_DEPENDENCY` and preserves the named repository/issue as the continuation owner rather than requesting or inventing a credential.

This observation path may be invoked by an admitted StegVerse-owned lane. No GitHub schedule, GitHub-hosted writeback, GitHub token, provider token, or Render runtime is a continuation prerequisite.

## Current continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19 / COMPLETE when VERIFIED
MC-04 Site projection -> StegVerse-Labs/Site#131 / COMPLETE when PAPER_ACCESSIBLE and live_trading_accessible=false
```

An anonymous observation block is not task failure and does not authorize GitHub-token repair. Canonical upstream repositories remain responsible for their own evidence production and custody.

## Incomplete work

### Controller retirement integration

- Owner: `SITE-MARKETPLACE-COINBASE-ACTIVATION-CONTROLLER-TOKEN-RETIREMENT-20260817`
- Branch: `chore/site-marketplace-coinbase-controller-validation-20260817`
- State: implementation installed; exact-head validation pending
- Release condition: credential-clean Site claim/orchestrator/bootstrap checks PASS; workflow census decrements by exactly one from current released main without canonical-surface loss; PR merges; main no longer contains the standalone controller workflow; claim and Actions handoff are released with immutable evidence.

### Exact paper-release tag evidence

- Owner: `StegVerse-Labs/crypto-bot#6`
- Required tag: `marketplace-coinbase-paper-v1.0.0`
- Required target: `73a0543ddb27a88fd4913e7dcfa2127132299baa`

## Collision boundaries

- TV/TVC remains credential authority.
- Do not export TV/TVC credentials into GitHub Actions.
- Do not use a GitHub/project/provider token to repair anonymous observation.
- Do not create a second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner.
- Do not infer Coinbase live trading, custody, withdrawal, funded execution, publication, release, or financial authority from paper accessibility or workflow cleanup.
- Do not modify StegFin, StegOS, or HIL claimed product paths.
- USER_ONLY remains the sole StegFin signing/broadcast authority.

## Archive condition

The Site paper-accessibility projection is already established, but the workflow-cleanup session is not archive-ready while the controller-retirement claim is active and broader Site #268 token/workflow debt remains unresolved. Product activation and workflow-cleanup completion remain separate claims.

## Progress

```text
paper-accessibility developed files: 5/5
paper-accessibility deterministic validation: previously PASS
Site paper projection integration: COMPLETE
controller token-retirement implementation: INSTALLED_ON_BRANCH
controller exact-head validation: PENDING
live/financial authority: NOT GRANTED
```
