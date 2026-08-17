# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: chore/site-ecosystem-node-canonical-events-b22r1-20260817
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
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B22-20260817
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source validation only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Released accounting before Batch 22

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 35/131 = 26.72%
remaining_audit_start_surfaces: 96/131
current_released_main_workflow_count: 103
workflow_files_eliminated_or_consolidated_by_released_cleanup: 24
released_completed_batches_or_equivalent_semantic_migrations: 21
released_validation_groups: 88/88 PASS
released_integrations: 21/21
review_required_surfaces: 1
canonical_workflows: 3
migration_required_operational: 100
placeholders: 0
```

The released baseline is PR #353 exact merge-checkout validation: `103 workflow file(s)`, `CANONICAL: 3`, `MIGRATION REQUIRED OPERATIONAL: 100`, `PLACEHOLDERS: 0`. Batch 22 is not counted as released until merge and post-merge recensus.

## Released minimization evidence

Released workflow/token-remediation work through Batch 21 includes PRs #270, #271, #272, #273, #305, #308, #310, #312, #313, #315, #316, #318, #324, #327, #329, #333, #337, #345, #349, #351, and #353. Detailed historical run IDs and immutable diffs remain in Git history and `data/session-work-claims.json`.

Most recent releases:

```text
PR #345 — bounded user-LLM capability validator folded into canonical credential-clean Site application validation
PR #349 — bounded user-LLM execution-import-status validator folded into canonical credential-clean Site application validation
PR #351 — bounded user-LLM execution-receipt validator folded into canonical credential-clean Site application validation
PR #353 — Ecosystem Chat provider-neutral binding validator folded into canonical credential-clean Site application validation
```

The Marketplace projection local-import correction is separately released at PR #352 / merge `218fee91a7d2214fec328f74247e079292c45ce0`. It hardens retained source acquisition and is not counted as an additional workflow-surface retirement.

## Active Batch 22 — Ecosystem Node canonical-event validation consolidation

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B22-20260817
task: SITE-ACTIONS-COST-CONTAINMENT-B22-20260817
PR: #355
branch: chore/site-ecosystem-node-canonical-events-b22r1-20260817
validated_head_before_handoff_update: 4b6cfc7eb0cd39b3380b1eff37dce380347a7ea9
state: CLAIMED_FOR_IMPLEMENTATION / FINAL_EXACT_HEAD_REVALIDATION_PENDING
```

The retired standalone validation surface is:

```text
.github/workflows/validate-ecosystem-node-canonical-events.yml
```

The surviving bounded validation surface is:

```text
.github/workflows/check-ecosystem-node-gateway-binding.yml
```

Batch 22 preserves the standalone workflow's complete deterministic evidence rather than weakening it:

- Python compatibility matrix remains `3.9`, `3.11`, and `3.12`;
- browser gateway-binding validation remains;
- canonical event fixture validation remains;
- canonical-event schema, fixture, tests, and integrity documentation are trigger paths;
- `pytest` is installed once in the surviving workflow;
- adversarial `tests/test_ecosystem_node_canonical_events.py` coverage is executed in every matrix lane;
- no schedule, write permission, repository writeback, artifact upload, runtime authority, provider authority, wallet authority, publication authority, custody authority, Master Record authority, or product activation is added.

### Exact-head evidence before this handoff update

At head `4b6cfc7eb0cd39b3380b1eff37dce380347a7ea9`:

```text
Site Handoff Orchestrator: 32051050356 SUCCESS
Ecosystem Heartbeat Orchestration: 32051050450 SUCCESS
Check StegFin Phone Projection: 32051050351 SUCCESS
Site Bootstrap Validate: 32051050337 SUCCESS
Check Ecosystem Node Gateway Binding: 32051050352 SUCCESS
```

Gateway job evidence:

```text
verify (3.9)  job 95450232718 SUCCESS
verify (3.11) job 95450232636 SUCCESS
verify (3.12) job 95450234063 SUCCESS
```

Each of the three jobs passed:

```text
Install canonical event test dependency
Validate browser gateway binding contract
Revalidate canonical event integrity fixture
Run canonical event adversarial tests
```

These hosted runs are source/test evidence only. They do not establish a live Ecosystem Node runtime, provider execution, local-model/runtime activation, HIL activation, Master Record release, StegFin execution, wallet signing/broadcast, publication, custody, or downstream authority.

Because this handoff update changes the PR head, all required exact-head validation groups must pass again before merge. The expected post-merge census is:

```text
workflow inventory: 102
canonical workflows: 3
migration-required operational: 99
placeholders: 0
```

## Superseded Batch 22 attempt

PR #354 is closed unmerged. Its Site Bootstrap validation exposed a stale/over-compacted branch copy of `data/session-work-claims.json`, where active StegOS and machine pre-work claims had lost required `expected_evidence` and `next_task_after_release` fields. That was a branch reconstruction defect, not an Ecosystem Node validation defect. PR #355 was rebuilt from fresh current main and preserves the complete active claim fields. PR #354 grants no authority and is not canonical continuation.

## Blocked distinct candidate — HIL session-consolidation workflow

The standalone `.github/workflows/check-hil-session-consolidation.yml` remains present and must not be changed by Batch 22. Prior attempts proved `check_session_retirement.py` correctly fails closed because the ARCHIVABLE `hil-runtime-consolidation-2026-08-02` receipt in `data/session-orchestration-registry.json` names that workflow as a required `material_state_location`.

Correct migration requires the canonical session-orchestration owner, Site #114, to update or explicitly admit migration of that archival material-state pointer. Cleanup must not weaken retirement validation or silently rewrite session-orchestration authority. Durable blocker evidence remains in Site #268.

`check-hil-linkedin-launch-readiness.yml` remains REVIEW_REQUIRED and is outside this batch.

## Collision boundaries

```text
Site #81: live same-origin HIL receiver/readiness/runtime observation
Site #67: HIL lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: cross-repository lifecycle consistency
master-records/orchestration: custody/reconstruction/candidate release authority
Site #114: session orchestration/retirement authority
SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT: separate claimed product paths
SHWP-HEALER-SOVEREIGN-SCHEDULER-001: MACHINE_OWNED
StegFin wallet signing/broadcast: USER_ONLY
```

Batch 22 may not create or duplicate any of those authorities. The surviving gateway-binding workflow still uses hosted checkout/setup mechanics; this consolidation does not declare those mechanics final or production-authoritative. They remain future minimization debt and are retained here only to preserve the existing three-version validation evidence while removing one redundant standalone workflow.

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

Trade execution remains machine/human-authority owned. Credential authority is TV/TVC. Wallet signing/broadcast are USER_ONLY. Workflow cleanup does not imply trade execution or settlement.

## Next executable action

Revalidate exact final PR #355 head after this handoff update. Inspect Site Bootstrap, Site Handoff Orchestrator, Ecosystem Heartbeat, StegFin phone projection, and all three Ecosystem Node gateway-binding jobs. Merge only if every required run succeeds. Then verify current-main census is exactly 102 / canonical 3 / migration-required 99 / placeholders 0, release the Batch-22 claim, record exact merge/post-merge evidence here, and inspect the next unclaimed workflow family under Site #268.

## Completion accounting — released work only

```text
task_completion: 35/131 = 26.72%
developed_files_for_completed_surfaces: 35/35
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 88/88 released validation groups PASS
integration: 21/21 released workflow/token-remediation groups
active_batch_22: implementation installed; preliminary exact-head validation PASS; final post-handoff exact-head validation pending
goal_activation_for_cleanup_goal: 35/131 = 26.72%
session_consolidation: incomplete
```

## Archive condition

This session is not archive-ready while Batch 22 is unreleased and broader Site #268 workflow/token debt remains. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately worker-owned and are not inferred from source or validation state.
