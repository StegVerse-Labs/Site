# Site Mirror Handoff Diagnostic Addendum

## Authority and precedence

This file is a repository-local addendum to `docs/SITE_MIRROR_HANDOFF.md` for `StegVerse-Labs/Site`.

`docs/SITE_MIRROR_HANDOFF.md` remains the current handoff and task source of truth. This addendum records only the bounded fail-path diagnostic contract used by the existing Site Task Runner. It does not expand repository authority, activate transport, authorize deployment, authorize release, or change Site state.

## Fail-path diagnostic contract

The existing Site task runner writes:

```text
reports/site-task-diagnostic.json
```

The diagnostic records the selected task, status, failed validator, validator index, exit code, completed-validator sequence, failure class, and the following authority-boundary fields:

```text
authority_effect = NONE
site_mode = PREVIEW_ONLY
state_change_authorized = false
```

The workflow uploads the diagnostic with `if: always()` under a run- and attempt-bound artifact name so both passing and failing task execution remain reconstructable.

The diagnostic is evidence of task execution only. It is not execution authority, deployment evidence, release authority, admissibility, standing, provider activation, Master-Records custody, or permission to mutate any repository.

## Continuation

A failed task remains failed. Uploading or inspecting the diagnostic does not convert failure to success and does not authorize bypassing the failed validator. The next bounded action is to repair only the exact repository-local failure recorded by the diagnostic and then observe a successor run.
