# Site Task Elimination Guard

## Assumptions

1. Site local continuation should be checked by repository workflows, not by manual review.
2. The guard checks that declared local continuation work has a workflow, script, or generated state surface.
3. Site remains a mirror and display repository; this guard does not grant execution authority.

## Done Definition

This document is done when the task-elimination guard has a clear role, workflow path, checker command, and non-authority boundary.

## Guard Workflow

Workflow path displayed without leading period for iOS compatibility:

```text
github/workflows/site-task-elimination-guard.yml
```

The canonical repository path begins with a leading period.

## Checker

```text
python scripts/check_site_manual_task_elimination.py
```

## Checked Surfaces

```text
docs/SITE_MANUAL_TASK_ELIMINATION.md
docs/SITE_MIRROR_HANDOFF.md
github/workflows/site-autonomous-continuation.yml
```

## Guard Meaning

The guard confirms that local continuation work is workflow-managed.

It does not claim:

```text
Site activation
Publisher closure
TT source authority
Governance Observatory source authority
SPE standing
commit-time permission
```

## Current State

```text
local_manual_tasks: eliminated
local_continuation: workflow_managed
remaining_blocker: external_workflow_evidence
```
