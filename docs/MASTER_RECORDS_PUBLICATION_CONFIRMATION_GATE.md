# master-records Publication Confirmation Gate

## Purpose

This gate defines when evaluator output has enough standing to be published.

master-records does not replace the evaluator. master-records confirms that the evaluator and workflow can be reconstructed with continuity before Publisher records the development state.

## Done Definition

This gate is complete when it defines:

```text
confirmation inputs
confirmation checks
allowed confirmation states
Publisher blocking states
workflow reconstructability requirements
```

## Confirmation Principle

```text
Evaluator approval is not publication standing.
Publication standing requires evaluator admission plus master-records confirmation.
```

## Required Inputs

```text
source_repository
release_tag
release_commit_sha
discovery_receipt_hash
evaluator_id
evaluator_version
evaluator_decision
evaluator_receipt_hash
evaluator_authority_reference
candidate_packet_hash
node_lineage_hash
```

## Confirmation Checks

master-records must verify:

```text
the evaluator is recognized
the evaluator has authority for this release family
the evaluator receipt is hash-bound to the release
the release commit hash matches the candidate packet
the packet can be reconstructed from declared inputs
the node lineage can be reconstructed
the packet does not contradict current canonical state
the affected surfaces are declared
the activation status is evidence-bound
```

## Allowed Confirmation States

```text
CONFIRMED
UNCONFIRMED
MISSING
CONTRADICTED
STALE
```

## State Meanings

### CONFIRMED

The evaluator output and workflow lineage have standing for Publisher ingestion.

### UNCONFIRMED

master-records cannot confirm evaluator standing or workflow standing.

### MISSING

Required evidence or receipt references are absent.

### CONTRADICTED

The candidate packet conflicts with existing canonical state.

### STALE

Evidence exists but is no longer sufficient at confirmation time.

## Publisher Blocking Rule

Publisher must not publish when master-records emits:

```text
UNCONFIRMED
MISSING
CONTRADICTED
STALE
```

Publisher may publish only when master-records emits:

```text
CONFIRMED
```

and the evaluator decision is:

```text
ADMIT
```

## Workflow-Level Confirmation

master-records should confirm the workflow, not only the evaluator.

The confirmation question is not only:

```text
Was the evaluator valid?
```

The confirmation question is:

```text
Was the entire publication workflow reconstructable at confirmation time?
```

Required workflow evidence:

```text
release discovery receipt
evaluator receipt
master-records confirmation receipt
candidate packet receipt
publisher update receipt
site mirror receipt
wiki stub receipt
receipt aggregation receipt
final workflow receipt
```

During the early documentation phase, downstream receipts may be declared as pending. Pending downstream receipts prevent activation claims but do not invalidate the handoff documentation.

## Confirmation Receipt Fields

```text
confirmation_node_id
confirmation_version
source_repository
release_tag
release_commit_sha
evaluator_id
evaluator_receipt_hash
candidate_packet_hash
node_lineage_hash
confirmation_state
confirmation_reason
canonical_state_reference
input_hash
output_hash
receipt_hash
created_at
```

## Current Status

```text
Status: confirmation_gate_defined
Execution status: not_yet_implemented
Publication status: blocked_without_confirmed_receipt
```

## Archive Readiness

This gate preserves the master-records confirmation requirement without relying on prior chat context.
