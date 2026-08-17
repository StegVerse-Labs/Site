# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
originating_goal: Preserve ST-018 deterministic validation evidence while removing NON-TV/TVC GitHub-token use, issue mutation, and GitHub-hosted custody/writeback semantics.
repository: StegVerse-Labs/Site
branch: main
canonical_issue: StegVerse-Labs/Site#141
parent_workflow_minimization_issue: StegVerse-Labs/Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_production_runtime_control_plane_authority: NONE
runtime_authority_effect: NONE
publication_authority_effect: NONE
release_authority_effect: NONE
```

This file is the scoped continuation source for the ST-018 hosted validation-evidence surface. Live repository state and exact validation evidence supersede chat history.

## Existing contract

ST-018 declares deterministic validation through:

```text
validation_manifests/repository-core.json
schemas/validation-execution-receipt.schema.json
scripts/capture_validation_manifest.py
scripts/write_site_current_main_validation_receipt.py
scripts/check_site_current_main_validation_receipt_writer.py
scripts/check_site_current_main_validation_evidence.py
data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json
```

The existing `.github/workflows/capture-validation-evidence.yml` is noncompliant with the current credential policy because it grants `issues: write`, uses `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, and exports `GH_TOKEN=${{ github.token }}` to publish a GitHub issue comment. Those mechanics may provide evidence transport but cannot remain a required evidence/custody or authority path under the TV/TVC-only credential rule.

## Active claim

No implementation claim is granted by this handoff itself. A branch-bound implementation claim must be installed in `data/session-work-claims.json` before source mutation.

Collision boundaries:
- do not weaken the declared validators or receipt schema;
- do not claim ST-018 validation proves factual truth, admissibility, publication, deployment, release, standing, certification, or runtime activation;
- do not export TV/TVC credentials into GitHub Actions;
- do not introduce any alternate GitHub/project/provider token;
- do not modify the active StegOS admitted-inference paths;
- do not duplicate Site pre-work admission or sovereign worker authority.

## Intended transition

```text
GitHub-hosted token/write-capable evidence publication
-> credential-clean deterministic validation execution only
-> local repository receipt generation/checking
-> durable repository state where source changes are appropriate
-> StegVerse/Master Records custody only when a canonical custody contract requires it
```

GitHub-hosted validation may remain only to the minimum technically necessary and with `permissions: {}` plus explicit credential-environment refusal. GitHub artifacts and issue comments are not custody authority.

## Exact next tasks

1. Create a bounded implementation branch from current main.
2. Install a branch-bound claim in `data/session-work-claims.json` with this handoff revision.
3. Replace or retire the token/write-capable ST-018 workflow while preserving deterministic validator execution.
4. Remove `issues: write`, `GH_TOKEN`, issue mutation, and upload-artifact dependency from the ST-018 validation path.
5. Prefer the existing anonymous exact-ref / preinstalled-Python validation pattern already established in Site Bootstrap where hosted validation remains necessary.
6. Validate exact branch state through Site claim/orchestration/bootstrap checks.
7. Merge only after exact evidence is green; release the claim and update the parent cost-containment handoff.
8. Reconcile Site #141 so its completion/evidence contract no longer requires a GitHub-hosted artifact or issue-comment custody path.

## Archive condition

This scoped task becomes archive-safe only after source integration, exact validation evidence, released claim state, and durable update of Site #141 and `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`. Product/runtime activation remains independent.
