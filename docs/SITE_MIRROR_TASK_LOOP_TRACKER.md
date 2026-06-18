# Site Mirror Task Loop Tracker

## Purpose

This tracker defines how mirror work continues without relying on a fresh ChatGPT instruction.

## Core Rule

A declared task starts the loop only when the tracker is committed with a current task below 100 percent complete.

When the current task reaches 100 percent, the next loop begins only if the tracker promotes another queued task and resets the new current task below 100 percent.

If no queued task exists, the tracker records that no queued task exists and stops.

## Current Task

```text
task_id: site-mirror-task-loop-tracker
task_title: Define task-loop tracker semantics
percent_complete: 40
state: active_task
```

## Queue

```text
1. publisher-site-live-evidence-collection
2. publisher-closure-finalization
```

## Loop Contract

```text
1. Current task must be less than 100 percent while active.
2. A completed task must not remain current if another queued task exists.
3. The next queued task must become current before the next build loop starts.
4. The new current task must restart below 100 percent.
5. The tracker must preserve the Publisher closure boundary.
```

## Completion Condition

This packet is valid when a checker confirms the current task, percent complete value, queue state, and continuation rule.

## Archive Readiness

This file lets a future runner, agent, or session determine the next mirror-loop task without needing the prior chat thread.
