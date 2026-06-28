# Site Final Goal After Local Receipt

## Assumptions

1. Final goal status now depends on the local completion receipt gate.
2. Local completion receipt generation is workflow-managed.
3. Site should not require manual coordination after the local receipt changes.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This document is done when the local completion receipt can trigger a repository-managed final goal status update.

## Workflow

```text
github/workflows/site-final-goal-after-local-receipt.yml
```

The canonical repository path begins with a leading period.

## Trigger

```text
workflow_run: Site Local Completion Receipt
push: docs/SITE_LOCAL_COMPLETION_RECEIPT.json
manual dispatch
```

## Action

```text
python scripts/update_site_final_goal_status.py
python scripts/check_site_final_goal_status.py
```

The workflow then commits:

```text
docs/SITE_FINAL_GOAL_STATUS.md
docs/SITE_FINAL_GOAL_STATUS.json
```

## Boundary

This workflow updates final goal status only after the local completion receipt changes. It does not activate Site, grant commit-time permission, or move source authority into Site.

## Current State

```text
local_receipt_to_final_goal_status: workflow_managed
activation_state: pending_external_evidence
remaining_blocker: external_workflow_evidence
```
