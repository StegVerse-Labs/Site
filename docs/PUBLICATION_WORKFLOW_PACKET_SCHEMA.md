# Publication Workflow Packet Schema

## Purpose

This document defines the canonical packet shape for the publication micro-node workflow.

The packet is the only object Publisher may ingest after release evaluation and master-records confirmation.

## Done Definition

The schema is complete when it defines:

```text
packet identity
release identity
evaluator result
master-records confirmation
surface routing
node lineage
receipt chain
publication status
activation boundary
```

## Canonical Packet Shape

```json
{
  "packet_schema": "publication-workflow-packet/v0.1",
  "workflow_class": "Publication Workflow Class",
  "workflow_id": "publication-workflow-<release-tag>-<hash>",
  "publication_status": "not_publishable_until_confirmed",
  "source": {
    "source_repository": "owner/repo",
    "release_tag": "dev/example-v0.1",
    "release_commit_sha": "<sha>",
    "release_url": "<url>",
    "release_created_at": "<timestamp>"
  },
  "discovery": {
    "node_type": "release_discovery",
    "decision": "DISCOVERED",
    "receipt_hash": "<hash>"
  },
  "evaluation": {
    "node_type": "release_evaluation",
    "evaluator_id": "<id>",
    "evaluator_version": "<version>",
    "decision": "ADMIT|DENY|QUARANTINE",
    "decision_reason": "<reason>",
    "receipt_hash": "<hash>"
  },
  "master_records_confirmation": {
    "node_type": "master_records_confirmation",
    "confirmation_state": "CONFIRMED|UNCONFIRMED|MISSING|CONTRADICTED|STALE",
    "confirmation_reason": "<reason>",
    "receipt_hash": "<hash>"
  },
  "affected_surfaces": {
    "publisher": [],
    "site": [],
    "admissibility_wiki": [],
    "stegguardian_wiki": []
  },
  "glossary_terms": [],
  "node_lineage": [
    {
      "node_type": "publication_supervisor",
      "node_instance_id": "<id>",
      "created_at": "<timestamp>",
      "destroyed_at": "<timestamp>",
      "receipt_hash": "<hash>"
    }
  ],
  "receipt_chain": [],
  "activation_boundary": {
    "site_is_display": true,
    "publisher_is_source_of_truth": true,
    "master_records_confirmation_required": true,
    "raw_release_publishable": false
  },
  "final_workflow_receipt_hash": "<hash>"
}
```

## Publication Status Values

```text
not_publishable_until_confirmed
publishable
published
mirrored
quarantined
denied
stale
contradicted
missing_evidence
```

## Publishable Rule

A packet may become `publishable` only when:

```text
evaluation.decision = ADMIT
master_records_confirmation.confirmation_state = CONFIRMED
activation_boundary.master_records_confirmation_required = true
activation_boundary.raw_release_publishable = false
final_workflow_receipt_hash is present
```

## Non-Publishable Rule

A packet must remain non-publishable when any of these are true:

```text
evaluation.decision != ADMIT
master_records_confirmation.confirmation_state != CONFIRMED
final_workflow_receipt_hash is missing
raw release is attempting to bypass evaluator
Publisher is attempting to bypass master-records
Site is attempting to claim source-of-truth authority
wiki stub is attempting to overwrite governed semantic meaning without review
```

## Affected Surface Routing

The packet may declare affected surfaces but must not require every surface to update.

Common affected surface entries:

```text
publisher/development-index
publisher/release-status
site/development-status
site/architecture
site/mirror-handoff
admissibility-wiki/execution-admissibility
admissibility-wiki/node-lifecycle-admissibility
stegguardian-wiki/micro-node-vocabulary
stegguardian-wiki/profile-capability-governance
```

## Current Development Packet Template

```json
{
  "packet_schema": "publication-workflow-packet/v0.1",
  "workflow_class": "Publication Workflow Class",
  "publication_status": "not_publishable_until_confirmed",
  "title": "Ingestion, Sandbox, SV-002, and Micro-Node Architecture Update",
  "summary": "Documents StegVerse-org demo upgrades, ingestion engine guidance, sandbox role guidance, StegVerse-002 new repos, and micro-node vocabulary as a coordinated development update.",
  "affected_surfaces": {
    "publisher": ["development-index", "release-status"],
    "site": ["development-status", "architecture", "mirror-handoff"],
    "admissibility_wiki": ["execution-admissibility", "node-lifecycle-admissibility"],
    "stegguardian_wiki": ["micro-node-vocabulary", "profile-capability-governance"]
  },
  "glossary_terms": [
    "Org Ingestion Engine",
    "Repo Ingestion Engine",
    "Destination Repository",
    "Sandbox",
    "Governance Vector",
    "Micro-Node",
    "Publication Supervisor",
    "Node Creation Receipt",
    "Node Destruction Receipt",
    "Node Lineage",
    "Publication Workflow Class"
  ]
}
```

## Current Status

```text
Status: packet_schema_defined
Execution status: not_yet_implemented
Publisher ingestion status: schema_requires_master_records_confirmation
```

## Archive Readiness

This schema preserves the packet shape for future automation without relying on prior chat context.
