# StegVerse Workspace Site Projection Mirror Handoff

Updated: 2026-08-31
Repository: StegVerse-Labs/Site
State: PERSONAL_KV_SOURCE_BOUND_RUNTIME_OBSERVATION_PENDING
Authority effect: NONE

## Source authority
Canonical Workspace semantics are owned by StegVerse-Labs/StegOS. Personal KV projection semantics are owned by StegVerse-Labs/continuity-vault-kit. Site is projection/interaction only.

## UI scope
Primary AI assistant, independently contactable AI Entities with mandatory AI labels, governed feed, friends/contacts, known organizations, memberships/departments, search, personal/organizational context switching, work, and KV context.

## Personal KV binding — implemented
`workspace.html` now loads the same registered Node + generated InTr + HB carrier + DEVICE_KV sync stack used by My KV, then `assets/workspace-kv-bridge.js` issues `WORKSPACE_PERSONAL_PROJECTION` as an exact Node-bound `kv.interlock.request.v1`.

The bridge requires:
- admitted DEVICE_KV ingress;
- current `STEGVERSE_KV_ROOT` at the resident receiver;
- CVK `runtime/workspace_projection.py`;
- persisted query response;
- HB-derived return carrier;
- exact recovered response bytes;
- projection authority effect `NONE`.

`assets/workspace.js` no longer uses browser localStorage as a substitute for Workspace principals/relationships/feed. Missing or blocked KV projection produces an empty/fail-closed UI. No default assistant identity is fabricated; the assistant appears only when the KV projection contains an admitted `AI_ENTITY` with `WORKSPACE_ASSISTANT` role.

## Organizational boundary
Organization mode does not reuse Personal KV. It remains locked until a distinct organizational runtime supplies Org-KV / Org-Emp-KV admission. The five required predicates remain employee identity + machine identity + active membership + role/capability + transition admission.

## Implemented files
- `workspace.html`
- `assets/workspace.js`
- `assets/workspace-kv-bridge.js`
- `assets/workspace.css`
- `data/workspace/bootstrap.json`
- `tests/workspace-kv-binding.test.cjs`
- `data/session-work-claims.d/site-workspace-interoperability-20260831.json`

Recent source commits:
- Personal KV bridge: `b61fe034f57106cd613085c5fd3d57487f957291`
- claim expansion: `1c6c9af3724a06de9d60668bddec85d85c433031`
- runtime assets wired: `2b35219b0b19ca77a1ccdea598d32791e09e0235`
- KV projection rendering / localStorage removal: `23280aaacdf2f390b0c94617222fcd6f0fce3dde`
- binding test: `79d4dcdbd8ca284d6e2f69f6c8324bd1c3dc1a63`

## Remaining evidence gates
Deterministic exact-head validation, Site publication observation, resident source refresh, and first authentic current-node Workspace KV response/consumption. Organizational runtime binding, federated discovery/feed, messaging/work transport, and assistant capability execution remain downstream.

## Non-claims
Source integration does not prove identity admission, KV runtime access, federation observation, membership truth, AI runtime activation, execution, or authority.