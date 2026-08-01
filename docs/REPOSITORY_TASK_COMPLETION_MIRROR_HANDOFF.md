# Repository Task Completion Mirror Handoff

## Authority

This file is the task-source-of-truth for non-halting repository work observation in `StegVerse-Labs/Site`. Read it after `docs/SITE_MIRROR_HANDOFF.md` and `data/site-orchestration-state.json`.

Live repository state, task objects, executable validators, workflow runs, committed reports, and immutable commits override conversational claims.

## Governing rule

There are no external tasks.

An active task is admissible only when all of the following are committed:

1. exact task identifier;
2. owning repository;
3. task object at `data/tasks/<TASK-ID>.json`;
4. implementation file locations;
5. verification file locations;
6. executable acceptance command;
7. required success marker;
8. explicit completion-state mutation.

A session name, person, agent, provider, or phrase such as `external-active-session` is not task ownership and must be replaced by a repository path.

## Controller

Location:

`StegVerse-Labs/Site/scripts/observe_and_complete_repository_tasks.py`

Responsibilities:

- enumerate active tasks from `data/site-orchestration-state.json`;
- require a matching object under `data/tasks/`;
- reject external dependencies;
- reject missing implementation or verification locations;
- execute each task's acceptance command;
- preserve every observation in `repository-task-observation.report.json`;
- normalize session-shaped ownership to repository task paths;
- move validated tasks from active to completed state;
- expose exact blockers rather than preserving ambiguous running status.

## Workflow

Location:

`StegVerse-Labs/Site/.github/workflows/observe-and-complete-repository-tasks.yml`

Triggers:

- relevant pushes to `main`;
- manual dispatch;
- hourly scheduled observation.

The workflow runs the controller with `--apply`, commits state transitions and the observation report, and preserves the report as an artifact.

## Current task

Task:

`SITE-0001-UPLOAD`

Task object:

`StegVerse-Labs/Site/data/tasks/SITE-0001-UPLOAD.json`

Implementation locations:

- `StegVerse-Labs/Site/humans-as-interoperability-layer.html`
- `StegVerse-Labs/Site/assets/hil-experiment-v1.1.js`
- `StegVerse-Labs/Site/assets/hil-direct-upload-v1.js`
- `StegVerse-Labs/Site/data/hil-experiment.json`
- `StegVerse-Labs/Site/data/hil-gateway-config.json`
- `StegVerse-Labs/Site/data/HIL_Canonical_Paper_v1_1.pdf`

Verification locations:

- `StegVerse-Labs/Site/scripts/check_hil_v1_1_release.py`
- `StegVerse-Labs/Site/scripts/verify_hil_site_contract.py`
- `StegVerse-Labs/Site/.github/workflows/hil-site-contract.yml`

Acceptance command:

```bash
python scripts/check_hil_v1_1_release.py
```

Required marker:

`HIL_V1_1_RELEASE_VERIFICATION=PASS`

## Corrected failure

The first durable controller observation identified a stale task contract:

- stale validator: `scripts/check_hil_v1_upload_surface.py`;
- stale expected manifest version: `v1.0`;
- live manifest version: `v1.1`;
- live verifier: `scripts/check_hil_v1_1_release.py`.

The task object was corrected to the live v1.1 implementation and validator chain in commit `c7898cd69a0aa64065f3fcec45482faacd9d55e6`.

The durable/self-reconciling controller was activated in commit `bd839502f9fa2eae5f268b5a99dacfa58e3928a3`.

## Completion behavior

When the acceptance command emits the required marker, the controller must:

1. remove `SITE-0001-UPLOAD` from `active_sequence.parallel_safe_tasks`;
2. append it to `active_sequence.completed_parallel_safe_tasks`;
3. set `ownership.hil_upload_surface` to `data/tasks/SITE-0001-UPLOAD.json`;
4. record zero remaining tasks when applicable;
5. write the idle terminal statement only when no tasks remain.

If validation fails, the exact command output remains the next repository-local work instruction. The task must not be described as waiting on an external session.

## Cross-repository Transition Element coordination

The StegVerse Transition Element layer is being built in these exact locations:

- conformance authority: `Admissible-Existence/ET`;
- public and interactive projection: `StegVerse-Labs/Site/transition-elements/`;
- authority map: `StegVerse-Labs/Site/data/transition-table/transition-element-action-authority-map-v1.json`;
- discovery controller: `StegVerse-Labs/Site/tools/transition_discovery_ledger.py`;
- public representation: `StegVerse-Labs/admissibility-wiki/docs/stegverse/transition-element-code-representation.md`;
- repository standard: `StegVerse-Labs/repo-standards/standards/ST-004_TRANSITION_TABLE_ELEMENTS.standard.md`.

All further ET work must be expressed as repository-local task objects at the owning repository. No external task status is valid.

## Release posture

This mechanism is activated as repository task-observation and completion infrastructure. It does not grant execution, publication, custody, or governance authority to any task output. Release tagging remains pending passing validation evidence and downstream synchronization.
