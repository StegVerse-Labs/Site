# MS-012L.2 Transition Dependency Closure Model

## Purpose

This artifact defines how a discovered transition becomes executable.

It does not modify workflows.
It does not modify tools.
It does not make blocked transitions executable.

## Core rule

```text
A transition may be discovered before it is executable,
but it may not execute until dependency closure is proven.
```

## Closure axes

```text
shell_closure:
  required shells exist and are known

surface_closure:
  required workflow/tool/data/capability surfaces are canonical

receipt_closure:
  required receipts exist or can be emitted

evidence_closure:
  observed evidence supports the claimed state

authority_closure:
  action remains within declared mapped surface scope
```

## Execution state rule

```text
executable requires:
  shell_closure = closed
  surface_closure = closed
  receipt_closure = closed
  evidence_closure = closed
  authority_closure = closed
```

Anything else is:

```text
non_executable
blocked
executable_partial
terminal_rejected
terminal_invalid
```

## Current important states

```text
T13:
  discovered
  blocked
  reason: bundle_ingest does not interpret data-defined transition-state rules

T14:
  discovered
  blocked
  reason: approval transition exists conceptually but dependency closure is incomplete

T20:
  discovered
  executable_receipts_only
  reason: vaulted capability gate can emit non-secret receipts only
```

## Files

```text
data/transition-table/transition-dependency-closure-model-v1.json
data/canonical/transition-record-schema-v1.json
data/canonical/transition-dependency-closure-status-v1.json
data/canonical/dependency-closure-receipt-schema-v1.json
```
