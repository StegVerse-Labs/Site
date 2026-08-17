# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: chore/site-master-records-import-validation-b23-20260817
coordination: StegVerse-Labs/.github#164
workflow_minimization_coordination: StegVerse-Labs/.github#167
repository_issues: Site#265, Site#268
credential_authority: TV/TVC
non_tv_tvc_project_or_provider_secret_allowed: false
github_actions_production_carrier_required: false
preferred_workflow_surface: <=2 stable GitHub entry surfaces, with evidence-backed exceptions only
canonical_claim_registry: data/session-work-claims.json
prework_validator: scripts/check_session_work_claims.py
repository_orchestrator: scripts/site_handoff_orchestrator.py
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B23-20260817
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source validation only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Current released accounting and exact census

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 37/131 = 28.24%
remaining_audit_start_surfaces: 94/131
current_released_main_workflow_count: 102
workflow_files_eliminated_or_consolidated_by_released_cleanup: 25
released_completed_batches_or_equivalent_semantic_migrations: 23
released_validation_groups: 97/97 PASS
released_integrations: 23/23
review_required_surfaces: 1
canonical_workflows: 3
migration_required_operational: 99
placeholders: 0
```

The released baseline remains `102 workflow file(s)`, `CANONICAL: 3`, `MIGRATION REQUIRED OPERATIONAL: 99`, `PLACEHOLDERS: 0`. Batch 23 is not counted as released until exact-head validation and merge.

## Released minimization evidence

Released workflow/token-remediation work includes PRs #270, #271, #272, #273, #305, #308, #310, #312, #313, #315, #316, #318, #324, #327, #329, #333, #337, #345, #349, #351, #353, #355, plus the ST-018 credential-clean remediation merged at commit `69f1f89e09b6b4e4d2d89267d3c148435df9b061`.

The Marketplace projection local-import correction is separately released at PR #352 / merge `218fee91a7d2214fec328f74247e079292c45ce0`; it hardens retained acquisition but is not counted as an additional audit-start workflow remediation.

## Latest released workflow batch — Batch 22 Ecosystem Node canonical-event validation consolidation

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B22-20260817
state: MERGED_INTO_CANONICAL_WORKSTREAM / RELEASED_INTEGRATION
PR: #355
final_head: eda1bef70514295838d991ba2e87ef369f9b4837
merge: 1b0391f3b9b0de65524aff5dbf10959b7573e67d
Site Handoff Orchestrator: 32051234538 SUCCESS
Ecosystem Heartbeat Orchestration: 32051178520 SUCCESS
Check StegFin Phone Projection: 32051178509 SUCCESS
Site Bootstrap Validate: 32051179223 SUCCESS
Check Ecosystem Node Gateway Binding: 32051181466 SUCCESS
workflow inventory: 102 / canonical 3 / migration-required operational 99 / placeholders 0
ST-017 sandbox: PASS
SESSION_WORK_CLAIMS_PASS
SITE_HANDOFF_ORCHESTRATION_PASS
ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS
authority_effect: NONE
runtime_activation_effect: NONE
provider_authority_effect: NONE
```

## Released adjacent remediation — ST-018 GitHub-token validation custody retirement

```text
claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
state: MERGED_INTO_CANONICAL_WORKSTREAM / RELEASED_INTEGRATION
release_commit: 69f1f89e09b6b4e4d2d89267d3c148435df9b061
final_head: a16f58fd2f138825f674afb714826b7af91fe331
Capture Validation Evidence: 32051470522 SUCCESS
Ecosystem Heartbeat Orchestration: 32051470520 SUCCESS
Site Handoff Orchestrator: 32051470664 SUCCESS
Site Bootstrap Validate: 32051470819 SUCCESS
credential refusal: PASS
exact public source fetch: PASS
declared validator receipt enforcement: PASS
artifact custody: NONE
issue custody: NONE
authority_effect: NONE
runtime_activation_effect: NONE
custody_authority_effect: NONE
```

`.github/workflows/capture-validation-evidence.yml` remains deterministic validation but is credential-clean and non-authorizing.

## Active Batch 23 — Master Records persistent-service evidence import validation consolidation

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B23-20260817
task: SITE-ACTIONS-COST-CONTAINMENT-B23-20260817
branch: chore/site-master-records-import-validation-b23-20260817
state: CLAIMED_FOR_IMPLEMENTATION
retired_candidate: .github/workflows/check-master-records-persistent-service-evidence-import.yml
retained_validator: scripts/check_master_records_persistent_service_evidence_import.py
retained_host_surface: .github/workflows/validate.yml
```

Installed bounded delta:

- removes the standalone workflow that used `actions/checkout@v4`, `actions/setup-python@v5`, and `contents: read`;
- keeps the existing fail-closed validator byte-for-byte unchanged;
- executes that validator inside the credential-refusing, anonymous-fetch, `permissions: {}` Site Bootstrap workflow;
- adds an explicit bootstrap self-check requiring the validator invocation to remain present;
- does not change imported Master Records evidence, source repository semantics, custody, reconstruction, release, publication, or activation authority;
- does not export TV/TVC credentials or introduce any NON-TV/TVC token;
- does not create a scheduler or runtime path.

Expected exact-head inventory is:

```text
workflow files: 101
canonical workflows: 3
migration-required operational: 98
placeholders: 0
```

Required validation before merge: `MASTER_RECORDS_PERSISTENT_SERVICE_EVIDENCE_IMPORT=PASS`, Site Bootstrap, Site Handoff Orchestrator, Ecosystem Heartbeat, StegFin phone projection if triggered, claim/orchestration checks, canonical Site application, and ST-017 sandbox.

## Blocked distinct candidate — HIL session-consolidation workflow

The standalone `.github/workflows/check-hil-session-consolidation.yml` remains present. Prior attempts proved `check_session_retirement.py` correctly fails closed because the ARCHIVABLE `hil-runtime-consolidation-2026-08-02` receipt in `data/session-orchestration-registry.json` names that workflow as a required `material_state_location`.

Correct migration requires the canonical session-orchestration owner, Site #114, to update or explicitly admit migration of that archival material-state pointer. `check-hil-linkedin-launch-readiness.yml` remains REVIEW_REQUIRED.

## Collision boundaries

```text
master-records/orchestration: source custody/reconstruction/candidate release authority; Batch 23 validates imported evidence only
Site #81: live same-origin HIL receiver/readiness/runtime observation
Site #67: HIL lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: cross-repository lifecycle consistency
Site #114: session orchestration/retirement authority
SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT: separate claimed product paths
SITE-PREWORK-CLAIM-GATE-MACHINE-001: MACHINE_OWNED orchestration admission
SHWP-HEALER-SOVEREIGN-SCHEDULER-001: MACHINE_OWNED scheduler
StegFin wallet signing/broadcast: USER_ONLY
```

Cleanup may not create or duplicate those authorities. Retained hosted validation mechanics remain migration debt unless evidence proves them technically necessary; they never become production/runtime/control-plane authority.

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

Canonical continuation remains:

```text
StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md
StegVerse-Labs/stegfin-governance/task-state/STEGFIN-CONTINUITY-CARRIER-007.json
StegFin #77 / current phone participant path
```

Credential authority is TV/TVC. Wallet signing/broadcast are USER_ONLY. No workflow cleanup, source merge, CI success, publication, or deployment implies trade execution or settlement.

## Session goal transfer inventory

```text
local model/runtime implementation: COMPLETE_RELEASED -> StegVerse-Labs/.github + StegVerse-002/micro-node-runtime handoffs
StegFin trade preparation/authority continuation: MERGED_INTO_CANONICAL_WORKSTREAM -> stegfin-governance handoff/task-state + StegFin #77
HIL live lifecycle/review/custody: MERGED_INTO_CANONICAL_WORKSTREAM -> Site #81/#67, TVC #8, StegCore #41, master-records/orchestration
Site workflow/token minimization: ACTIVE_REMEDIATION -> this handoff + Site #268
session archival determination: ACTIVE until no unique validation/integration/reconciliation/propagation responsibility remains
```

## Next executable action

Open and validate the Batch-23 PR from this exact branch. Inspect workflow runs, jobs and logs. Merge only if the exact head passes and the merge-checkout inventory is exactly `101 / 3 / 98 / 0`. After merge, release the Batch-23 claim and record immutable evidence here, then inspect the next bounded unclaimed workflow family under Site #268.

## Completion accounting — released work only

```text
task_completion: 37/131 = 28.24%
developed_files_for_completed_surfaces: 37/37
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 97/97 released validation groups PASS
integration: 23/23 released workflow/token-remediation groups
active_batch_23: implementation installed; exact-head validation pending
goal_activation_for_cleanup_goal: 37/131 = 28.24%
session_consolidation: 3/5 durable goal groups complete or transferred
```

## Archive condition

This session is not archive-ready while Batch 23 is unreleased and broader Site #268 workflow/token debt remains. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately owned and are not inferred from source or validation state.
