# Site Mirror Priority Queue

## Purpose

This packet defines how Site mirror orchestration chooses the next task from all tasks currently in scope.

The queue is priority-dependent. A task does not become next merely because it was mentioned first. A task becomes next because it has the strongest admissible priority after blockers, dependencies, and verification state are considered.

## Queue Inputs

A task may enter the queue from:

```text
mirror handoff
activation ledger
evidence requirements
evidence transition rules
activation status
closure guard
workflow failures
new repository mirror docs
human-authored task declaration
agent-authored task declaration
```

## Task Record Fields

Every queued task should declare:

```text
task_id
title
repository
source_packet
priority_class
blocked_by
completion_evidence
verification_command
percent_complete
state
```

## Priority Classes

```text
P0: prevents false activation, authority drift, or invalid completion claims
P1: blocks current mirror activation goal
P2: improves verification, handoff quality, or queue continuity
P3: improves documentation, clarity, or future automation
```

## Selection Rule

The next task is the highest-priority unblocked task whose required authority boundary is local to this repository.

If the highest-priority task is blocked by another repository, evidence artifact, or external closure condition, the queue must preserve that task as blocked and select the next unblocked local task.

## Completion Verification Rule

A queued task is complete only when:

```text
1. The declared artifact exists.
2. The declared checker exists if the task requires enforcement.
3. The declared checker passes or the handoff records why it is pending.
4. The handoff or tracker records the completed task.
5. The next queued task is promoted if any unblocked task remains.
```

## Current Queue Seed

```text
P0: preserve Publisher activation boundary
P0: prevent evidence transition beyond pending without governed closure evidence
P1: collect actual Publisher receipt artifact
P1: collect actual Site evidence artifact
P1: collect Publisher closure receipt
P1: update Publisher verification tracker after closure
P1: update Publisher activation status after closure
P2: add executable priority queue checker
P2: promote next queued task after current task reaches 100 percent
```

## Non-Activation Rule

Queue progress does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Archive Readiness

This packet lets a future runner, agent, or session determine task order from declared queue priority rather than from prior chat context.
