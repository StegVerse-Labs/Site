# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing the StegVerse-Labs/Site build without prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Primary surface: ecosystem-chat.html
Activation state: phase_7_governed_solver_response_preview_installed
Live backend state: not installed
Live provider invocation: false
Live solver execution: false
Current pricing state: not asserted
Site authority state: none
Site execution state: disabled
Receipt issuance state: not issued by Site
Workflow standard: exactly two active workflows
Documentation mesh state: shared endpoint registry and Site cross-wiki health record installed
```

## Installed Ecosystem Chat capabilities

```text
- single primary governed chat entry
- local route and transition-intent classification
- contextual continuation panel
- INTRA / INTER / RESEARCH / PROVIDER / SOLVER / RECEIPT interaction bands
- fixture-bound HPS heartbeat and standing visualization
- bounded request-to-receipt traversal preview
- fixture-bound provider routing, fallback, quota, usage, cost, and latency visualization
- provider state explicitly NOT_INVOKED
- current pricing explicitly false
- billable usage explicitly zero
- provider latency explicitly unavailable/null
- governed solver fixture with expression, operation class, answer, units, proof steps, verification, and resource limits
- solver state explicitly live_solver_execution=false
- solver verification explicitly fixture-backed and not independent
- local SDK manifest and receipt-window previews
- restricted-admin fail-closed routing
```

## Documentation Mesh

```text
Endpoint registry: data/ecosystem-documentation-endpoints.json
Cross-wiki health: data/cross-wiki-health-status.json
Validator: scripts/check_documentation_mesh_status.py
Validation surfaces: scripts/run_site_task.py validate and public-guard
Public registry URL: https://stegverse-labs.github.io/Site/data/ecosystem-documentation-endpoints.json
Public health URL: https://stegverse-labs.github.io/Site/data/cross-wiki-health-status.json
Current health state: pending_live_peer_checks
```

Canonical endpoints:

```text
https://stegverse-labs.github.io/Site/
https://stegverse-labs.github.io/admissibility-wiki/
https://stegverse-002.github.io/stegguardian-wiki/
https://stegverse-labs.github.io/stegtalk-wiki/
```

These records describe discovery and health posture only. They do not grant authority, execution standing, admissibility, receipt standing, or cross-repo control.

## Built files central to the current phase

```text
ecosystem-chat.html
assets/ecosystem-chat.js
assets/ecosystem-chat-hps.js
assets/ecosystem-chat-traversal.js
assets/ecosystem-chat-provider.js
assets/ecosystem-chat-solver.js
fixtures/ecosystem-chat/hps-visualization-status.example.json
fixtures/ecosystem-chat/provider-status.example.json
fixtures/ecosystem-chat/solver-response.example.json
data/ecosystem-documentation-endpoints.json
data/cross-wiki-health-status.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_traversal.py
scripts/check_ecosystem_chat_provider_status.py
scripts/check_ecosystem_chat_solver_response.py
scripts/check_site_hps_visualization.py
scripts/check_site_unified_governed_experience.py
scripts/check_documentation_mesh_status.py
scripts/run_site_task.py
docs/hps/ecosystem-chat-visualization.md
docs/ECOSYSTEM_CHAT_PROVIDER_STATUS.md
docs/ECOSYSTEM_CHAT_SOLVER_STATUS.md
docs/SITE_MIRROR_HANDOFF.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands, access credentials, mutate repositories, grant authority, or grant admissibility.
A local hash must not be described as an authority-issued receipt.
HPS, traversal, provider, and solver inputs must fail closed when preview contracts are not satisfied.
Provider fixture values must not be described as live provider state, current pricing, actual billing, account quota, or model availability.
Solver fixture values must not be described as live execution or independent verification.
A correct mathematical result does not itself grant authority to act on that result.
Payment, quota, provider availability, or solver correctness must never be treated as execution standing.
Documentation endpoint registration and health records must not be treated as cross-repo authority or peer verification.
Technical SDK and gateway details remain secondary and collapsible.
```

## Validation surface

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_application.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/check_ecosystem_chat_traversal.py
python scripts/check_ecosystem_chat_provider_status.py
python scripts/check_ecosystem_chat_solver_response.py
python scripts/check_site_hps_visualization.py
python scripts/check_site_unified_governed_experience.py
python scripts/check_documentation_mesh_status.py
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The consolidated task runner includes traversal, provider-status, solver-response, and documentation-mesh checks in both `validate` and `public-guard` where applicable.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Active workflow 2: .github/workflows/site-task-runner.yml

Do not create additional workflows for HPS, traversal, provider, solver, cost, quota, usage, authority handshake, or documentation-mesh work. Add validators and declared tasks behind the two stable workflows.
```

## Remaining targets

### StegVerse-Labs/Site

```text
1. Verify validate and all-local on the current main branch.
2. Confirm GitHub Pages publishes HPS, traversal, provider, solver, endpoint-registry, and cross-wiki health surfaces.
3. Define the backend authority handshake required to change STEGVERSE_LOCAL_MODE.
4. Define live provider response provenance and pricing-source requirements.
5. Define live solver execution allowlist, resource limits, independent verification posture, and receipt path.
6. Do not update public verification JSON until the live URL checker confirms deployed state.
```

### StegVerse-org/StegVerse-SDK

```text
- ingest interaction profile and bands
- ingest transition intent and destination
- ingest HPS display posture without treating display as authority
- ingest provider status, fallback, quota, usage, cost, and latency posture
- ingest solver expression, operation class, units, proof steps, verification, and resource-limit posture
- return explicit live_invocation, live_solver_execution, pricing_current, authority, execution, and receipt fields
```

### StegVerse-org/LLM-adapter

```text
- implement bounded provider-routing contract
- provide quota and free-tier counters with provenance
- provide cost and latency accounting schema
- provide fallback posture
- preserve no-capability-by-payment governance rule
```

### Documentation mesh destinations

```text
Installed:
- StegVerse-Labs/Site
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/stegtalk-wiki

Next:
- verify all four public registry and health-record URLs
- compare record schemas and report drift
- promote reusable documentation-mesh standard to StegVerse-Labs/repo-standards
```

### Downstream publication targets

```text
GCAT-BCAT-Engine/Publisher: publication/import awareness after Site validation
StegVerse-Labs/admissibility-wiki: downstream implementation summary after Site validation
stegguardian-wiki: boundary and authority summary after Site validation
StegVerse-Labs/Sit: integration status after Site validation
```

## Next integration goal

```text
Phase 8: backend authority handshake contract for changing STEGVERSE_LOCAL_MODE.

Begin with a machine-readable request/response fixture and validator. The handshake must distinguish identity, delegation, policy, evidence freshness, allowed operation, resource limits, provider/solver posture, authority result, execution result, and receipt result. Do not enable live execution merely because the handshake schema exists.
```

## Handoff instruction

Continue from this file before relying on prior conversation context. The complete thread is ready for archiving; no additional part of the thread is needed to move forward.
