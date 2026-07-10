# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing the StegVerse-Labs/Site build without prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Primary surface: ecosystem-chat.html
Activation state: phase_8_backend_authority_handshake_preview_installed
Live backend state: not installed
Site local mode: preserved true
Live provider invocation: false
Live solver execution: false
Site authority state: DENY preview
Site execution state: NOT_ATTEMPTED
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
- governed solver fixture with proof steps, units, verification, and resource limits
- backend authority-handshake request and response fixtures
- explicit identity, delegation, policy, evidence freshness, operation allowlist, resource limit, provider, solver, authority, execution, and receipt fields
- deterministic authority result DENY
- deterministic execution result NOT_ATTEMPTED
- local mode preserved after denial
- replayable request and reconstructable decision posture
- local SDK manifest and receipt-window previews
- restricted-admin fail-closed routing
```

## Documentation Mesh

```text
Endpoint registry: data/ecosystem-documentation-endpoints.json
Cross-wiki health: data/cross-wiki-health-status.json
Validator: scripts/check_documentation_mesh_status.py
Validation surfaces: scripts/run_site_task.py validate and public-guard
Current health state: pending_live_peer_checks
```

Canonical endpoints:

```text
https://stegverse-labs.github.io/Site/
https://stegverse-labs.github.io/admissibility-wiki/
https://stegverse-002.github.io/stegguardian-wiki/
https://stegverse-labs.github.io/stegtalk-wiki/
```

Documentation discovery and health records do not grant authority, execution standing, admissibility, receipt standing, or cross-repo control.

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
fixtures/ecosystem-chat/authority-handshake-request.example.json
fixtures/ecosystem-chat/authority-handshake-response.example.json
data/ecosystem-documentation-endpoints.json
data/cross-wiki-health-status.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_traversal.py
scripts/check_ecosystem_chat_provider_status.py
scripts/check_ecosystem_chat_solver_response.py
scripts/check_ecosystem_chat_authority_handshake.py
scripts/check_site_hps_visualization.py
scripts/check_site_unified_governed_experience.py
scripts/check_documentation_mesh_status.py
scripts/run_site_task.py
docs/hps/ecosystem-chat-visualization.md
docs/ECOSYSTEM_CHAT_PROVIDER_STATUS.md
docs/ECOSYSTEM_CHAT_SOLVER_STATUS.md
docs/ECOSYSTEM_CHAT_AUTHORITY_HANDSHAKE.md
docs/SITE_MIRROR_HANDOFF.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands, access credentials, mutate repositories, grant authority, or grant admissibility.
A local hash must not be described as an authority-issued receipt.
HPS, traversal, provider, solver, and authority-handshake inputs must fail closed when preview contracts are not satisfied.
Provider fixture values must not be described as live provider state, current pricing, actual billing, account quota, or model availability.
Solver fixture values must not be described as live execution or independent verification.
Handshake schema existence must not be treated as backend activation.
An authority ALLOW would still not itself equal execution.
Payment, quota, provider availability, solver correctness, endpoint registration, or documentation health must never be treated as execution standing.
```

## Validation surface

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_application.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/check_ecosystem_chat_traversal.py
python scripts/check_ecosystem_chat_provider_status.py
python scripts/check_ecosystem_chat_solver_response.py
python scripts/check_ecosystem_chat_authority_handshake.py
python scripts/check_site_hps_visualization.py
python scripts/check_site_unified_governed_experience.py
python scripts/check_documentation_mesh_status.py
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The consolidated task runner includes traversal, provider-status, solver-response, authority-handshake, and documentation-mesh checks in `validate` and `public-guard` where applicable.

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
3. Define the first positive authority-handshake test without enabling execution.
4. Define live provider response provenance and pricing-source requirements.
5. Define live solver operation allowlist, independent verification posture, and receipt path.
6. Do not change STEGVERSE_LOCAL_MODE until a governed backend independently validates the handshake at commit time.
7. Do not update public verification JSON until the live URL checker confirms deployed state.
```

### StegVerse-org/StegVerse-SDK

```text
- ingest interaction profile and bands
- ingest HPS, provider, solver, and authority-handshake posture
- independently reconstruct identity, delegation, policy, evidence freshness, operation allowlisting, and resource limits
- return explicit authority, execution, provider, solver, pricing, and receipt results
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
Phase 9: positive authority-evaluation fixture that can return ALLOW while execution remains NOT_ATTEMPTED.

The positive fixture must use verified identity, valid delegation, current policy, fresh complete evidence, an allowlisted bounded operation, and non-zero but constrained resource limits. It must still prove that authority and execution are separate transitions and that Site cannot issue the governing receipt.
```

## Handoff instruction

Continue from this file before relying on prior conversation context. The complete thread is ready for archiving; no additional part of the thread is needed to move forward.
