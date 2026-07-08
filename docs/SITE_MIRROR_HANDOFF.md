# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Source repository: StegVerse-Labs/admissibility-wiki
LLM trust source repository: StegVerse-org/LLM-adapter
Target paths: index.html, ecosystem-chat.html, governed-ecosystem.html, and docs status surfaces
Activation state: phase_2_local_transition_intent_engine_installed
Live URL state: live_url_checker_and_pending_state_wired
Homepage state: ecosystem_chat_primary_operating_surface_installed
Micro-node return-path state: display_only_installed_on_branch
LLM free-tier trust state: display_only_installed
Public mirror guard state: consolidated_into_site_task_runner
Workflow reduction state: two_active_workflows_with_legacy_guard_workflows_retired
Ecosystem Chat UX state: simplified_to_one_primary_governed_chat_preview_entry_validate_wired_and_status_artifact_installed
Ecosystem Chat interaction-band state: local_preview_installed_for_intra_inter_research_provider_solver_receipt
Ecosystem Chat intent state: local_transition_intent_catalog_and_classifier_installed
Math solver band state: preview_routing_installed_no_live_solver_execution
Interaction-band fixture state: request_response_sdk_examples_updated
Interaction-band verifier state: boundary_checker_enforces_preview_telemetry_contract
Unified governed experience state: phase_2_intent_engine_installed
Local completion receipt state: migrated_into_site_task_runner
```

## Built Files

```text
index.html
governed-ecosystem.html
ecosystem-chat.html
assets/ecosystem-chat.js
data/ecosystem-chat-transition-intents.json
fixtures/ecosystem-chat/request.example.json
fixtures/ecosystem-chat/response.example.json
fixtures/ecosystem-chat/sdk-form-payload.example.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_site_unified_governed_experience.py
scripts/check_site_governed_ecosystem_mirror.py
scripts/check_site_governed_ecosystem_public_verification.py
scripts/check_site_governed_ecosystem_live_url.py
scripts/check_site_homepage_governed_ecosystem.py
scripts/check_site_public_paths.py
scripts/check_site_llm_free_tier_trust.py
scripts/write_site_local_completion_receipt.py
scripts/check_site_local_completion_receipt.py
scripts/run_site_task.py
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md
docs/ECOSYSTEM_CHAT_UX_STATUS.md
docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json
docs/SITE_PUBLIC_PATHS.md
docs/LLM_FREE_TIER_TRUST_STATUS.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
docs/SITE_MIRROR_HANDOFF.md
```

## Unified Governed Experience Rule

```text
Site should behave as one governed application, not a flat collection of equal entry pages.
Primary user path:
1. user starts at Ecosystem Chat
2. request is classified
3. boundary is checked
4. evidence route is selected
5. destination is offered as a governed transition
6. receipt/replay path becomes available only when live authority exists

The homepage must emphasize Ecosystem Chat as the primary operating surface.
Demo, Wiki, Papers, Runtime, Formalisms, Product, and Math Solver remain available as transition destinations, not competing starting points.
```

## Local Transition Intent Engine

```text
Catalog: data/ecosystem-chat-transition-intents.json
Browser classifier: assets/ecosystem-chat.js
Validator: scripts/check_ecosystem_chat_boundary.py
Declared task: data/headless-tasks/ecosystem-chat-boundary-check-v1.json
Status doc: docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md

Installed categories:
- Explain
- Demonstrate
- Compare
- Research
- Build
- Replay
- Runtime
- Formalism
- SDK
- Implementation
- Solver

Every local chat preview should include transition intent, suggested transition, transition destination, transition boundary, interaction bands, and no-authority/no-shell posture.
```

## Ecosystem Chat Simplification Rule

```text
ecosystem-chat.html should remain a governed chat preview with one primary user path:
1. user reads the boundary
2. user tries the governed chat preview
3. technical SDK/gateway details remain secondary under a collapsible technical section

Do not re-expand the hero into multiple competing primary buttons.
Do not present the page as a task launcher, demo index, repo control panel, or execution console.
Site remains preview-only and cannot issue receipts, access credentials, execute shell commands, or grant authority.
```

## Ecosystem LLM Interaction Bands

```text
The Ecosystem Chat page is the public preview surface for the future StegVerse Ecosystem LLM interface.
Every interaction should eventually expose transparent routing bands:
- intra: StegVerse repos, wikis, manifests, receipts, standards, and local ecosystem records
- inter: connected adapters, partner systems, provider clients, and external ecosystem nodes
- research: networked sources outside the ecosystem when outside evidence is necessary
- provider: LLM/model calls, model routing, fallback, cost, latency, and quota accounting
- solver: math-problem solver, calculation traces, symbolic checks, unit conversion, and proof-step verification
- receipt: hash, replay, reconstruction, admissibility, continuity, and authority evidence load

Current Site implementation is preview-only. It deterministically classifies local text, renders a local band meter, and suggests a governed transition destination. It does not call providers, search the network, solve math live, issue receipts, or grant authority.
```

## Workflow Standard

```text
Active workflow 1: .github/workflows/validate.yml
Role: bootstrap validation gate
Runs: scripts/check_ecosystem_chat_application.py

Active workflow 2: .github/workflows/site-task-runner.yml
Role: stable declared-task execution surface plus GitHub Pages deployment
Runs: scripts/run_site_task.py <task>
Tasks: all-local, validate, test-readiness, mirror-readiness, public-guard, live-url, tt-status, external-evidence, task-elimination-guard, local-completion-receipt, autonomous-continuation, universal-ingest

Retired legacy workflows:
- .github/workflows/site-mirror-closure-guard.yml
- .github/workflows/site-task-elimination-guard.yml
- .github/workflows/site-mirror-evidence-transition-guard.yml
- .github/workflows/site-local-completion-receipt.yml
```

## Current branch addition

```text
Branch: main
index.html frames Ecosystem Chat as the primary Site operating surface and converts major destinations into governed transition cards.
data/ecosystem-chat-transition-intents.json defines the local transition intent catalog.
assets/ecosystem-chat.js classifies local requests into transition intents and includes transition intent/destination/boundary in responses, local receipt hash payloads, SDK manifest previews, and receipt windows.
docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md records phase-2 local intent engine status and the next contextual continuation panel target.
scripts/check_site_unified_governed_experience.py validates homepage single-entry framing and transition menu status.
scripts/check_ecosystem_chat_boundary.py validates the transition intent catalog, JavaScript classifier, fixture transition fields, single-entry UX contract, and interaction-band preview surface.
data/headless-tasks/ecosystem-chat-boundary-check-v1.json now declares data/ecosystem-chat-transition-intents.json as an expected input.
fixtures/ecosystem-chat/request.example.json now includes transition_intent and transition_destination.
fixtures/ecosystem-chat/response.example.json now includes transition intent, suggested transition, and transition destination text.
fixtures/ecosystem-chat/sdk-form-payload.example.json now includes transition intent metadata in manifest and receipt_window.
scripts/run_site_task.py validate runs the unified governed experience checker and Ecosystem Chat boundary/UX/intent checker.
site-task-runner.yml carries validation, readiness, mirror, TT, evidence, local completion receipt, task-elimination, autonomous continuation, live URL, and ingest tasks.
```

## Checkers

```text
python scripts/run_site_task.py validate
python scripts/check_site_unified_governed_experience.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/run_site_task.py test-readiness
python scripts/run_site_task.py mirror-readiness
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py live-url
python scripts/run_site_task.py tt-status
python scripts/run_site_task.py external-evidence
python scripts/run_site_task.py task-elimination-guard
python scripts/run_site_task.py local-completion-receipt
python scripts/run_site_task.py autonomous-continuation
python scripts/run_site_task.py universal-ingest
python scripts/run_site_task.py all-local
```

## Remaining targets

```text
StegVerse-Labs/Site:
  - verify Site Bootstrap Validate passes
  - verify Site Task Runner all-local passes after local intent engine installation
  - confirm no legacy guard workflows remain active beyond validate.yml and site-task-runner.yml
  - update public verification JSON only after live URL passes
  - keep Ecosystem Chat as a single-primary-path preview page
  - phase 3: build contextual continuation panel using the transition intent result
  - connect live_governed_gateway.py, provider clients, cost model, usage metrics, and math solver behind the preview boundary when backend authority path exists

StegVerse-org/StegVerse-SDK:
  - ingest quota/receipt/replay metadata contract from StegVerse-org/LLM-adapter
  - ingest interaction_profile, math_solver_supported, transition_intent, and transition_destination fields from Ecosystem Chat

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after Site mirror validation

admissibility-wiki:
  - downstream summary after Site mirror validation

stegguardian-wiki:
  - downstream summary after Site mirror validation
```

## Handoff instruction

Continue from this file before relying on prior chat context. The complete thread can be archived without needing additional context to continue.
