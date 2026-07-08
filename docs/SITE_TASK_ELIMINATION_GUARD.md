# Site Task Elimination Guard

## Assumptions

1. Site local continuation should be checked by repository workflows and declared tasks, not by manual review.
2. The guard checks that declared local continuation work has a workflow, script, or generated state surface.
3. Site remains a mirror and display repository.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical repository paths begin with a leading period.

## Done Definition

This document is done when the task-elimination guard has a clear role, workflow path, checker commands, and boundary statement.

## Guard Workflow

Workflow path displayed without leading period for iOS compatibility:

```text
github/workflows/site-task-runner.yml
```

The canonical repository path begins with a leading period.

## Checkers

```text
python scripts/run_site_task.py task-elimination-guard
python scripts/run_site_task.py local-completion-receipt
python scripts/check_site_manual_task_elimination.py
python scripts/check_site_ecosystem_management_handoff.py
```

## Checked Surfaces

```text
docs/SITE_MANUAL_TASK_ELIMINATION.md
docs/SITE_TASK_ELIMINATION_GUARD.md
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
github/workflows/site-task-runner.yml
scripts/run_site_task.py
```

## Guard Meaning

The guard confirms that local continuation work is workflow-managed through the consolidated Site task runner and that ecosystem management handoffs are repository-resident.

Boundary:

```text
Site activation remains pending.
Publisher closure remains external.
TT source authority remains external.
Governance Observatory source authority remains external.
SPE standing remains separate.
Commit-time permission remains separate.
```

## Current State

```text
local_manual_tasks: eliminated
local_continuation: workflow_managed
ecosystem_handoff_validation: workflow_managed
remaining_blocker: external_workflow_evidence
```
