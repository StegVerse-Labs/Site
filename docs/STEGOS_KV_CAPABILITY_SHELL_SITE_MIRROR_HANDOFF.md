# Site StegOS KnowledgeVault Capability Shell Mirror Handoff

Updated: 2026-08-27

```text
repository: StegVerse-Labs/Site
issue: #534
branch: validate/stegos-kv-capability-shell-live-534
claim: SITE-STEGOS-KV-CAPABILITY-SHELL-534-20260827
state: LIVE_PRODUCTION_OBSERVATION_IN_PROGRESS
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
source tests/validator: COMPLETE_MERGED
original implementation PR #537: MERGED 4a0674fa4cfb8a307833c4f434fa9db0b144e492
original PR source observer: PASS / LIVE STEP SKIPPED BY PR EVENT
validation continuation: REOPENED ON SAME #534 CLAIM
observer receipt tightened to require KV shell source + public markers: IMPLEMENTED_ON_BRANCH
Site handoff orchestrator on validation PR: PENDING
ecosystem heartbeat orchestration on validation PR: PENDING
observer repair merge: PENDING
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


## Reopened completion correction — 2026-08-27

Issue #534 was automatically closed when PR #537 merged, but inspection of workflow run `33041487729` showed the live observation step was skipped because the run was a pull-request event.

That means the source projection was merged, but the handoff's explicit post-merge public-observation gate had not actually been satisfied.

The same canonical issue/claim was reopened rather than creating a duplicate lane.

Validation branch:

`validate/stegos-kv-capability-shell-public-534`

Observer repair:

- main/push path includes this handoff and #534 claim;
- observation receipt requires both `STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS` and `STEGOS_NODE_KV_CAPABILITY_SHELL_PUBLIC_OBSERVATION_PASS`;
- source receipt similarly requires both offline-proof and KV-shell source PASS markers;
- no activation or authority semantics change.

Completion still requires a non-PR main observation against `https://stegverse.org/stegos-node/`.


## Live-validation branch — 2026-08-27

The merge-triggered workflow did not instantiate after PR #539 because the merge was performed through the connected GitHub App and did not recursively schedule a push Actions run.

To preserve the original completion gate without weakening normal PR behavior, the existing observer now performs the live production fetch on the exact validation branch:

`validate/stegos-kv-capability-shell-live-534`

This branch is observer/claim/handoff only. The capability shell source itself was already merged in PR #537.

The live observer must fetch:

`https://stegverse.org/stegos-node/`

and emit:

```text
STEGOS_NODE_KV_CAPABILITY_SHELL_PUBLIC_OBSERVATION_PASS
STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
NETWORK_ACTIVATION_CLAIMED=false
```

Only that observed run can release #534.
