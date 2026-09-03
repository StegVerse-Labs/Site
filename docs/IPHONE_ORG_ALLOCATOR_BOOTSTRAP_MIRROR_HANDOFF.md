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


## Implemented source — 2026-09-02

Exact projections:

```text
stegos-node/org-allocator-portable.js
  blob 4df48314fa6cebf96d39cb1366a275468f5a3cbc

stegos-node/org-allocator-current-iphone-package.json
  blob e97411f7c70a9724f6d62f10899fef6ceafaeaae
```

Runner:
`stegos-node/org-allocator-bootstrap.html`.

Persistence:
`IndexedDB stegos-org-allocator-v1 / canonical-portable-state`.

The runner verifies established `stegos-web-bootstrap-v1` node/device continuity, invokes the exact canonical allocator, persists portable state through atomic compare-and-swap, and appends a non-authorizing execution/claim-observation receipt into the established node journal.

Validation:
- exact upstream blobs: PASS;
- JavaScript syntax: PASS;
- no `stegos-bootstrap/*` product-path dependency: PASS;
- Site/HB/browser claim-authority widening: absent;
- physical iPhone allocator execution: NOT OBSERVED;
- TASK-2026-0008 grant: NOT OBSERVED.

The completed older resident-task publication claim `SITE-STEGOS-IPHONE-RESIDENT-TASK-938-20260902` is terminalized to RELEASED on this branch after merged Site PR #940 / commit `13baddb05104729fb85c41e029c675add07a4107`.


## Post-merge reconciliation — 2026-09-02

Source implementation merged through Site PR #946:

`9868b62ba2bfaaba0a0164318ac4d1d4f6d235d5`

Exact-head validation succeeded:
- Site Bootstrap Validate `33714257695`;
- Site Handoff Orchestrator `33714257500`;
- Ecosystem Heartbeat Orchestration `33714257631`;
- StegOS Node Public Observation `33714257528`;
- StegFin Phone Projection validation `33714257571`;
- Physical Economics validation `33714257516`.

Current truth:
```text
source implementation: MERGED
repository validation: PASS
canonical allocator source: MERGED
public HTTP route observation: NOT OBSERVED
physical current-iPhone allocator execution: NOT OBSERVED
TASK-2026-0008 claim: NOT OBSERVED
claim role/state: VALIDATION / CLAIMED_FOR_VALIDATION
```

No more product/source implementation is authorized by this bootstrap claim unless public/on-device validation exposes a concrete defect.
