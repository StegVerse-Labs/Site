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
```

## Built Files

```text
index.html
governed-ecosystem.html
ecosystem-chat.html
scripts/check_site_governed_ecosystem_mirror.py
scripts/check_site_governed_ecosystem_public_verification.py
scripts/check_site_governed_ecosystem_live_url.py
scripts/check_site_homepage_governed_ecosystem.py
scripts/check_site_public_paths.py
scripts/check_site_llm_free_tier_trust.py
scripts/run_site_task.py
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json
docs/SITE_PUBLIC_PATHS.md
docs/LLM_FREE_TIER_TRUST_STATUS.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
docs/SITE_MIRROR_HANDOFF.md
```

## Workflow Standard

```text
Active workflow 1: .github/workflows/validate.yml
Role: bootstrap validation gate
Runs: scripts/run_site_task.py validate

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
ecosystem-chat.html includes a display-only Bounded free-tier trust display mirrored from StegVerse-org/LLM-adapter free_tier_trust metadata.
site-task-runner.yml now carries the former validation, readiness, mirror, TT, evidence, autonomous continuation, live URL, and ingest tasks.
```

## Checkers

```text
python scripts/run_site_task.py validate
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
