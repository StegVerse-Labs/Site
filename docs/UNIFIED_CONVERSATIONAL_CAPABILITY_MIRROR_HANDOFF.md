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

The existing main-branch StegGate progress machinery consumed the merge and emitted the synchronization commit, proving the merged records remained consumable by the repository's synchronization path.

## Shared browser/device-local conversational runtime

The primary chat no longer gives a canned non-VA capability response. PR #402 connected ordinary non-VA conversation to the same admitted device-local StegOS inference bridge already used by the shared surface.

```text
PR: #402
merge: ad0ecdf1b502fda1abb375067da96710c01ec804
shared runtime client: assets/ecosystem-chat-va-runtime.js
primary general client: assets/ecosystem-chat-simple.js
boundary validator: scripts/check_ecosystem_chat_boundary.py
bridge: stegos-bootstrap/ecosystem-chat-bridge.html
```

The shared browser path now exposes `askGeneral`, executes through the device-local bridge, and rejects the result unless the bridge reports:

```text
same_execution: true
reconstruction_state: PASS
```

Short browser-session history is retained separately for general conversation and VACC continuity. VACC still applies its official-VA-grounded specialty behavior instead of using unrestricted general prompting.

The browser/device-local topology has prior real browser proof for the execution mechanism it uses. This shared-runtime merge extends that existing execution path to ordinary Ecosystem Chat prompts; it does not convert the browser proof into evidence for the separate resident sovereign-carrier topology.

## Typed state/task endpoint propagation

The organization state-language control plane now projects the current unified-conversation state into actual Site worker-task endpoints without granting execution authority.

Canonical source projection:

```text
StegVerse-Labs/.github/control/task-projections/unified-conversational-capability.json
source state hash: b01c9197a735eed4f5a460320db1fec01ea5a232d0a4fd87884809ac7d47e3b7
```

Installed Site endpoints:

```text
data/tasks/UNIFIED-CONVERSATION-MATH-SPECIALTY-001.json
data/tasks/UNIFIED-CONVERSATION-HIL-SPECIALTY-001.json
```

Both endpoints are `PROJECTED_PENDING_SEPARATE_ADMISSION`, remain `UNCLAIMED`, require source-state revalidation before any claim/fence, and fail closed if the canonical source-state hash changes. The projection does not replace or widen the resident owners:

```text
Math execution owner: Site#240 + existing shared runtime/tool owners
HIL execution owner: Site#81/#136/#243 + existing participant/experiment lane
```

The projection layer must not create a second primary chat, second provider/runtime lane, new credential authority, release authority, or activation authority. Material endpoint propagation must emit an append-only state-alignment packet and Master Records custody record.

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

Current execution accounting remains machine-owned in `data/steggate-four-app-status.json`; the historical `four-app` term there is compatibility/accounting terminology only.

## Runtime topology distinction

```text
browser/device-local service-worker topology: real execution mechanism previously browser-proven; now shared by general + VACC conversation
resident sovereign carrier/server topology: distinct lifecycle and evidence path; not substituted by browser proof
```

Neither topology invalidates the other. Do not request redundant browser proof merely to satisfy evidence belonging to the resident carrier path.

## Collision boundary

- Do not create a second primary conversational surface.
- Do not create a second VACC provider/runtime lane.
- Do not create a second mathematics provider/runtime lane.
- Do not duplicate heartbeat, TVC route authority, StegGate, or Master Records custody authority.
- No NON-TV/TVC secret/token.
- Model output does not grant authority.

## Next executable work

Continue product activation rather than additional topology reconciliation. The highest-value open paths are:

1. emit and custody the append-only alignment transition for the newly materialized Math/HIL Site task endpoints;
2. consume/record the shared browser runtime as actual capability-family execution evidence where its existing proof satisfies the applicable gate;
3. advance the distinct resident carrier chain from its current machine state without asking the user to re-prove the browser topology;
4. let the resident Math and HIL owners consume the state-bound projections only after preclaim revalidation;
5. propagate only after each capability's real activation/release condition passes.
