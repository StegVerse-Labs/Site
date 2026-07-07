# Ecosystem Chat Gateway Preview Status

## Status

The Site repository now contains a local, deterministic preview module for the future Ecosystem Chat backend gateway.

```text
Module: backend/ecosystem_chat_gateway_preview.py
Checker: scripts/check_ecosystem_chat_gateway_preview.py
Declared task: data/headless-tasks/ecosystem-chat-gateway-preview-check-v1.json
Registry state: active in data/headless-task-registry-v1.json
```

## Purpose

The preview gateway gives the repository a backend-shaped contract without activating a live service.

It validates the response shape expected by the future `/api/ecosystem-chat` endpoint:

```text
routed_module
task_status
receipt_id
interaction_bands
interaction_profile
math_solver_supported
next_action
```

## Current behavior

```text
Route classification: local deterministic preview
Interaction telemetry: local deterministic preview
Math solver: route/telemetry preview only
Receipt id: always null
Authority: none
Provider calls: not active
Network research: not active
Repository mutation: not active
```

## Checked cases

The checker verifies representative gateway responses for:

```text
Site request -> preview_only
Solver request -> preview_only
Research/provider-shaped request -> preview_only
Restricted administration-shaped request -> pending_authority
```

## Non-claims

```text
The preview gateway is not a deployed API.
The preview gateway is not a model provider.
The preview gateway is not a live math solver.
The preview gateway is not a network research adapter.
The preview gateway is not receipt authority.
```

## Next integration target

When backend activation begins, the live gateway should preserve the same response shape while replacing local deterministic preview values with governed runtime values from approved ecosystem handlers.
