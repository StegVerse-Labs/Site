# Site Task Elimination Guard

## Assumptions

1. Site local continuation should be checked by repository workflows, not by manual review.
2. The guard checks that declared local continuation work has a workflow, script, or generated state surface.
3. Site remains a mirror and display repository; this guard does not grant commit-time permission.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical repository paths begin with a leading period.

## Done Definition

This document is done when the task-elimination guard has a clear role, workflow path, checker commands, and non-authority boundary.

## Guard Workflow

Workflow path displayed without leading period for iOS compatibility:

```text
github/workflows/site-task-elimination-guard.yml
```

The canonical repository path begins with a leading period.

## Checkers

```text
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
github/workflows/site-autonomous-continuation.yml
github/workflows/site-task-elimination-guard.yml
```

## Guard Meaning

The guard confirms that local continuation work is workflow-managed and that ecosystem management handoffs are repository-resident.

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
ecosystem_handoff_validation: workflow_managed
remaining_blocker: external_workflow_evidence
```
