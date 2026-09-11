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

```text
StegVerse-Labs/.github/tasks/TASK-2026-0011.json
Git blob: a9f90414e59e308d66faf7ff2d5c31173b1687ca
requested_at: 2026-09-11T01:51:58Z
dependency surface: site:current-iphone-kv-testflight-static-bootstrap
workspace: claim/current-iphone-kv-testflight-static-bootstrap-r1
```

The task explicitly retains TASK-0010 generation-6/fence-6 as predecessor provenance and forbids retroactive scope widening.

## TASK-2026-0011 v1 publication and authentic observation

Site PR #1225 merged at `e8da5540ba5c243f47c2e8c7b647f9f407a0618e`; exact-merge build, validation, observation, and native GitHub Pages deployment passed.

Authentic current-iPhone Safari then loaded the published immutable v1 path with the established node continuity verified and produced:

```text
FAIL_CLOSED: canonical preview selected TASK-2026-0009 instead of TASK-2026-0011
selected_task_id: TASK-2026-0011
allocator_release: task0011-g7-v1-20260910
mutation_performed: false
```

This is a valid no-mutation observation. It exposed a retained-state reconstruction gap rather than a canonical ordering defect: the exact retained journal proves prior canonical TASK-0009 and TASK-0010 allocations, while the retained allocator state presented to the successor package can omit historical predecessor `task_statuses`. The successor allocator then correctly falls back to the package's queued floor for a missing predecessor status and selects the older TASK-0009.

The repair must not mark predecessors complete, invent historical claims, reset IndexedDB, or treat the journal as claim authority.

## TASK-2026-0011 v2 journal-status reconciliation

The active coordination claim was extended on Site `main` before implementation to admit the immutable v2 path. The v1 path remains unchanged evidence.

New immutable surface:

```text
stegos-node/org-allocator-bootstrap-task0011-g7-v2.html
release: task0011-g7-v2-20260910
```

V2 performs this bounded sequence:

1. verify the established node/device binding;
2. cryptographically replay the complete retained node journal;
3. identify predecessor tasks only from retained `stegos.org_allocator_same_device_execution_receipt/v1` entries whose canonical allocator receipt and claim observation agree on the exact selected task;
4. require retained TASK-2026-0010 allocator evidence before successor reconciliation;
5. if a proven predecessor's `task_statuses` field is missing or `queued`, reconstruct it only as `active` in the in-memory allocator snapshot; never synthesize `completed`;
6. run the unchanged TASK-0011 canonical allocator preview against that normalized snapshot;
7. require exact TASK-2026-0011 selection and generation +1;
8. atomically compare the current raw IndexedDB state with the pre-reconciliation raw snapshot and commit the normalized successor state plus TASK-0011 allocation in one CAS;
9. append the resulting canonical allocator receipt to the node journal and expose exact export evidence.

The reconciliation itself has `reconciliation_grants_claim_authority:false` and `reconciliation_synthesizes_completion:false`. Canonical allocator selection remains the only path to the TASK-0011 claim.

The service-worker lineage advances to `stegos-node-shell-v14-task0011-g7-journal-reconciliation-v2`; v1, v2, successor JS, and package inputs are network-only with `no-store`.

## Validation predicate

1. v1 must remain unchanged as the authentic fail-closed observation surface.
2. v2 must require cryptographically replayed canonical allocator receipts before reconstructing predecessor status.
3. v2 may reconstruct only missing/queued predecessor status to `active`; it must never synthesize `completed`.
4. v2 must require retained TASK-0010 evidence before reconciliation.
5. v2 must still require exact TASK-0011 canonical preview selection and generation +1.
6. commit must atomically compare against the raw retained allocator state, not bypass CAS.
7. service worker must publish v2 network-only.
8. exact-head Site validation must pass before merge; native Pages must publish the exact merge before another current-iPhone attempt.

## README impact

Root Site README and `stegos-node/README.md` were reviewed. This bounded reconstruction repair does not change Site product authority semantics. The allocator handoff remains the canonical operational documentation; no repository-wide README semantic rewrite is required.

## Current first unresolved predicate

`AUTHENTIC_TASK_2026_0011_V2_CURRENT_IPHONE_CANONICAL_ALLOCATION_EVIDENCE`

After exact-head validation, merge, and Pages publication, open only the published TASK-0011 v2 immutable entrypoint on the established current iPhone without clearing IndexedDB, Safari site state, node journal, or continuity state. Export exact evidence if TASK-0011 is recovered or newly allocated; preserve any exact fail-closed result without resetting state.
