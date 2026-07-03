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
README.md
ecosystem-chat.html
assets/ecosystem-chat.js
docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md
docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md
docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md
docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md
fixtures/ecosystem-chat/request.example.json
fixtures/ecosystem-chat/response.example.json
fixtures/ecosystem-chat/sdk-form-payload.example.json
```

The verifier also checks that `ecosystem-chat.html` keeps public links to:

```text
docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md
docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md
docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md
```

The verifier also checks that `README.md` keeps references to:

```text
docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md
scripts/check_ecosystem_chat_boundary.py
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
data/headless-task-registry-v1.json
python scripts/check_ecosystem_chat_boundary.py
```

The verifier also checks that `docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md` keeps these public state declarations:

```text
No-shell boundary state: installed
No-credential boundary state: installed
Restricted-admin routing state: installed
Boundary verifier state: installed
Declared task state: installed
Registry state: installed
Backend gateway state: not installed
Authority-issued receipt state: not installed
```

The verifier also checks that the declared task and registry remain aligned:

```text
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
  task_id = ecosystem-chat-boundary-check-v1
  command = python scripts/check_ecosystem_chat_boundary.py
  authority_class = ordinary_analysis
  expected_inputs include README, page, JavaScript, docs, activation status, fixtures, task file, and registry

data/headless-task-registry-v1.json
  contains exactly one ecosystem-chat-boundary-check-v1 entry
  task_path = data/headless-tasks/ecosystem-chat-boundary-check-v1.json
  status = active
  authority_class = ordinary_analysis
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

A failure means the public page, JavaScript behavior, documentation, activation status, README references, public links, declared task, registry, or fixtures no longer agree on the same execution boundary.

A failed check should be treated as a public-surface drift event. The page should not be advertised as a governed advancement interface until the drift is corrected.
