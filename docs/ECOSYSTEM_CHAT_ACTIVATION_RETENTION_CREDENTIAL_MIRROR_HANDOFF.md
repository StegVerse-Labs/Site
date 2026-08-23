# Ecosystem Chat Activation Retention Credential Mirror Handoff

Updated: 2026-08-23
Repository: `StegVerse-Labs/Site`
Issue: `#471`
Pull request: `#474`
Claim: `SITE-ECOSYSTEM-CHAT-ACTIVATION-RETENTION-CREDENTIAL-CLEAN-471-20260823`
Branch: `claim/site-ecosystem-chat-activation-retention-credential-clean-471`
State: `IMPLEMENTED_AWAITING_TASK_SPECIFIC_PUSH_RUN_VISIBILITY`

## Goal

Remove the non-TV/TVC repository-sync secret dependency from the existing Ecosystem Chat activation-retention observer while preserving its active evidence-observation, persistence, and fail-closed activation responsibilities.

## Canonical sources of truth

- `docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md`
- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `docs/SITE_MIRROR_HANDOFF.md`

The activation goal remains incomplete. This task is **not** clock retirement and grants no runtime, provider, custody, reconstruction, publication, release, or activation authority.

## Proven credential defect and repair

The pre-repair workflow injected `secrets.STEGVERSE_REPO_SYNC_TOKEN` into `scripts/import_ecosystem_chat_external_activation_states.py`. The importer used that token only for the Master Records custody-state record.

The exact record is publicly readable at:

```text
master-records/orchestration
reports/ecosystem-chat-custody-activation-state.json
```

Observed owner state remains fail-closed:

```text
state: CUSTODY_ACTIVATION_PENDING_EXTERNAL_EVIDENCE
authenticated_custody_receipt.complete: false
reconstructability_pass.complete: false
live_receipt.present: false
live_receipt.verified: false
```

The implemented #471 branch therefore:

- removes `STEGVERSE_REPO_SYNC_TOKEN` and `secrets.STEGVERSE_REPO_SYNC_TOKEN` from the retention workflow;
- removes token discovery and Authorization-header construction from the importer;
- reads both external owner states anonymously from public raw GitHub paths;
- retains record-type, `manual_user_action_required`, canonical SHA-256, and gate-object validation;
- retains partial/stale fail-closed state when either owner record cannot be validated;
- adds `scripts/check_ecosystem_chat_activation_retention_credential_boundary.py` to reject regression of the non-TV/TVC credential path;
- runs that credential-boundary check before external-state import in the retention workflow.

## Retained behavior

- hourly schedule `11 * * * *` remains;
- `workflow_run` trigger remains;
- bounded source push trigger remains;
- `workflow_dispatch` remains;
- adapter activation-receipt acquisition remains;
- owner-state import and hash validation remain;
- machine activation-state recomputation remains;
- existing evidence persistence remains;
- activation remains pending unless every pre-existing gate is actually satisfied.

## Exact PR-head repository validation

PR #474 head `07fa9e9c53cbc58af5539b20e0fdc3247b2b58ba` was built from exact observed main `b445cd35818510dd0eee81884b56ea8d549fe518` and changes only the five claimed paths.

```text
Ecosystem Heartbeat Orchestration: 32669886282 SUCCESS
  exclusive pre-work claim validation: SUCCESS
  repository workload reconciliation: SUCCESS
Site Handoff Orchestrator: 32669886276 SUCCESS
Site Bootstrap Validate: 32669886318 SUCCESS
  credential refusal: SUCCESS
  anonymous exact-source acquisition: SUCCESS
  workflow inventory / exclusive claims / canonical application: SUCCESS
```

PR #474 is mergeable. Combined commit status exposes no task-specific Actions status.

## Task-specific execution visibility boundary

`ecosystem-chat-activation-retention.yml` intentionally has no pull-request trigger; adding one merely to create inspectable evidence would add a new paid PR fanout lane and alter the active observer contract. Its branch push trigger should execute when the workflow/importer changes, but the connected GitHub run reader only exposes PR-associated workflow runs and does not list ordinary branch-push executions. The available connector also exposes no workflow-dispatch action.

A hosted shell clone attempt was additionally blocked by that environment's outbound DNS, which is an execution-environment limitation rather than Site evidence.

Therefore this handoff does **not** claim the task-specific retention execution has been observed. Source implementation and repository-wide validation are complete; integration/release remain open until the retention lane itself is directly inspectable or equivalent task-specific execution evidence is durably available.

## Collision boundaries

- Do not modify `StegVerse-org/LLM-adapter` provider/runtime execution files.
- Do not modify `master-records/orchestration` custody evidence.
- Do not hand-edit activation-state semantics.
- Do not retire the retention clock while activation evidence is pending.
- Do not modify `.github/workflows/validate.yml` while Site #388 owns it.
- No Render.
- No NON-TV/TVC credential.
- No GitHub-token production/runtime authority.

## Remaining completion gate

1. Observe the exact #471 retention workflow execution and require the credential-boundary step, anonymous external-state import, activation-state consistency validation, and persistence phase to complete without authority escalation.
2. Reconcile against exact current `main` immediately before merge.
3. Merge PR #474.
4. Terminalize the claim fragment and close #471.
5. Do not reclassify workflow success as Ecosystem Chat activation.
