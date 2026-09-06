# Node Status Contract Mirror Handoff

## Source of truth
This file is the bounded continuation record for the Site-wide public Node-status and Node/KV product-surface lane in `StegVerse-Labs/Site`. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md` / `SITE_MIRROR_HANDOFF.md` as applicable. Existing Node continuity, KV, StegOS, and capability handoffs remain authoritative for their underlying semantics.

## Goal
Promote the explicit-consent interaction contract proven on the Hugging Face analysis into canonical public production surfaces without changing underlying Node Receipt #1, KV custody, StegOS runtime, or capability authority semantics.

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

A selected class may be requested but not yet established. Base continuity must remain independent from class predicates so the UI never converts a desired class into proof.

## Universal display contract
The Site-wide top-of-page status format is `(NODE_CLASS) Node established. (What is this?)` or `(NODE_CLASS) Node not established. (What is this?)`. For a new context the canonical default is `Unselected Node not established. (What is this?)`.

The universal `What is this?` link points to `node-status.html`, a concise nontechnical explanation. Function-specific sections separately link to their technical/capability test pages.

## Implemented production foundation on `feat/node-status-production-pages-1035-r2`
- `data/node-status-contract.json` encodes the five classes, exact default state, custody boundaries, resident-StegOS requirement, selectability, and no-authority invariants.
- `assets/stegverse-node-status.js` is the shared Node-state resolver/header/action surface.
- The resolver is deliberately passive on page load: it uses `indexedDB.databases()` to determine whether the existing canonical Node DB is already present before invoking the legacy continuity reader. If passive DB discovery is unavailable or no DB exists, it reports `Unselected Node not established.` rather than opening/creating IndexedDB merely to inspect state.
- `explicitConnect()` is the only shared Node-establishment path and calls canonical `StegVerseNodeContinuity.registerDevice()` only after explicit user action.
- `explicitSelectNodeClass()` writes class receipts only after explicit user action. Private Sovereign and Main Ecosystem selection can establish their non-resident class boundary; StegOS selection records a request and remains not-established until resident predicates exist. Ecosystem Sovereign StegOS remains eligibility-restricted and has no consumer selection control.
- `node-status.html` explains continuity, explicit consent, capability separation, and links to Node comparison.
- `nodes.html` presents all five types, KV boundary first, and no rank/tier semantics.
- `hugging-face-analysis.html` is migrated from its local Node-status implementation to the canonical shared component while preserving function-specific SV-DN-1 capability testing and refresh fail-closed behavior.
- `scripts/validate_node_status_contract.py` statically enforces the class list, exact labels, passive-resolution non-mutation markers, explainer/product content, restricted ecosystem class, and Hugging Face shared-component binding.

## My KV / Organizational KV integration boundary
The existing My KV surface has substantial continuity, resident DEVICE_KV, file-fallback, profile, and receipt behavior. It must not be rewritten casually. The next phase is to add the shared universal header and an onboarding gate ahead of persistent KV installation:
`static/readable My KV intro → explicit Connect Node if absent → Unselected Node established → required Node-class selection → class verification/provisioning → existing KV installation/profile flow`.

Organizational KV must use the same global status vocabulary while preserving its existing NOT CONNECTED, organization membership, identity, authorization, Interlock, and SKAP boundaries. A public Node-class choice must never create organization membership or grant shared-KV access.

## Custody and authority boundary
The public product/explainer surfaces grant no identity, credential, KV, StegOS, execution, publication, or governance authority. Existing `assets/stegverse-node-continuity.js` remains the canonical Receipt #1 registration path.

## Collision boundary
Do not rewrite Node Receipt #1 semantics. Do not silently change the current 10-execution unregistered Ecosystem Chat behavior while defining the new class contract; inspect and reconcile it explicitly before changing that product behavior. Do not reinterpret existing KV receipts, InTr evidence, or resident StegOS state. Do not make the Ecosystem Sovereign StegOS Node appear generally consumer-orderable unless eligibility semantics are explicitly established.

## Completion state
handoff: ESTABLISHED
pre-work claim: ACTIVE
authentic Hugging Face share-readiness predecessor: COMPLETE_READY_TO_SHARE
machine-readable contract: IMPLEMENTED_ON_BRANCH
shared resolver/header: IMPLEMENTED_ON_BRANCH
page-load persistent mutation prevention: IMPLEMENTED_ON_BRANCH
Node-status explainer: IMPLEMENTED_ON_BRANCH
Node comparison/product page: IMPLEMENTED_ON_BRANCH
Hugging Face shared-component migration: IMPLEMENTED_ON_BRANCH
My KV integration: PENDING
Organizational KV integration: PENDING
validator source: IMPLEMENTED_ON_BRANCH
validator execution: PENDING
merge/deploy/public observation: PENDING

## Remaining machine work
Validate and merge the production foundation, then perform the collision-sensitive My KV and Organizational KV integrations, add/execute their regression coverage, deploy, and publicly observe the new Node production routes and shared status behavior.

## Archive readiness
Not archive-ready. Required public production-page work remains incomplete and is not durably owned by an independent autonomous executor.
