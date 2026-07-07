# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: governed ecosystem Site mirror propagation plus bounded LLM free-tier trust display
Repository: StegVerse-Labs/Site
Source repository: StegVerse-Labs/admissibility-wiki
LLM trust source repository: StegVerse-org/LLM-adapter
Target paths: governed-ecosystem.html, ecosystem-chat.html, and docs status surfaces
Activation state: display_only_installed
Live URL state: live_url_checker_and_pending_state_wired
Homepage state: governed_ecosystem_homepage_link_wired
Micro-node return-path state: display_only_installed_on_branch
LLM free-tier trust state: display_only_installed
Public mirror guard state: consolidated_into_site_task_runner
Workflow reduction state: reduced_to_two_active_workflows_plus_disabled_legacy_test_readiness_placeholder
Ecosystem Chat UX state: simplified_to_one_primary_governed_chat_preview_entry_validate_wired_and_status_artifact_installed
```

## Built Files

```text
index.html
governed-ecosystem.html
ecosystem-chat.html
scripts/check_ecosystem_chat_boundary.py
scripts/check_site_governed_ecosystem_mirror.py
scripts/check_site_governed_ecosystem_public_verification.py
scripts/check_site_governed_ecosystem_live_url.py
scripts/check_site_homepage_governed_ecosystem.py
scripts/check_site_public_paths.py
scripts/check_site_llm_free_tier_trust.py
scripts/run_site_task.py
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md
docs/ECOSYSTEM_CHAT_UX_STATUS.md
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json
docs/SITE_PUBLIC_PATHS.md
docs/LLM_FREE_TIER_TRUST_STATUS.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
docs/SITE_MIRROR_HANDOFF.md
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

## Workflow Standard

```text
Active workflow 1: .github/workflows/validate.yml
Role: bootstrap validation gate
Runs: scripts/run_site_task.py validate
Validate now includes: scripts/check_ecosystem_chat_application.py and scripts/check_ecosystem_chat_boundary.py

Active workflow 2: .github/workflows/site-task-runner.yml
Role: stable declared-task execution surface
Runs: scripts/run_site_task.py <task>
Tasks: all-local, validate, test-readiness, mirror-readiness, public-guard, live-url, tt-status, external-evidence, autonomous-continuation, universal-ingest

Legacy placeholder: .github/workflows/test-readiness.yml
Role: disabled superseded file only; direct deletion was blocked by connector safety layer
Triggers: none declared
```

## Current branch addition

```text
Branch: main
governed-ecosystem.html includes a display-only Portable Governed Return Path section and link to the admissibility-wiki source page.
ecosystem-chat.html now uses one primary governed chat preview entry, with SDK/gateway details moved into a secondary technical section.
scripts/check_ecosystem_chat_boundary.py now enforces the single-entry UX contract and checks docs/ECOSYSTEM_CHAT_UX_STATUS.md.
data/headless-tasks/ecosystem-chat-boundary-check-v1.json now declares docs/ECOSYSTEM_CHAT_UX_STATUS.md as an expected input.
scripts/run_site_task.py validate now runs the Ecosystem Chat boundary/UX checker.
site-task-runner.yml now carries the former validation, readiness, mirror, TT, evidence, autonomous continuation, live URL, and ingest tasks.
```

## Checkers

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_boundary.py
python scripts/run_site_task.py test-readiness
python scripts/run_site_task.py mirror-readiness
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py live-url
python scripts/run_site_task.py tt-status
python scripts/run_site_task.py external-evidence
python scripts/run_site_task.py autonomous-continuation
python scripts/run_site_task.py universal-ingest
python scripts/run_site_task.py all-local
```

## Remaining targets

```text
StegVerse-Labs/Site:
  - verify Site Bootstrap Validate passes
  - verify Site Task Runner all-local passes
  - remove disabled .github/workflows/test-readiness.yml if a later connector/local Git path permits deletion
  - update public verification JSON only after live URL passes
  - keep Ecosystem Chat as a single-primary-path preview page

StegVerse-org/StegVerse-SDK:
  - ingest quota/receipt/replay metadata contract from StegVerse-org/LLM-adapter

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after Site mirror validation

admissibility-wiki:
  - downstream summary after Site mirror validation

stegguardian-wiki:
  - downstream summary after Site mirror validation
```

## Handoff instruction

Continue from this file before relying on prior chat context. The complete thread can be archived without needing additional context to continue.
