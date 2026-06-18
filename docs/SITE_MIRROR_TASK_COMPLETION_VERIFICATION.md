# Site Mirror Task Completion Verification

## Purpose

This packet defines how a queued mirror task is verified complete.

A task is not complete merely because a file was added or a chat response said it was complete. A task is complete only when the task's declared completion evidence exists and the verification surface records the result.

## Verification Inputs

```text
SITE_MIRROR_PRIORITY_QUEUE.md
SITE_MIRROR_TASK_LOOP_TRACKER.md
SITE_MIRROR_HANDOFF.md
SITE_MIRROR_ACTIVATION_LEDGER.json
SITE_MIRROR_ACTIVATION_STATUS.md
SITE_MIRROR_EVIDENCE_REQUIREMENTS.md
SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md
```

## Completion Evidence Types

```text
artifact_file
checker_file
workflow_file
receipt_artifact
ledger_update
handoff_update
status_update
external_closure_evidence
```

## Completion States

```text
queued
active
blocked
ready_for_verification
verified_complete
complete_no_queued_task
```

## Completion Rule

A task may move to `verified_complete` only when:

```text
1. Its declared artifact exists.
2. Its required checker exists, unless the task is documentation-only.
3. Its checker passes, or the handoff records why a checker cannot yet run.
4. Its completion is reflected in the tracker, handoff, or ledger.
5. The next queued task is selected by priority if one exists.
```

## Blocked Rule

A task blocked by Publisher evidence, Site evidence, workflow artifacts, or closure receipts must remain `blocked` until that evidence exists.

Blocked tasks remain in the queue and may outrank local tasks, but the orchestrator should select the next unblocked local task when blocked evidence is outside Site authority.

## Non-Activation Rule

Task completion does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Archive Readiness

This packet lets a future runner, agent, or session verify completed work from repository artifacts rather than prior chat context.
