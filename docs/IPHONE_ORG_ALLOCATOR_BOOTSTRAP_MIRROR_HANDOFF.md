# iPhone Organization Allocator Bootstrap Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Issue: #945
Root goal: `GLOBAL-RUNTIME-EVIDENCE-CLOSURE-001`
Immediate task: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Immediate target: `TASK-2026-0011`

## Purpose

Carry the canonical StegVerse organization allocator on the established current iPhone while preserving retained node/journal state, exact source lineage, and canonical allocation semantics.

Canonical allocator source remains `StegVerse-Labs/.github`; Site is bootstrap/projection transport only. TV/TVC remains credential authority. Interlock/InTr remains transition authority. The established StegOS node journal is retained continuity/evidence, not an alternate allocator.

## Retained lineage

```text
TASK-2026-0007 -> generation/fence 3
TASK-2026-0008 -> generation/fence 4
TASK-2026-0009 -> generation/fence 5
TASK-2026-0010 -> generation/fence 6 (authentic retained evidence recovered; replay PASS)
TASK-2026-0011 -> next eligible successor; fresh allocation required
```

TASK-2026-0010 remains immutable provenance. Its generation-6/fence-6 claim is not reactivated or widened to cover KV-gated files added later in StegOS.

## TASK-2026-0010 observations retained

The first current-iPhone attempt showed an obsolete `g6-auto-20260909-1` wrapper failure requiring exactly one queued successor and performed no mutation. A later immutable G6-v2 observation failed closed when the preview selected TASK-2026-0009. Those observations remain useful evidence of correct fail-closed behavior, but they are superseded as current blockers.

TASK-2026-0010 was subsequently recovered from the retained StegOS node journal with generation 6, fence 6, `ALLOCATION_COMPLETE`, and journal replay `PASS`. No further TASK-0010 allocation attempt is allowed.

## Canonical TASK-2026-0011 source

Canonical source:

```text
StegVerse-Labs/.github/tasks/TASK-2026-0011.json
Git blob: a9f90414e59e308d66faf7ff2d5c31173b1687ca
requested_at: 2026-09-11T01:51:58Z
dependency surface: site:current-iphone-kv-testflight-static-bootstrap
workspace: claim/current-iphone-kv-testflight-static-bootstrap-r1
```

The task explicitly retains TASK-0010 generation-6/fence-6 as predecessor provenance and forbids retroactive scope widening.

## TASK-2026-0011 fresh current-iPhone allocator delivery

Pre-work coordination claim:

```text
claim: SITE-TASK0011-CURRENT-IPHONE-ALLOCATION-20260910
registry: data/session-work-claims.d/site-task0011-current-iphone-allocation-20260910.json
base registration commits: fb46192843845a2f014658eaebd48a9336fc5cd8, 610d09d686321c0e7805c9321fa1f7090cfc8b53
branch: fix/task0011-current-iphone-allocation
state: CLAIMED_FOR_IMPLEMENTATION
```

New files:

```text
stegos-node/org-allocator-portable-task0011.js
stegos-node/org-allocator-current-iphone-task0011-package.json
stegos-node/org-allocator-bootstrap-task0011-g7-v1.html
```

The original TASK-0010 portable allocator JS and package remain unchanged. The TASK-0011 successor JS preserves the same ordering, dependency, conflict, lease, fencing, receipt-hash, observation, and atomic-CAS algorithm while widening package admission by exactly one source-bound successor task. It requires all five lineage tasks and the exact TASK-0011 blob SHA.

The TASK-0011 supplement contains the canonical task body and predecessor provenance. The browser surface fetches the proven base package plus this supplement using `cache:no-store`, combines them only in memory, validates the exact source binding, verifies established node/device continuity and complete journal replay, and checks for retained TASK-0011 evidence before reading or mutating allocator state.

If no TASK-0011 receipt is retained, allocation can commit only when canonical preview includes and selects exact TASK-2026-0011 and advances the retained claim generation by exactly one. A different canonical selection, missing dependency declaration, stale state, source mismatch, replay failure, or CAS race fails closed with no mutation.

The service-worker lineage advances to `stegos-node-shell-v13-task0011-g7-fresh-delivery-v1`; the TASK-0011 page, successor JS, supplement, and base allocator package are network-only.

## Validation predicate

Before publication:

1. Dedicated TASK-0011 tests must prove exact `.github` blob binding and predecessor generation/fence provenance.
2. Successor allocator must retain canonical sort/conflict/CAS semantics and must not perform network source fetches itself.
3. Browser surface must recover journal evidence before allocator-state mutation.
4. Browser surface must require exact TASK-0011 canonical preview selection.
5. Service worker must deliver all TASK-0011 allocator inputs network-only with `no-store`.
6. Site Handoff Orchestrator, Site Bootstrap, StegOS Node Public Observation, and applicable heartbeat validation must pass at the exact PR head.
7. Native Pages must publish the exact merge before another current-iPhone action.

## README impact

Root Site README and `stegos-node/README.md` were reviewed. This change adds a bounded successor allocator delivery surface and does not change Site's product authority semantics. The allocator handoff is the canonical operational documentation for this bounded continuation; a repository-wide README semantic rewrite is not required.

## Current first unresolved predicate

`AUTHENTIC_TASK_2026_0011_CURRENT_IPHONE_CANONICAL_ALLOCATION_EVIDENCE`

After exact-head validation, merge, and Pages publication, open only the published TASK-0011 immutable entrypoint on the established current iPhone without clearing IndexedDB, Safari site state, node journal, or continuity state. Export the exact evidence JSON if TASK-0011 is recovered or newly allocated; preserve any exact fail-closed result without resetting state.
