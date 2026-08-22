# Unified Conversational Capability Mirror Handoff

## Source of truth

This is the authoritative continuation record for `TASK-2026-0007` and `StegVerse-Labs/Site#239`.

```text
Goal: one primary governed conversational surface with specialty capability families
Repository: StegVerse-Labs/Site
Branch: claim/unified-conversational-capabilities-site-239-r1
Canonical issue: StegVerse-Labs/Site#239
Task: StegVerse-Labs/.github/tasks/TASK-2026-0007.json
Primary public surface: ecosystem-chat.html
Runtime owner: StegVerse-org/LLM-adapter
VA specialty owner: StegVerse-Labs/Site#113
Mathematics specialty owner: StegVerse-Labs/Site#240
HIL owner: StegVerse-Labs/Site#81/#136/#243
Canonical StegGate owner: StegVerse-Labs/StegCore#68
```

## Product topology

The public product has one primary conversational entry. Capability families are selected behind that surface and must not create competing general chat/provider/runtime stacks.

```text
user request
-> ecosystem-chat.html
-> shared intent/context classification
-> capability family selection
-> governed evidence/tool/runtime route
-> conversational response
-> separately admitted transition/action when required
```

Capability families:

```text
general_ecosystem
vacc_va
mathematics_educator
hil_experiment
```

Dedicated pages may remain deterministic guides, deep specialty workspaces, compatibility routes, proof surfaces, or transition destinations. HIL may retain an experiment-specific participant surface. None becomes a second primary general chat application.

## Shared capability contract

Machine contract: `data/unified-conversational-capabilities.json`.
Validator: `scripts/check_unified_conversational_capabilities.py`.
Tests: `tests/test_unified_conversational_capabilities.py`.

Every capability family consumes `ecosystem-chat.html`, rejects alternate primary chat stacks, retains a bounded source/evidence policy, and carries explicit deployed execution evidence requirements. The HIL specialty destination is canonically `humans-as-interoperability-layer.html`; an earlier incorrect `hil-experiment.html` contract value was corrected on this branch and is now protected by validator/test assertions.

## Legacy semantic reconciliation

The following records have been rewritten on this task branch so they no longer define competing primary chat products:

```text
docs/STEGGATE_FOUR_APP_MIRROR_HANDOFF.md
data/steggate-four-app-status.json
scripts/check_steggate_four_app_status.py
docs/TWO_ENTRY_POINTS_MIRROR_HANDOFF.md
data/two-entry-points-execution-state.json
docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
math-solver/README.md
docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md
```

Historical `four-app` and `two-entry` names remain only where needed for continuity/schema/synchronizer compatibility. Their machine semantics explicitly classify those names as historical gate/accounting terminology rather than product topology authority. Existing runtime/CI evidence in the four-app status was retained while the topology semantics were corrected.

## Current implementation state

```text
contract_handoff: INSTALLED
machine_contract: INSTALLED
validator: INSTALLED
unit tests: INSTALLED
legacy four-app semantic reconciliation: IMPLEMENTED
legacy two-entry semantic reconciliation: IMPLEMENTED
VACC specialty semantic reconciliation: IMPLEMENTED
Mathematics specialty semantic reconciliation: IMPLEMENTED
HIL specialty destination reconciliation: IMPLEMENTED
Site unified-status reconciliation: IMPLEMENTED
four-app synchronizer compatibility markers: RESTORED
PR: StegVerse-Labs/Site#400
PR state: READY FOR MERGE / MERGEABLE OBSERVED
runtime activation: OWNED BY EXISTING CANONICAL RUNTIME LANES
product completion: INCOMPLETE
```

No contract, issue, task, branch, CI pass, or merge constitutes runtime activation.

## VACC runtime note

VACC is consumed through the shared public surface. The browser/device-local topology has prior real browser evidence for the execution path it actually proves. The distinct resident sovereign-carrier/server topology retains its own evidence requirement. Neither topology invalidates the other.

## Exit gates

`TASK-2026-0007` is complete only when:

1. the shared machine-readable capability contract exists and validates;
2. VACC and Mathematics are represented as specialty profiles consumed through `ecosystem-chat.html`;
3. general Ecosystem Chat remains the default/general capability rather than a separate provider stack;
4. HIL remains a capability family with an allowed experiment-specific surface exception and correct canonical destination while remaining discoverable from the unified surface;
5. legacy four-app/two-entry status records no longer imply competing primary chat products;
6. repository validation/synchronization passes on the merged state;
7. PR #400 is merged.

The repository's existing `StegGate four-app progress` workflow is push-to-main validation/synchronization, so final hosted validation is necessarily observed on the merge commit rather than fabricated from PR mergeability. A failed merged-state validator remains an open task and must be repaired immediately; merge itself is not completion.

Product-level 100% for Site#239 remains separate and requires real deployed execution, StegGate where applicable, persistence/custody/reconstruction, and direct public evidence for all four capability-family gates.

## Collision boundary

Do not create a second provider/runtime authority, second VACC runtime, second mathematics runtime, second heartbeat, or replacement StegGate.

## Next executable work

Merge PR #400, observe the existing main-branch synchronization/validation workflow, repair any failure rather than treating merge as success, then return immediately to runtime activation through the existing VACC/general/math/HIL owners.
