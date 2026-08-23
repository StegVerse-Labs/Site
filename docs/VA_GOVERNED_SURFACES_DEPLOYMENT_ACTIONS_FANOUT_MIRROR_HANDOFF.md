# VA Governed Surfaces Deployment Actions Fanout Mirror Handoff

## Canonical scope

```text
goal: SITE-ACTIONS-COST-CONTAINMENT-VA-GOVERNED-SURFACES-20260823
parent_goal: SITE-ACTIONS-COST-CONTAINMENT-001 / Site#268
repository: StegVerse-Labs/Site
workflow: .github/workflows/va-governed-surfaces-deployment.yml
claim: SITE-VA-GOVERNED-SURFACES-OBSERVER-RETIREMENT-20260823
credential_authority: TV/TVC
state: MERGED_AWAITING_TASK_SPECIFIC_MAIN_OBSERVATION
authority_effect: NONE
activation_effect: NONE
```

## Proven precondition

The durable deployment observation was already terminal before this cost repair:

```text
receipt: data/va-claim-assistant/governed-surfaces-deployment.json
state: VERIFIED
blockers: []
guide: http 200 + byte_equal true
chat: http 200 + byte_equal true
capability: http 200 + byte_equal true
private_document_upload_enabled: false
automated_filing_enabled: false
authority_effect: false
activation_effect: false
```

## Released source mutation

```text
pull_request: 473
validated_head: b06b01cf59b13a120c8a050e2b4ee98debdb8a56
merge_commit: b526c69a647b96cf8ee6e9e44aca0facc1d61241
Site Handoff Orchestrator: 32669715065 SUCCESS
Ecosystem Heartbeat Orchestration: 32669715039 SUCCESS
Site Bootstrap Validate: 32669715040 SUCCESS
```

These gates prove claim/orchestration/repository integration. They do not substitute for direct observation of the retained task-specific main-source deployment verifier.

## Removed hosted fanout and mutation

The merged workflow removes:

- the six-hour `schedule` execution;
- `permissions.contents: write`;
- credential-bearing `actions/checkout` and `actions/setup-python` dependencies;
- repository commits/pushes of observation state back to `main`;
- GitHub artifact custody on every observation.

## Retained validation

The merged workflow retains:

- `workflow_dispatch` for intentional public re-verification;
- bounded `main` push execution when the guide, Claims Chat, capability state, observer source, or workflow definition changes;
- exact-source anonymous Git acquisition with credential helper and extra-header suppression;
- preinstalled Python validation;
- live deployment observation;
- enforcement that guide/chat/capability return HTTP 200 and are byte-equal to repository source;
- fail-closed enforcement that private document upload and automated filing remain false;
- fail-closed authority/activation boundary checks.

Automatic pull-request execution is intentionally not added. This observer compares repository bytes with deployed `main`; a legitimate PR changing one of those surfaces would necessarily differ from deployed main and would fail for the wrong reason. Repository-wide PR validation remains owned by the canonical Site Bootstrap/Handoff/Heartbeat lanes.

## Authority boundary

```text
github_token_runtime_authority: NONE
repository_writeback_authority: NONE
artifact_custody_required: false
provider_authority: false
runtime_authority: false
custody_authority: false
publication_authority: false
filing_authority: false
activation_authority: false
render_required: false
```

No workflow success or deployment receipt grants private-document upload, automated filing, provider, runtime, custody, publication, release, admissibility, or activation authority.

## Remaining exact gate

The connected GitHub reader exposes PR-triggered runs for a commit but not push-triggered workflow runs, and it does not expose workflow dispatch in this session. Therefore the retained main-source verifier has not yet been directly observed through the supported reader after merge.

The claim remains open until one of these becomes inspectable:

1. the retained main-source `VA Governed Surfaces Deployment Observer` run on/after merge `b526c69a647b96cf8ee6e9e44aca0facc1d61241` with `VA_GOVERNED_SURFACES_DEPLOYMENT=VERIFIED`; or
2. an equivalent task-specific execution receipt proving the merged credential-clean workflow against current main.

Until then the correct state is `MERGED_AWAITING_TASK_SPECIFIC_MAIN_OBSERVATION`, not released or activated.
