# Release Evaluator Handoff

## Purpose

This handoff defines the boundary between a repository release and Publisher ingestion.

Publisher must not evaluate raw releases directly. A release must first pass through a release evaluator and then receive master-records confirmation before Publisher may record the development state.

## Done Definition

This handoff is complete when it defines:

```text
release inputs
evaluator responsibilities
evaluator prohibited behavior
evaluator outputs
master-records confirmation dependency
Publisher ingestion rule
quarantine rule
```

## Input Trigger

The initial trigger is a repository tag or release.

Recommended tag families:

```text
dev/<name>-v<version>
proof/<name>-v<version>
activation/<name>-v<version>
```

Examples:

```text
dev/ingestion-sandbox-micronodes-v0.1
proof/stale-state-minimal-path-v0.1
activation/core-lite-intake-m10
```

## Required Release Inputs

```text
source_repository
release_tag
release_commit_sha
release_url
release_created_at
release_author
release_notes
changed_paths
artifact_manifest
```

If required release inputs are absent, the evaluator must emit `QUARANTINE` or `DENY`.

## Evaluator Responsibilities

The evaluator must:

```text
read release metadata
verify required release fields
verify artifact manifest presence when required
classify release family
classify affected surfaces
check required receipt references
check whether the release claims activation
emit ADMIT, DENY, or QUARANTINE
emit an evaluator receipt
```

## Evaluator Prohibited Behavior

The evaluator must not:

```text
publish to Publisher
mirror to Site
edit wikis
claim master-records confirmation
invent missing receipts
upgrade activation state without evidence
collapse DENY, QUARANTINE, and UNCONFIRMED into the same state
```

## Evaluator Outputs

Allowed decisions:

```text
ADMIT
DENY
QUARANTINE
```

Required evaluator receipt fields:

```text
evaluator_id
evaluator_version
evaluator_authority_reference
source_repository
release_tag
release_commit_sha
release_family
affected_surfaces
decision
decision_reason
input_hash
output_hash
receipt_hash
created_at
```

## Handoff To master-records

Evaluator output is not publishable by itself.

The evaluator must hand off its receipt to master-records for confirmation.

master-records must confirm:

```text
evaluator identity
evaluator authority
evaluator receipt continuity
release hash continuity
packet reconstruction viability
non-contradiction with prior canonical state
```

## Publisher Ingestion Rule

Publisher may ingest only packets satisfying both conditions:

```text
evaluator_decision = ADMIT
master_records_confirmation = CONFIRMED
```

Any other state is not publishable.

## Quarantine Rule

A release is quarantined when it may be valid but lacks enough standing to publish.

Common quarantine causes:

```text
missing artifact manifest
missing receipt reference
ambiguous affected surfaces
activation claim without evidence
unrecognized evaluator authority
master-records confirmation unavailable
```

Quarantine must preserve evidence for later reconstruction.

## Current Status

```text
Status: handoff_defined
Execution status: not_yet_implemented
Publisher ingestion status: gated_by_master_records_confirmation
```

## Archive Readiness

This handoff preserves the evaluator boundary without relying on prior chat context.
