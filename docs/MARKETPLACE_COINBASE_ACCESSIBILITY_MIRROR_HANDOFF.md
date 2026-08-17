# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Active cleanup claim: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B16R1-20260817`
- Active branch: `chore/site-marketplace-accessibility-import-retirement-b16r1-20260817`
- Goal: preserve the already-verified paper-accessibility projection while removing the remaining GitHub-hosted importer mechanics that are no longer required.

## Authoritative files

- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/marketplace-coinbase-accessibility-status.json`
- `scripts/advance_marketplace_coinbase_activation.py`
- `data/marketplace-coinbase-activation-tasks.json`
- this handoff

`.github/workflows/import-marketplace-coinbase-accessibility.yml` is intentionally removed on B16R1. Deterministic source/tests and the committed projection are retained for bounded StegVerse-local reconstruction.

## Current product state

```text
state: PAPER_ACCESSIBLE
paper_trading_accessible: true
live_trading_accessible: false
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
financial_authority: NOT_GRANTED
```

The Site projection is display/continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified product evidence

- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`
- initial Site projection activation: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine importer persistence: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- deterministic projection tests: `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- projection digest: `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`

Retained deterministic contract:

```text
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
historical result: 4 passed
```

## Controller retirement — released

PR #329 already removed the GitHub-token/writeback activation controller and bound local observation to the existing sovereign Healer scheduler `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` target `marketplace-coinbase-local-observer`. That path remains machine-owned; B16R1 does not duplicate it.

## B16R1 hosted importer retirement

The removed importer workflow previously contained:

```text
hourly schedule
permissions.contents: write
actions/checkout@v4
actions/setup-python@v5
repository commit/pull/rebase/push writeback
actions/upload-artifact@v4
```

Those mechanics are unnecessary after the bounded Site projection is already durably `PAPER_ACCESSIBLE`. No replacement GitHub workflow, scheduler, heartbeat, PAT, GitHub token, provider credential, or TV/TVC credential export is introduced.

`import_marketplace_coinbase_accessibility.py` remains available only for bounded, admitted StegVerse-local reconstruction or a fresh explicit projection task. State retention is not wall-clock execution authority. A future upstream change requires a fresh claim rather than silently reactivating hosted automation.

## Continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19 / COMPLETE when VERIFIED
MC-04 Site projection -> StegVerse-Labs/Site#131 / COMPLETE at PAPER_ACCESSIBLE with live_trading_accessible=false
observer scheduling -> StegVerse-Labs/StegVerse-Healer / SHWP-HEALER-SOVEREIGN-SCHEDULER-001
paper-release tag evidence -> StegVerse-Labs/crypto-bot#6
```

## B16R1 release condition

```text
import-marketplace-coinbase-accessibility.yml: ABSENT
committed state remains PAPER_ACCESSIBLE
live_trading_accessible: false
publication/release/execution/live authority: NOT_GRANTED
retained deterministic importer tests: PASS
SESSION_WORK_CLAIMS_PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
Check StegFin Phone Projection: PASS
workflow inventory: 107 total / 3 canonical / 104 migration-required / 0 placeholders
```

Hosted validation remains source evidence only and cannot activate Marketplace, Coinbase, StegFin, HIL, heartbeat, model, wallet, publication, or financial authority.

## Collision boundaries

- TV/TVC remains credential authority.
- No NON-TV/TVC secret/token may become a project/runtime dependency.
- Do not export TV/TVC credentials into GitHub Actions.
- Do not create a second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner.
- Do not infer live trading, custody, withdrawal, funded execution, publication, release, or financial authority from paper accessibility or workflow cleanup.
- Do not modify StegFin, StegOS, or HIL claimed product paths.
- USER_ONLY remains the sole StegFin signing/broadcast authority.
- Do not use Render.

## Archive condition

B16R1 may be released only after exact-head validation, merge, post-merge census, claim release, and canonical cost-containment handoff update. The broader Site #268 cleanup remains active afterward while workflow/token remediation debt exists.
