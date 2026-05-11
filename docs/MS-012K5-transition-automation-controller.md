# MS-012K.5 Transition Automation Controller

## Purpose

This bundle creates a data-driven controller for the currently unlocked automation sequence.

It is not a workflow. It is the tool/policy layer that a stable bounded dispatcher can call.

## Initial sequence

```text
failed bundle boundary processor
→ transition discovery automation runset
→ reports and receipts
```

## Safety

```text
No workflow files.
No direct install.
No deletion.
No authority expansion.
No force push.
No arbitrary shell expansion.
```
