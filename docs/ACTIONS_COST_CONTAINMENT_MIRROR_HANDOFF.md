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
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17-20260817
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source validation only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Released accounting bound to current main

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 31/131 = 23.66%
remaining_audit_start_surfaces: 100/131
current_main_workflow_count: 107
workflow_files_eliminated_or_consolidated_by_released_cleanup: 20
released_completed_batches_or_equivalent_semantic_migrations: 17
released_validation_groups: 72/72 PASS
released_integrations: 17/17
review_required_surfaces: 1
canonical_workflows: 3
migration_required_operational: 104
placeholders: 0
```

Current released main remains bound to PR #337 and merge `b106d3479bafa458d56f4f450f1975925e7887e6`; claim release commit `7eca3a6a8d2b9b5f5853fd028aa4a26a8083a7ab`; current main handoff commit `e791f394d22b3615246dc9ec346dec59505bcc23`.

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
PR #337 — Marketplace Coinbase hosted accessibility importer retired after bounded Site projection was already PAPER_ACCESSIBLE
```

Hosted validation establishes source consistency only. It does not create runtime, provider, financial, wallet, HIL, inference, publication or product activation authority.

## Active Batch 17 — ST-018 GitHub-token custody retirement

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17-20260817
branch: chore/site-st018-token-custody-retirement-b17-20260817
scoped_handoff: docs/ST018_VALIDATION_EVIDENCE_MIRROR_HANDOFF.md
state: CLAIMED_FOR_IMPLEMENTATION
candidate_workflow_delta: 107 -> 106
candidate_released_classification_delta: 31 -> 32 after validated merge only
credential_authority: TV/TVC
```

Batch 17 retires only `.github/workflows/capture-validation-evidence.yml`, whose hosted mechanics included `issues: write`, `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, and `GH_TOKEN=${{ github.token }}` issue mutation. Deterministic ST-018 scripts, schema, manifest, receipt writers/checkers, and historical evidence are preserved.

The unfinished ST-018 native-main observation is transferred to the existing Site repository heartbeat capability `.stegverse/repo-heartbeat.json::activation_receipt_validation`, which declares `github_token_required=false`. No second scheduler/heartbeat/custody path is created. GitHub artifacts and issue comments cease to be required ST-018 custody/completion evidence after Site #141 reconciliation.

Do not count the candidate 106-workflow / 32-remediated state as released until exact branch validation, merge, claim release, Site #141 reconciliation, and current-main census evidence are complete.

## HIL / Healer / runtime collision boundaries

Canonical HIL participant/runtime handoff: `docs/HIL_SITE_MIRROR_HANDOFF.md`.

```text
Site #81: live same-origin receiver/readiness/runtime observation
Site #67: participant lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: cross-repository lifecycle consistency
master-records/orchestration: custody/reconstruction/candidate release authority
LinkedIn launch readiness: REVIEW_REQUIRED
StegOS admitted inference: separate active product paths
Healer scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / MACHINE_OWNED
StegFin wallet signing/broadcast: USER_ONLY
```

Cleanup may not create a second scheduler, runtime, review path, publication path, wallet authority, financial authority, provider authority or product-activation claim. Do not modify `check-hil-linkedin-launch-readiness.yml` while its semantic drift remains `REVIEW_REQUIRED`.

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

Canonical continuation:
- `StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`
- `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-CONTINUITY-CARRIER-007.json`
- StegFin #77 / current phone participant path

Trade execution remains machine/human-authority owned. Credential authority is TV/TVC. Wallet signing/broadcast are USER_ONLY. Workflow cleanup does not imply trade execution or settlement.

## Current claims / collision state

```text
workflow minimization/remediation through B16R1: MERGED_INTO_CANONICAL_WORKSTREAM
Batch 17 ST-018 cleanup: CLAIMED_FOR_IMPLEMENTATION
Site pre-work admission: SITE-PREWORK-CLAIM-GATE-MACHINE-001 / MACHINE_OWNED / admission only
StegOS iPod admitted inference: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT / CLAIMED_FOR_INTEGRATION / separate product paths
HIL LinkedIn semantic drift: REVIEW_REQUIRED
live sovereign runtime/inference: canonical StegVerse workers / observation only
TV/TVC route/credential authority: TV/TVC only
Healer resident scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / MACHINE_OWNED / do not compete
```

## Next executable action

Complete Batch 17 exact branch validation. Merge only on green evidence, then release the claim, reconcile Site #141 and released accounting, and continue the next bounded unclaimed token-bearing/redundant workflow family under Site #268.

## Completion accounting — released work only

```text
task_completion: 31/131 = 23.66%
developed_files_for_completed_surfaces: 31/31
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 72/72 released validation groups PASS
integration: 17/17 released workflow/token-remediation groups
propagation: not applicable to released B16R1 workflow-only cleanup
goal_activation_for_cleanup_goal: 31/131 = 23.66%
session_consolidation: incomplete
```

## Archive condition

The local-model/runtime requirement and StegFin execution requirement are durably transferred to canonical owners. This session remains active while Batch 17 is unvalidated/unmerged or while further unclaimed token-bearing/redundant workflow families remain executable under Site #268. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately worker-owned and are not inferred from source or validation state.
