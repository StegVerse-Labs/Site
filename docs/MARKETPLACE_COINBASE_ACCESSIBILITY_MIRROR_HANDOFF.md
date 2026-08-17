# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and authority

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Released workflow claim: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B16R1-20260817`
- Active source-hardening claim: `SITE-MARKETPLACE-PROJECTION-LOCAL-SOURCE-HARDENING-20260817`
- Active branch: `fix/site-marketplace-projection-local-source-20260817`
- Goal: preserve the already-verified paper-accessibility projection while ensuring the deterministic importer retained after B16R1 is safe for the existing sovereign Healer local target and cannot perform remote GitHub source acquisition.

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

The Site projection remains display/continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified product evidence

- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`
- initial Site projection activation: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine importer persistence: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- deterministic projection tests: `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- projection digest: `sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3`

## Released B16R1 workflow retirement

```text
PR: #337
merge: b106d3479bafa458d56f4f450f1975925e7887e6
release record: 7eca3a6a8d2b9b5f5853fd028aa4a26a8083a7ab
workflow: .github/workflows/import-marketplace-coinbase-accessibility.yml ABSENT
workflow inventory: 107 / canonical 3 / migration-required 104 / placeholders 0
authority_effect: NONE
runtime_activation_effect: NONE
financial_authority_effect: NONE
```

B16R1 correctly removed the hourly GitHub-hosted schedule, `contents: write`, checkout/setup actions, repository writeback, and artifact upload. It retained deterministic importer source/tests and the committed `PAPER_ACCESSIBLE` state.

## Post-B16R1 source-hardening finding

After B16R1 released, the retained `scripts/import_marketplace_coinbase_accessibility.py` still contained:

```text
from urllib import error, request
https://raw.githubusercontent.com/GCAT-BCAT-Engine/Publisher/...
request.urlopen(...)
```

That was acceptable only as dormant reconstruction source while no local recurring execution was bound to it. Healer PR #9 subsequently source-bound fixed target `marketplace-coinbase-local-projection-import` to the retained Site importer, which made the remote-fetch capability a live precondition risk for any future admitted Healer execution.

The active hardening claim therefore changes the retained importer itself rather than recounting or recreating B16R1 workflow cleanup.

## Installed local-only importer contract

On `fix/site-marketplace-projection-local-source-20260817`:

```text
source repository: GCAT-BCAT-Engine/Publisher
source path: data/marketplace-coinbase-release-evidence-status.json
source transport: LOCAL_MATERIALIZED_REPOSITORY
repository roots: STEGVERSE_REPO_ROOTS_JSON
credential requirement: NONE
github_token_allowed: false
remote_source_fetch_allowed: false
publication/release/execution/live/financial authority: NOT_GRANTED
```

The importer now:

- rejects GitHub/Marketplace credential environment;
- requires an already-materialized Publisher repository in `STEGVERSE_REPO_ROOTS_JSON`;
- reads the exact Publisher evidence file locally;
- has no `urllib`, `raw.githubusercontent.com`, URL fetch, or authorization header path;
- treats missing local Publisher repository/evidence as bounded `PENDING_UPSTREAM` rather than permission to acquire credentials or fetch remotely;
- preserves digest, evidence-binding, paper-only, and authority-escalation validation.

Tests now prove local source materialization, credential refusal, no remote-fetch contract, committed projection integrity, Publisher digest validation, and authority-escalation rejection.

## Healer continuation and safety gate

Healer issue `StegVerse-Labs/StegVerse-Healer#8` remains the integration owner.

- Healer PR #9 merged source target `marketplace-coinbase-local-projection-import` at `b280025ed0007d10fdbb377cdf77cfd74443565c`.
- Because Site B16R1 released concurrently and retained the legacy remote-fetch source, Healer follow-up PR #10 adds a fail-closed capability gate: the target will not execute unless the materialized Site importer visibly binds `STEGVERSE_REPO_ROOTS_JSON` and `GCAT-BCAT-Engine/Publisher` and contains no remote URL/network markers.
- Until Site hardening releases, the correct Healer outcome is `SITE_MARKETPLACE_PROJECTION_LOCAL_CAPABILITY_NOT_INSTALLED`.

Source merge or CI does not prove ordinary Healer runtime activation. Runtime remains machine-owned by `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` and requires admitted post-carrier evidence.

## Continuation ownership

```text
MC-01 crypto accessibility -> StegVerse-Labs/crypto-bot#7
MC-02 Marketplace collection -> GCAT-BCAT-Engine/Marketplace#1
MC-03 Publisher verification -> GCAT-BCAT-Engine/Publisher#19
MC-04 Site projection -> StegVerse-Labs/Site#131
observer recurrence -> SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / marketplace-coinbase-local-observer
projection-import recurrence -> SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / marketplace-coinbase-local-projection-import, fail closed until this source-hardening claim releases
paper-release tag evidence -> StegVerse-Labs/crypto-bot#6
```

## Collision boundaries

- B16R1 workflow retirement is already canonical; do not recreate, re-delete, or count it twice.
- TV/TVC remains credential authority; no NON-TV/TVC secret/token may become runtime dependency.
- Do not export TV/TVC credentials into GitHub Actions.
- Do not create a second scheduler, heartbeat, runtime, Marketplace owner, Publisher owner, crypto-bot owner, or Site product owner.
- Do not infer live trading, custody, withdrawal, funded execution, publication, release, or financial authority from paper accessibility or source hardening.
- Do not modify StegFin, StegOS, or HIL claimed product paths.
- USER_ONLY remains sole StegFin signer/broadcaster.
- Do not use Render.

## Active hardening release condition

1. Healer PR #10 capability gate passes credential-clean validation and merges.
2. Site deterministic Marketplace projection tests pass against the local-only source.
3. Site claim/orchestrator, Heartbeat, Bootstrap, and StegFin projection checks pass on exact head.
4. Source-hardening PR merges without changing workflow census or recounting B16R1.
5. Main importer has no `urllib`, `raw.githubusercontent.com`, GitHub token/PAT/provider credential path, and binds only local Publisher materialization.
6. Site and Healer claims/handoffs record exact release evidence.

## Archive condition

This source-hardening claim is not archive-safe until those release gates complete. Broader Site #268 workflow/token minimization remains active afterward. Product live/financial activation remains separately governed and is not inferred from this source change.
