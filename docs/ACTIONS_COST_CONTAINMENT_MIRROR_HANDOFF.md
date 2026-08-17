# Actions Cost Containment Mirror Handoff

## Canonical goal and authority

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
originating_goal: reduce GitHub-hosted workflow/token dependence to the minimum technically necessary while preserving StegVerse execution, TV/TVC credential authority, deterministic validation, and canonical authority boundaries
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: chore/site-hil-public-response-import-validation-20260817
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
active_implementation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B10-20260817
active_validation_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B10-20260817
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity is StegVerse-owned. GitHub Actions is non-authorizing source/validation infrastructure only. No Render production path is allowed and no TV/TVC protected value is exported into GitHub Actions.

## Current accounting — released main

```text
audit_start_workflow_surfaces: 131
current_active_workflow_surfaces: 118
explicitly_classified_or_remediated: 23/131 = 17.56%
remaining_classification_denominator: 108/131
workflow_files_eliminated_or_consolidated: 13
recurring_schedules_removed_without_deleting_workflow_files: 9
completed_workflow_minimization_batches: 9
released_validation_groups: 37/37 PASS
released_batch_integrations: 9/9
review_required_surfaces: 1
```

The 118 workflow count derives from the verified 119-file post-batch-8 census minus the exact standalone transfer workflow removed by PR #313.

If active batch 10 releases with no concurrent workflow-file change, the expected released state is 117 workflow files, 24/131 explicitly classified/remediated, 107/131 remaining, 14 workflow files eliminated/consolidated, and 10 completed minimization batches. These are expected values only until exact-head validation, merge, claim release, and post-merge census occur.

## Released minimization evidence

```text
PR #270 merge 5fc9929f39c9feae2423b00e9d6830c65fd07ccd — HIL first-release validation consolidation — count 130
PR #271 merge 2d48a626f288e3583b7d69857ce012b82a0180dd — obsolete HIL v0.5 installers removed — count 128
PR #272 merge 093f627f08993048ce8a2b74d16b52bcddc410b1 — completed HIL deployment investigation removed — count 126
PR #273 merge 1d5e1b202f13b881b19f84b05c7860040fbdac4d — completed HIL pilot evidence investigation removed — count 124
PR #305 merge 1f59d1861bed56cf90354df06b753e44fd2fb7ed — HIL import validators folded — count 122
PR #308 merge 00123d8cd46ceaab9492d3d07939d65b2bfc0529 — Master Record release projection folded; LinkedIn retained REVIEW_REQUIRED — count 121
PR #310 merge bbf285af75e6473dfd09bbee6db8f6d1280a298d — Federal-Plus validation folded; hosted schedule retired — count 120
PR #312 merge 104a823254cccf0b2ae15a5524fb762ad05c6ec4 — Master Records return-receipt validation folded — count 119
PR #313 merge 5b7e4bb563d9c335e986e03a06be5e372637456c — Master Records transfer-packet validation folded — count 118
```

## Active batch 10 — HIL public-response import validation

```text
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B10-20260817
branch: chore/site-hil-public-response-import-validation-20260817
classification: CONSOLIDATE_INTO_STABLE_DISPATCHER
standalone workflow: .github/workflows/check-hil-public-response-import.yml
retained validator: scripts/check_hil_public_response_import.py
stable dispatcher: .github/workflows/check-hil-live-readiness.yml
```

Direct inspection before mutation established that the standalone workflow was only a `contents: read` GitHub-hosted checkout/setup-python wrapper around the repository-local deterministic validator. The validator itself requires the canonical HIL v1.1 primary and prompt hashes, exact response/receiver-receipt byte continuity, verified receiver chain state, authenticated private acceptance, authenticated append-only publication, published public state, fail-closed acquisition, and explicit false custody/endorsement/scientific-proof/Master-Record authority fields.

Installed on the active branch:

- `data/hil-responses.json`, `data/hil-public-response-imports/**`, the import schema, and the validator are watched by the credential-clean HIL dispatcher;
- `python3 scripts/check_hil_public_response_import.py` runs before downstream HIL validators;
- `.github/workflows/check-hil-public-response-import.yml` is absent;
- no replacement schedule, secret, token, artifact transport, repository mutation, publication action, private-review action, custody action, provider execution, wallet action, or runtime activation path was introduced.

Batch 10 is not complete until the exact final head passes HIL Validation and Live Readiness, Site Handoff Orchestrator, Ecosystem Heartbeat Orchestration, Check StegFin Phone Projection, and Site Bootstrap Validate; the PR then merges, the claim is released, and the post-merge workflow census confirms the released count.

## HIL authority and collision boundaries

Canonical HIL participant/runtime handoff: `docs/HIL_SITE_MIRROR_HANDOFF.md`.

```text
Site #81: live same-origin receiver/readiness/runtime observation
Site #67: participant lifecycle projection/integration
TVC #8: exact-byte lifecycle + authenticated private review
StegCore #41: cross-repository lifecycle consistency
master-records/orchestration: custody/reconstruction/candidate release authority
LinkedIn launch readiness: REVIEW_REQUIRED
StegOS admitted-inference claim: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT / separate product paths
```

No cleanup may weaken Site #81 activation semantics, Site #67 lifecycle projection authority, TVC #8 review authority, separate publication authority, Master Records authority, the active StegOS product paths, or the LinkedIn `REVIEW_REQUIRED` evidence gap.

## Healer convergence

`StegVerse-Labs/StegVerse-Healer/docs/HEALER_MIRROR_HANDOFF.md` establishes the resident-heartbeat-bound no-GitHub-token scheduler as source/control complete and machine-owned. Necessary recurring operational work may transfer to that canonical StegVerse execution path when the exact capability is admitted; this Site cleanup lane must not create a second scheduler or compete with `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`.

## Local model/runtime convergence

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

Do not duplicate this implementation in Site. Live activation is worker-owned and is not inferred from source validation.

## StegFin convergence

Canonical continuation:
- `StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`
- `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-CONTINUITY-CARRIER-007.json`

Trade execution remains machine/human-authority owned. Credential authority is TV/TVC. Wallet signing/broadcast are USER_ONLY. Workflow cleanup does not imply trade execution or settlement.

## Classification states

- `KEEP_GITHUB_VALIDATION`: bounded repository/CI behavior retained while consolidation is incomplete.
- `KEEP_STANDALONE_EXCEPTION`: standalone only with concrete technical/authority evidence.
- `CONSOLIDATE_INTO_STABLE_DISPATCHER`: useful repository validation moved behind the minimum stable doorway.
- `TRANSFER_TO_STEGVERSE_WORKER`: necessary operational recurrence whose execution belongs to StegVerse runtime.
- `ELIMINATE`: redundant, completed, superseded, or unnecessary.
- `REVIEW_REQUIRED`: semantic drift or ownership uncertainty blocks safe consolidation.

## Current claims / collision state

```text
workflow minimization batches 1-9: MERGED_INTO_CANONICAL_WORKSTREAM
workflow minimization batch 10: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B10-20260817 / CLAIMED_FOR_INTEGRATION
Site pre-work admission: SITE-PREWORK-CLAIM-GATE-MACHINE-001 / MACHINE_OWNED / admission only
StegOS iPod admitted inference: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817-CURRENT / CLAIMED_FOR_INTEGRATION / separate product paths
HIL LinkedIn semantic drift: REVIEW_REQUIRED
repository hygiene: StegVerse-Labs/.github#165
live sovereign runtime/inference: canonical StegVerse workers / observation only
TV/TVC route/credential authority: TV/TVC only
Healer resident scheduler: SHWP-HEALER-SOVEREIGN-SCHEDULER-001 / MACHINE_OWNED / do not compete
```

## Propagation obligations

Workflow-only cleanup does not create a product release requiring Publisher, admissibility-wiki, or stegguardian-wiki propagation. Product activation propagation remains fail-closed until canonical activation/release evidence exists.

## Next executable action

Open the bounded batch-10 PR and validate its exact final head. Merge only after all required validation groups pass, then release claim B10, update this handoff on `main`, verify the standalone workflow remains absent, and directly census `.github/workflows`.

## Completion accounting — released work only

```text
task_completion: 23/131 = 17.56%
developed_files_for_completed_batches: 23/23 required mutations/records/classifications present
scaffolding_or_stubs: 0
missing_required_files_for_completed_batches: 0
validation: 37/37 required released-batch validation groups PASS
integration: 9/9 workflow-minimization batches merged
propagation: not applicable for workflow-only cleanup
goal_activation: 23/131 = 17.56%
session_consolidation: incomplete while additional unique Site workflow minimization/hygiene work remains
```

## Archive condition

The local-model/runtime requirement and StegFin execution requirement are durably transferred to their canonical owners; Site batches 1-9 are released. Batch 10 is active and unique to this session. This support session remains not archive-ready while batch 10 is unreleased and additional Site workflow minimization/hygiene work remains executable or untransferred.
