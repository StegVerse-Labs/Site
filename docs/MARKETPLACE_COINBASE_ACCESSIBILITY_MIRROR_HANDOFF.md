# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Released workflow-cleanup claim: `SITE-MARKETPLACE-COINBASE-ACTIVATION-CONTROLLER-TOKEN-RETIREMENT-20260817`
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

## Verified upstream and product evidence

- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher machine persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`
- initial Site projection activation commit: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine-owned importer persistence commit: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- projection tests: `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- workflow validation binding: `04dab58eafc6d47779f1196486c1384d5fe1ed3a`
- projection digest: `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`

## Credential-clean controller retirement — RELEASED

The former standalone `.github/workflows/advance-marketplace-coinbase-activation.yml` is absent from current `main`. It previously depended on `secrets.MARKETPLACE_COINBASE_EVIDENCE_TOKEN`, `github.token`, repository write permissions, checkout/setup actions, git commit/push writeback, and artifact upload.

The retained observation surface is local-only:

```text
scripts/advance_marketplace_coinbase_activation.py
data/marketplace-coinbase-activation-tasks.json
credential_requirement: NONE
github_token_allowed: false
non_tv_tvc_secret_or_token_allowed: false
remote_github_api_observation: false
continuation_mode: STEGVERSE_OWNED_OBSERVATION_ONLY
publication/release/execution/live/financial authority: false
```

The observer reads cross-repository evidence only from already-materialized repositories supplied through `STEGVERSE_REPO_ROOTS_JSON`. Missing local repositories or evidence become `BLOCKED_DEPENDENCY` owned by the named canonical repository/issue. No token, remote checkout, anonymous GitHub API fallback, or Render runtime is authorized.

## Canonical continuation owner

The fixed local invocation path is merged in `StegVerse-Labs/StegVerse-Healer`:

```text
Healer issue: #6
Healer PR: #7
Healer merge: ecf96188348c097dfdea3ce55c47db9dff6e84ef
Healer exact-head credential-clean validation: 32044423476 SUCCESS
Healer job: 95429249175 SUCCESS
scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001
target: marketplace-coinbase-local-observer
runtime inputs: already-materialized StegVerse repositories only
```

This is source integration only. Ordinary Healer runtime activation remains machine-owned and is not inferred from merge or CI.

## Site cleanup release evidence

```text
Site PR: #329
final head: caf9b6dae32f09b7475a0dbe61cbc5e7e873c089
merge: 72ca1b9377a918983d5bcb329fa4c13ab0294cc8
claim release commit: c00ac1906dc6bcfd5195e07dc7916e3cc2d760bc
Site Bootstrap Validate: 32044523223 SUCCESS
Check StegFin Phone Projection: 32044523162 SUCCESS
Ecosystem Heartbeat Orchestration: 32044523264 SUCCESS
Site Handoff Orchestrator: 32044523168 SUCCESS
workflow inventory: 109 / canonical 3 / migration-required operational 106 / placeholders 0
```

## Current continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19 / COMPLETE when VERIFIED
MC-04 Site projection -> StegVerse-Labs/Site#131 / COMPLETE when PAPER_ACCESSIBLE and live_trading_accessible=false
observer scheduling -> SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / StegVerse-Labs/StegVerse-Healer
```

## Remaining product work

Exact paper-release tag evidence remains owned by `StegVerse-Labs/crypto-bot#6`:

```text
required tag: marketplace-coinbase-paper-v1.0.0
required target: 73a0543ddb27a88fd4913e7dcfa2127132299baa
```

That product evidence task is separate from the now-released Site workflow/token migration.

## Collision boundaries

- TV/TVC remains credential authority.
- Do not export TV/TVC credentials into GitHub Actions.
- Do not use a GitHub/project/provider token to repair observation.
- Do not create a second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner.
- Do not infer Coinbase live trading, custody, withdrawal, funded execution, publication, release, or financial authority from paper accessibility or workflow cleanup.
- Do not modify StegFin, StegOS, or HIL claimed product paths.
- USER_ONLY remains the sole StegFin signing/broadcast authority.

## Archive condition

The controller-retirement integration is complete and released. The broader workflow-cleanup session is not archive-ready while Site #268 retains workflow/token remediation debt. Marketplace/Coinbase product activation remains separately bounded by its canonical owners and must not be inferred from this cleanup.

## Progress

```text
paper-accessibility developed files: 5/5
paper-accessibility deterministic validation: PASS historical contract
Site paper projection integration: COMPLETE
Healer local observer source integration: MERGED
controller token-retirement implementation: MERGED
controller exact-head validation: PASS
controller claim: RELEASED
live/financial authority: NOT GRANTED
```
