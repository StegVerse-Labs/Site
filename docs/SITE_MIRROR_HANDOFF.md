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
Public mirror guard state: includes_llm_free_tier_trust_checker
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
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json
docs/SITE_PUBLIC_PATHS.md
docs/LLM_FREE_TIER_TRUST_STATUS.md
github/workflows/site-public-mirror-status-guard.yml
github/workflows/site-governed-ecosystem-live-url.yml
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. Actual repository paths include the leading dot.

## Current branch addition

```text
Branch: sync/micro-node-site
governed-ecosystem.html includes a display-only Portable Governed Return Path section and link to the admissibility-wiki source page.
ecosystem-chat.html includes a display-only Bounded free-tier trust display mirrored from StegVerse-org/LLM-adapter free_tier_trust metadata.
site-public-mirror-status-guard.yml now runs scripts/check_site_llm_free_tier_trust.py.
```

## Checkers

```text
python scripts/check_site_governed_ecosystem_mirror.py
python scripts/check_site_governed_ecosystem_public_verification.py
python scripts/check_site_governed_ecosystem_live_url.py
python scripts/check_site_homepage_governed_ecosystem.py
python scripts/check_site_public_paths.py
python scripts/check_site_llm_free_tier_trust.py
```

## Remaining targets

```text
StegVerse-Labs/Site:
  - run public mirror status guard
  - run governed ecosystem live URL workflow
  - update public verification JSON only after live URL passes

StegVerse-org/StegVerse-SDK:
  - ingest quota/receipt/replay metadata contract from StegVerse-org/LLM-adapter

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after Site mirror validation

stegguardian-wiki:
  - downstream summary after Site mirror validation
```

## Handoff instruction

Continue from this file before relying on prior chat context. The complete thread can be archived without needing additional context to continue.
