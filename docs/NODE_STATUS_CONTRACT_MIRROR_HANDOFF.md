# Node Status Contract Mirror Handoff

## Source of truth
This file is the bounded continuation record for the Site-wide public Node-status and Node/KV product-surface lane in `StegVerse-Labs/Site`. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md` / `SITE_MIRROR_HANDOFF.md` as applicable. Existing Node continuity, KV, StegOS, and capability handoffs remain authoritative for their underlying semantics.

## Goal
Promote the explicit-consent interaction contract proven on the Hugging Face interface into canonical public production surfaces without changing underlying Node Receipt #1, KV custody, StegOS runtime, or capability authority semantics.

## Governing invariants
1. A brand-new device/browser context is displayed as `Unselected Node not established.`
2. Page arrival is not consent to establish or mutate a Node.
3. Page load may only resolve/display already-existing Node state and capabilities.
4. Establishing a new Node requires an explicit user-confirmed action such as `Connect a StegVerse Node`.
5. No Site page may establish, select, elevate, repair, replace, or otherwise transition a Node solely because the page loaded.
6. `Node established` and `capability established` are independent states.
7. Elevation expands admitted capability; it does not increase governance authority.
8. Public informational content remains readable without an established Node.
9. KV is attached to sovereignty, not subscription level. Node level changes capability, not ownership.
10. Payment/entitlement can make a capability available but cannot itself authorize KV access, execution, or a consequence-bearing transition.

## Five user-visible Node types
1. `Unselected Node` — default/bootstrap type. Before explicit establishment it has no Node identity; after explicit establishment it can carry bounded introductory continuity/capability.
2. `Private Sovereign Node` — private/user-or-organization sovereignty without requiring resident StegOS.
3. `Main Ecosystem Node` — ecosystem-governed/shared participation without private-KV custody.
4. `Private Sovereign StegOS Node` — private sovereignty with resident StegOS eligibility/capability.
5. `Ecosystem Sovereign StegOS Node` — ecosystem-governed resident StegOS substrate for common/public services.

`Elevated Node` is not a sixth class.

## Three-layer model
- Node identity/continuity: whether an actual Node exists and continuity is verified.
- Node class: the requested/effective sovereignty and operating boundary.
- Capabilities: independently established function-specific abilities such as KV, Ecosystem Chat, analysis observation, or resident execution.

A selected class may be requested but not yet established. Base continuity remains independent from class predicates so the UI never converts a desired class into proof.

## Universal display contract
The Site-wide top-of-page status format is `(NODE_CLASS) Node established. (What is this?)` or `(NODE_CLASS) Node not established. (What is this?)`. For a new context the canonical default is `Unselected Node not established. (What is this?)`.

The universal `What is this?` link points to `node-status.html`, a concise nontechnical explanation. Function-specific sections separately link to their technical/capability test pages.

## Production foundation
PR #1039 merged the canonical foundation at `d1676e49be2ef605fc75f33bafdfd108d657b7cd`.

Merged foundation:
- `data/node-status-contract.json` encodes the five classes, exact default state, custody boundaries, resident-StegOS requirement, selectability, and no-authority invariants.
- `assets/stegverse-node-status.js` is the shared Node-state resolver/header/action surface.
- The resolver is deliberately passive on page load: it uses `indexedDB.databases()` to determine whether the existing canonical Node DB is already present before invoking the legacy continuity reader. If passive DB discovery is unavailable or no DB exists, it reports `Unselected Node not established.` rather than opening/creating IndexedDB merely to inspect state.
- `explicitConnect()` is the only shared Node-establishment path and calls canonical `StegVerseNodeContinuity.registerDevice()` only after explicit user action.
- `explicitSelectNodeClass()` writes class receipts only after explicit user action. Private Sovereign and Main Ecosystem selection can establish their non-resident class boundary; StegOS selection records a request and remains not-established until resident predicates exist. Ecosystem Sovereign StegOS remains eligibility-restricted and has no consumer selection control.
- `node-status.html` explains continuity, explicit consent, capability separation, and links to Node comparison.
- `nodes.html` presents all five types, KV boundary first, and no rank/tier semantics.
- `scripts/validate_node_status_contract.py` statically enforces the class list, exact labels, passive-resolution non-mutation markers, explainer/product content, restricted ecosystem class, and shared-component contract.
- The Hugging Face page migration to the shared Node-status component is complete. The living analytical content of `hugging-face-analysis.html` is no longer owned by this Node-status claim and is transferred to Site #1069 / parent #1001.

## My KV / Organizational KV integration boundary
The existing My KV surface has substantial continuity, resident DEVICE_KV, file-fallback, profile, and receipt behavior. It must not be rewritten casually. A future separately admitted phase adds the shared universal header and onboarding gate ahead of persistent KV installation:
`static/readable My KV intro → explicit Connect Node if absent → Unselected Node established → required Node-class selection → class verification/provisioning → existing KV installation/profile flow`.

Organizational KV must use the same global status vocabulary while preserving its existing NOT CONNECTED, organization membership, identity, authorization, Interlock, and SKAP boundaries. A public Node-class choice must never create organization membership or grant shared-KV access.

## Custody and authority boundary
The public product/explainer surfaces grant no identity, credential, KV, StegOS, execution, publication, or governance authority. Existing `assets/stegverse-node-continuity.js` remains the canonical Receipt #1 registration path.

## Collision boundary
Do not rewrite Node Receipt #1 semantics. Do not silently change the current 10-execution unregistered Ecosystem Chat behavior. Do not reinterpret existing KV receipts, InTr evidence, or resident StegOS state. Do not make the Ecosystem Sovereign StegOS Node appear generally consumer-orderable unless eligibility semantics are explicitly established. Do not claim the living Hugging Face analytical-content surface from this Node-status lane; Site #1069 owns that continuation.

## README completeness preflight
The foundation materially changes public Node interaction semantics and therefore requires README impact review. PR #1039 merged implementation without a repository-root README semantic rewrite because the canonical behavior contract is maintained in this handoff, `data/node-status-contract.json`, the public explainer, and product page; no repository bootstrap/dependency/interface prerequisite outside those Site surfaces changed. If later KV integration changes repository-level prerequisites or capability meaning, README impact must be reassessed in that change set.

## Completion state
handoff: RECONCILED_POST_MERGE
pre-work claim: ACTIVE_RECONCILIATION
foundation PR: MERGED_1039
foundation merge: d1676e49be2ef605fc75f33bafdfd108d657b7cd
machine-readable contract: MERGED
shared resolver/header: MERGED
page-load persistent mutation prevention: MERGED
Node-status explainer: MERGED
Node comparison/product page: MERGED
Hugging Face shared-component migration: MERGED_COMPLETE_AND_SURFACE_RELEASED_TO_SITE_1069
My KV integration: PENDING_SEPARATE_CLAIM
Organizational KV integration: PENDING_SEPARATE_CLAIM
public Node explainer/product exact-route observation: PENDING
claim terminalization: PENDING_PUBLIC_OBSERVATION

## Remaining machine work
Observe the exact public `node-status.html` and `nodes.html` routes from the merged foundation, terminalize this foundation claim, then admit My KV / Organizational KV integration as a separate collision-sensitive claim. The Hugging Face living-analysis content is independently owned by Site #1069 and may proceed without claiming this Node-status dependency surface.

## Archive readiness
Not archive-ready. Required public Node route observation and later KV integrations remain incomplete and are not durably owned by an independent autonomous executor.
