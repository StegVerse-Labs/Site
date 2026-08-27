# Site StegOS KnowledgeVault Capability Shell Mirror Handoff

Updated: 2026-08-27

```text
repository: StegVerse-Labs/Site
issue: #534
branch: feature/stegos-kv-capability-shell-site-534
claim: SITE-STEGOS-KV-CAPABILITY-SHELL-534-20260827
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
source_authority: StegVerse-Labs/StegOS
source_merge: 4dad89be44e472eb4a5db10bfd294ded803d1456
source_handoff: StegVerse-Labs/StegOS/docs/STEGOS_KV_CAPABILITY_SHELL_VIEW_MIRROR_HANDOFF.md
credential_authority: TV/TVC
authority_effect: NONE
activation_effect: false
```

## Goal

Project the merged StegOS KnowledgeVault capability shell view-model onto the existing public `/stegos-node/` surface.

The Site projection is rendering only. StegOS remains authoritative for the shell semantics; KnowledgeVault remains authoritative for readiness state; Interlock/InTr remains the governed transition boundary.

## Current source state

The current validated StegOS/KV chain resolves to:

```text
installed entries: 46
locally available: 45
locally blocked: 1
single local blocker: stegid-continuity / BLOCKED_CURRENT_IDENTITY
governed controls enabled: 0
governed controls disabled: 46
activation_performed: false
authority_effect: NONE
```

## Projection requirements

The public Node surface must render four deterministic sections:

```text
Available Modules
Available Services
Blocked Modules
Blocked Services
```

Each capability card must preserve:

```text
entry_type
entry_id
install_state=INSTALLED_INACTIVE
local_state
governed control present
governed control enabled only from source view-model
exact governed blockers
```

Locally blocked entries must show the exact local blocked reason.

## Authority boundary

The Site projection must not expose:

- an activation control;
- KV mutation authority;
- provider execution authority;
- identity authority;
- governance authority;
- Node/peer/Network admission authority.

Required invariants:

```text
authority_effect=NONE
activation_effect=false
runtime_activation_claimed=false
network_activation_claimed=false
provider_execution_available=false
kv_state_mutation_available=false
activation_control_present=false
```

## Existing Site surfaces that must remain unchanged

- Register Device / Receipt #1 semantics;
- one-action Register & Export Evidence flow;
- physical evidence export schema;
- offline-reload proof;
- Personal KV sync display;
- StegOS Network sync display;
- canonical Device History.

Historical Site #468, #480 and #488 are released and are incidental dependencies only.

## Collision boundary

Active HIL upload work and Site #491 generic login/KV onboarding are separate live owners. This lane does not claim their files or dependency surfaces.

## Completion gates

```text
exact pre-work claim: COMPLETE
dedicated handoff: COMPLETE
source projection implementation: COMPLETE_ON_BRANCH
source tests/validator: COMPLETE_ON_BRANCH
Site handoff orchestrator on PR: NEXT
ecosystem heartbeat orchestration on PR: NEXT
merge: PENDING
post-merge exact public observation: PENDING
release to StegOS readiness lane: PENDING
runtime activation: NOT CLAIMED
```


## Implemented source state

```text
public surface: stegos-node/index.html
renderer: stegos-node/stegos-node.js
cache migration: stegos-node/service-worker.js -> stegos-node-shell-v2-kv-capabilities
validator: scripts/check_stegos_node_projection.py
tests: tests/test_stegos_node_projection.py

projected entries: 46
local available: 45
local blocked: 1
governed enabled: 0
governed blocked: 46
stegid-continuity local state: BLOCKED_CURRENT_IDENTITY
activation control: absent
KV mutation: unavailable
provider execution: unavailable
authority effect: NONE
```

The Site projection is bound to the current canonical KV readiness snapshot Git blob and the merged StegOS capability-shell view-model commit. No runtime fetch from GitHub or a third party is introduced.
