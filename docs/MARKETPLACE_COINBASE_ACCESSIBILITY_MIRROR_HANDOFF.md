# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and authority

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Released controller-cleanup claim: `SITE-MARKETPLACE-COINBASE-ACTIVATION-CONTROLLER-TOKEN-RETIREMENT-20260817`
- Active projection-import cleanup claim: `SITE-MARKETPLACE-COINBASE-PROJECTION-IMPORT-RETIREMENT-20260817`
- Goal: preserve verified Publisher paper projection while removing GitHub-hosted scheduling/writeback/token mechanics and retaining no live or financial authority.

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

Existing verified projection evidence remains bound to Publisher status `VERIFIED`, Publisher status digest `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`, Site projection digest `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`, and historical deterministic projection tests.

## Released local observer path

The former `advance-marketplace-coinbase-activation.yml` hosted controller is absent from main. Local observation is source-bound to existing Healer scheduler `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` target `marketplace-coinbase-local-observer` via Healer PR #7 merge `ecf96188348c097dfdea3ce55c47db9dff6e84ef` and Site PR #329 merge `72ca1b9377a918983d5bcb329fa4c13ab0294cc8`.

## Active projection-import migration

Released main still has `.github/workflows/import-marketplace-coinbase-accessibility.yml`, which schedules hourly hosted execution, grants `contents: write`, uses checkout/setup-python, installs pytest, commits/pushes Site projection state, and uploads artifacts. That hosted recurrence is being retired under the active cleanup claim.

Installed on the active branch:

```text
.github/workflows/import-marketplace-coinbase-accessibility.yml: REMOVED
scripts/import_marketplace_coinbase_accessibility.py: LOCAL_ONLY
Publisher source transport: LOCAL_MATERIALIZED_REPOSITORY
repository roots input: STEGVERSE_REPO_ROOTS_JSON
credential requirement: NONE
GitHub token allowed: false
remote source fetch allowed: false
publication/release/execution/live/financial authority: NOT_GRANTED
```

The importer no longer imports `urllib`, references `raw.githubusercontent.com`, or performs remote source acquisition. It rejects GitHub/Marketplace credential environment and reads only `GCAT-BCAT-Engine/Publisher/data/marketplace-coinbase-release-evidence-status.json` from an already-materialized Publisher repository. Missing Publisher repository/evidence becomes a bounded `PENDING_UPSTREAM`/dependency state; forbidden credentials fail closed.

Deterministic tests now cover:

- committed projection digest and paper-only authority boundary;
- valid Publisher acceptance;
- authority escalation rejection;
- digest tamper rejection;
- required local Publisher materialization;
- exact local Publisher evidence loading;
- forbidden credential rejection;
- absence of remote GitHub-fetch contract.

## Canonical recurrence owner under construction

Healer issue `StegVerse-Labs/StegVerse-Healer#8` and PR #9 bind fixed target `marketplace-coinbase-local-projection-import` into the existing `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`.

The handler requires already-materialized Site and Publisher repositories, invokes only the local Site importer, fails closed when either required local surface is absent, and creates no second scheduler/heartbeat or credential path. Healer merge/CI will be source evidence only; ordinary scheduler activation remains machine-owned and requires its admitted post-carrier runtime receipt.

## Current continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19
MC-04 Site projection -> StegVerse-Labs/Site#131
observer recurrence -> SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / marketplace-coinbase-local-observer
projection-import recurrence -> Healer#8 / PR #9 pending source release
```

Exact paper-release tag evidence remains separately owned by `StegVerse-Labs/crypto-bot#6` and is not altered by this workflow migration.

## Collision and authority boundaries

- TV/TVC remains credential authority.
- No TV/TVC credential is exported to GitHub Actions.
- No GitHub/project/provider token is authorized for projection import.
- No second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner may be created.
- Paper accessibility does not grant Coinbase live trading, custody, withdrawal, funded execution, publication, release, or financial authority.
- StegFin signing/broadcast remains USER_ONLY.
- Do not modify StegOS or HIL claimed product paths.
- Do not use Render.

## Release condition for active cleanup

1. Healer #8 / PR #9 fixed local projection-import handler passes credential-clean tests and merges.
2. Site projection regression tests pass on exact cleanup head.
3. Site claim/orchestrator, Heartbeat, Bootstrap, and StegFin projection checks pass.
4. Exact workflow census falls from released 108 to 107, retains canonical 3, placeholders 0.
5. Site PR merges; hosted projection workflow is absent from main; importer remains local-only.
6. Site and Healer claims/handoffs are released with exact evidence.

## Archive condition

The paper product projection is already established, but this workflow migration is not archive-safe until the active projection-import claim is released. Broader Site #268 workflow/token minimization remains active afterward. Product live/financial activation remains separately governed and is not inferred from this cleanup.
