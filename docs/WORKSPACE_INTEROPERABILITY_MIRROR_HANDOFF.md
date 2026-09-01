# StegVerse Workspace Site Projection Mirror Handoff

Updated: 2026-08-31T21:14:00-05:00
Repository: StegVerse-Labs/Site
State: ACTIVE_IMPLEMENTATION
Authority effect: NONE

## Source authority
Canonical Workspace semantics are owned by StegVerse-Labs/StegOS:
- docs/WORKSPACE_INTEROPERABILITY_MIRROR_HANDOFF.md
- schemas/workspace_interoperability.v1.schema.json
- stegos/workspace_interoperability.py

Site is projection/interaction only.

## UI scope
- primary AI assistant surface, visibly labeled AI Assistant;
- contacts/friends including independently identified AI Entities with mandatory AI badges;
- governed feed from known and unknown principals only when visibility policy permits;
- known organizations;
- organizational memberships and member/department projection;
- user/organization search;
- personal and organizational workspace context switch;
- Personal KV, Org-KV, Org-Emp-KV shown as distinct contexts;
- Org-Emp-KV locked unless employee identity + machine identity + active membership + role/capability + transition admission all match;
- work and messaging launch surfaces represented as governed capability requests, not direct authority.

## Non-claims
No static Site projection proves identity admission, KV access, federation observation, membership truth, AI runtime activation, execution, or authority.


## 2026-08-31 implementation state

Implemented on current main:
- `workspace.html`;
- `assets/workspace.js`;
- `assets/workspace.css`;
- `data/workspace/bootstrap.json`;
- homepage `Workspace` entry in `index.html`;
- Site pre-work claim `data/session-work-claims.d/site-workspace-interoperability-20260831.json`.

Projected behavior:
- primary AI assistant explicitly labeled AI;
- independently contactable AI Entities retain AI badges;
- empty-state-safe feed, contacts, organizations, memberships, and work projections;
- local known-principal search projection;
- Personal vs Organizational Workspace context switch;
- Personal KV distinct from Org-KV / Org-Emp-KV;
- Org-Emp-KV displays fail-closed five-predicate access state and cannot be overridden by UI;
- contact actions produce non-authorizing Interlock/InTr request objects;
- no fabricated identities, memberships, feed events, KV admission, or runtime observation.

Source commits:
- handoff: 28b542a7b797d329737fef6d3218e59405da4813
- claim: 81668f5d833ee4714dd616bae0ed24ee9cd444cd
- bootstrap: 073d6cef2fc899bab0c22c324a6f52ace1540357
- styles: cbe65502e1e0fd7067258b5bf0a996158e913e3d
- behavior: b9e1fa9ceaea357f62baaf6ef9d61c632a753692
- page: 55297f9d91106445a4a340a5a0d776c911a6d905
- claim expansion: 106ef00b1f5472e2936a7152644a6ab9d40bd3df
- homepage entry: 5c4f7edf37acb837e4d563f34d7e1174ae1391be

Lifecycle:
```text
implemented: YES
projection linked from primary Site: YES
publication observed: NO
identity/KV/federation runtime activation: NOT CLAIMED
```
