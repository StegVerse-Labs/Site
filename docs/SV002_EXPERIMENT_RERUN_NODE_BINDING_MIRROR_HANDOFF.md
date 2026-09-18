# SV002 Experiment Rerun Node Binding Mirror Handoff

Status: ACTIVE
Updated: 2026-09-17
Repository: StegVerse-Labs/Site

## Canonical coordination
- Goal Task ID: `STEGVERSE-002-EXPERIMENT-RERUN-001`
- COSV: `50000000107000`
- Canonical registry: `StegVerse-Labs/.github/data/canonical-task-records/STEGVERSE-002-EXPERIMENT-RERUN-001.json`
- Root experiment: `STEGVERSE-002-SELF-CHARACTERIZATION-001`
- Tracking issue: `StegVerse-Labs/.github#2070`
- Canonical InTr profile owner: `StegVerse-Labs/StegOS` merge `fd7d2837d9b8f054f2fcf530a3c8264f3231d560`
- Target organization execution owner: `StegVerse-002/.github`

## Purpose
Bind exactly one deterministic existing SDK `REQUEST_SELF_CHARACTERIZATION` request to the registered StegVerseNode write-once InTr outbox using the canonical `sv002-self-characterization` profile. Site is only the same-device request projection. It does not execute the principal, mint a WorkerCoordinator claim/fence, open a runtime lease, create a listener, or grant transition/credential authority.

## Exact request identity
- request schema: `stegverse.external_organization.interlock_request.v1`
- request class: `EXTERNAL_ORGANIZATION_INTERACTION`
- operation: `REQUEST_SELF_CHARACTERIZATION`
- manifest id: `SDK-SV002-FIRST-SELF-CHARACTERIZATION-001`
- experiment id: `STEGVERSE-002-SELF-CHARACTERIZATION-001`
- source organization id: `StegVerse-SDK-Evaluator`
- target entity: `StegVerse-002`
- Goal: `STEGVERSE-002-EXPERIMENT-RERUN-001`
- COSV: `50000000107000`
- invocation count: `1`

## Runtime evidence boundary
A successful write-once Node queue operation may retain request-binding evidence on the current device. Source/CI/merge alone is not `REQUEST_BOUND`. Authentic promotion requires a current-device retained Node receipt/outbox identity that hashes the exact request and correlates the exact Goal/COSV/invocation count.

Downstream predicates remain unproven until separately observed:
`INTR_MATERIALIZATION_ADMITTED`, lease, runtime identity, WorkerCoordinator claim/fence, target-org ingress, T0, v0.3 principal transitions, egress/return, Master Records custody/reconstruction, and origin-return.

## Invariants
No new runtime, scheduler, host, Healer dependency, corpus prerequisite, alternate authority path, second user-operated device, or browser observation-principal substitution is permitted.

## Manual work
None.
