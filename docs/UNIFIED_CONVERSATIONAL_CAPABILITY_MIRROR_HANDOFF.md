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
HIL owner: StegVerse-Labs/Site#81/#136
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

Dedicated pages may remain deterministic guides, deep specialty workspaces, compatibility routes, proof surfaces, or transition destinations. They are not alternate primary chat shells.

## Shared capability contract

Every capability family must declare:

- one shared public conversational entry;
- one canonical runtime owner or an explicitly bounded exception;
- deterministic specialty classification signals;
- source/evidence policy;
- authority boundary;
- execution/custody/reconstruction requirements;
- completion evidence requirements;
- no false completion from static UI, fixtures, CI, assignment, or handoff state.

The machine-readable contract is `data/unified-conversational-capabilities.json` and is validated by `scripts/check_unified_conversational_capabilities.py` plus `tests/test_unified_conversational_capabilities.py`.

## Current implementation state

```text
contract_handoff: INSTALLED_ON_TASK_BRANCH
machine_contract: INSTALLING
validator: INSTALLING
tests: INSTALLING
legacy semantic reconciliation: PENDING
runtime activation: OWNED BY EXISTING CANONICAL RUNTIME LANES
product completion: INCOMPLETE
```

No contract, issue, task, branch, CI pass, or merge constitutes runtime activation.

## Exit gates

`TASK-2026-0007` is complete only when:

1. the shared machine-readable capability contract exists and validates;
2. VACC and Mathematics are represented as specialty profiles consumed through `ecosystem-chat.html`;
3. general Ecosystem Chat remains the default/general capability rather than a separate provider stack;
4. HIL remains a capability family with an allowed experiment-specific surface exception but is discoverable from the unified surface;
5. legacy four-app/two-entry status records no longer imply competing primary chat products;
6. deterministic validation passes on the task branch;
7. the task branch is reviewed and merged through a PR.

Product-level 100% for Site#239 remains separate and requires real deployed execution, StegGate where applicable, persistence/custody/reconstruction, and direct public evidence for all four capability-family gates.

## Collision boundary

Do not create a second provider/runtime authority, second VACC runtime, second mathematics runtime, second heartbeat, or replacement StegGate. This task changes the shared contract and semantic classification only.

## Continuation

After contract reconciliation, execution continues through existing canonical owners. VACC runtime activation remains under Site#113 + `StegVerse-org/LLM-adapter`; Mathematics remains under Site#240 and shared runtime/tool owners; HIL remains under Site#81/#136; general runtime remains the common Ecosystem Chat substrate.
