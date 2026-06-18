# Site Mirror Handoff Appendix — Priority Queue

## Purpose

This appendix extends `docs/SITE_MIRROR_HANDOFF.md` with priority-based orchestration rules.

## Added Packets

```text
docs/SITE_MIRROR_PRIORITY_QUEUE.md
docs/SITE_MIRROR_TASK_COMPLETION_VERIFICATION.md
docs/SITE_MIRROR_TASK_LOOP_TRACKER.md
```

## Queue Rule

The mirror loop should select the next task from all tasks currently in scope by priority, blocker state, authority boundary, and verification status.

## Completion Rule

A task is complete only when its declared completion evidence exists and verification is recorded.

## Current Priority Model

```text
P0: prevent false activation, authority drift, or invalid completion claims
P1: unblock current mirror activation goal
P2: improve verification, handoff quality, or queue continuity
P3: improve documentation, clarity, or future automation
```

## Current Continuation Candidate

```text
P2: add executable priority queue checker
```

This is lower priority than live Publisher/Site evidence tasks, but those are currently blocked by external evidence and Publisher closure authority.

## Archive Readiness

This appendix lets a future runner, agent, or session continue from priority-ranked task scope without needing prior chat context.
