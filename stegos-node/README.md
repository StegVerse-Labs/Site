# StegOS Node Site Projection

This directory is a Site-hosted projection/carrier for current-device StegOS Node continuity and bootstrap flows. Site does not grant allocator claims, execution authority, credentials, or transition authority.

## Organization allocator execution surfaces

Allocator execution pages are release-immutable. Once an execution URL has been published it is not reused as the canonical continuation surface for later allocator logic changes. A corrected execution release receives a new path.

Current TASK-2026-0010 surfaces:

- `org-allocator-evidence-recovery-task0010-g6-v1.html` — read-only recovery of an already-retained `TASK-2026-0010` same-device allocator execution receipt from the established StegOS node journal. It does not open or mutate the allocator state database.
- `org-allocator-bootstrap-task0010-g6-v2.html` — immutable TASK-2026-0010 execution surface. It checks the established node journal first and exports retained evidence without re-running allocation when TASK-2026-0010 has already executed. Only if no retained execution exists may it run the existing canonical allocator predicates and CAS path.
- `org-allocator-bootstrap-auto.html` — historical mutable auto-execution path retained for provenance/backward compatibility; it must not be treated as the canonical continuation URL after a newer immutable release exists.

TASK-2026-0010 generation/fence 6 is authentic retained provenance. Its pre-KV scoped claim is not widened. The complete KV-gated entry is a distinct successor, TASK-2026-0011.

## TASK-2026-0011 allocator source transport

Canonical `.github` PR #1365 merged the retained-state TASK-0011 allocator extension at `1fe1d041fa87bc00be9bc40703cd14473a7ab02d`. Site projects those source bytes exactly rather than implementing allocator semantics locally.

Exact transport destinations:

```text
stegos-node/org-allocator-portable-task0011.js
stegos-node/org-allocator-current-iphone-package-task0011.json
```

The `TASK-0011 Allocator Source Transport - Evidence Only` workflow downloads only that pinned canonical merge, verifies the exact Git blob identities, and commits the two files to a dedicated Site materialization branch. This is deterministic source/evidence transport only. It does not execute the allocator, reset IndexedDB, select a task, mint a claim/fence, access TV/TVC credentials, or confer runtime authority.

A TASK-0011 execution page will receive its own immutable path and must require already-retained allocator state before invoking the canonical allocator.

The service worker treats current allocator execution/recovery and canonical allocator source/package requests as network-only. Browser document freshness is not identity, continuity, claim, or transition authority.

Authority remains separated: canonical organization allocator/WorkerCoordinator owns claim/fence semantics, Interlock/InTr owns governed transitions, TV/TVC owns credentials/provider operations, HB is observability only, and Site/GitHub Actions are projection/validation/evidence transport only. No Render fallback is used.
