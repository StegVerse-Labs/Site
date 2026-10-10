# StegVerse Workspace Site Projection Mirror Handoff

Updated: 2026-10-10
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

## Context isolation and intent hardening — Site#1509 W2/W3 (2026-10-10)
- **W2:** Organization mode no longer reads `sessionStorage` `stegverse.workspace.orgEmpGate`; browser storage cannot assert Org-KV/Org-Emp-KV admission. The gate renders `LOCKED`, disposition `FAIL_CLOSED`, predicate `ORG_KV_PROJECTION_NOT_OBSERVED`, each predicate `NOT_OBSERVED`, until an authenticated organizational KV projection bridge exists.
- **Context scoping:** Organization mode renders no Personal KV rows (contacts, organizations, memberships, feed, assistant); switching context invalidates any pending interaction draft.
- **W3:** Contact actions no longer `alert()` request JSON. They render an ephemeral, unsubmitted `stegverse.workspace.interaction-request.v1` draft with `disposition: FAIL_CLOSED`, `failing_predicate: WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND`, `authority_effect: NONE_REQUEST_ONLY`; nothing is sent.
- **Test:** `tests/workspace-context-isolation.test.cjs` (behavioral, no dependencies) covers browser-asserted admission refusal, cross-context non-leakage, draft invalidation, and non-ALLOW no-effect. The validation workflow now also runs on `pull_request`.
- **Open (not changed here):** W1 — the bridge still requires `node.status().registered` because the DEVICE_KV authority reference is node-bound; a device-independent verified-user-continuity query path must come from the KV/SKAP owner (continuity-vault-kit), not from Site.

## Capability descriptor / freshness / provenance contract — Site#1509 (2026-10-10)
Approved as a source-only, non-authorizing item by ChatGPT final review (Site#1509 comment 6091953259).
- `data/workspace/bootstrap.json` → `capability_descriptors` (`stegverse.workspace.capability-descriptor/v1`). Descriptors hold only capability, label, projection_field, allowed_projection_schemas, workspace_types, max_age_seconds, `default_state: NOT_OBSERVED` and `authority_effect: NONE`. Any other key (available, admitted, fresh, observed_at, disposition…) rejects the descriptor.
- `assets/workspace-capabilities.js` derives `stegverse.workspace.capability-status/v1` per capability **only** from the authenticated KV projection: `NOT_OBSERVED`, `UNAVAILABLE` (`NO_KV_PROJECTION_CONTRACT`, `PROJECTION_FIELD_ABSENT`, `CAPABILITY_NOT_DEFINED_FOR_CONTEXT`), `MALFORMED`, `CONTEXT_MISMATCH`, `REVOKED`, `STALE`, `FRESHNESS_UNKNOWN`, `OBSERVED`. No status ever carries ALLOW/ADMITTED; `authority_effect` is always `NONE`.
- Rows are withheld for `DESCRIPTOR_REJECTED`/`MALFORMED`/`CONTEXT_MISMATCH`/`REVOKED`, and whenever descriptors are missing (fail closed). `STALE` rows render, labelled.
- Freshness reads an optional `projection_metadata` block (`observed_at`, `provenance_ref`, `source_cursor`, `grant_state`/`revoked`). CVK `runtime/workspace_projection.py` (blob `6181b193`) does not emit it yet, so Personal KV capabilities show `FRESHNESS_UNKNOWN` (`PROJECTION_OBSERVED_AT_ABSENT`) — never `OBSERVED`. Emitting that block is a proposal for the CVK owner, not implemented here.
- Calendar, email, messaging/VoIP, documents, social, tasks, GitHub governance, CryptoBot portfolio and Org Workspace have no KV projection contract and render `UNAVAILABLE`.
- Test: `tests/workspace-capability-contract.test.cjs` (forged descriptors, absent/stale/revoked/cross-context/malformed metadata, future timestamps, no forged success, UI fail-closed rendering).

## Implemented files
- `workspace.html`
- `assets/workspace.js`
- `assets/workspace-kv-bridge.js`
- `assets/workspace-capabilities.js`
- `assets/workspace.css`
- `data/workspace/bootstrap.json`
- `tests/workspace-kv-binding.test.cjs`
- `tests/workspace-context-isolation.test.cjs`
- `tests/workspace-capability-contract.test.cjs`
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