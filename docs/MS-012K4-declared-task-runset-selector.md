# MS-012K.4 Declared Task Runset Selector

## Purpose

This bundle makes automation data-driven.

A runset declares which tasks are currently available to run for transition-table discovery. The workflow plane does not need to change when the runset changes.

## Boundary

```text
data/headless-task-runsets/*.json
→ tools/headless_task_runset.py
→ tools/headless_cmd_runner.py
→ declared tasks
→ reports and receipts
```

## Safety

```text
No workflow files.
No arbitrary task glob execution.
No privileged task classes.
No authority expansion.
```
