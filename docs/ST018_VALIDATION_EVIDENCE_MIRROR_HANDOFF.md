# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
parent_goal: SITE-ACTIONS-COST-CONTAINMENT-001
batch_claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B17R1-20260817
repository: StegVerse-Labs/Site
branch: chore/site-st018-token-custody-retirement-b17r1-20260817
canonical_issue: StegVerse-Labs/Site#141
parent_workflow_minimization_issue: StegVerse-Labs/Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_production_runtime_control_plane_authority: NONE
state: CLAIMED_FOR_IMPLEMENTATION
```

Live repository state, claim state, exact validation evidence, and the parent cost-containment handoff supersede chat.

## Retained deterministic contract

`validation_manifests/repository-core.json`, `schemas/validation-execution-receipt.schema.json`, `scripts/capture_validation_manifest.py`, `scripts/write_site_current_main_validation_receipt.py`, `scripts/check_site_current_main_validation_receipt_writer.py`, `scripts/check_site_current_main_validation_evidence.py`, and `data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json` remain retained.

## B17R1 migration

The retired `.github/workflows/capture-validation-evidence.yml` used `issues: write`, `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, and `GH_TOKEN=${{ github.token }}` issue mutation. Those hosted transport/custody mechanics are not ST-018 semantics and conflict with the TV/TVC-only credential requirement.

B17R1 removes that workflow and transfers unfinished native-main observation to the existing Site heartbeat capability `.stegverse/repo-heartbeat.json::activation_receipt_validation`, with `github_token_required=false`. No second scheduler, heartbeat, custody authority, runtime, publication path, or product activation lane is created.

Canonical task: `data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json`, state `BLOCKED_DEPENDENCY_MACHINE_OWNED`, owner `Site repository heartbeat activation_receipt_validation capability / StegVerse control plane`.

## Collision boundaries

Do not weaken validators/receipt schema, export TV/TVC credentials, add alternate GitHub/project/provider tokens, modify active StegOS admitted-inference or HIL product paths, duplicate Site pre-work admission/heartbeat/scheduler/Master Records custody, or infer runtime/HIL/StegFin/wallet authority from validation cleanup.

## Release gates

Before merge: claim validation, Site handoff/orchestration, Site Bootstrap Validate, Ecosystem Heartbeat Orchestration, retained ST-018 deterministic source presence, and no new non-TV/TVC credential use must pass.

After merge: release B17R1 claim, update `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`, reconcile Site #141 so GitHub artifact ID/digest and issue-comment custody are not required completion evidence, and leave actual native-main ST-018 completion machine-owned until its own evidence is observed.

## Supersession

PR #343 / branch `chore/site-st018-token-custody-retirement-b17-20260817` is superseded because `main` advanced the canonical claim registry during implementation. B17R1 is reconstructed from the newer base and must be validated independently.

## Archive condition

This scoped cleanup is archive-safe only after exact validation, merge, claim release, parent handoff update, and Site #141 contract reconciliation. Product/runtime activation remains independent.
