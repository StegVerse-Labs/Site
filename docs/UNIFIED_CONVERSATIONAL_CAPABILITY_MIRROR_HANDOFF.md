# Unified Conversational Capability Mirror Handoff

## Source of truth

This is the authoritative continuation record for the shared Site conversational topology and `StegVerse-Labs/Site#239`.

```text
Goal: one primary governed conversational surface with specialty capability families
Repository: StegVerse-Labs/Site
Canonical branch: main
Canonical issue: StegVerse-Labs/Site#239
Reconciliation task: TASK-2026-0007 — COMPLETE_MERGED
Primary public surface: ecosystem-chat.html
Shared runtime owner: StegVerse-org/LLM-adapter
Device-local execution surface: StegOS service-worker bridge
VA specialty owner: StegVerse-Labs/Site#113
Mathematics specialty owner: StegVerse-Labs/Site#240
HIL owner: StegVerse-Labs/Site#81/#136/#243
Canonical StegGate owner: StegVerse-Labs/StegCore#68
```

## Product topology

```text
user request
-> ecosystem-chat.html
-> shared intent/context classification
-> capability family selection
-> admitted runtime/evidence/tool path
-> conversational response
-> separately admitted transition/action only when required
```

Capability families:

```text
general_ecosystem
vacc_va
mathematics_educator
hil_experiment
```

Dedicated pages may remain deterministic guides, deep specialty workspaces, compatibility routes, proof surfaces, or experiment-specific destinations. They do not create another primary chat/provider/runtime authority.

## Reconciliation task — COMPLETE_MERGED

TASK-2026-0007 was completed through the current-main reconciliation PR and merged.

```text
superseded PR: #400 — closed during branch rebase/reset; no completion effect
completed PR: #401
merge: cdf68fe70294d43b59607c2991478c2cc4b53546
post-merge synchronizer commit: ddcdd8d8a1c023b4c2e673cb795a701a575679a7
shared contract: data/unified-conversational-capabilities.json
contract validator: scripts/check_unified_conversational_capabilities.py
contract tests: tests/test_unified_conversational_capabilities.py
legacy four-app semantics: RECONCILED
legacy two-entry semantics: RECONCILED
VACC specialty semantics: RECONCILED
Mathematics specialty semantics: RECONCILED
HIL canonical destination: humans-as-interoperability-layer.html
product activation effect from reconciliation: NONE
```

## Shared browser/device-local conversational runtime

PR #402 connected ordinary non-VA conversation to the same admitted device-local StegOS inference bridge already used by the shared surface.

```text
PR: #402
merge: ad0ecdf1b502fda1abb375067da96710c01ec804
shared runtime client: assets/ecosystem-chat-va-runtime.js
primary general client: assets/ecosystem-chat-simple.js
boundary validator: scripts/check_ecosystem_chat_boundary.py
bridge: stegos-bootstrap/ecosystem-chat-bridge.html
```

The shared browser path exposes `askGeneral` and rejects the result unless the bridge reports `same_execution: true` and `reconstruction_state: PASS`. Browser/device-local proof remains distinct from resident sovereign-carrier proof.

## Typed state/task endpoint propagation

The organization state-language control plane has propagated the current unified-conversation state into actual Site worker-task endpoints without granting execution authority.

Canonical upstream source:

```text
StegVerse-Labs/.github/control/state-projections/unified-conversational-capability.json
StegVerse-Labs/.github/control/task-projections/unified-conversational-capability.json
canonical state hash: b01c9197a735eed4f5a460320db1fec01ea5a232d0a4fd87884809ac7d47e3b7
```

Site-local semantic state mirror:

```text
data/state-projections/unified-conversational-capability.json
install commit: 5710cc35d064efc7940310a27356c75b9ba22538
canonical normalized hash: b01c9197a735eed4f5a460320db1fec01ea5a232d0a4fd87884809ac7d47e3b7
```

State-bound task endpoints:

```text
data/tasks/UNIFIED-CONVERSATION-MATH-SPECIALTY-001.json
  state-bound commit: 0bb85acd0dcab3b17c5c51224a45f3190988e754
  resident owner: Site#240

data/tasks/UNIFIED-CONVERSATION-HIL-SPECIALTY-001.json
  state-bound commit: d864c8503bb078b105b415d9d69c9929a58dff1e
  resident owners: Site#81/#136/#243
```

Both tasks remain `PROJECTED_PENDING_SEPARATE_ADMISSION` and `UNCLAIMED`. They now carry top-level `source_state_vector_ref` and `source_state_hash`, which opts them into the WorkerCoordinator semantic-state preclaim guard. The referenced vector is inside the Site repository root, so the guard can re-normalize and hash the current vector immediately before any claim/fence. Missing, unreadable, out-of-root, or stale state fails closed before worker selection or fencing.

This binding does not admit either task, does not take ownership from the resident Math/HIL lanes, and grants no execution, route, credential, publication, release, or activation authority.

## Alignment evidence

Endpoint materialization is preserved append-only as transition 002:

```text
StegVerse-Labs/.github/receipts/state-alignment/ALIGN-UNIFIED-CONVERSATION-SITE-ENDPOINTS-002.json
packet commit: 2f4faafa8bc36dd68aca1d51310849d9ded3911c
Master Records custody commit: 7c98ff3c6244aaf629ca49fd7c886a0dd0fd3a9a
```

The Site-local vector plus WorkerCoordinator preclaim binding is a subsequent material endpoint transition and must be preserved as transition 003 rather than rewriting transition 002.

## Public UI requirement

```text
ordinary language first
technical competency assumption: none
internal architecture hidden by default
contextual links/actions only when useful
no public worker/runtime/receipt jargon unless needed for a user-visible limitation
```

## Completion boundary

Source implementation and semantic reconciliation are not the product-level completion gate. Site#239 remains open until each capability family's required real execution/evidence gates are satisfied for the topology being claimed.

## Runtime topology distinction

```text
browser/device-local service-worker topology: real execution mechanism previously browser-proven; now shared by general + VACC conversation
resident sovereign carrier/server topology: distinct lifecycle and evidence path; not substituted by browser proof
```

## Collision boundary

- Do not create a second primary conversational surface.
- Do not create a second VACC provider/runtime lane.
- Do not create a second mathematics provider/runtime lane.
- Do not duplicate HIL participant/runtime authority.
- Do not duplicate heartbeat, TVC route authority, StegGate, or Master Records custody authority.
- No NON-TV/TVC secret/token.
- Model output does not grant authority.

## Next executable work

1. Emit and custody append-only transition 003 for the Site-local state-vector and preclaim-guard binding.
2. Observe fresh hosted all-object Master Records custody validation; repair only an exact failure without weakening checks.
3. Let resident Math and HIL owners revalidate their own handoffs plus the Site-local source-state hash before any separate admission/claim.
4. Consume/record shared browser runtime as capability-family execution evidence where its existing proof satisfies the applicable gate.
5. Continue the distinct resident carrier chain without re-requesting browser proof.
6. Propagate to Publisher/admissibility-wiki/stegguardian-wiki only after real activation/release predicates pass.
