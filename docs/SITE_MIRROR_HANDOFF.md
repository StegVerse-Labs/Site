# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: governed ecosystem Site mirror propagation
Repository: StegVerse-Labs/Site
Source repository: StegVerse-Labs/admissibility-wiki
Target path: governed-ecosystem.html and docs status surfaces
Activation state: display_only_installed
Guard state: governed_ecosystem_public_verification_pending_wired
Public path state: governed_ecosystem_registered
Live URL state: live_url_checker_present
```

## Built Files

```text
governed-ecosystem.html
scripts/check_site_governed_ecosystem_mirror.py
scripts/check_site_governed_ecosystem_public_verification.py
scripts/check_site_governed_ecosystem_live_url.py
scripts/check_site_public_paths.py
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json
docs/SITE_PUBLIC_PATHS.md
github/workflows/site-public-mirror-status-guard.yml
github/workflows/site-governed-ecosystem-live-url.yml
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. Actual repository paths include the leading dot.

## Public Governed Ecosystem Page

```text
governed-ecosystem.html
```

## Source repository

```text
StegVerse-Labs/admissibility-wiki
```

## Checkers

```text
python scripts/check_site_governed_ecosystem_mirror.py
python scripts/check_site_governed_ecosystem_public_verification.py
python scripts/check_site_governed_ecosystem_live_url.py
python scripts/check_site_public_paths.py
```

## Guard workflows

```text
github/workflows/site-public-mirror-status-guard.yml
github/workflows/site-governed-ecosystem-live-url.yml
```

## Boundary

Site is display-only for this surface. The wiki remains the source repository for governed ecosystem vocabulary, capability lifecycle framing, and capability status examples.

## Remaining targets

```text
StegVerse-Labs/Site:
  - run public mirror status guard
  - run governed ecosystem live URL workflow
  - update public verification JSON only after live URL passes

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after Site mirror validation

stegguardian-wiki:
  - downstream summary after Site mirror validation
```

## Handoff instruction

Continue from this file before relying on prior chat context.
