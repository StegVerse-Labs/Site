# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: chore/site-ecosystem-node-canonical-events-b22-20260817
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

## Released accounting before active Batch 22

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

The released baseline is PR #353 exact merge-checkout validation: 103 workflows / canonical 3 / migration-required operational 100 / placeholders 0. Batch 22 is not counted as released until exact-head validation, merge, post-merge census, and claim/handoff release are complete.

## Recent released minimization evidence

```text
PR #345 — bounded user-LLM capability validator folded into canonical credential-clean Site application validation
PR #349 — bounded user-LLM execution-import-status validator folded into canonical credential-clean Site application validation
PR #351 — bounded user-LLM execution-receipt validator folded into canonical credential-clean Site application validation
PR #353 — Ecosystem Chat provider-neutral binding validator folded into canonical credential-clean Site application validation
```

Older released batches remain immutable in Git history and the claim-registry history anchor.

## Active Batch 22 — Ecosystem Node canonical-event validation consolidation

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B22-20260817
task: SITE-ACTIONS-COST-CONTAINMENT-B22-20260817
branch: chore/site-ecosystem-node-canonical-events-b22-20260817
state: CLAIMED_FOR_IMPLEMENTATION / EXACT_HEAD_VALIDATION_PENDING
```

The standalone workflow being retired is:

```text
.github/workflows/validate-ecosystem-node-canonical-events.yml
```

It independently ran a Python 3.9/3.11/3.12 matrix, installed pytest, validated the canonical event fixture, and ran `tests/test_ecosystem_node_canonical_events.py`.

The existing `.github/workflows/check-ecosystem-node-gateway-binding.yml` already carries the same Python 3.9/3.11/3.12 compatibility matrix and already revalidates `scripts/validate_ecosystem_node_canonical_events.py`. Batch 22 therefore preserves the standalone workflow's full deterministic coverage inside that existing bounded validation surface rather than weakening compatibility coverage.

Installed delta:

- `validate-ecosystem-node-canonical-events.yml` removed;
- `check-ecosystem-node-gateway-binding.yml` retains Python 3.9/3.11/3.12;
- trigger paths now include the canonical-event schema, fixture, adversarial tests, and integrity documentation;
- pytest installation is retained once in the surviving workflow;
- gateway binding validation remains;
- canonical event fixture validation remains;
- adversarial canonical event tests are now executed by the surviving workflow;
- no schedule, write permission, repository writeback, artifact upload, runtime authority, provider authority, wallet authority, publication authority, custody authority, Master Record authority, or product activation is added.

This batch does not claim that GitHub-hosted checkout/setup is an acceptable final stable surface. It removes one redundant workflow while preserving the existing evidence-backed three-version compatibility check. Later workflow minimization may migrate or further consolidate that remaining validation path only with equivalent evidence.

Required exact-head release gates:

```text
SESSION_WORK_CLAIMS_PASS
Check Ecosystem Node Gateway Binding: PASS for Python 3.9, 3.11, 3.12
browser gateway binding validator: PASS
canonical event fixture validator: PASS
canonical event adversarial tests: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS including ST-017 sandbox and canonical application
Check StegFin Phone Projection: PASS if triggered
merge-checkout workflow inventory: 102 / canonical 3 / migration-required operational 99 / placeholders 0
standalone canonical-event workflow absent
```

Hosted validation is source/test evidence only. It does not activate an Ecosystem Node runtime, provider execution, local model, HIL, Master Records, StegFin, wallet, publication, custody, or downstream authority.

## Blocked / protected collision boundaries

The standalone HIL session-consolidation candidate remains blocked on Site #114 archival material-state migration. `check-hil-linkedin-launch-readiness.yml` remains REVIEW_REQUIRED. Neither may be modified by Batch 22.

```text
Site #81: live same-origin HIL receiver/readiness/runtime observation
Site #67: HIL lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: lifecycle consistency
master-records/orchestration: custody/reconstruction/candidate release
Site #114: session orchestration/retirement authority
SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT: separate claimed product paths
SHWP-HEALER-SOVEREIGN-SCHEDULER-001: MACHINE_OWNED
StegFin wallet signing/broadcast: USER_ONLY
```

## Local model/runtime and StegFin convergence

```text
formal_local_model: COMPLETE_RELEASED
local_runtime_discovery_launch_inference_proof: COMPLETE_RELEASED
descriptive_select_local_model_runtime_step: SUPERSEDED
local_model_credential_requirement: NONE
credential_authority: TV/TVC
github_token_production_authority: NONE
```

Canonical runtime continuation remains `StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md` and `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`. StegFin continuation remains `StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`, `task-state/STEGFIN-CONTINUITY-CARRIER-007.json`, and StegFin #77/current phone path. USER_ONLY remains sole signing/broadcast authority.

## Next executable action

Open the exact Batch-22 PR and inspect all exact-head validation runs, jobs, and relevant logs. Correct only deterministic credential-clean validation defects. Merge only after the surviving Ecosystem Node workflow proves all three Python lanes plus fixture/adversarial coverage and the merge-checkout census is 102 / canonical 3 / migration-required operational 99 / placeholders 0. Then release the claim, update this handoff to 36/131 released, and continue the next unclaimed Site #268 workflow family.

## Completion accounting — released work only

```text
task_completion: 35/131 = 26.72%
developed_files_for_completed_surfaces: 35/35
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 88/88 released validation groups PASS
integration: 21/21 released workflow/token-remediation groups
active_batch_22: implementation installed; exact-head validation pending
goal_activation_for_cleanup_goal: 35/131 = 26.72%
session_consolidation: incomplete
```

## Archive condition

This session is not archive-ready while Batch 22 is unreleased and broader Site #268 workflow/token debt remains. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately worker-owned and are not inferred from source or validation state.
