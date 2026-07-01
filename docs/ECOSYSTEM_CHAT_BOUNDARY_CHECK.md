# Ecosystem Chat Boundary Check

## Purpose

This document defines the local verification task for the public Ecosystem Chat surface.

The check exists so the Site repo can detect drift before Ecosystem Chat is advertised or connected to any governed backend gateway.

## Task

Declared task:

```text
ecosystem-chat-boundary-check-v1
```

Task definition:

```text
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
```

Verifier:

```text
scripts/check_ecosystem_chat_boundary.py
```

## Direct command

```bash
python scripts/check_ecosystem_chat_boundary.py
```

## Declared-task path

The task is registered in:

```text
data/headless-task-registry-v1.json
```

The task uses the existing headless task pattern. No new workflow is required.

## Boundary verified

The verifier checks that these files preserve the same boundary language and fixture values:

```text
ecosystem-chat.html
assets/ecosystem-chat.js
docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md
docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md
fixtures/ecosystem-chat/request.example.json
fixtures/ecosystem-chat/response.example.json
fixtures/ecosystem-chat/sdk-form-payload.example.json
```

The verified boundary is:

```text
no shell
no credential authority
authority required before execution
rate limits required before live submission
receipt required for execution
restricted administration routed separately
```

## Done condition

The check is passing when the verifier emits JSON with:

```json
{
  "ok": true,
  "boundary": "no-shell/no-credential/authority-required/receipt-required"
}
```

## Failure meaning

A failure means the public page, JavaScript behavior, documentation, or fixtures no longer agree on the same execution boundary.

A failed check should be treated as a public-surface drift event. The page should not be advertised as a governed advancement interface until the drift is corrected.
