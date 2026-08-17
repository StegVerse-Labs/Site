# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and every canonical product/runtime authority boundary
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
active_implementation_claim: NONE
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity remains StegVerse-owned. GitHub Actions is non-authorizing source/validation infrastructure only. No Render production path is allowed. No TV/TVC protected value should be injected into GitHub Actions to replace GitHub credentials.

## Current accounting

```text
audit_start_workflow_surfaces: 131
current_active_workflow_surfaces: 120
explicitly_classified_or_remediated_surfaces: 21/131 = 16.03%
remaining_classification_denominator: 110/131
workflow_files_eliminated_or_consolidated: 11
recurring_schedules_removed_without deleting workflow files: 9
completed_workflow_minimization_batches: 7
required_validation_groups_for_released_batches: 27/27 PASS
completed_batch_integrations: 7/7
review_required_surfaces: 1
```

The current 120-workflow count is the verified prior 121-file canonical census after PR #308 minus the one exact standalone workflow removed by PR #310. `check-hil-federal-plus-security-baseline.yml` is directly observed absent on `main`; `check-hil-live-readiness.yml` remains present.

## Released containment / minimization history

```text
Containment PR #266 merge 41db95c9df05e4a91b44d466ca1ed1231d46cfef
  removed recurring schedules from 4 operational workflows

Containment PR #267 merge 44f593f7b7075958d6b363ddf8caac1ee3541132
  removed recurring schedules from 5 additional operational workflows

Batch 1 PR #270 merge 5fc9929f39c9feae2423b00e9d6830c65fd07ccd
  HIL first-release validation folded into credential-clean HIL dispatcher
  post-merge workflow count 130

Batch 2 PR #271 merge 2d48a626f288e3583b7d69857ce012b82a0180dd
  obsolete HIL v0.5 installer workflows removed
  post-merge workflow count 128

Batch 3 PR #272 merge 093f627f08993048ce8a2b74d16b52bcddc410b1
  completed HIL deployment-investigation workflows removed
  post-merge workflow count 126

Batch 4 PR #273 merge 1d5e1b202f13b881b19f84b05c7860040fbdac4d
  completed HIL pilot-evidence investigation workflows removed
  post-merge workflow count 124

Batch 5 PR #305 merge 1f59d1861bed56cf90354df06b753e44fd2fb7ed
  full-cycle artifact import + HTTPS receiver-probe import validators folded into HIL dispatcher
  exact-head runs: HIL 32003984673; orchestrator 32003984788; heartbeat 32003984727; StegFin phone 32003984698; bootstrap 32003984664 — SUCCESS
  post-merge workflow count 122

Batch 6 PR #308 merge 00123d8cd46ceaab9492d3d07939d65b2bfc0529
  Site-side HIL Master Record release-chain projection validation folded into HIL dispatcher
  LinkedIn launch-readiness workflow retained as REVIEW_REQUIRED after deterministic drift was exposed
  exact-head runs: HIL 32008475367; orchestrator 32008475454; heartbeat 32008475401; StegFin phone 32008475518; bootstrap 32008475512 — SUCCESS
  post-merge workflow count 121

Batch 7 PR #310 merge bbf285af75e6473dfd09bbee6db8f6d1280a298d
  scheduled HIL Federal-Plus workflow removed
  Federal-Plus deterministic validator folded into credential-clean HIL dispatcher
  HIL-SEC-009 recurrence rebound to Site #81 StegVerse-controlled observation; HIL-SEC-012 rebound to stable dispatcher + StegVerse live observation
  exact-head runs: HIL 32009536203; orchestrator 32009536171; heartbeat 32009536167; StegFin phone 32009536202; bootstrap 32009536119 — SUCCESS
  Federal-Plus validator step: SUCCESS
  post-merge workflow count 120
```

## HIL authority / collision boundaries

Canonical participant/runtime handoff: `docs/HIL_SITE_MIRROR_HANDOFF.md`.

```text
Site #81: live same-origin HIL receiver/readiness/runtime observation
Site #67: participant lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: cross-repository lifecycle consistency
master-records/orchestration: independent candidate validation/release
LinkedIn launch readiness: REVIEW_REQUIRED
```

The LinkedIn validator previously failed because `humans-as-interoperability-layer.html` lacks current prompt SHA `cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c`. The standalone LinkedIn workflow is retained until its canonical semantic/public-page reconciliation is corrected with independent evidence. Cleanup may not weaken that validator merely to reduce workflow count.

## Federal-Plus security consolidation — released

Canonical validator: `scripts/check_hil_federal_plus_security_baseline.py`.

Released disposition:

```text
.github/workflows/check-hil-federal-plus-security-baseline.yml -> CONSOLIDATE_INTO_STABLE_DISPATCHER / REMOVED
scripts/check_hil_federal_plus_security_baseline.py -> RETAINED
.github/workflows/check-hil-live-readiness.yml -> RETAINED CREDENTIAL-CLEAN DISPATCHER
HIL-SEC-009 live recurrence -> TRANSFER_TO_STEGVERSE_WORKER / Site #81 observation path
HIL-SEC-012 source regression gate -> CONSOLIDATE_INTO_STABLE_DISPATCHER
replacement GitHub schedule -> NONE
replacement GitHub token path -> NONE
artifact-upload requirement -> NONE
```

The first branch run failed closed because HIL-SEC-009 and HIL-SEC-012 still referenced the deleted workflow. The profile was corrected to preserve the capability under the StegVerse-owned observation path and stable source dispatcher; a fresh exact-head run then passed. This is a semantic ownership correction, not a weakened security check.

## Local model/runtime convergence

Do not reopen or duplicate the released model/runtime implementation.

```text
formal_local_model: COMPLETE_RELEASED
local_runtime_discovery_launch_inference_proof: COMPLETE_RELEASED
descriptive_select_local_model_runtime_step: SUPERSEDED
local_model_credential_requirement: NONE
credential_authority: TV/TVC
github_token_production_authority: NONE
```

Canonical continuation:
- `StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md`
- `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`

Live same-carrier activation remains worker-owned and is not inferred from Site source validation.

## StegFin convergence

Trade-readiness execution is not owned by this cleanup lane.

Canonical continuation:
- `StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`
- `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-CONTINUITY-CARRIER-007.json`
- `StegVerse-Labs/.github/handoffs/STEGFIN-CONTINUITY-CARRIER-007.json`

Credential authority remains TV/TVC. Wallet signing and broadcast remain USER_ONLY. `WALLET_HANDOFF_READY` is not inferred from workflow cleanup.

## Current active claims / convergence

```text
Site workflow-minimization batch 7: MERGED_INTO_CANONICAL_WORKSTREAM
Site workflow-minimization session claim: NONE
Site pre-work admission: SITE-PREWORK-CLAIM-GATE-MACHINE-001 / MACHINE_OWNED / admission only
StegOS iPod admitted-inference projection: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT / CLAIMED_FOR_INTEGRATION / separate paths
HIL LinkedIn semantic drift: REVIEW_REQUIRED / separate canonical reconciliation
repository hygiene: StegVerse-Labs/.github#165
live sovereign runtime/inference: canonical StegVerse workers / observation only here
TV/TVC credential and route authority: TV/TVC only
```

The StegOS active claim is preserved in `data/session-work-claims.json`; batch 7 was explicitly rebased/merged with current `main` instead of overwriting that concurrent work.

## Validation commands / evidence path

For each next batch, the release gate remains:

```text
read current handoff + claim registry
install exact branch-bound claim before mutation
retain or transfer necessary capability before deleting a workflow
run exact-head HIL or relevant focused dispatcher
run Site Handoff Orchestrator
run Ecosystem Heartbeat Orchestration
run Check StegFin Phone Projection when triggered
run Site Bootstrap Validate
inspect job steps/logs for substantive failures
merge only the validated exact head
verify removed paths and retained replacement paths on main
release the claim
update this handoff
```

Hosted validation proves source/policy only. It does not prove runtime activation, publication, custody, wallet execution, settlement, or trade execution.

## Integration / propagation obligations

Workflow-only cleanup does not itself create a release-bearing Site product change requiring Publisher/admissibility-wiki/stegguardian-wiki propagation. Product activation propagation remains fail-closed until canonical activation/release evidence exists. Master Records authority is independent and is not granted by a Site validator.

## Exact next executable action

Under Site #268, inspect the next small unclaimed workflow family. Create exactly one fresh branch-bound claim before mutation. Prefer completed one-off investigation/import surfaces or compatible read-only validators. For any necessary recurring operational behavior, transfer recurrence to a named StegVerse-controlled worker before deleting its GitHub doorway. Do not touch paths held by the active StegOS claim.

## Completion / archive condition

```text
task_completion: 21/131 = 16.03%
developed_file/classification_completion: 21/131 = 16.03%
validation: 27/27 released-batch groups PASS
integration: 7/7 released minimization batches merged
propagation: N/A for cleanup-only changes
workflow_goal_activation: 21/131 = 16.03%
session_consolidation: incomplete
remaining_audit_start_surfaces: 110
```

The local-model/runtime and StegFin requirements are durably transferred. This support session is not archive-ready while 110/131 audit-start Site workflow surfaces remain undisposed and repository hygiene remains executable or untransferred. A fresh exact claim is required before additional Site mutation.
