# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing the StegVerse-Labs/Site build without prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Primary surface: ecosystem-chat.html
Activation state: phase_5_bounded_traversal_preview_installed
Live backend state: not installed
Site authority state: none
Site execution state: disabled
Receipt issuance state: not issued by Site
Workflow standard: exactly two active workflows
```

## Installed Ecosystem Chat capabilities

```text
- single primary governed chat entry
- local route classification
- local transition-intent classification
- contextual continuation panel
- INTRA / INTER / RESEARCH / PROVIDER / SOLVER / RECEIPT interaction bands
- fixture-bound HPS heartbeat and standing visualization
- fail-closed HPS fixture validation
- visible standing, continuity, capability-window, replay, reconstruction, and chain-head posture
- bounded traversal preview: request -> intent -> boundary -> evidence -> destination -> receipt
- traversal evidence posture: fixture-only
- traversal receipt posture: not-issued
- local SDK manifest and receipt-window previews
- restricted-admin fail-closed routing
- math-solver routing preview without live solver execution
```

## Built files central to this phase

```text
ecosystem-chat.html
assets/ecosystem-chat.js
assets/ecosystem-chat-hps.js
assets/ecosystem-chat-traversal.js
data/ecosystem-chat-transition-intents.json
fixtures/ecosystem-chat/hps-visualization-status.example.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_traversal.py
scripts/check_site_hps_visualization.py
scripts/check_site_unified_governed_experience.py
scripts/run_site_task.py
docs/hps/ecosystem-chat-visualization.md
docs/SITE_MIRROR_HANDOFF.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands.
Site must not access credentials or secrets.
Site must not mutate repositories.
Site must not grant authority or admissibility.
Site must not describe a local hash as an authority-issued receipt.
Site must fail closed when HPS or traversal inputs do not satisfy the preview contract.
Technical SDK and gateway details remain secondary and collapsible.
The hero must not become a multi-entry task launcher or repository control panel.
```

## Validation surface

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_application.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/check_ecosystem_chat_traversal.py
python scripts/check_site_hps_visualization.py
python scripts/check_site_unified_governed_experience.py
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The consolidated task runner now includes the traversal checker in both `validate` and `public-guard`.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Role: bootstrap validation gate

Active workflow 2: .github/workflows/site-task-runner.yml
Role: declared-task execution plus GitHub Pages deployment

No additional workflow should be created for Ecosystem Chat traversal, HPS, provider, solver, cost, or usage work. Add validators and declared tasks behind the two stable workflows.
```

## Remaining targets

### StegVerse-Labs/Site

```text
1. Verify validate and all-local on the current main branch.
2. Confirm GitHub Pages publishes the visible HPS panel and traversal behavior.
3. Preserve preview-only behavior while adding a provider-status contract fixture.
4. Add cost, quota, latency, fallback, and usage fields as bounded display contracts before live provider calls.
5. Add a governed math-solver response fixture and checker before live solver execution.
6. Define the backend authority handshake required to change STEGVERSE_LOCAL_MODE.
7. Do not update public verification JSON until the live URL checker confirms the deployed state.
```

### StegVerse-org/StegVerse-SDK

```text
- ingest interaction_profile
- ingest interaction_bands
- ingest math_solver_supported
- ingest transition_intent and transition_destination
- ingest HPS display posture without treating display as authority
- return explicit authority, execution, receipt, replay, reconstruction, quota, cost, and provider fields
```

### StegVerse-org/LLM-adapter

```text
- provide bounded provider-routing contract
- provide quota and free-tier counters
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
Phase 6: bounded provider-status, cost, quota, latency, and usage visualization contract.

The next phase should begin with fixtures and validators, not live provider execution. The public page may display declared provider posture only when it remains clearly distinguished from actual model invocation, current pricing, authority, execution, or proof.
```

## Handoff instruction

Continue from this file before relying on prior conversation context. The complete thread is ready for archiving; no additional part of the thread is needed to move forward.
