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

A selected class may be requested but not yet established. Internally preserve base continuity independently from class predicates so the UI never converts a desired class into proof.

## Universal display contract
The Site-wide top-of-page status format is:
`(NODE_CLASS) Node established. (What is this?)`
or
`(NODE_CLASS) Node not established. (What is this?)`

For a new context the canonical default is:
`Unselected Node not established. (What is this?)`

The universal `What is this?` link points to a concise nontechnical Node-status explanation page. Function-specific sections separately link to their technical/capability test pages.

## Public production surfaces
- Shared read-only Node-state resolver and header component.
- Concise Node-status explainer page.
- Five-type Node comparison/product page.
- My KV onboarding integration: explicit Node connect first, then required Node-type selection before persistent KV setup proceeds.
- Organizational KV integration preserving organization membership/authorization boundaries.
- Hugging Face hub migration from its local prototype header to the canonical shared component while preserving the already-proven explicit-consent semantics.

## Custody and authority boundary
The shared resolver may read existing browser Node continuity but must not mint or mutate state merely to render a header. Explicit connect/class-transition functions must be called only from affirmative user actions. Existing `assets/stegverse-node-continuity.js` remains the canonical Receipt #1 registration path unless another current handoff explicitly supersedes it.

The public product/explainer surfaces grant no identity, credential, KV, StegOS, execution, publication, or governance authority.

## Sequence
1. Establish this handoff and an exclusive pre-work claim.
2. Add a machine-readable five-class Node-status contract.
3. Add the shared resolver/header component and passive default state.
4. Add Node-status explainer and Node comparison/product pages.
5. Integrate the shared header into the Hugging Face hub as a regression/proof consumer.
6. Integrate My KV onboarding, preserving all existing KV custody and installation semantics while requiring explicit Node connection and class selection in the correct order.
7. Integrate Organizational KV without granting organization membership/authorization.
8. Add validators/tests proving page-load non-mutation, exact labels, public-readability, and capability separation.
9. Validate, merge, deploy, and publicly observe the new production surfaces.

## Collision boundary
Do not rewrite Node Receipt #1 semantics. Do not silently change the current 10-execution unregistered Ecosystem Chat behavior while defining the new class contract; inspect and reconcile it explicitly before changing that product behavior. Do not reinterpret existing KV receipts, InTr evidence, or resident StegOS state. Do not make the Ecosystem Sovereign StegOS Node appear generally consumer-orderable unless eligibility semantics are explicitly established.

## Completion state
handoff: ESTABLISHED_ON_FEATURE_BRANCH
pre-work claim: PENDING
machine-readable contract: PENDING
shared resolver/header: PENDING
Node-status explainer: PENDING
Node comparison/product page: PENDING
Hugging Face shared-component migration: PENDING
My KV integration: PENDING
Organizational KV integration: PENDING
validator/test coverage: PENDING
merge/deploy/public observation: PENDING

## Archive readiness
Not archive-ready. Required public production-page work remains incomplete and is not yet durably owned by an independent autonomous executor.
