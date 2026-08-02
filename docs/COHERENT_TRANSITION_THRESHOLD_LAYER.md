# Coherent Transition Threshold Layer

## Status

Repository-local machine-observable implementation contract. This layer has no execution, activation, publication, custody, biological, or scientific authority.

## Purpose

The ecosystem heartbeat is already implemented as a transition-driven, health-relative coherence reference. This layer adds the missing threshold distinction between:

1. a cluster of transitions that merely exists;
2. a cluster that exhibits a recurring coordination signal;
3. a cluster whose coordinated transitions preserve the conditions required for another coherent transition cycle.

The third posture is the **coherent transition threshold**. It is a system-state classification, not elapsed time and not proof of biological life.

## Core distinction

A heartbeat-like signal is not time. It is a synchronization reference.

A transition cluster does not cross the threshold merely because:

- transitions are concurrent;
- an oscillator exists;
- a periodic signal is emitted;
- a watchdog remains active;
- components report healthy independently.

The threshold is crossed only when repository evidence establishes all required conditions:

- `transition_cluster_declared`
- `coherence_reference_observed`
- `required_transitions_jointly_ready`
- `continuation_conditions_preserved`
- `coherence_reference_regenerated_or_maintained`
- `next_cycle_admissible`
- `evidence_reconstructable`

## State model

The machine state is one of:

- `UNDECLARED`
- `CLUSTER_DECLARED`
- `SYNCHRONY_OBSERVED`
- `THRESHOLD_CANDIDATE`
- `THRESHOLD_ESTABLISHED`
- `CONTINUITY_DEGRADED`
- `FAILED_CLOSED`

`THRESHOLD_ESTABLISHED` requires every condition above to be true and every evidence reference to resolve to a committed repository location.

## TT / RTG / GTG : ET relationship

- **TT** identifies locally admissible transitions.
- **RTG** identifies relational correspondence and required coordination among transitions.
- **GTG** identifies traversable propagation structure through the relevant intersections.
- **ET** is the transition that actually propagates through that structure.
- **Heartbeat** is the coherence reference used to determine whether the required ET cluster is jointly ready for continuation.
- **Threshold event** is the first validated system transition from synchronized activity to recursively sustained coherent continuity.

The threshold layer does not redefine these formalisms. It records whether their required system-level closure has been established for a declared implementation.

## Non-manufacture rule

No resulting state may manufacture the synchronization medium, evidence, or continuation conditions through which it claims to have crossed the threshold.

All evidence must pre-exist the threshold determination or be emitted atomically by the validated transition that establishes it.

## Machine-owned task

Task ID: `SITE-0001-COHERENT-TRANSITION-THRESHOLD`

Task object:

`data/tasks/SITE-0001-COHERENT-TRANSITION-THRESHOLD.json`

Implementation:

- `data/coherent-transition-threshold.schema.json`
- `data/coherent-transition-threshold-state.json`
- `scripts/check_coherent_transition_threshold.py`

Verification:

- `.github/workflows/coherent-transition-threshold.yml`

External tasks, session ownership, and manual completion are prohibited. The validator derives the status from committed state and fails closed when evidence is absent or contradictory.
