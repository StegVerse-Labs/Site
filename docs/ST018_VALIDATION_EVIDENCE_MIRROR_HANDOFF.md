# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
parent_goal: SITE-ACTIONS-COST-CONTAINMENT-001
batch_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17-20260817
repository: StegVerse-Labs/Site
branch: chore/site-st018-token-custody-retirement-b17-20260817
canonical_issue: StegVerse-Labs/Site#141
parent_workflow_minimization_issue: StegVerse-Labs/Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_production_runtime_control_plane_authority: NONE
runtime_authority_effect: NONE
publication_authority_effect: NONE
release_authority_effect: NONE
state: CLAIMED_FOR_IMPLEMENTATION
```

This is the scoped continuation source for the ST-018 validation-evidence surface. Live repository state, branch claim state, exact validation evidence, and the parent Actions Cost Containment handoff supersede chat history.

## Existing deterministic contract retained

```text
validation_manifests/repository-core.json
schemas/validation-execution-receipt.schema.json
scripts/capture_validation_manifest.py
scripts/write_site_current_main_validation_receipt.py
scripts/check_site_current_main_validation_receipt_writer.py
scripts/check_site_current_main_validation_evidence.py
data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json
```

No validator, receipt schema, or deterministic evidence script is removed by Batch 17.

## Batch 17 migration

The previous `.github/workflows/capture-validation-evidence.yml` granted `issues: write`, used `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, and exported `GH_TOKEN=${{ github.token }}` for issue-comment publication. Those mechanics are evidence transport/custody mechanics, not ST-018 semantics, and conflict with the current TV/TVC-only credential requirement.

Batch 17 therefore:

1. retires `.github/workflows/capture-validation-evidence.yml`;
2. preserves all deterministic ST-018 validators, schema, manifest, receipt writers, and existing historical evidence;
3. moves unfinished native-main completion observation to the existing Site repository heartbeat capability `.stegverse/repo-heartbeat.json::activation_receipt_validation`;
4. requires `github_token_required=false` and prohibits GITHUB_TOKEN/GH_TOKEN/STEGVERSE_GITHUB_TOKEN/PAT/provider fallback;
5. removes GitHub artifact and issue-comment publication as required custody/completion conditions;
6. does not create a second scheduler, heartbeat, custody authority, runtime, publication path, or product activation lane.

## Current machine-owned continuation

Canonical task: `data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json`.

```text
owner: Site repository heartbeat activation_receipt_validation capability / StegVerse control plane
state: BLOCKED_DEPENDENCY_MACHINE_OWNED
github_token_required: false
next action: observe exact current-main deterministic ST-018 evidence through the existing StegVerse-owned lane
```

The machine lane must emit deterministic COMPLETE/BLOCKED/RETRY/REVIEW_REQUIRED/FAILED state. Missing source/evidence remains blocked rather than being treated as success.

## Claim / collision boundaries

Active implementation claim: `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17-20260817` in `data/session-work-claims.json`.

Do not:
- weaken ST-018 validators or receipt schema;
- claim validation proves factual truth, admissibility, publication, deployment, release, standing, certification, runtime activation, HIL activation, StegFin execution, or wallet authority;
- export TV/TVC credentials into GitHub Actions;
- introduce alternate GitHub/project/provider tokens;
- modify the active StegOS admitted-inference paths;
- modify HIL product-owned paths;
- duplicate Site pre-work admission, heartbeat, scheduler, Master Records custody, or sovereign worker authority.

## Validation / release gates

Before merge:

1. `scripts/check_session_work_claims.py` passes with the B17 claim.
2. Site handoff/orchestration validation passes.
3. Site Bootstrap Validate passes.
4. Ecosystem Heartbeat Orchestration passes.
5. retained ST-018 deterministic scripts/schema remain present and syntactically valid.
6. no B17 diff introduces NON-TV/TVC credential use.

After exact validated merge:

1. release B17 claim to `MERGED_INTO_CANONICAL_WORKSTREAM`;
2. update `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md` released accounting;
3. reconcile Site #141 so workflow artifact ID/digest and issue-comment custody are no longer required completion evidence;
4. leave native-main ST-018 completion machine-owned until its own deterministic evidence is observed;
5. continue the next unclaimed Site #268 token-bearing/redundant workflow family.

## Archive condition

This scoped cleanup becomes archive-safe after exact validation, merge, claim release, parent handoff update, and Site #141 contract reconciliation. ST-018 adoption itself may remain machine-owned and blocked without keeping this chat active once its complete execution state and release conditions are durably represented.
