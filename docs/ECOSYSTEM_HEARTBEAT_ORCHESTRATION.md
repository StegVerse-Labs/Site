# Ecosystem Heartbeat Orchestration

## Purpose

The canonical StegVerse protocol heartbeat is a **continuous 100 Hz carrier/reference** derived from the durable HB32 protocol anchor. A new heartbeat reference exists every 10 ms by elapsed oscillator phase, independent of repository activity, workers, workflows, observations, or process liveness.

This Site document governs a separate mechanism: **transition-driven repository/workload health orchestration**. Historical Site fields named `ecosystem_heartbeat` and `repository_heartbeat` are workload-health counters, not canonical heartbeat epochs.

The ecosystem heartbeat is a governed continuity signal produced by admitted orchestration transitions **only in this narrower Site workload-health sense**. It is not defined by a fixed wall-clock interval and it does not replace, drive, suppress, or advance the canonical 10 ms protocol heartbeat.

The live working state is both a receiver and transmitter of heartbeat data in the workload-health sense. It receives accepted workflow transitions, recomputes repository health and task succession, and exposes the resulting state to other sessions, workflows, and dependent repositories.

## Canonical protocol heartbeat boundary

```text
anchor: HB32 @ 2026-08-23T19:00:00.000Z
period: 10 ms
rate: 100 Hz
progression_dependency: OSCILLATOR_ONLY
continuous_process_required: false
resident_sampler_required_for_progression: false
observation_is_causal: false
LIVE-009: COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
authority_effect: NONE
```

For the same timestamp, conforming observers derive the same protocol reference. Missed references still existed. Site orchestration transitions may observe or correlate with protocol references but cannot cause them.

## Mandatory session entry

Every session touching this repository must:

1. Read `docs/SITE_MIRROR_HANDOFF.md`.
2. Invoke `scripts/site_handoff_orchestrator.py`.
3. Read `data/ecosystem-heartbeat-state.json`.
4. Treat the incoming request as a candidate workload rather than automatic execution authority.
5. Join the active task sequence only when the workload is `PARALLEL_SAFE`.
6. Queue `EXCLUSIVE` work until the current sequence states `end of current work task sequence ####, no tasks running`.
7. Preserve the first exact blocker or validation failure.
8. Update handoff, orchestration, and workload-health state before relinquishing ownership.

## Workload-health transition production

The following admitted transitions advance Site repository workload-health counters:

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

None of these events creates a protocol heartbeat reference. Protocol references continue every 10 ms whether or not any Site transition occurs.

## Health-relative interpretation

Workload-health meaning is relative to system health and expected activity.

- `HEALTHY_IDLE`: no work is expected and no task is running.
- `HEALTHY_ACTIVE`: admitted work is progressing.
- `HEALTHY_BLOCKED`: orchestration is functioning and a declared dependency prevents progress.
- `DEGRADED`: expected transitions are absent, validation is failing, or ownership is stale.
- `PARTITIONED`: required repositories or services cannot exchange continuity state.
- `CRITICAL`: orchestration continuity or state integrity cannot be established.

A missing work heartbeat is significant only when the health model establishes that progress was expected. A missing Site workload transition never means the canonical 100 Hz heartbeat stopped.

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

Heartbeat implementation observes and coordinates this vertical slice. The vertical slice does not wait for ecosystem-wide heartbeat migration. The canonical protocol heartbeat also does not grant or gate HIL execution authority.

## Authority boundary

Protocol heartbeat reference != progress.
Heartbeat != progress unless bound to an admitted transition in the narrower Site workload-health model.
Watchdog != work heartbeat.
Repository heartbeat != canonical HB protocol epoch.
Repository heartbeat != ecosystem execution authority.
Sequence completion != activation.
Health classification != admissibility.
Live working state != custody.
Protocol heartbeat != execution, activation, publication, custody, release, route, credential, or Guardian authority.
