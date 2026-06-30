# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: governed ecosystem Site mirror propagation
Repository: StegVerse-Labs/Site
Source repository: StegVerse-Labs/admissibility-wiki
Source path: governed ecosystem public pages and capability status surface
Target path: governed-ecosystem.html and docs status surfaces
Activation state: display_only_installed
Self-management state: repository_managed_continuation_ready
Guard state: governed_ecosystem_checker_wired
```

## Built Files

```text
governed-ecosystem.html
scripts/check_site_governed_ecosystem_mirror.py
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
github/workflows/site-public-mirror-status-guard.yml
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. Actual repository paths include the leading dot.

## Public Governed Ecosystem Page

Site exposes a public HTML mirror surface:

```text
governed-ecosystem.html
```

The source pages are maintained in:

```text
StegVerse-Labs/admissibility-wiki
```

The checker is:

```text
python scripts/check_site_governed_ecosystem_mirror.py
```

The status document is:

```text
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
```

The guard workflow is displayed without the leading dot:

```text
github/workflows/site-public-mirror-status-guard.yml
```

## Boundary

Site is display-only for this surface. The wiki remains the source repository for governed ecosystem vocabulary, capability lifecycle framing, and capability status examples.

This mirror does not create production authority, release authorization, operational standing, or connector installation.

## Remaining targets

```text
StegVerse-Labs/Site:
  - run public mirror status guard
  - public deployment verification

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after Site mirror validation

stegguardian-wiki:
  - downstream summary after Site mirror validation
```

## Handoff instruction

Continue from this file before relying on prior chat context.
