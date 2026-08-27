# Site Mirror Workflow Validator Mirror Handoff

Updated: 2026-08-26
Repository: `StegVerse-Labs/Site`
Canonical issue: `#519`
Parent continuation: `Site#501`

## Source of truth

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.
Site Task Runner orchestration authority remains `docs/SITE_ORCHESTRATION_REPAIR.md`.
This handoff owns only the stale Site-mirror workflow validator exposed after Site#517 merged.

## Machine-discovered failure

Main Bootstrap `33029094754` completed SUCCESS and Site Task Runner `33029116012` advanced through the repaired Site mirror goal gate.

The next exact failure was:

```text
scripts/check_site_mirror_full_readiness.py
 -> scripts/check_site_mirror_readiness.py
  -> scripts/check_site_mirror_workflow.py
failure: required consolidated workflow text missing: schedule:
classification: VALIDATOR_AUTHORITY_DRIFT
```

The current Site Task Runner contract intentionally forbids schedule authority. Adding a schedule would be a regression.

## Repair contract

The Site mirror workflow validator must require:

```text
workflow_dispatch: present, validation-only
workflow_run: present
successful upstream Bootstrap predicate: present
main-branch upstream predicate: present
mirror-readiness binding: present
run_site_task.py binding: present
```

It must explicitly reject these independent worker triggers:

```text
push:
schedule:
pull_request:
```

No schedule is added to the worker.

## Machine-readable vector visibility

Canonical operational task-vector notation is owned by `StegVerse-Labs/.github`:

```text
profile: task.v1
notation: L R U I V G O C M T B E A P
width: 14 digits
profile authority: StegVerse-Labs/.github/management/COSV_PROFILE_V1.json
```

This Site repair task references that canonical profile but does not invent a task vector. Until a canonical Site COSV projection is emitted, the concrete 14-digit vector remains `null` rather than being guessed.

The separate semantic state-vector mechanism is also visible and machine-readable in the organization control plane through `stegverse.semantic-state-vector/v1`; it is distinct from COSV `task.v1`.

## Current state

```text
issue: #519
branch: fix/site-mirror-workflow-validator-519
validator repair: IMPLEMENTED
exact-head hosted validation: PENDING
merge: NOT_MERGED
next Site Task Runner advance: PENDING
authority effect: NONE
activation effect: false
```

## Remaining work

1. Admit bounded task/claim.
2. Validate exact head.
3. Merge only after required gates pass.
4. Observe subsequent Bootstrap -> Site Task Runner advance beyond Site mirror workflow validation.
5. Return control to Site#501 and continue the next exact failure until Pages/live semantic observation is reached.

## Archive posture

This handoff plus issue #519, its machine task/claim, and workflow evidence preserve the continuation state.
