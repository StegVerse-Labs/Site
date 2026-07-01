# External Reviewable Artifact Repos

## Source of truth

The source standard and registry remain in `StegVerse-Labs/repo-standards`:

```text
standards/external-reviewable-artifact-repos.md
registries/external-reviewable-artifact-repos.json
```

## Purpose

This page exposes the externally reviewable artifact repo standard to the site/docs surface without changing the underlying registry scope.

## Initial registered artifact repo

```text
StegVerse-Labs/soil-to-structure-matrix
```

Status: externally reviewable as a research artifact and readiness automation system.

## Required artifact repo handoff files

```text
README.md
FINAL_HANDOFF.md
HANDOFF.md
ARCHIVAL.md
```

## Required artifact repo status outputs

```text
reports/final_handoff_status.json
reports/repository_completion_status.json
```

## Required artifact repo command

```bash
python tools/final_handoff_automation.py
```

## Boundary

This site page is an index only. It preserves registry visibility but does not change repo authority, review status, release status, or deployment status.
