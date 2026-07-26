# Ecosystem Heartbeat Orchestration

## Purpose

The ecosystem heartbeat is a governed continuity signal produced by admitted orchestration transitions. It is not defined by a fixed wall-clock interval.

The live working state is both a receiver and transmitter of heartbeat data. It receives accepted workflow transitions, recomputes repository health and task succession, and exposes the resulting state to other sessions, workflows, and dependent repositories.

## Mandatory session entry

Every session touching this repository must:

1. Read `docs/SITE_MIRROR_HANDOFF.md`.
2. Invoke `scripts/site_handoff_orchestrator.py`.
3. Read `data/ecosystem-heartbeat-state.json`.
4. Treat the incoming request as a candidate workload rather than automatic execution authority.
5. Join the active task sequence only when the workload is `PARALLEL_SAFE`.
6. Queue `EXCLUSIVE` work until the current sequence states `end of current work task sequence ####, no tasks running`.
7. Preserve the first exact blocker or validation failure.
8. Update handoff, orchestration, and heartbeat state before relinquishing ownership.

## Heartbeat production

The following admitted transitions advance repository heartbeat state:

- task admitted;
- ownership acquired or transferred;
- dependency satisfied;
- artifact produced;
- validation passed or failed;
- custody or reconstruction receipt accepted;
- handoff updated;
- task completed, blocked, recovered, or abandoned;
- task sequence opened or closed.

A watchdog observation may prove liveness but must have `progress_effect: false`. Time detects silence; it does not manufacture progress.

## Health-relative interpretation

Heartbeat meaning is relative to system health and expected activity.

- `HEALTHY_IDLE`: no work is expected and no task is running.
- `HEALTHY_ACTIVE`: admitted work is progressing.
- `HEALTHY_BLOCKED`: orchestration is functioning and a declared dependency prevents progress.
- `DEGRADED`: expected transitions are absent, validation is failing, or ownership is stale.
- `PARTITIONED`: required repositories or services cannot exchange continuity state.
- `CRITICAL`: orchestration continuity or state integrity cannot be established.

A missing work heartbeat is significant only when the health model establishes that progress was expected.

## Task execution classes

- `PARALLEL_SAFE`: may run within the active sequence when paths, issues, PRs, state files, and dependencies do not conflict.
- `EXCLUSIVE`: requires the prior sequence to close with no tasks running.
- `DEPENDENCY_BLOCKED`: cannot run until its declared prerequisite emits an accepted completion transition.

Handoff, orchestration-state, release, activation, and repository-wide reconciliation writes are exclusive unless a narrower governed rule explicitly proves safety.

## HIL priority

The first seamless HIL user experience is the highest-priority exclusive integration sequence:

1. authorized persistent provider endpoint;
2. one real governed request;
3. exact response and usage persistence;
4. transition and usage custody;
5. reconstruction PASS for both chains;
6. immutable zero-blocker receipt;
7. automatic Site import;
8. synchronized Conversation, Governed Record, and Split rendering;
9. one simple invited-test entry surface;
10. user-observed outcome receipt.

Heartbeat implementation observes and coordinates this vertical slice. The vertical slice does not wait for ecosystem-wide heartbeat migration.

## Authority boundary

Heartbeat != progress unless bound to an admitted transition.
Watchdog != work heartbeat.
Repository heartbeat != ecosystem execution authority.
Sequence completion != activation.
Health classification != admissibility.
Live working state != custody.
