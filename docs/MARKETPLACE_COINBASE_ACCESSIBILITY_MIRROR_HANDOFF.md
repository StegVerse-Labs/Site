# Marketplace–Coinbase Accessibility Mirror Handoff

## Canonical authority

```text
goal_id: MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001
active_task: SITE-MARKETPLACE-COINBASE-PROJECTION-LOCAL-IMPORT-CORRECTION-20260817
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: claim/site-marketplace-projection-local-import-correction-20260817
owner_issue: Site#131
parent_cleanup: Site#268
cross_repository_owner: StegVerse-Labs/StegVerse-Healer#8
scheduler_owner: SHWP-HEALER-SOVEREIGN-SCHEDULER-001
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_production_authority: NONE
```

Live repository state and exact validation evidence supersede chat history.

## Product boundary

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

`.github/workflows/import-marketplace-coinbase-accessibility.yml` was removed by released B16R1 and remains absent.

## Cross-repository integration correction

Healer PR #9 merged fixed target `marketplace-coinbase-local-projection-import` and supplies already-materialized Site and `GCAT-BCAT-Engine/Publisher` roots through `STEGVERSE_REPO_ROOTS_JSON`. The retained Site importer on canonical main still used `raw.githubusercontent.com`, so the child implementation ignored that local-only contract.

The active correction now requires `STEGVERSE_REPO_ROOTS_JSON`, reads `GCAT-BCAT-Engine/Publisher/data/marketplace-coinbase-release-evidence-status.json` locally, removes raw GitHub acquisition, refuses GitHub/project credential environments, and fails closed to bounded `PENDING_UPSTREAM` when local evidence is unavailable. Existing schema, digest, VERIFIED-state, paper-only, and authority-escalation checks are retained.

Authoritative correction files:
- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/tasks/SITE-MARKETPLACE-COINBASE-PROJECTION-LOCAL-IMPORT-CORRECTION-20260817.json`
- `data/session-work-claims.json`
- this handoff

## Validation and release condition

Required evidence:

```text
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
SESSION_WORK_CLAIMS_PASS
Site Handoff Orchestrator PASS
Ecosystem Heartbeat Orchestration PASS
Site Bootstrap Validate PASS
Check StegFin Phone Projection PASS
merged exact-head Site PR
Healer #8 reconciliation after Site merge
```

No source/CI success grants ordinary Healer runtime activation. That remains MACHINE_OWNED under `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`.

## Collision boundaries

- do not create a second scheduler or heartbeat;
- do not modify Healer machine-owned runtime implementation in this Site claim;
- do not export TV/TVC credentials or introduce any GitHub/PAT/provider token;
- do not infer publication, release, live trading, custody, withdrawal, financial, HIL, StegFin, wallet, model, or runtime authority;
- USER_ONLY remains sole StegFin signing/broadcast authority;
- do not use Render.

## Session consolidation

B16R1 is `MERGED_INTO_CANONICAL_WORKSTREAM`. This correction is `CLAIMED_FOR_INTEGRATION` until exact-head merge and Healer #8 reconciliation are durable. Developed correction files: 4/4; scaffolding/stubs: 0; integration remains pending.
