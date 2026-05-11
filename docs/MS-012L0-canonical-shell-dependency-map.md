# MS-012L.0 Canonical Shell Dependency Map

## Purpose

This artifact resets the repo state into a canonical shell/dependency model.

It does not modify workflows.
It does not modify tools.
It does not claim blocked transitions are executable.

## Core correction

```text
Shells do not complete independently.
Transitions may be discovered out of shell order.
Discovery order is not execution authority order.
A transition may not execute until its dependency closure is satisfied.
```

## Roles

```text
Shells:
  organize authority surfaces

Transitions:
  connect authority surfaces

StegDB:
  records the canonical dependency graph

Receipts:
  prove state changes inside the graph
```

## Key invariant

```text
Authority cannot emerge from an unmapped surface.
A mapped surface cannot exceed its declared scope.
```

## Current blocked transitions

```text
T13:
  data-defined transition authority discovery
  discovered but blocked

T14:
  approved privileged install candidate
  discovered but blocked

MS-012K.6:
  manifest post-install task bridge
  blocked by tool edge
```

## Why blocked

```text
The current ingestion tool does not interpret data-defined transition-state rules.
The current ingestion tool treats already_failed as stale before evaluating approval transition state.
The current workflow does not expose retry_failed or maintenance transition input.
```

## Valid next actions

```text
record canonical dependency
record blocked state
map dependency closure
do not retry blocked engine mutations as ordinary bundles
do not use fresh-hash carriers as claimed transition solutions
```

## Files

```text
data/canonical/shells-v1.json
data/canonical/execution-surfaces-v1.json
data/canonical/transition-dependency-graph-v1.json
data/canonical/blocked-transitions-v1.json
data/transition-table/execution-surface-transition-blocks-v1.json
```
