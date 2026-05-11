# MS-012L.1 Transition Table Self-Correction Ledger

## Purpose

This artifact defines how the transition table absorbs mistakes, failed attempts, blocked routes, and contradictory evidence.

It does not modify workflows.
It does not modify tools.
It does not make blocked transitions executable.

## Core rule

```text
Mistakes may reveal real boundaries.
They must not silently become authority.
```

## Discovery is not execution

```text
discovery_state:
  unknown / suspected / discovered / validated / deprecated

execution_state:
  non_executable / blocked / executable_partial / executable / terminal_success / terminal_rejected / terminal_invalid
```

A transition can be discovered before it can execute.

## Correction loop

```text
propose transition
→ attempt or observe
→ collect receipt
→ classify result
→ update dependency graph
→ refine transition table
```

## Forbidden correction patterns

```text
Treating repeated upload as new authority.
Using fresh hash as a substitute for dependency closure.
Claiming execution state from discovery state.
Adding guardrails outside the transition model.
Allowing a path class to grant authority by itself.
Treating workflow/tool mutation as ordinary data evolution.
Ignoring receipts that contradict the proposed transition.
```

## Recorded corrections

```text
MS-012K.6:
  discovered but blocked by tool edge

T13:
  data-defined transition authority discovered but blocked because bundle_ingest does not consume that rule data

T14:
  approved privileged install candidate discovered but blocked because current ingestion sees already_failed before approval state
```

## Files

```text
data/transition-table/transition-table-self-correction-model-v1.json
data/canonical/transition-correction-ledger-v1.json
data/canonical/transition-evidence-schema-v1.json
data/canonical/transition-status-index-v1.json
```
