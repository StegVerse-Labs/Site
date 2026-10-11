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

## Informational-only status and CVK metadata binding — Site#1509 (2026-10-10)
Follows ChatGPT cycle-2 final review (comment 6092132771):
- Every `stegverse.workspace.capability-status/v1` record carries `action_eligible: false`. `OBSERVED`, `STALE` and `FRESHNESS_UNKNOWN` are UI data-status only, never Interlock/InTr ALLOW. A later write/action interface must reject them until authentic freshness and authority are separately established.
- `projection_metadata.schema`, when present, must be `stegverse.kv.workspace-projection-metadata/v1` (emitted by continuity-vault-kit PR #237); otherwise `MALFORMED`. `source_revision` and `grant_state` (`UNKNOWN` unless verified) are surfaced in the capability card.

## Replay status — Site#1509 R1 as revised (2026-10-10)
ChatGPT cycle-3 final review (comment 6092615946) rejected a browser-persisted replay gate. Replay/rollback refusal requires an owner-defined authenticated KV/SKAP continuity checkpoint (a monotonic sequence or a signed/receipt-linked source epoch, bound to principal, context, grant epoch and source revision), enforced by the producer, receiver or governed projection admission layer. Until that exists:
- every capability status carries `replay_status: REPLAY_STATUS_UNKNOWN`, and projection metadata cannot override it;
- Workspace scripts use no localStorage, sessionStorage or IndexedDB (the test enforces this), so browser state can never become a continuity or replay root.

## Session-authentication contract — Site#1509 W4 (2026-10-10)
- `assets/workspace-session-authentication.js` defines `stegverse.workspace.session-authentication/v1`. It takes `state.session` only; the KV projection is never an input, so no projection field can become the session principal.
- The MyKV assistant binding resolver (`assets/workspace-assistant-binding.js`, CVK parity) receives a `principal_id` only from an `ALLOW` session decision. A bare `principal_id`, a principal copied from `projection_metadata.owner_principal_id` / `workspace.owner_principal_id` / `principals[]` (`KV_OWNERSHIP_IS_NOT_AUTHENTICATION`), a StegOS node registration (`DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION`) or any browser-held value (`BROWSER_STATE_IS_NOT_AUTHENTICATION`) is refused `FAIL_CLOSED` before the binding resolver runs.
- `ALLOW` (`CALLER_AUTHENTICATION_RECEIPT_PRESENT`) requires `source_class: CALLER_AUTHENTICATION_RECEIPT` and an `authentication` receipt with `authenticated: true`, `credential_authority: TV/TVC`, a non-empty `receipt_ref`, the same `principal_id`, and no transaction/execution/delegation authority. The page does not verify the receipt (`verification: CALLER_SUPPLIED_NOT_PAGE_VERIFIED`); `action_eligible` is false and `authority_effect` is `NONE`.
- Every decision also carries `admission_class: CALLER_SUPPLIED_FIELDS_ACCEPTED` and `runtime_authentication_evidence: false` (ChatGPT review Site#1509 comment 6102365201): `ALLOW` is an informational acceptance of caller-supplied receipt fields, never TV/TVC verification, never runtime authentication evidence, and never a reason to raise `action_eligible`. The card says so.
- The page still holds no receipt (`source_class: NO_AUTHENTICATED_SESSION_PRINCIPAL`), so the card renders `FAIL_CLOSED · SESSION_PRINCIPAL_UNAUTHENTICATED` with no generic-LLM fallback. Issuing a TV/TVC-backed caller-authentication receipt to the page is owner work: the SIWE runtime (`data/stegwallet-siwe-runtime.json`) is `CONFIGURATION_REQUIRED` and authenticates a wallet, not a KV principal.
- Tests: `tests/workspace-session-authentication.test.cjs` (contract and page wiring) and `tests/workspace-assistant-binding.test.cjs` (KV-owner-copied, bare and receipt-less sessions never bind; a receipt-backed session binds display-only).

## Mobile navigation acceptance — Site#1509 W6 (2026-10-10)
- Defect found by a local headless layout observation (Chromium, 375×812 and 390×844; not CI evidence): the phone media query fixed the nav at four `1fr` tracks, so single-word labels such as “Organizations” forced the shell to ~455px and the page scrolled horizontally on iPhone widths.
- Fix in `assets/workspace.css` (phone query only): one fluid shell column (`minmax(0,1fr)`), `min-width:0` on sidebar and main, nav tracks `repeat(auto-fit,minmax(min(100%,110px),1fr))`, nav buttons that shrink and wrap with a 44px tap height, and a 44px context switch; `.card` and `.assistant` get `min-width:0; overflow-wrap:anywhere` so long predicate and schema tokens (e.g. `SESSION_PRINCIPAL_UNAUTHENTICATED`) wrap instead of widening the page. Desktop layout otherwise unchanged. After the fix the same observation reports no horizontal overflow at 375 and 390, nav targets all present, tap heights 44px.
- Accessibility (same lane): the section nav is a `<nav aria-label="Workspace sections">` landmark of `type="button"` buttons; the active button carries `aria-current="true"` and the click handler moves it; the search field is `type="search"` with an `aria-label`; keyboard focus is visible via `:focus-visible`.
- `tests/workspace-mobile-navigation.test.cjs` (CI, deterministic, no browser): viewport meta without zoom lock, labelled context switch and live runtime status, every nav button targets an existing section, nav precedes main content, phone layout rules as above, and the nav click handler moves the active marker and scrolls to the target without storage, device or user-agent dependence.
- This is source conformance, not runtime proof: `WORKSPACE_SOURCE_PRESENT`, not `WORKSPACE_RUNTIME_VERIFIED`.

## Node binding on a new device — Site#1509 WU2 / WU5 (2026-10-10)
- **Finding (ChatGPT cycle 21, comment 6103393345; canonical work unit WU2):** the Personal KV path required `node.status().registered === true` and otherwise threw a bare string, so a device-local node registration was an identity gate in effect, which the canonical task prohibits (`physical_device_identity_gate: NONE_PROHIBITED`).
- **Existing recovery authority:** browser-independent recovery is owned by StegVerse-Labs/StegOS#347 (`stegos/device_continuity_recovery.py`, result schema `stegos.device_continuity_recovery_result.v1`, `ADMITTED_FOR_LOCAL_REHYDRATION`, nothing minted, TV/TVC + Interlock/InTr). Site holds no browser rehydration interface and no authorized channel that delivers such a result to the page.
- **Contract:** `assets/workspace-node-binding.js` defines `stegverse.workspace.node-binding/v1`. A directly observed registration binds (`REGISTERED_NODE_DIRECTLY_OBSERVED`). Otherwise only an admitted recovery result, validated fail-closed (schema, admitted state, nothing minted, authorities, retained node, exact Receipt #1 predicates and digest, continuity and binding match), may bind the retained node (`RETAINED_NODE_REHYDRATION_ADMITTED`, lineage carried). Absent it: `FAIL_CLOSED · DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED` naming WU2 and the StegOS#347 owner. The page never calls `registerDevice` (test-enforced) and reads no identity or recovery input from storage or the URL.
- **Bridge:** `assets/workspace-kv-bridge.js` resolves the node binding first and surfaces a structured refusal (`error.decision`). On an admitted recovery it requires a node-continuity `rehydrateRegistration` interface, re-reads status and demands the same retained node; without that interface it fails closed `LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE` (rehydration owner: the StegOS node continuity surface, not this lane). The page passes `recovery_result: null` today.
- **WU5:** the page requests `navigator.storage.persist()` once at init and renders the result (`PERSISTENT_STORAGE_GRANTED` / `PERSISTENT_STORAGE_REFUSED` / `PERSISTENCE_API_UNAVAILABLE`) as advisory; it never discharges WU1 and is never authority.
- **Not implemented here (owner work):** the browser rehydration interface in the StegOS node continuity surface; the authorized channel that delivers an admitted recovery result to the page; WU3 receipt-lineage survival across re-registration.
- **Real-script observation (local Chromium, fresh profile, 375×812):** the new-device path renders `FAIL_CLOSED · DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED`, node status stays `UNREGISTERED`, no console errors, no failed requests. It also exposed that the structured runtime-state text overflowed the phone width in the `.topbar` flex row; `.topbar` and its children now shrink and wrap (`min-width:0; overflow-wrap:anywhere`).
- **Tests:** `tests/workspace-node-binding.test.cjs` (contract cases incl. denied/revoked/stale/tampered/authority-claiming results; bridge harness proving no registration and no side effects on refusal, seam-absent refusal, denied-recovery never rehydrates, admitted recovery proceeds only through rehydration with the same node; page rendering and WU5).

## Universal search — Site#1509 WS-SEARCH (2026-10-11)
- **Directive:** owner/ChatGPT parallel implementation plan (Site#1509 comment 6104154989) item WS-SEARCH: universal search over provided KV projections only; provenance, context boundaries, stale/ambiguous refusal, no independent index.
- **Contract:** `assets/workspace-search.js` defines `stegverse.workspace.search/v1`. `search({query, workspace_type, descriptors, projections, now_ms, visibility})` evaluates the capability descriptors against the supplied projections through `StegVerseWorkspaceCapabilities.evaluateAll` and searches a field only when its status does not withhold rows. Extractors exist for principals, organizations, memberships, feed (visibility-filtered), assistant and the CryptoBot portfolio; every hit carries `context.workspace_type` and the source projection's provenance (schema, freshness state and predicate, observed_at, age, provenance_ref, source_revision, cursor, grant state, replay status). `STALE` and `FRESHNESS_UNKNOWN` sources still search with labelled hits; revoked, malformed, context-mismatched and unobserved sources are listed in `excluded`; a second source for one capability fails the whole search closed (`PROJECTION_SOURCE_AMBIGUOUS`); an unknown context or missing descriptors fail closed. `index: NONE_EPHEMERAL_QUERY_ONLY`: nothing is stored, fetched or cached; results are informational only (`action_eligible: false`).
- **Page:** the Search card renders results with provenance in `#searchResults` (live region); the existing contact and organization filters still apply; organizational context searches only organizational projections, of which none is bound, so personal rows never surface there.
- **Tests:** `tests/workspace-search.test.cjs`: multi-projection filtering (personal + CryptoBot), cross-context denial both ways, source ambiguity, stale/freshness-unknown labelling, revoked/authority-asserting refusal, visibility withholding, determinism and hit cap, page rendering and context switch. iPhone navigation remains covered by `tests/workspace-mobile-navigation.test.cjs`.

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