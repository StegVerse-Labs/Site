# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: chore/site-marketplace-projection-import-retirement-20260817
coordination: StegVerse-Labs/.github#164
workflow_minimization_coordination: StegVerse-Labs/.github#167
repository_issues: Site#265, Site#268
credential_authority: TV/TVC
non_tv_tvc_project_or_provider_secret_allowed: false
github_actions_production_carrier_required: false
preferred_workflow_surface: <=2 stable GitHub entry surfaces, with evidence-backed standalone exceptions only
canonical_claim_registry: data/session-work-claims.json
prework_validator: scripts/check_session_work_claims.py
repository_orchestrator: scripts/site_handoff_orchestrator.py
active_implementation_claim: SITE-MARKETPLACE-COINBASE-PROJECTION-IMPORT-RETIREMENT-20260817
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source validation only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Released accounting before active projection-import retirement

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 30/131 = 22.90%
remaining_audit_start_surfaces: 101/131
current_released_main_workflow_count: 108
workflow_files_eliminated_or_consolidated_by_released_cleanup: 19
released_completed_batches_or_equivalent_semantic_migrations: 16
released_validation_groups: 68/68 PASS
released_integrations: 16/16
review_required_surfaces: 1
canonical_workflows: 3
migration_required_operational: 105
placeholders: 0
```

PR #333 / Batch 15 is released at merge `bb2850425943d1590594096b6d453a5c1822881f`; exact census is 108 workflows / canonical 3 / migration-required 105 / placeholders 0. The active projection-import claim is not counted as released.

## Released minimization evidence

Released work includes PRs #270, #271, #272, #273, #305, #308, #310, #312, #313, #315, #316, #318, #324, #327, #329, and #333. Immutable commit/run evidence remains in Git history and released claims.

Most recent released batches:

```text
PR #329 merge 72ca1b9377a918983d5bcb329fa4c13ab0294cc8 — Marketplace Coinbase token/writeback controller retired; local observation bound to sovereign Healer
PR #333 merge bb2850425943d1590594096b6d453a5c1822881f — HIL HTTPS receiver-probe regression workflow retired; deterministic regression retained in credential-clean HIL dispatcher
```

## Active distinct cleanup — Marketplace Coinbase projection importer

```text
claim: SITE-MARKETPLACE-COINBASE-PROJECTION-IMPORT-RETIREMENT-20260817
task: SITE-ACTIONS-COST-CONTAINMENT-MARKETPLACE-PROJECTION-IMPORT-20260817
branch: chore/site-marketplace-projection-import-retirement-20260817
Healer issue: StegVerse-Labs/StegVerse-Healer#8
Healer branch: feat/site-marketplace-projection-local-import-8
state: CLAIMED_FOR_IMPLEMENTATION
```

The still-released-main workflow `.github/workflows/import-marketplace-coinbase-accessibility.yml` currently carries an hourly GitHub-hosted schedule, `contents: write`, `actions/checkout`, `actions/setup-python`, `pip install pytest`, repository commit/push writeback, and artifact upload. It therefore remains inconsistent with the no-NON-TV/TVC-token / no-GitHub-runtime-authority direction even though its product contract is paper-only.

Installed on the active Site branch:

- `.github/workflows/import-marketplace-coinbase-accessibility.yml` removed;
- `scripts/import_marketplace_coinbase_accessibility.py` no longer imports `urllib` or fetches `raw.githubusercontent.com`;
- Publisher evidence resolves only from already-materialized `GCAT-BCAT-Engine/Publisher` in `STEGVERSE_REPO_ROOTS_JSON`;
- GitHub/Marketplace credential environment is rejected;
- missing local Publisher repository/evidence fails closed to bounded dependency/pending state;
- projection state records local source transport, credential requirement `NONE`, GitHub token disallowed, remote fetch disallowed, and financial/live/publication/release/execution authority not granted;
- deterministic tests cover local materialization, credential refusal, no remote GitHub fetch contract, digest/authority boundaries.

Companion Healer source on issue #8 / PR pending binds fixed target `marketplace-coinbase-local-projection-import` into the existing `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`; no second scheduler or heartbeat is permitted.

## Collision boundaries

```text
Site #81: live HIL runtime observation — do not compete
Site #67: HIL lifecycle projection — do not compete
TVC #8: private review — do not compete
StegCore #41: lifecycle authority — do not compete
StegOS admitted inference: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT / CLAIMED_FOR_INTEGRATION
Site pre-work admission: SITE-PREWORK-CLAIM-GATE-MACHINE-001 / MACHINE_OWNED
Healer scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / MACHINE_OWNED; add fixed targets only, no second scheduler
HIL LinkedIn readiness: REVIEW_REQUIRED; do not modify check-hil-linkedin-launch-readiness.yml
```

The active cleanup may not grant Marketplace, Coinbase live/financial/custody/withdrawal, Publisher, crypto-bot, Site publication/release/execution, StegFin, provider, wallet, heartbeat, or runtime authority. USER_ONLY remains sole StegFin signer/broadcaster.

## Local model/runtime and StegFin convergence

```text
formal_local_model: COMPLETE_RELEASED
local_runtime_discovery_launch_inference_proof: COMPLETE_RELEASED
descriptive_select_local_model_runtime_step: SUPERSEDED
credential_authority: TV/TVC
github_token_production_authority: NONE
StegFin wallet signing/broadcast: USER_ONLY
```

Do not recreate those machine-owned capabilities in Site or GitHub Actions.

## Required release gates for active claim

1. Healer issue #8 fixed local projection target passes credential-clean deterministic validation and merges.
2. Site claim/orchestrator validation PASS.
3. Ecosystem Heartbeat Orchestration PASS.
4. Site Bootstrap Validate PASS, including canonical application and ST-017 sandbox.
5. StegFin phone projection PASS if triggered, without wallet authority.
6. Marketplace projection regression tests PASS.
7. Exact merge-checkout workflow inventory decrements exactly one from released baseline 108 to 107, retains canonical 3 and placeholders 0.
8. Main no longer contains `.github/workflows/import-marketplace-coinbase-accessibility.yml`; importer remains local-only and handoffs/claim are released with immutable evidence.

## Next executable action

Complete Healer #8 validation/merge, update the Site Marketplace product handoff to the local-only continuation contract, open the Site PR, inspect exact-head runs/jobs/logs, merge only after all required gates pass, then release the claim and recensus. If this migration releases, continue the next unclaimed workflow family under Site #268.

## Completion accounting — released work only

```text
task_completion: 30/131 = 22.90%
developed_files_for_completed_surfaces: 30/30
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 68/68 released validation groups PASS
integration: 16/16 released groups
active_projection_import_retirement: implementation installed; validation/integration pending
propagation: not yet applicable
goal_activation_for_cleanup_goal: 30/131 = 22.90%
session_consolidation: incomplete
```

## Archive condition

The session remains active because this projection-import claim is unreleased and 101/131 audit-start surfaces remain unremediated/unclassified before this delta. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately worker-owned and are not inferred from source or CI state.
