# Site Mirror Index

## Purpose

This index lists mirror documents that belong to the same ecosystem work surface.

The Site handoff is one indexed mirror source. Other repository handoffs can be added as peer mirror sources when they enter scope.

## Indexed Source Fields

Each source should declare:

```text
mirror_id
repository
mirror_path
source_type
status
priority_class
blocked_by
next_task
verification_surface
```

## Current Index Seed

```text
mirror_id: site-main-handoff
repository: StegVerse-Labs/Site
mirror_path: docs/SITE_MIRROR_HANDOFF.md
source_type: primary_site_handoff
status: active
priority_class: P0
blocked_by: Publisher closure evidence for activation
next_task: keep Site mirror queue, index, and checkers aligned while Publisher evidence remains pending
verification_surface: scripts/check_site_mirror_handoff.py
```

```text
mirror_id: publisher-main-handoff
repository: GCAT-BCAT-Engine/Publisher
mirror_path: docs/PUBLISHER_MIRROR_HANDOFF.md
source_type: companion_publisher_handoff
status: external_required
priority_class: P1
blocked_by: Publisher-side live evidence and closure artifacts
next_task: produce Publisher receipt artifact and closure record
verification_surface: Publisher repository validators
```

## Inclusion Rule

Any repository that contains a mirror handoff, mirror ledger, mirror task tracker, mirror queue, or mirror activation-status file should be added to this index when it enters the same task scope.

## Engine Rule

A mirror-index engine should:

```text
1. Read every indexed mirror source.
2. Preserve each source's repository boundary.
3. Identify blockers and queued tasks per source.
4. Rank unblocked tasks by priority.
5. Select the highest-priority task local to the current surface.
6. Record blocked tasks without overwriting them.
7. Update the relevant mirror handoff or appendix after completing work.
```

## Archive Readiness

This index lets a future runner, agent, or session discover mirror documents from repository artifacts rather than prior chat context.
