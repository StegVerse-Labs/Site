# VA Governed Surfaces Deployment Actions Fanout Mirror Handoff

## Canonical scope

```text
goal: SITE-ACTIONS-COST-CONTAINMENT-VA-GOVERNED-SURFACES-20260823
parent_goal: SITE-ACTIONS-COST-CONTAINMENT-001 / Site#268
repository: StegVerse-Labs/Site
workflow: .github/workflows/va-governed-surfaces-deployment.yml
claim: SITE-VA-GOVERNED-SURFACES-OBSERVER-RETIREMENT-20260823
credential_authority: TV/TVC
state: IMPLEMENTED_AWAITING_EXACT_HEAD_VALIDATION_AND_MERGE
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

This repair does not change any VA product surface, provider behavior, filing behavior, privacy capability, or deployment target.

## Removed hosted fanout and mutation

The pre-repair workflow had:

- six-hour `schedule` execution;
- `permissions.contents: write`;
- credential-bearing `actions/checkout` with GitHub repository credentials;
- `actions/setup-python` dependency;
- repository commits/pushes of observation state back to `main`;
- GitHub artifact custody on every observation.

The repaired workflow removes all of those recurring/mutating mechanics.

## Retained validation

The repaired workflow retains:

- `workflow_dispatch` for intentional public re-verification;
- bounded `main` push execution when the guide, Claims Chat, capability state, observer source, or workflow definition changes;
- exact-source anonymous Git acquisition with credential helper and extra-header suppression;
- preinstalled Python validation;
- live deployment observation;
- enforcement that guide/chat/capability return HTTP 200 and are byte-equal to the repository source;
- fail-closed enforcement that private document upload and automated filing remain false;
- fail-closed authority/activation boundary checks.

Automatic pull-request execution is intentionally not added. This observer compares repository bytes with deployed `main`; a legitimate PR changing one of those surfaces would necessarily differ from the deployed main site and would fail for the wrong reason. Repository-wide PR validation remains owned by the canonical Site validation/orchestration lanes.

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

No workflow success or existing deployment receipt grants private-document upload, automated filing, provider, runtime, custody, publication, release, admissibility, or activation authority.

## Completion contract

This handoff is not terminal until all of the following are true:

1. exact branch/head claim validation passes;
2. Site Handoff Orchestrator passes;
3. Ecosystem Heartbeat Orchestration passes;
4. Site Bootstrap Validate passes;
5. the repaired workflow source is merged into current `main`;
6. the claim fragment is terminalized with the exact PR/head/merge/run evidence;
7. the shared Actions cost handoff consumes the released result.

Current state is therefore `IMPLEMENTED_AWAITING_EXACT_HEAD_VALIDATION_AND_MERGE`, not released.
