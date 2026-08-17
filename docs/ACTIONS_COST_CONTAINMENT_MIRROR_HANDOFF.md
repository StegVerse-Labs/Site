# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
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
active_implementation_claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-B17-20260817
active_validation_claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-B17-20260817
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source validation only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Current released accounting and exact census

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 31/131 = 23.66%
remaining_audit_start_surfaces: 100/131
current_released_main_workflow_count: 107
workflow_files_eliminated_or_consolidated_by_released_cleanup: 20
released_completed_batches_or_equivalent_semantic_migrations: 17
released_validation_groups: 72/72 PASS
released_integrations: 17/17
review_required_surfaces: 1
canonical_workflows: 3
migration_required_operational: 104
placeholders: 0
```

Released main is bound to PR #337 exact validation at `107 / canonical 3 / migration-required 104 / placeholders 0`.

## Released minimization evidence

```text
PR #270 — HIL first-release validation consolidation
PR #271 — obsolete HIL v0.5 installers removed
PR #272 — completed HIL deployment investigation removed
PR #273 — completed HIL pilot evidence investigation removed
PR #305 — HIL import validators folded
PR #308 — Master Record release projection folded; LinkedIn retained REVIEW_REQUIRED
PR #310 — Federal-Plus validation folded; hosted schedule retired
PR #312 — Master Records return-receipt validation folded
PR #313 — Master Records transfer-packet validation folded
PR #315 — Site Bootstrap token/writeback/private-runtime authority retired
PR #316 — HIL public-response import validation folded
PR #318 — HIL activation-state validation folded and stale validator semantics repaired
PR #324 — terminal Marketplace first-accessibility hosted continuation retired
PR #327 — terminal Marketplace first-accessibility hosted importer retired
PR #329 — Marketplace Coinbase GitHub-token/writeback controller retired; continuation bound to sovereign Healer scheduler
PR #333 — HIL HTTPS receiver-probe regression workflow retired; deterministic regression suite folded into credential-clean HIL dispatcher
PR #337 — Marketplace Coinbase hosted accessibility importer retired after terminal PAPER_ACCESSIBLE projection
```

## Active B17 — ST-018 GitHub-token/evidence-transport retirement

```text
claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-B17-20260817
branch: chore/site-st018-validation-consolidation-b17-20260817
scoped_handoff: docs/ST018_VALIDATION_EVIDENCE_MIRROR_HANDOFF.md
state: CLAIMED_FOR_IMPLEMENTATION
released_main_baseline: 107 workflows / canonical 3 / migration-required 104 / placeholders 0
projected_branch_census: 106 workflows / canonical 3 / migration-required 103 / placeholders 0
```

The removed `.github/workflows/capture-validation-evidence.yml` had `issues: write`, checkout/setup actions, two artifact-upload paths, `GH_TOKEN=${{ github.token }}`, and GitHub issue-comment mutation. It treated GitHub artifacts/comments as native-main custody evidence even though current policy requires TV/TVC-only credentials and denies GitHub production/control-plane authority.

B17 preserves the ST-018 manifest/schema/source and moves deterministic execution into canonical credential-clean `.github/workflows/validate.yml`:

```text
python3 scripts/capture_validation_manifest.py
-> require receipt status PASS
-> require all authority fields false
-> no upload-artifact
-> no issue mutation
-> no GH_TOKEN/github.token
```

The canonical validator already uses `permissions: {}`, refuses credential-bearing environment variables, anonymously fetches the exact ref, and uses preinstalled Python. B17 does not create a replacement scheduler or custody authority. GitHub-hosted validation remains source evidence only.

Release requires exact-head claim/orchestrator/heartbeat/bootstrap/StegFin PASS, ST-018 local receipt PASS with authority ceiling false, census `106 / 3 / 103 / 0`, merge, Site #141 reconciliation, claim release and handoff finalization.

## HIL / runtime / financial collision boundaries

```text
Site #81: live HIL receiver/readiness/runtime observation
Site #67: HIL lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: lifecycle consistency
master-records/orchestration: custody/reconstruction/candidate release authority
StegOS admitted inference: separate active product paths
Healer scheduler: MACHINE_OWNED / do not compete
StegFin signing/broadcast: USER_ONLY
```

Do not modify `check-hil-linkedin-launch-readiness.yml` while its semantic drift remains `REVIEW_REQUIRED`. Cleanup may not mint provider, credential, runtime, publication, financial, wallet, model, HIL review or Master Records authority.

## Local model/runtime convergence

```text
formal_local_model: COMPLETE_RELEASED
local_runtime_discovery_launch_inference_proof: COMPLETE_RELEASED
descriptive_select_local_model_runtime_step: SUPERSEDED
local_model_credential_requirement: NONE
credential_authority: TV/TVC
github_token_production_authority: NONE
```

Canonical continuation remains `StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md` and `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`. Do not recreate local-model/runtime execution in Site or GitHub Actions.

## StegFin convergence

Canonical continuation remains `StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`, `task-state/STEGFIN-CONTINUITY-CARRIER-007.json`, and StegFin #77/current phone. Trade execution remains machine/human-authority owned; wallet signing/broadcast are USER_ONLY.

## Next executable action

Validate B17 exact head. If green, merge, recensus current main, reconcile Site #141, release the claim, finalize this handoff, then inspect the next bounded unclaimed token-bearing/redundant workflow under Site #268.

## Completion accounting — released work only

```text
task_completion: 31/131 = 23.66%
developed_files_for_completed_surfaces: 31/31
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 72/72 released validation groups PASS
integration: 17/17 released workflow/token-remediation groups
B17: implemented on branch / exact-head validation pending
session_consolidation: incomplete
```

## Archive condition

This session remains active because B17 is not yet released and 100/131 audit-start Site workflow surfaces remain unremediated/unclassified at the released baseline. Live HIL, sovereign runtime/inference, Healer execution and StegFin settlement remain separately worker-owned and are not inferred from source or validation state.
