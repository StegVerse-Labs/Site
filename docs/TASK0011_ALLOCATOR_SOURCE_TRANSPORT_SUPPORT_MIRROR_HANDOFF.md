# TASK-2026-0011 Allocator Source Transport Support Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Support task: `SITE-TASK0011-ALLOCATOR-SOURCE-TRANSPORT-001`
Parent goal: `GLOBAL-RUNTIME-EVIDENCE-CLOSURE-001`
Canonical successor: `TASK-2026-0011`
Status: `ACTIVE / EXACT CANONICAL ALLOCATOR SOURCE TRANSPORT IN IMPLEMENTATION`

## Purpose

Transport the exact canonical current-iPhone allocator source and retained-state TASK-0011 package from merged `.github` source into Site's bootstrap carrier namespace. Site remains transport/presentation only.

## Canonical source

`.github` PR #1365 merged at:

`1fe1d041fa87bc00be9bc40703cd14473a7ab02d`

Exact source blobs:

```text
org_allocator/portable_allocator.js
blob 0bc3b2f302ff30fbf0c73e86bf9bf958e2d7c06b

control/portable-org-allocator/current-iphone-package-task0011.json
blob 4b6db0a870035a795fd2d2cdc8b083ac12b7ae7d
```

The canonical allocator extension preserves the existing allocation/CAS/fencing algorithm and adds an exact retained-state successor package for TASK-0011. Deterministic validation proved retained G6 can advance to G7/fence 7 only when the new dependency surface is non-colliding; a held claim on that surface leaves generation unchanged.

## Transport contract

`.github/workflows/task0011-allocator-source-transport.yml` performs deterministic source/evidence transport only. It runs on a dedicated materialization branch request, fetches only the pinned merged `.github` source, verifies Git blob identities before writing, and commits only:

```text
stegos-node/org-allocator-portable-task0011.js
stegos-node/org-allocator-current-iphone-package-task0011.json
```

It does not execute the allocator, open IndexedDB, grant claims, access TV/TVC credentials, or create an alternative claim authority.

## Authority invariants

```text
canonical allocator / WorkerCoordinator claim-fence authority: unchanged
Interlock/InTr transition authority: unchanged
TV/TVC credential authority: unchanged
HB authority: observability only
GitHub Actions runtime authority: NONE
Site claim authority: false
second user-operated machine required: false
Render fallback: none
```

## Next sequence

1. Validate/merge this support workflow.
2. Create the dedicated Site materialization branch from current main and add the request marker.
3. Require exact source-blob verification and transport commit.
4. Build the immutable TASK-0011 G7 carrier around those exact transported bytes.
5. Validate/merge the carrier and publish it.
6. Only then return to the current iPhone for one authentic successor allocation attempt.

## Manual work

None.
