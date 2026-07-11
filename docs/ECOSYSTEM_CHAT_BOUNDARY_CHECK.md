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
docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md
docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_contract.py
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
data/headless-task-registry-v1.json
python scripts/check_ecosystem_chat_contract.py
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
Contract check state: installed and aligned with boundary task
Backend gateway state: not installed
Authority-issued receipt state: not installed
```

The verifier also checks that `docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md` keeps the checker-alignment chain:

```text
scripts/check_ecosystem_chat_contract.py -> confirms contract surfaces and boundary-task references
scripts/check_ecosystem_chat_boundary.py -> confirms no-shell/no-credential/authority-required/receipt-required boundary
data/headless-tasks/ecosystem-chat-boundary-check-v1.json -> declares the boundary verifier
data/headless-task-registry-v1.json -> keeps ecosystem-chat-boundary-check-v1 active
```

The verifier also checks that the declared task and registry remain aligned:

```text
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
  task_id = ecosystem-chat-boundary-check-v1
  command = python scripts/check_ecosystem_chat_boundary.py
  authority_class = ordinary_analysis
  expected_inputs include README, page, JavaScript, docs, activation status, fixtures, boundary checker, contract checker, task file, and registry

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

The exact fixture-aligned declarations preserved by this check are:

```text
raw_shell_allowed = false
authority_required = true
rate_limit_required = true
receipt_required_for_execution = true
Restricted admin requests are routed separately and are not available through the public preview.
```

These declarations describe verification requirements only. They do not install a backend, grant execution authority, issue receipts, authorize repository mutation, or enable restricted administration.

## Done condition

The check is passing when the verifier emits JSON with:

```json
{
  "ok": true,
  "boundary": "no-shell/no-credential/authority-required/receipt-required"
}
```

## Failure meaning

A failure means the public page, JavaScript behavior, documentation, activation status, checker-alignment chain, README references, public links, declared task, registry, or fixtures no longer agree on the same execution boundary.

A failed check should be treated as a public-surface drift event. The page should not be advertised as a governed advancement interface until the drift is corrected.
