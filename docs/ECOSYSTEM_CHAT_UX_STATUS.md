# Ecosystem Chat UX Status

## Status

```text
Repository: StegVerse-Labs/Site
Page: ecosystem-chat.html
Status: installed
UX contract: single-primary-governed-chat-preview-entry
Validation path: python scripts/run_site_task.py validate
Validator: scripts/check_ecosystem_chat_boundary.py
Workflow posture: existing validate workflow only; no new workflow
```

## Primary Path

```text
1. Read the boundary.
2. Try the governed chat preview.
3. Receive local route classification.
```

## Secondary Path

```text
1. Open collapsible Technical preview details.
2. Inspect SDK manifest preview.
3. Inspect gateway request shape.
```

## Required Hero Actions

```text
Primary: Try the governed chat preview -> #console
Secondary: How the boundary works -> #how-it-works
```

## Forbidden Page Shapes

```text
multi-entry console
task launcher
demo index
repo control panel
execution console
receipt issuer
```

## Boundary Summary

Site may draft, classify, and display local preview text.

Site may not execute commands, accept secrets, change repositories, issue proof receipts, or grant admissibility.

Any future live path must preserve:

```text
raw_shell_allowed=false
authority_required=true
rate_limit_required=true
receipt_required_for_execution=true
```

## Current Guard

The active guard is part of the existing validation path:

```text
python scripts/run_site_task.py validate
```

The validator enforces:

```text
one primary governed chat action
one secondary boundary action
technical details in collapsible section
no return to the old multi-entry hero layout
```
