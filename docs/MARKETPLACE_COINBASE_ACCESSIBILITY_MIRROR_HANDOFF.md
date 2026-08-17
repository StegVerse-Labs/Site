# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Workflow-minimization continuation: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B13-20260817`
- Goal: project the verified Publisher paper chain into a public StegVerse accessibility state without granting live or financial authority.

## Authoritative files

- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/marketplace-coinbase-accessibility-status.json`
- `.github/workflows/import-marketplace-coinbase-accessibility.yml`
- `scripts/advance_marketplace_coinbase_activation.py`
- `data/marketplace-coinbase-activation-tasks.json`
- this handoff

## Current state

```text
SITE_MARKETPLACE_COINBASE_PAPER_ACCESSIBILITY_ACTIVATED_AND_MACHINE_PERSISTED
```

The Site projection is display and continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified upstream

- Publisher repository: `GCAT-BCAT-Engine/Publisher`
- Publisher status path: `data/marketplace-coinbase-release-evidence-status.json`
- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher machine persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`

## Completed work and evidence

- initial Site projection activation commit: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine-owned importer persistence commit: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- projection tests: commit `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- workflow validation binding: commit `04dab58eafc6d47779f1196486c1384d5fe1ed3a`

Current checked-in projection:

```text
state = PAPER_ACCESSIBLE
publisher_status = VERIFIED
publisher_status_digest = sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477
paper_trading_accessible = true
live_trading_accessible = false
publication_authority = NOT_GRANTED
release_authority = NOT_GRANTED
execution_authority = NOT_GRANTED
live_authority = NOT_GRANTED
```

Current projection digest:

```text
sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3
```

## Deterministic validation

The production Site contract is retained and validated with:

```text
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
```

The tests verify the committed projection digest, paper-only state, valid Publisher acceptance, authority-escalation rejection after re-signing, and tampered-status rejection.

## Batch 13 — GitHub token/control-plane retirement

Claim `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B13-20260817` retires the separate GitHub-hosted activation controller `.github/workflows/advance-marketplace-coinbase-activation.yml`.

The retired workflow carried:

```text
MARKETPLACE_COINBASE_EVIDENCE_TOKEN
GH_TOKEN = github.token
contents: write
issues: write
actions/checkout
actions/setup-python
git commit/push writeback
actions/upload-artifact
```

Those mechanics are not required for the already-proven paper-accessibility projection and conflict with the current boundary that NON-TV/TVC secrets/tokens must not be consumed and GitHub Actions must not become production/runtime/control-plane authority.

The retained observation path is:

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
publication authority: false
release authority: false
execution authority: false
live authority: false
financial authority: false
```

The observer explicitly rejects `STEGVERSE_CROSS_REPO_READ_TOKEN`, `MARKETPLACE_COINBASE_EVIDENCE_TOKEN`, `GITHUB_TOKEN`, `GH_TOKEN`, and `STEGVERSE_GITHUB_TOKEN`. It sends no Authorization header. If a named upstream evidence path is not anonymously observable, it records `BLOCKED_DEPENDENCY` and preserves the named repository/issue as canonical owner instead of requesting a token.

StegVerse-owned execution may invoke this observer against public/already-materialized evidence. No GitHub schedule, GitHub-hosted writeback, or GitHub credential is a continuation prerequisite.

## Exact evidence bindings

- intent: `intent-marketplace-release-73a0543ddb27`
- packet: `sha256:ae990ce837cac3077a80c966b4e2d960f4158065dcec9c7fdc4da8b8f26ea89b`
- sequence 1: `sha256:f6f41875a5e066fc348cac68691c1d4fb77f3559282eb4ede26a398c87ee7e64`
- acknowledgement: `sha256:c76c0decad6b82f9356a58598ef5e217f92802dc657e9f5ed95cae9b8f77f0a3`
- sequence 2: `sha256:805000ab776b00863f5962514bcb8f843ccaa27ab9e0ac7821b92499b2e347f1`
- Publisher projection: `sha256:4ab30925412757058f3f752fad1d7e452e95dcddf3d2e272ecd9605cee97e8d9`
- publication receipt: `sha256:0dc495cf5f7de0b4610d5b4fc7732f3ddb888543fbe6c9a55ef07ad7f175d240`

## Machine-owned continuation

1. Canonical upstream repository/issue owners retain their own task completion and evidence production.
2. Site #131 retains the public projection and bounded observation state.
3. Credential-clean StegVerse-owned observation may rerun `scripts/advance_marketplace_coinbase_activation.py`; blocked anonymous paths remain exact dependency blockers rather than token requests.
4. Invalid digest, schema, source, binding, or authority evidence remains fail-closed.
5. Crypto-bot finalization proceeds independently at `StegVerse-Labs/crypto-bot#6`.

## Incomplete work

- Batch 13 workflow-retirement integration.
  - Owner while active: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B13-20260817`
  - Branch: `chore/site-marketplace-coinbase-token-retirement-b13-20260817`
  - Release condition: claim/orchestrator/bootstrap validation PASS, exact PR head merged, post-merge workflow inventory recorded, claim released.
- Complete exact paper-release tag evidence in crypto-bot.
  - Owner: `StegVerse-Labs/crypto-bot#6`
  - Required tag: `marketplace-coinbase-paper-v1.0.0`
  - Required target: `73a0543ddb27a88fd4913e7dcfa2127132299baa`

## Archive conditions

The Site paper-accessibility product projection is already established. This workflow-minimization session remains active until Batch 13 is validated/merged/released and the broader Site #268 workflow surface is reduced or durably transferred. Nothing in this handoff grants live Coinbase/trading authority.

## Progress

- paper-accessibility developed files: 5/5 = 100%
- deterministic projection validation: previously validated; exact Batch 13 regression validation pending
- Site paper projection integration: 100%
- Batch 13 token/controller retirement: implementation installed on branch; exact-head validation pending
- live/financial authority: NOT GRANTED
