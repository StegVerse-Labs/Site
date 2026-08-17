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
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17R1-20260817
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

Released cleanup is canonical through PR #337 / Batch 16R1. Detailed prior evidence remains in Git history and the claim registry.

## Active Batch 17R1 — ST-018 GitHub-token custody retirement

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17R1-20260817
branch: chore/site-st018-token-custody-retirement-b17r1-20260817
scoped_handoff: docs/ST018_VALIDATION_EVIDENCE_MIRROR_HANDOFF.md
state: CLAIMED_FOR_IMPLEMENTATION
candidate_workflow_delta: 107 -> 106
candidate_remediated_delta: 31 -> 32 after validated merge only
```

B17R1 retires `.github/workflows/capture-validation-evidence.yml`, which used `issues: write`, checkout/setup actions, upload-artifact, and `GH_TOKEN=${{ github.token }}` issue mutation. Deterministic ST-018 manifest/schema/receipt scripts and historical evidence remain retained. Unfinished native-main observation moves to the existing Site repository heartbeat `activation_receipt_validation` capability with `github_token_required=false`; no replacement GitHub scheduler, token, artifact custody, or issue-comment custody path is created.

PR #343 / original B17 branch is superseded because `main` advanced the canonical claim registry during implementation. B17R1 is reconstructed from current main and requires fresh validation.

Do not count 106 workflows / 32 remediated surfaces as released until merge, claim release, Site #141 reconciliation, and current-main evidence are complete.

## Collision boundaries

- Site #81 HIL runtime/readiness, Site #67 HIL lifecycle, TVC #8 private review, StegCore #41 lifecycle, and Master Records custody/release remain separate owners.
- Active StegOS admitted-inference product paths remain claimed separately.
- Healer scheduler remains `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` MACHINE_OWNED.
- Local model/runtime remains canonical in `StegVerse-002/micro-node-runtime` / org heartbeat; do not recreate it in Site or Actions.
- StegFin continuation remains `StegVerse-Labs/stegfin-governance`; wallet signing/broadcast is USER_ONLY.
- Do not modify `check-hil-linkedin-launch-readiness.yml` while its semantic drift is `REVIEW_REQUIRED`.

## Next executable action

Validate exact B17R1 head. Merge only on green source/claim/orchestration evidence; then release the claim, reconcile Site #141, update released accounting, and continue the next unclaimed Site #268 token-bearing/redundant workflow family.

## Completion accounting — released work only

```text
task_completion: 31/131 = 23.66%
developed_files_for_completed_surfaces: 31/31
scaffolding_or_stubs: 0
missing_required_files_for_completed_surfaces: 0
validation: 72/72 released validation groups PASS
integration: 17/17 released workflow/token-remediation groups
goal_activation_for_cleanup_goal: 31/131 = 23.66%
session_consolidation: incomplete
```

## Archive condition

The local-model/runtime and StegFin execution requirements are durably transferred to canonical owners. This session remains active while B17R1 is unvalidated/unmerged or while further unclaimed token-bearing/redundant workflow families remain executable under Site #268. Live HIL, sovereign runtime/inference, ordinary Healer execution, and StegFin settlement remain separately worker-owned and are not inferred from source or validation state.
