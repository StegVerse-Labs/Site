# Ecosystem Chat Activation Retention Credential Mirror Handoff

Updated: 2026-08-26
Repository: `StegVerse-Labs/Site`
Issue: `#471`
Pull request: `#474`
Claim: `SITE-ECOSYSTEM-CHAT-ACTIVATION-RETENTION-CREDENTIAL-CLEAN-471-20260823`
Branch: `claim/site-ecosystem-chat-activation-retention-credential-clean-471`
State: `IMPLEMENTED_VALIDATION_ONLY_CORRECTION_AWAITING_EXACT_HEAD_PASS_AND_MERGE`

## Goal

Remove the non-TV/TVC repository-sync secret dependency from the existing Ecosystem Chat activation-retention observer while preserving its active evidence-observation, persistence, and fail-closed activation responsibilities.

## Canonical sources of truth

- `docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md`
- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `docs/ACTIONS_SESSION_ARCHIVE_RECOVERY_MIRROR_HANDOFF.md`
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

The initial implementation head `07fa9e9c53cbc58af5539b20e0fdc3247b2b58ba` was built from exact observed main `b445cd35818510dd0eee81884b56ea8d549fe518` and changed only the five claimed paths.

```text
Ecosystem Heartbeat Orchestration: 32669886282 SUCCESS
Site Handoff Orchestrator: 32669886276 SUCCESS
Site Bootstrap Validate: 32669886318 SUCCESS
```

A later PR-head Bootstrap run exposed an independent claim-admission defect: the claim fragment used bespoke machine state `IMPLEMENTED_AWAITING_TASK_SPECIFIC_PUSH_RUN_VISIBILITY`, which passed the general claim validator but was not one of the active states admitted by `site_handoff_orchestrator.py`. The branch therefore could not map to exactly one active pre-work claim.

That defect was repaired on 2026-08-26 by preserving the lifecycle detail separately while changing the machine claim state to the canonical active validation enum:

```text
state: CLAIMED_FOR_VALIDATION
validation_state: IMPLEMENTED_AWAITING_TASK_SPECIFIC_PUSH_RUN_VISIBILITY
repair commit: d430a0d09a7fede50a42ccf577776d87af2705d7
```

Exact repaired-head PR-associated validation then passed:

```text
Ecosystem Heartbeat Orchestration: 33038408763 SUCCESS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: 33038408806 SUCCESS
Site Handoff Orchestrator: 33038408771 SUCCESS
```

This proves the #471 claim is again admitted by the canonical pre-work orchestration lane without weakening credential, authority, activation, or collision boundaries. It does **not** prove the task-specific push-triggered retention workflow ran.

## Task-specific execution visibility boundary

`ecosystem-chat-activation-retention.yml` intentionally has no pull-request trigger; adding one merely to create inspectable evidence would add a new paid PR fanout lane and alter the active observer contract. Its branch push trigger should execute when the workflow/importer changes, but the connected commit run reader exposes only pull-request-associated workflow runs. The connected generic GitHub reader rejects the workflow-specific run-list endpoint, and the available connector exposes no workflow-dispatch action.

A hosted shell clone attempt was additionally blocked by that environment's outbound DNS, which is an execution-environment limitation rather than Site evidence.

Therefore this handoff does **not** claim the task-specific retention execution has been observed. Source implementation and exact repaired-head repository validation are complete; integration/release remain open until the retention lane itself is directly inspectable or equivalent task-specific execution evidence is durably available.

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


## TVC upstream activation-evidence packet relationship — 2026-08-27

The sovereign inference continuation now has a merged TVC-owned durable evidence-persistence seam. This #471/#474 lane remains the existing Site activation-retention/import owner and must not be duplicated.

```text
upstream parent owner: StegVerse-Labs/.github#60 / SHWP-ECOSYSTEM-CHAT-INFERENCE-001
upstream LLM projection: StegVerse-org/LLM-adapter receipts/ecosystem-chat-sovereign-activation.verified.json
TVC persistence task: TVC-ECOSYSTEM-CHAT-ACTIVATION-EVIDENCE-001
TVC handoff: StegVerse-Labs/TVC docs/ECOSYSTEM_CHAT_ACTIVATION_EVIDENCE_TRANSPORT_MIRROR_HANDOFF.md
TVC packet: receipts/ecosystem-chat-activation-evidence/transport.latest.json
required TVC packet state: READY_FOR_SITE_IMPORT
TVC source validation: 33135951150 SUCCESS
TVC merge: 4c8d3440fde168414c700f7e54909e81b2f27e1e
TVC runtime packet observed: false
duplicate Site importer authorized: false
```

This relationship does not make a TVC packet equal Site activation. When authentic upstream evidence eventually exists, this lane or its canonical reconciled successor must independently validate/retain the evidence under Site's existing fail-closed activation contract. The current upstream packet is absent because the sovereign parent has not yet executed terminally.

No user action is required for this relationship. No GitHub token, repository-sync token, Render dependency, credential material, provider authority, or Site mutation authority is granted by the TVC packet.

Because this handoff update changes the open PR head after earlier validation, PR #474 must be revalidated on its new exact head before merge; prior validation remains historical evidence only.


## Post-consolidation exact-head validation — 2026-08-27

The upstream TVC relationship and claim-pointer reconciliation were followed by fresh exact-head repository validation.

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: 33138271994 SUCCESS
Ecosystem Heartbeat Orchestration: 33138271971 SUCCESS
Site Handoff Orchestrator: 33138271985 SUCCESS
```

These runs validate the current claimed branch after the consolidation metadata changes. They remain validation-only and do not satisfy the task-specific activation-retention execution-visibility gate, do not merge PR #474, and do not prove Ecosystem Chat activation.

Current Site #471/#474 state is therefore:
```text
claim: CLAIMED_FOR_VALIDATION
source/claim exact-head validation: PASS
task-specific retention workflow execution visibility: PENDING
merge: PENDING
activation: NOT PROVEN
upstream TVC runtime packet: NOT OBSERVED
```


## Validation-only authority correction — 2026-08-27

The prior completion gate requiring direct execution of the writeback-capable retention workflow is superseded because that workflow itself carried GitHub repository-persistence authority incompatible with the current sovereign authority model.

Observed stale main behavior before correction:
```text
permissions.contents: write
actions/download-artifact with github.token
runtime/evidence acquisition inside GitHub Actions
activation-state rebuild inside GitHub Actions
git commit / git push
NON-TV/TVC repository-sync secret on main
```

The existing #474 claimed lane now replaces that design with validation-only semantics:

```text
permissions: contents: read
checkout persist-credentials: false
GitHub Actions runtime persistence authority: NONE
GitHub Actions activation authority: NONE
GitHub Actions evidence acquisition authority: NONE
repository writeback: prohibited
git commit/push: prohibited
artifact github-token path: prohibited
external state mutation/import execution: prohibited in hosted workflow
credential authority: TV/TVC
```

The task-specific workflow visibility requirement is therefore narrowed to **validation of the corrected non-authorizing source contract**, not execution of the superseded writeback runtime behavior. Running the old writeback behavior is no longer an admissible completion step.

Actual activation evidence retention/persistence remains an admitted sovereign-runtime responsibility. The future TVC `READY_FOR_SITE_IMPORT` packet must be consumed by a non-GitHub-runtime Site execution path under the existing Site activation contract or a canonical successor; hosted validation may only verify source and checked-in state consistency.

This correction changes neither product activation state nor upstream runtime evidence. Ecosystem Chat remains activation-pending until the sovereign parent/TVC/LLM/Master Records chain produces authentic evidence.
