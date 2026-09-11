# iPhone Organization Allocator Bootstrap Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Issue: #945
Root goal: `GLOBAL-RUNTIME-EVIDENCE-CLOSURE-001`
Immediate target: `TASK-2026-0010`

## Purpose

Carry the canonical StegVerse organization allocator on the established current iPhone without granting Site, browser presentation, HB, or GitHub Actions claim authority.

Canonical allocator source remains `StegVerse-Labs/.github`; Site is bootstrap/projection transport only. TV/TVC remains credential authority. Interlock/InTr remains transition authority. The established StegOS node journal is retained continuity/evidence, not an alternate allocator.

## Retained lineage

Authentic current-iPhone allocator lineage previously reached:

```text
TASK-2026-0007 -> generation/fence 3
TASK-2026-0008 -> generation/fence 4
TASK-2026-0009 -> generation/fence 5
TASK-2026-0010 -> next intended generation/fence 6
```

`.github#1308` removed the accidental TASK-0009/TASK-0010 scoped-exclusive collisions. Site cache-freshness remediation then made allocator HTML/JS/package requests network-only and introduced an immutable G6 entry after stale WebKit presentation was authentically observed.

## Exact canonical projections

```text
stegos-node/org-allocator-portable.js
  blob af4ada6b50647ffab0061960e7e4a153dbd83b68
stegos-node/org-allocator-current-iphone-package.json
  blob f244f4cbc792a3bce1dc6486654be9a47fac6dec
TASK-2026-0010 source binding
  248bed8cf5428c3ba759ee0d34db5fec8949a835
```

## Current authentic observation

After exact KV TestFlight projection artifacts were produced, the current iPhone opened the allocator surface. The user observed one opening in the ChatGPT browser as green/successful, then later ChatGPT-browser and Safari openings showed the obsolete failure:

```text
FAIL_CLOSED: auto-execution requires exactly one queued canonical successor
mutation_performed: false
```

Current merged source no longer contains that single-queue restriction; Site#1205 removed it and requires instead:

```text
canonical queue contains TASK-2026-0010
canonical allocator actually selects TASK-2026-0010
```

Therefore the later red presentation is stale document code. The first green execution may already have committed TASK-2026-0010 and retained its `stegos.org_allocator_same_device_execution_receipt/v1` plus claim observation in the established node journal. Repeated allocation must not be attempted before journal recovery checks that retained evidence.

## Immutable execution rule

Allocator execution documents are release-immutable from this point forward. Once a path has been used for an allocator release it is not overwritten as the canonical continuation surface. A corrected release receives a new path.

Current new surfaces:

```text
stegos-node/org-allocator-evidence-recovery-task0010-g6-v1.html
  read-only journal recovery
  validates node/device binding and full journal chain
  accepts only retained TASK-2026-0010 same-device allocator receipt with claim observation
  contains no allocator DB, CAS, or allocate() mutation path

stegos-node/org-allocator-bootstrap-task0010-g6-v2.html
  immutable TASK-0010 execution release
  checks journal first
  if TASK-0010 receipt already exists: exports it and performs no allocator mutation
  otherwise uses the existing canonical preview + retained-state CAS path
  still fails closed if TASK-0010 is absent or another canonical task is selected
```

Service-worker cache lineage advances to `stegos-node-shell-v11-immutable-allocator-recovery-v1`; both new paths plus allocator JS/package are network-only. Browser freshness remains presentation state, never continuity or authority.

## Current first unresolved predicate

```text
RETAINED_TASK_2026_0010_EXECUTION_RECEIPT_RECOVERY_OR_FRESH_IMMUTABLE_G6_EXECUTION
```

Required sequence:

1. Open the immutable read-only recovery surface on the same current-iPhone browser storage partition that displayed the green execution.
2. If a retained TASK-2026-0010 receipt is found, export it exactly; do not re-run allocation.
3. Validate `selected_task_id`, generation, claim observation and fencing tokens from the exact exported evidence.
4. Only if recovery proves no retained TASK-2026-0010 execution exists, use the immutable `task0010-g6-v2` execution URL.
5. Do not reset allocator IndexedDB, node journal, browser state, or continuity state.
6. After authentic claim/fence evidence is retained, bind it to the task-gated TestFlight static bootstrap work and continue the KV-bound current-iPhone TestFlight trajectory.

## Authority invariants

```text
canonical organization allocator / WorkerCoordinator claim-fence authority: retained
Site claim authority: false
StegOS presentation claim authority: false
browser freshness authority: false
HB execution/claim authority: false
GitHub Actions runtime authority: NONE
credential authority: TV/TVC
second user-operated machine required: false
```

## README impact

`stegos-node/README.md` now documents the immutable execution/recovery rule and current TASK-2026-0010 surfaces. Root Site README product semantics are unchanged.

## Manual work after merge/publication

Use the immutable read-only recovery URL first. Export retained TASK-2026-0010 evidence if present. Only use the immutable execution URL if recovery reports that no retained TASK-2026-0010 receipt exists.
