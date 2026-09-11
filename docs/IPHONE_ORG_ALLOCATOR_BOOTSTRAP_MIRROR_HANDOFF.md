# iPhone Organization Allocator Bootstrap Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Issue: #945
Root goal: `GLOBAL-RUNTIME-EVIDENCE-CLOSURE-001`
Immediate task: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Immediate target: `TASK-2026-0010`

## Purpose

Carry the canonical StegVerse organization allocator on the established current iPhone while preserving retained node/journal state and canonical allocation semantics.

Canonical allocator source remains `StegVerse-Labs/.github`; Site is bootstrap/projection transport only. TV/TVC remains credential authority. Interlock/InTr remains transition authority. The established StegOS node journal is retained continuity/evidence, not an alternate allocator.

## Retained lineage

```text
TASK-2026-0007 -> generation/fence 3
TASK-2026-0008 -> generation/fence 4
TASK-2026-0009 -> generation/fence 5
TASK-2026-0010 -> next intended generation/fence 6
```

`.github#1308` removed accidental TASK-0009/TASK-0010 scoped-exclusive collisions. Site#1205 removed the wrapper-local exactly-one-queued restriction and requires instead that TASK-2026-0010 is in the canonical queue and is actually selected by the canonical allocator.

## Current authentic observation

Authentic current-iPhone Safari evidence on 2026-09-10 showed continuity verified but delivered the obsolete `g6-auto-20260909-1` failure `FAIL_CLOSED: auto-execution requires exactly one queued canonical successor`, with `mutation_performed:false`.

Current Site `main` no longer contains that restriction, native Pages publication succeeds, and allocator paths are network-only. The observation is therefore retained as stale delivered/navigation representation rather than current allocator source logic.

An earlier green execution may already have committed TASK-2026-0010 and retained its same-device execution receipt. Repeated allocation must never occur before journal recovery checks retained evidence.

## Existing recovery-aware surface

`stegos-node/org-allocator-bootstrap-task0010-g6-v2.html` checks the node journal first. If TASK-0010 is already retained it exports that evidence without allocator mutation; otherwise it uses canonical preview + retained-state CAS and fails closed unless TASK-0010 is queued and canonically selected.

## G7 fresh-delivery remediation — PR #1217

The exact pre-work claim is canonical on Site `main` before implementation evaluation:

```text
claim: SITE-TASK0010-G7-FRESH-DELIVERY-20260910
registry: data/session-work-claims.d/site-task0010-g7-fresh-delivery-20260910.json
main commit: eaa2e679ff5611d8138f8a735110ff141c1c40fc
branch: fix/task0010-g7-fresh-delivery
state: CLAIMED_FOR_IMPLEMENTATION
```

New immutable entrypoint:

```text
stegos-node/org-allocator-bootstrap-task0010-g7-v1.html
release: task0010-g7-v1-20260910
```

G7 fetches the existing recovery-aware G6-v2 source with `cache:no-store`, rejects any delivered source containing the obsolete exactly-one-queued rule, and requires the journal-recovery, TASK-0010 queue-membership, canonical-selection, and recovered-no-mutation markers before entering that source.

The service-worker lineage advances to `stegos-node-shell-v12-task0010-g7-fresh-delivery-v1`; G7, G6-v2, recovery, allocator JS, and allocator package are network-only. This remediation does not reset IndexedDB, force TASK-0010 selection, or bypass CAS/claim/fence behavior.

## Current first unresolved predicate

`RETAINED_TASK_2026_0010_EXECUTION_RECEIPT_RECOVERY_OR_FRESH_RECOVERY_AWARE_EXECUTION`

Required sequence:

1. Merge and publish PR #1217 only after exact-head validation passes.
2. Open the new immutable G7 entrypoint on the same current-iPhone Safari storage partition.
3. G7 rejects stale pre-repair source before any allocator mutation.
4. G6-v2 checks retained journal evidence first.
5. If TASK-0010 is already retained, export it and perform no new allocation.
6. Otherwise allocation may proceed only if TASK-0010 is queued and canonically selected.
7. Do not reset allocator IndexedDB, node journal, browser state, or continuity state.
8. After authentic claim/fence evidence is retained, continue the task-gated TestFlight bootstrap trajectory.

## README impact

`stegos-node/README.md` already documents immutable execution/recovery behavior. Root Site README was reviewed; this delivery remediation introduces no repository-wide product semantic change, so no root README replacement is required.

## Manual work after merge/publication

Open only the published G7 immutable entrypoint on the established current iPhone. Export exact TASK-2026-0010 evidence if it recovers or executes successfully. If it fails closed, preserve the exact displayed result and do not reset browser/allocator/node state.
