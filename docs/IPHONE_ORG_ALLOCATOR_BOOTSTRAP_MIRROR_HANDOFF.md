# iPhone Organization Allocator Bootstrap Mirror Handoff

Updated: 2026-09-02
Repository: `StegVerse-Labs/Site`
Issue: #945
Claim: `SITE-IPHONE-ORG-ALLOCATOR-BOOTSTRAP-945-20260902`

## Purpose

Break the allocator/publication bootstrap circularity without bypassing the organization allocator or TASK-2026-0008.

Canonical allocator authority:
- `StegVerse-Labs/.github#884`
- merge `d3da58e0f6822bde7316ada3f532f15f75a2fdcf`

Site role is orchestration/bootstrap transport only.

## Exact projected authority artifacts

- `.github:org_allocator/portable_allocator.js`
- `.github:control/portable-org-allocator/current-iphone-package.json`

The Site copies must remain byte-identical to their merged source blobs.

## Same-device execution

```text
established CURRENT_USER_IPHONE node continuity
-> exact canonical allocator JS/package
-> dedicated IndexedDB portable allocator state
-> atomic compare-and-swap
-> canonical allocator selection
-> claim/fence generation
-> claim observation retained in established node journal
```

Site, HB, browser shell, static hosting, transport, and source materialization grant no claim authority.

## Bootstrap/product separation

This lane does NOT modify any `stegos-bootstrap/*` path owned by TASK-2026-0008.

The bootstrap runner lives only under `stegos-node/` orchestration infrastructure. A TASK-0008 claim produced by the canonical allocator is a later runtime predicate; this source publication does not satisfy it.

## Expected first allocations

From the exact packaged current state:
- first uncontended allocation may select TASK-2026-0007 / generation 3;
- a later invocation may select TASK-2026-0008 / generation 4 because the dependency surfaces are disjoint.

Those are source-semantic expectations only until the physical iPhone executes them.

## Runtime evidence

Authentic evidence is retained as:
- canonical allocator portable state in dedicated IndexedDB;
- allocator receipt;
- claim observation;
- established StegOS node continuity journal entry.

Source/merge/CI never substitute for those receipts.
