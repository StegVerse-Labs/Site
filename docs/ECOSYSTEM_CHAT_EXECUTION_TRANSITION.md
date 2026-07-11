# Ecosystem Chat Execution Transition Preview

## Status

```text
mode: dry-run preview
authority input: ALLOW
authority scope: ecosystem_chat.gateway.evaluate
authority sufficient for execution: false
execution result: DRY_RUN_ONLY
state changed: false
provider invoked: false
solver executed: false
repository mutated: false
raw shell used: false
receipts issued by Site: false
```

## Purpose

This contract proves that a valid authority result may be consumed as an input without collapsing authority into execution. Commit-time revalidation still occurs, execution remains disabled, resource use remains zero, recoverability remains available, and Site does not issue governing receipts.

## Fixtures

```text
fixtures/ecosystem-chat/execution-transition-request.example.json
fixtures/ecosystem-chat/execution-transition-response.example.json
```

## Commit-time revalidation

The request requires revalidation of:

- identity
- delegation
- policy
- evidence freshness
- operation allowlist
- resource limits

The response records a passing revalidation result, but this does not activate execution.

## Recoverability posture

The dry-run contract requires:

- pre-state capture and preservation
- rollback availability
- operator interrupt support
- no post-state creation
- no rollback performance when no state changed

## Receipt boundary

Authority and execution receipts remain required from `governed_backend_authority`. Site may not issue either receipt, and fixture receipt identifiers remain null.

## Validator

```text
python scripts/check_ecosystem_chat_execution_transition.py
```

The validator is included in:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Activation boundary

A future live execution transition must independently revalidate standing at commit time, enforce operation and resource bounds, preserve interruption and rollback posture, record actual resource use and state change, and receive a governing backend execution receipt. A prior authority `ALLOW` is an input—not execution standing by itself.
