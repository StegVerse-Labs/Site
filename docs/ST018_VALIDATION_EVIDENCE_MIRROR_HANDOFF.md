# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
originating_goal: Preserve ST-018 deterministic validation evidence while removing NON-TV/TVC GitHub-token use, issue mutation, and GitHub-hosted custody/writeback semantics.
repository: StegVerse-Labs/Site
branch: chore/site-st018-github-token-retirement-20260817
canonical_issue: StegVerse-Labs/Site#141
parent_workflow_minimization_issue: StegVerse-Labs/Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_production_runtime_control_plane_authority: NONE
runtime_authority_effect: NONE
publication_authority_effect: NONE
release_authority_effect: NONE
claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
claim_state: CLAIMED_FOR_IMPLEMENTATION
implementation_state: IMPLEMENTED_PENDING_VALIDATION
```

This file is the scoped continuation source for the ST-018 hosted validation-evidence surface. Live repository state and exact validation evidence supersede chat history.

## Existing deterministic contract

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

The legacy `.github/workflows/capture-validation-evidence.yml` granted `issues: write`, used `actions/checkout`, `actions/setup-python`, two `actions/upload-artifact` steps, exported `GH_TOKEN=${{ github.token }}`, and mutated Site #141 through `gh issue comment`. Those mechanics are not admissible as required evidence/custody or authority paths under the TV/TVC-only credential rule.

## Active claim and collision boundaries

```text
claim_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
branch: chore/site-st018-github-token-retirement-20260817
role: IMPLEMENTATION
state: CLAIMED_FOR_IMPLEMENTATION
dependency_surface: site:st018-validation-evidence
claimed_paths:
- data/session-work-claims.json
- .github/workflows/capture-validation-evidence.yml
- docs/ST018_VALIDATION_EVIDENCE_MIRROR_HANDOFF.md
- data/tasks/SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817.json
```

Collision boundaries:
- do not weaken the declared validators or receipt schema;
- do not claim ST-018 validation proves factual truth, admissibility, publication, deployment, release, standing, certification, or runtime activation;
- do not export TV/TVC credentials into GitHub Actions;
- do not introduce any alternate GitHub/project/provider token;
- do not modify the active StegOS admitted-inference paths;
- do not duplicate Site pre-work admission or sovereign worker authority.

## Installed branch implementation

The ST-018 workflow is converted from GitHub-token/write-capable evidence custody to credential-clean deterministic validation:

```text
permissions: {}
actions/checkout: REMOVED
actions/setup-python: REMOVED
actions/upload-artifact: REMOVED
issues: write: REMOVED
GH_TOKEN: REMOVED
github.token reference: REMOVED
GitHub issue mutation: REMOVED
repository writeback: NONE
TV/TVC credential export: NONE
anonymous exact-SHA public source fetch: INSTALLED
credential-bearing environment refusal: INSTALLED
preinstalled Python execution: RETAINED
public jsonschema installation: RETAINED
capture_validation_manifest.py: RETAINED
receipt status enforcement: RETAINED
artifact custody effect: NONE
issue custody effect: NONE
```

The workflow chooses the pull-request head SHA for PR validation and `github.sha` otherwise, anonymously retrieves that exact public Site source through codeload, executes the repository-declared validator manifest, writes the receipt only inside the ephemeral validation workspace, and fails closed when receipt status is not PASS. No hosted artifact or issue comment is treated as custody evidence.

## Intended authority transition

```text
GitHub-hosted token/write-capable evidence publication
-> credential-clean deterministic validation execution only
-> local deterministic receipt generation/checking
-> repository state as source evidence where source changes are appropriate
-> StegVerse/Master Records custody only when a canonical custody contract requires it
```

GitHub-hosted validation remains non-authorizing. Source merge, CI success, log output, or receipt generation does not prove runtime/product activation.

## Required validation before merge

1. `scripts/check_session_work_claims.py` reports `SESSION_WORK_CLAIMS_PASS`.
2. ST-018 workflow reports `ST018_CREDENTIAL_REFUSAL=PASS`.
3. ST-018 workflow reports exact-SHA `ST018_SOURCE_FETCH=PASS`.
4. `scripts/capture_validation_manifest.py` completes and receipt status is PASS.
5. workflow reports `ST018_VALIDATION=PASS`, `authority_effect=NONE`, and `custody_effect=NONE`.
6. Site Handoff Orchestrator passes.
7. Ecosystem Heartbeat Orchestration passes.
8. Site Bootstrap Validate passes.
9. Exact-head PR state is inspected before merge.

Do not restore private GitHub runtime dependencies or any GitHub token merely to make a validation gate green. Repair only deterministic validation boundaries.

## Post-merge release work

After exact-head validation is green and the PR merges:

1. release `SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817` in `data/session-work-claims.json`;
2. mark `data/tasks/SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817.json` released with exact merge/run evidence;
3. reconcile Site #141 so its completion contract no longer requires a hosted artifact or issue-comment custody path;
4. update `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md` accounting and released evidence;
5. continue the next bounded unclaimed token-bearing/redundant Site #268 workflow family.

## Archive condition

This scoped task becomes archive-safe only after source integration, exact validation evidence, released claim state, and durable update of Site #141 and `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`. Product/runtime activation remains independent. The broader session remains active while Site #268 has unremediated workflow/token surfaces.
