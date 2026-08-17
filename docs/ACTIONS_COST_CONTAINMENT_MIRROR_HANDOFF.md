# Actions Cost Containment Mirror Handoff

## Canonical state

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: claim/site-two-entry-observer-token-retirement-b25-20260817
canonical_issue: Site#268
credential_authority: TV/TVC
non_tv_tvc_project_or_provider_secret_allowed: false
github_actions_production_carrier_required: false
preferred_workflow_surface: <=2 stable entry surfaces with evidence-backed exceptions
canonical_claim_registry: data/session-work-claims.json
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B25-20260817
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity remains StegVerse-owned. GitHub-hosted execution is non-authorizing validation only. No Render path or TV/TVC credential export is permitted.

## Released accounting

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 41/131 = 31.30%
remaining_audit_start_surfaces: 90/131
current_main_workflow_count: 100
workflow_files_eliminated_or_consolidated: 27
released_integrations_or_semantic_remediations: 27/27
canonical_workflows: 3
migration_required_operational: 97
placeholders: 0
review_required_surfaces: 1
```

Batch 25 is active and is not counted as released until exact-head validation and merge. Because it hardens a retained scheduled observer rather than deleting it, the expected physical workflow census remains `100 / canonical 3 / migration-required 97 / placeholders 0`.

## Active remediation — Batch 25 two-entry observer credential/writeback/custody retirement

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B25-20260817
task: SITE-ACTIONS-COST-CONTAINMENT-B25-20260817
branch: claim/site-two-entry-observer-token-retirement-b25-20260817
state: CLAIMED_FOR_IMPLEMENTATION
workflow: .github/workflows/two-entry-points-execution-state.yml
validator: scripts/validate_two_entry_points_execution_state.py
schedule: 11 */6 * * *
product_owner_change: NONE
```

Installed bounded delta:

- preserves the six-hour schedule and fail-closed validator;
- preserves the canonical `data/two-entry-points-execution-state.json` ownership/blocker state unchanged;
- uses `permissions: {}`;
- refuses GitHub/OIDC/provider/Master-Records/HIL credential-bearing environment;
- fetches the exact public Site commit anonymously via codeload;
- uses preinstalled Python rather than `actions/setup-python`;
- validates the execution-state receipt result, stale-claim set, authority flags, and canonical SHA-256;
- emits inspectable evidence to workflow logs and `$GITHUB_STEP_SUMMARY`;
- removes `actions/checkout`, `actions/setup-python`, and `actions/upload-artifact`;
- removes persisted GitHub checkout credentials;
- removes repository receipt commit/push writeback;
- removes GitHub artifact custody;
- grants no Ecosystem Chat, VACC, runtime/provider, Site activation, downstream ingestion, publication, custody, TVC protected execution, StegOS, HIL, or StegFin wallet authority.

The preceding Site #152 stale-claim reconciliation is COMPLETE_RELEASED through PR #373 / merge `792eff2396758761f94c2c062c5662f6e5132e4b`; ECP-001, ECP-002, and VACP-001 remain BLOCKED under their current canonical owners and CONS-001 is terminal `MERGED_INTO_CANONICAL_WORKSTREAM`.

Required exact-head evidence before merge:

1. `TWO_ENTRY_OBSERVER_CREDENTIAL_REFUSAL=PASS` and `TWO_ENTRY_OBSERVER_GITHUB_TOKEN_AUTHORITY=NONE`.
2. `TWO_ENTRY_OBSERVER_SOURCE_FETCH=PASS` and preinstalled Python PASS.
3. `TWO ENTRY POINTS EXECUTION STATE: PASS`, `Stale claims: none`, `Errors: none`.
4. `TWO_ENTRY_OBSERVER_RECEIPT_HASH=PASS`, `TWO_ENTRY_OBSERVER_AUTHORITY_GRANTED=FALSE`, `TWO_ENTRY_OBSERVER_RELEASE_AUTHORIZED=FALSE`.
5. `TWO_ENTRY_OBSERVER_VALIDATION_ONLY=PASS`, repository writeback NONE, artifact custody NONE, runtime-control-plane authority NONE.
6. Site Handoff Orchestrator PASS.
7. Ecosystem Heartbeat Orchestration PASS.
8. Site Bootstrap Validate PASS including claim/orchestration/application/ST-017 checks.
9. Check StegFin Phone Projection PASS with USER_ONLY wallet/signing and hosted runtime authority NONE.
10. Workflow inventory remains `100 / 3 / 97 / 0` unless an independently released concurrent remediation changes current main first.
11. Branch must be zero commits behind current `main` immediately before merge.

## Latest released workflow remediation — Batch 24

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B24-20260817
state: MERGED_INTO_CANONICAL_WORKSTREAM / RELEASED_INTEGRATION
PR: #372
final_head: c17725d6e78919b582167cdafa2dd4bb060bc4bf
merge: db7da79ee1916a0249c3d1893cedac4861326961
claim_release_commit: c831d263167842bcce6d0dda685d2a54fda07822
Site Bootstrap Validate: 32056528914 SUCCESS
Site Handoff Orchestrator: 32056529186 SUCCESS
Ecosystem Heartbeat Orchestration: 32056528958 SUCCESS
Check StegFin Phone Projection: 32056528989 SUCCESS
SV_CONTINUITY_109_SITE_VALIDATION: PASS
SV_CONTINUITY_109_PREMATURE_PASS_REJECTION: PASS
workflow inventory: 100 / 3 / 97 / 0
authority_effect: NONE
```

Batch 24 removed `.github/workflows/validate-sv-continuity-109-site.yml` and moved its unchanged fail-closed receipt validation into credential-clean `.github/workflows/validate.yml` without changing the canonical BLOCK receipt.

## Other recent released semantic remediations

- TVC receipt-import credential cleanup: PR #371, merge `8d85061bbc20d08449381b63f9c74c00b709830d`; retained workflow credential-clean, TVC protected runtime/execution authority unchanged.
- GP10 GitHub-token/writeback/artifact-custody retirement: PR #367, merge `96423f16cf6d3f440630d322cc5d5c196e4fa672`; historical GP10 receipts retained, runtime/evidence authority remains `StegVerse-Labs/GP10`.
- Batch 23 Master Records importer consolidation: PR #362, merge `e936f1481bf9b13468e83c80b7289f657640c81c`; standalone importer workflow retired into credential-clean `validate.yml`.

## Protected and blocked surfaces

- `check-hil-session-consolidation.yml`: BLOCKED on Site #114 archival material-state migration.
- `check-hil-linkedin-launch-readiness.yml`: REVIEW_REQUIRED.
- Protected owners include Site #81, Site #67, TVC #8, StegCore #41, master-records/orchestration, Site #114, `SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT`, `SITE-PREWORK-CLAIM-GATE-MACHINE-001`, `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`, and USER_ONLY StegFin signing/broadcast.
- `validate-review-authority-projection.yml` retains a real 3.9/3.11/3.12 compatibility matrix and must not be collapsed into a single-version carrier without equal coverage.
- VACC Goal-3 and Conectrr machine-owned workflow families retain their current canonical owner contracts and are not generic cleanup surfaces.

## Transferred session goals

```text
formal_local_model: COMPLETE_RELEASED
local_runtime_discovery_launch_inference_proof: COMPLETE_RELEASED
descriptive_select_local_model_runtime_step: SUPERSEDED
local_model_credential_requirement: NONE
local runtime continuation: StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md + StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md
StegFin continuation: StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md + task-state/STEGFIN-CONTINUITY-CARRIER-007.json + StegFin #77
HIL continuation: Site #81/#67 + TVC #8 + StegCore #41 + master-records/orchestration
GP10 runtime/evidence continuation: StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md
TVC protected execution continuation: StegVerse-Labs/TVC
Two-entry product continuation: docs/TWO_ENTRY_POINTS_MIRROR_HANDOFF.md + current Ecosystem Chat/VACC product owners
```

USER_ONLY remains sole StegFin signing/broadcast authority. Source validation, CI success, or merge does not imply a live trade or settlement.

## Automation and continuation

Credential-clean `.github/workflows/validate.yml` is the canonical machine path for aggregate deterministic repository validation. The two-entry observer remains scheduled because stale-claim/product-owner drift is a recurring condition, but Batch 25 constrains that hosted observer to non-authorizing credential-clean validation. `data/session-work-claims.json` and the MACHINE_OWNED pre-work gate continue to prevent duplicate mutation.

## Next executable action

Open Batch 25 from the exact claim branch and inspect the exact-head Two Entry Points observer, Site Handoff Orchestrator, Ecosystem Heartbeat, Site Bootstrap, and StegFin runs. Merge only when every required check is green and the branch remains current with main. After merge, release the claim and reconcile both handoffs; then inspect the next bounded unclaimed Site #268 workflow/token surface.

## Completion and archive state

```text
task_completion: 41/131 = 31.30% released; Batch 25 active and not counted
released_developed_files: 41/41
prepared_developed_files: 42/42
scaffolding_or_stubs: 0
missing_required_files_for_prepared_surfaces: 0
validation: 115/115 released validation groups PASS; Batch 25 exact path pending
integration: 27/27 released; Batch 25 integration pending
session_consolidation: 3/5 durable goal groups complete or transferred
goal_activation: 41/131 = 31.30% released
```

This session is not archive-ready: 90/131 audit-start surfaces remain unreleased/unclassified before Batch 25, 97 operational workflows remain migration-required, and distinct workflow/token minimization work remains executable under Site #268. Live HIL, sovereign runtime/inference, Healer execution, GP10 runtime/commercial activation, TVC protected execution, Ecosystem Chat/VACC product activation, and StegFin settlement remain separately owned and are not inferred from source or CI state.
