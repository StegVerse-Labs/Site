# Ecosystem Chat Solver Response Preview

## Status

```text
mode: fixture-bound preview
live solver execution: false
authority: none
execution: disabled
Site-issued receipt: false
independent verification engine: false
```

## Purpose

This surface demonstrates how a governed solver result should expose the original expression, operation class, answer, units, proof steps, verification method, resource limits, and confidence posture before any live solver is connected.

It is not a live calculation service and must not be represented as authority, execution, independent verification, or receipt issuance.

## Fixture

```text
fixtures/ecosystem-chat/solver-response.example.json
```

The fixture is required to declare:

- `preview_only=true`
- `live_solver_execution=false`
- `authority_granted=false`
- `execution_enabled=false`
- `receipt_issued_by_site=false`
- sequential proof steps
- explicit units posture
- verification method and equality check
- `independent_engine=false`
- operation allowlist posture
- resource limits and steps used

## Renderer

```text
assets/ecosystem-chat-solver.js
```

The renderer self-mounts before the chat console, validates the fixture, rejects failed verification, rejects resource-limit violations, and fails closed when the fixture is unavailable or incomplete.

## Validator

```text
python scripts/check_ecosystem_chat_solver_response.py
```

The validator is included in:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Live integration boundary

A future live solver must require:

- bounded operation allowlist
- resource and recursion limits
- explicit unit handling
- deterministic proof-step output where applicable
- result verification
- independent verification posture when available
- authority handshake before any downstream execution
- receipt issuance by the governing backend, not Site

A correct mathematical answer does not itself grant authority to act on that answer.
