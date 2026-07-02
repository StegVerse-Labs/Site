# Site Mirror Orchestration

## Purpose

This page defines the Site mirror orchestration layer for public documentation surfaces that depend on upstream repository handoffs, validation receipts, release references, and deployment checks.

The Site should act as a public coordination and navigation layer. It should not become the source of runtime authority for upstream repositories.

## Source Priority

When a Site mirror task starts, use this source order:

1. target repository `*_MIRROR_HANDOFF.md`;
2. source repository handoff;
3. source repository validation receipt;
4. source public documentation page;
5. source release or tag metadata;
6. Site local plan;
7. prior conversation context.

Conversation context is never the first source of truth.

## Mirror Lifecycle

```text
DISCOVER_HANDOFFS
-> READ_SOURCE_STATUS
-> BUILD_DEPENDENCY_PLAN
-> CHECK_RELEASE_GATES
-> INSTALL_PUBLIC_SUMMARY
-> UPDATE_NAVIGATION
-> RUN_LOCAL_VALIDATION
-> VERIFY_PUBLIC_DEPLOYMENT
-> RECORD_ARCHIVE_READY
```

## Current Mirror Workstreams

| Workstream | Status | Gate |
| --- | --- | --- |
| Governed LLM demo mirror | Existing handoff active | Runtime and SDK handoffs |
| Repo standards public summary | Prepared | repo-standards release and admissibility-wiki validation |

## Boundary

The Site mirror may publish summaries, links, readiness states, and public navigation.

The Site mirror must not claim:

- execution authority;
- runtime standing;
- repository admissibility;
- release authority for another repository;
- source-of-truth priority over the source repository handoff.

## Current Result

```text
SITE_MIRROR_ORCHESTRATION_PREPARED
```
