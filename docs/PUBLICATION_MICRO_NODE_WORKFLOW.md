# Publication Micro-Node Workflow

## Purpose

This document defines the first reference workflow class for release-tag-driven publication across Publisher, Site, and wiki surfaces.

The workflow exists so repository releases can be evaluated, confirmed, packetized, published, mirrored, and documented without allowing any single surface to become a competing source of truth.

## Done Definition

This workflow is considered built enough for documentation-level activation when the repository contains:

```text
docs/PUBLICATION_MICRO_NODE_WORKFLOW.md
docs/RELEASE_EVALUATOR_HANDOFF.md
docs/MASTER_RECORDS_PUBLICATION_CONFIRMATION_GATE.md
docs/PUBLICATION_WORKFLOW_PACKET_SCHEMA.md
scripts/check_publication_micro_node_workflow.py
github/workflows/check-publication-micro-node-workflow.yml
```

Note: `github/workflows/...` is displayed without the leading dot. The actual repository path includes the leading dot.

The workflow is considered execution-ready only after a future implementation can produce real node receipts, evaluator receipts, master-records confirmation receipts, publication packets, mirror receipts, and a final workflow receipt.

## Authority Chain

```text
Repository release proposes.
Release Evaluator admits or rejects.
master-records confirms evaluator standing and workflow reconstructability.
Publisher records admitted development state.
Site mirrors public display state.
Wikis explain semantic meaning through generated stubs and governed edits.
```

Publisher must not ingest raw repository releases directly.

Publisher may ingest only evaluator-admitted packets that have master-records confirmation standing.

## Workflow Class

```text
Workflow Class:
A reconstructable sequence of micro-nodes performing a bounded ecosystem function.
```

The first workflow class is:

```text
Publication Workflow Class
```

Its purpose is to transform a release tag into an admitted, confirmed, mirrored, and receipt-bound publication event.

## Reference Flow

```text
Release Tag Created
        ↓
Publication Supervisor Node
        ↓
Release Discovery Node
        ↓
Release Evaluation Node
        ↓
master-records Confirmation Node
        ↓
Packet Construction Node
        ↓
Publisher Update Node
        ↓
Site Mirror Node
        ↓
Wiki Stub Node
        ↓
Receipt Aggregation Node
        ↓
Final Publication Workflow Receipt
```

## Node Boundaries

### Publication Supervisor Node

The supervisor orchestrates the workflow only.

It must not:

```text
evaluate release admissibility
confirm master-record standing
publish canonical state
mirror public state
write semantic wiki meaning as authority
```

It may:

```text
measure incoming release metadata
determine required node sequence
instantiate bounded child nodes
track node lineage
collect receipts
terminate child nodes
emit final workflow receipt
```

### Release Discovery Node

The discovery node reads release metadata and emits a discovery receipt.

Required inputs:

```text
source_repository
release_tag
release_commit_sha
release_url
release_created_at
```

Required outputs:

```text
discovery_receipt_hash
release_hash
source_repository
release_tag
release_commit_sha
```

### Release Evaluation Node

The evaluator decides whether a release is publishable.

Allowed outputs:

```text
ADMIT
DENY
QUARANTINE
```

The evaluator may not publish.

The evaluator may not bypass master-records confirmation.

### master-records Confirmation Node

The confirmation node verifies evaluator standing and workflow reconstructability.

Allowed outputs:

```text
CONFIRMED
UNCONFIRMED
MISSING
CONTRADICTED
STALE
```

Only `CONFIRMED` permits publication packet construction.

### Packet Construction Node

The packet node constructs the canonical development packet from evaluator and master-records confirmed inputs.

It must preserve:

```text
source_repository
release_tag
release_commit_sha
evaluator_decision
evaluator_receipt_hash
master_records_confirmation
master_records_receipt_hash
affected_surfaces
glossary_terms
publication_status
```

### Publisher Update Node

The Publisher node records the admitted development packet.

It must not infer missing meaning.

It must not mark activation complete without the required confirmation receipts.

### Site Mirror Node

The Site node mirrors the Publisher-confirmed public state.

It must preserve the existing Site rule:

```text
Site is display.
Publisher is source of truth.
master-records confirms standing.
```

### Wiki Stub Node

The wiki node generates update stubs for governed review.

It may generate:

```text
new vocabulary stubs
changed concept stubs
affected transition table stubs
guardian behavior stubs
micro-node lifecycle stubs
```

It must not silently overwrite governed semantic meaning.

### Receipt Aggregation Node

The aggregation node collects all workflow receipts and emits the final publication workflow receipt.

## Publication Standing

Publication standing exists only when all are true:

```text
release_discovered = true
evaluator_decision = ADMIT
master_records_confirmation = CONFIRMED
packet_constructed = true
publisher_update_ready = true
mirror_targets_declared = true
workflow_receipt_emitted = true
```

If any required condition is false, the workflow status is not publishable.

## Failure States

```text
DENY = release evaluated and rejected
QUARANTINE = release requires review before publication
UNCONFIRMED = evaluator or workflow standing could not be confirmed
MISSING = required evidence is absent
CONTRADICTED = packet conflicts with canonical state
STALE = evidence is no longer sufficient at confirmation time
```

None of these states should be described as completed publication.

## Micro-Node Receipt Requirements

Every node must emit:

```text
node_type
node_instance_id
parent_workflow_id
created_at
destroyed_at
input_hash
output_hash
decision
receipt_hash
```

The final workflow receipt must include:

```text
workflow_id
workflow_class
source_repository
release_tag
release_commit_sha
node_lineage
receipt_chain
final_publication_status
```

## Current Status

```text
Status: documentation_reference_built
Execution status: not_yet_implemented
Activation status: not_publishable_without_master_records_confirmation
```

## Archive Readiness

This document is sufficient to preserve the publication micro-node workflow concept without relying on prior chat context.
