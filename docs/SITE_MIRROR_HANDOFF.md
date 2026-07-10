# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing the StegVerse-Labs/Site build without prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Primary surface: ecosystem-chat.html
Activation state: phase_6_bounded_provider_status_preview_installed
Live backend state: not installed
Live provider invocation: false
Current pricing state: not asserted
Site authority state: none
Site execution state: disabled
Receipt issuance state: not issued by Site
Workflow standard: exactly two active workflows
```

## Installed Ecosystem Chat capabilities

```text
- single primary governed chat entry
- local route and transition-intent classification
- contextual continuation panel
- INTRA / INTER / RESEARCH / PROVIDER / SOLVER / RECEIPT interaction bands
- fixture-bound HPS heartbeat and standing visualization
- visible standing, continuity, capability windows, replay, reconstruction, and chain-head posture
- bounded traversal preview: request -> intent -> boundary -> evidence -> destination -> receipt
- fixture-bound provider routing, fallback, quota, usage, cost, and latency visualization
- provider state explicitly NOT_INVOKED
- current pricing explicitly false
- billable usage explicitly zero
- provider latency explicitly unavailable/null
- local SDK manifest and receipt-window previews
- restricted-admin fail-closed routing
- math-solver routing preview without live solver execution
```

## Built files central to the current phase

```text
ecosystem-chat.html
assets/ecosystem-chat.js
assets/ecosystem-chat-hps.js
assets/ecosystem-chat-traversal.js
assets/ecosystem-chat-provider.js
fixtures/ecosystem-chat/hps-visualization-status.example.json
fixtures/ecosystem-chat/provider-status.example.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_traversal.py
scripts/check_ecosystem_chat_provider_status.py
scripts/check_site_hps_visualization.py
scripts/check_site_unified_governed_experience.py
scripts/run_site_task.py
docs/hps/ecosystem-chat-visualization.md
docs/ECOSYSTEM_CHAT_PROVIDER_STATUS.md
docs/SITE_MIRROR_HANDOFF.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands, access credentials, mutate repositories, grant authority, or grant admissibility.
A local hash must not be described as an authority-issued receipt.
HPS, traversal, and provider inputs must fail closed when their preview contracts are not satisfied.
Provider fixture values must not be described as live provider state, current pricing, actual billing, account quota, or model availability.
Payment, quota, or provider availability must never be treated as execution standing.
Technical SDK and gateway details remain secondary and collapsible.
```

## Validation surface

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_application.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/check_ecosystem_chat_traversal.py
python scripts/check_ecosystem_chat_provider_status.py
python scripts/check_site_hps_visualization.py
python scripts/check_site_unified_governed_experience.py
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The consolidated task runner includes traversal and provider-status checks in both `validate` and `public-guard`.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Active workflow 2: .github/workflows/site-task-runner.yml

Do not create additional workflows for HPS, traversal, provider, solver, cost, quota, or usage. Add validators and declared tasks behind the two stable workflows.
```

## Remaining targets

### StegVerse-Labs/Site

```text
1. Verify validate and all-local on the current main branch.
2. Confirm GitHub Pages publishes HPS, traversal, and provider preview surfaces.
3. Add a governed math-solver response fixture and checker before live solver execution.
4. Define the backend authority handshake required to change STEGVERSE_LOCAL_MODE.
5. Define live provider response provenance and pricing-source requirements.
6. Do not update public verification JSON until the live URL checker confirms deployed state.
```

### StegVerse-org/StegVerse-SDK

```text
- ingest interaction profile and bands
- ingest transition intent and destination
- ingest HPS display posture without treating display as authority
- ingest provider status, fallback, quota, usage, cost, and latency posture
- return explicit live_invocation, pricing_current, authority, execution, and receipt fields
```

### StegVerse-org/LLM-adapter

```text
- implement bounded provider-routing contract
- provide quota and free-tier counters with provenance
- provide cost and latency accounting schema
- provide fallback posture
- preserve no-capability-by-payment governance rule
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
Phase 7: governed math-solver response fixture, proof-step posture, units, verification result, and fail-closed checker.

Begin with fixtures and validators. Do not enable live solver execution until a backend authority handshake, bounded operation allowlist, resource limits, result verification, and receipt path are defined.
```

## Handoff instruction

Continue from this file before relying on prior conversation context. The complete thread is ready for archiving; no additional part of the thread is needed to move forward.
