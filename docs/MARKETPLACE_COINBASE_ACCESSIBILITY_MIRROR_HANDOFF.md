# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Active workflow-cleanup claim: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B16-20260817`
- Active cleanup branch: `chore/site-marketplace-accessibility-import-retirement-b16-20260817`
- Goal: preserve the verified paper-accessibility projection while removing GitHub-hosted token/writeback/runtime mechanics that are no longer required.

## Authoritative files

- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/marketplace-coinbase-accessibility-status.json`
- `scripts/advance_marketplace_coinbase_activation.py`
- `data/marketplace-coinbase-activation-tasks.json`
- this handoff

`.github/workflows/import-marketplace-coinbase-accessibility.yml` is intentionally removed on the active B16 branch. Its deterministic importer source and tests remain retained for bounded StegVerse-local reconstruction and validation.

## Current product state

```text
SITE_MARKETPLACE_COINBASE_PAPER_ACCESSIBILITY_ACTIVATED_AND_MACHINE_PERSISTED
state: PAPER_ACCESSIBLE
paper_trading_accessible: true
live_trading_accessible: false
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
financial_authority: NOT_GRANTED
```

The committed projection is display/continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified product evidence

- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher machine persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`
- initial Site projection activation commit: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine-owned importer persistence commit: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- projection tests: `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- workflow validation binding: `04dab58eafc6d47779f1196486c1384d5fe1ed3a`
- projection digest: `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`

Deterministic contract retained:

```text
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
historical result: 4 passed
```

## Hosted workflow retirement

The retired importer workflow previously had all of the following GitHub-hosted mechanics:

```text
hourly schedule
permissions.contents: write
actions/checkout@v4
actions/setup-python@v5
repository commit/pull/rebase/push writeback
actions/upload-artifact@v4
```

Those mechanics are not needed to preserve a projection that is already committed as `PAPER_ACCESSIBLE`. No replacement GitHub workflow, scheduler, token, PAT, provider secret, or TV/TVC credential export is introduced.

The importer implementation remains source-only and may be executed only in an admitted StegVerse-local context when reconstruction or a fresh bounded upstream projection is explicitly required. Missing or changed upstream evidence does not silently reactivate hosted automation; it requires a fresh admitted task/claim.

## Canonical continuation owner

The separate Marketplace/Coinbase observation path is already source-bound to the existing sovereign Healer scheduler:

```text
StegVerse-Labs/StegVerse-Healer issue: #6
Healer PR: #7
Healer merge: ecf96188348c097dfdea3ce55c47db9dff6e84ef
scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001
target: marketplace-coinbase-local-observer
credential_requirement: NONE
runtime inputs: already-materialized StegVerse repositories only
```

B16 does not create a second scheduler and does not add the importer as a recurring Healer task. The projection is state-retained, not clock-driven. Ordinary Healer runtime activation remains machine-owned and is not inferred from source merge or CI.

## Current continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19 / COMPLETE when VERIFIED
MC-04 Site projection -> StegVerse-Labs/Site#131 / COMPLETE at PAPER_ACCESSIBLE with live_trading_accessible=false
observer scheduling -> StegVerse-Labs/StegVerse-Healer / SHWP-HEALER-SOVEREIGN-SCHEDULER-001
```

Exact paper-release tag evidence remains separately owned by `StegVerse-Labs/crypto-bot#6` for tag `marketplace-coinbase-paper-v1.0.0` at target `73a0543ddb27a88fd4913e7dcfa2127132299baa`.

## B16 validation/release condition

Required before B16 release:

```text
import-marketplace-coinbase-accessibility.yml: ABSENT
committed Site state: PAPER_ACCESSIBLE
live_trading_accessible: false
publication/release/execution/live authority: NOT_GRANTED
retained deterministic importer tests: PASS
session claim validation: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
Check StegFin Phone Projection: PASS
workflow census: 108 total / 3 canonical / 105 migration-required / 0 placeholders
```

Hosted validation is source evidence only and cannot activate Marketplace, Coinbase, StegFin, HIL, heartbeat, model, wallet, publication, or financial authority.

## Collision boundaries

- TV/TVC remains credential authority.
- No NON-TV/TVC secret/token or GitHub token may be introduced as a project/runtime dependency.
- Do not export TV/TVC credentials into GitHub Actions.
- Do not create a second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner.
- Do not infer Coinbase live trading, custody, withdrawal, funded execution, publication, release, or financial authority from paper accessibility or workflow cleanup.
- Do not modify StegFin, StegOS, or HIL claimed product paths.
- USER_ONLY remains the sole StegFin signing/broadcast authority.
- Do not use Render.

## Archive condition

B16 may be released only after exact-head validation, merge, post-merge census, claim release, and canonical cost-containment handoff update. The broader workflow-cleanup session remains active while Site #268 retains workflow/token remediation debt.
