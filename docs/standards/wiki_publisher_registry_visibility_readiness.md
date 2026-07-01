# Wiki Publisher Registry Visibility Readiness

## Purpose

This note defines the next integration target after Site standards mirror closure: a Publisher or wiki mirror surface that can display registry-backed standards visibility downstream while preserving the `repo-standards` source of truth.

## Upstream source of truth

```text
StegVerse-Labs/repo-standards
```

Authoritative paths:

```text
standards/external-reviewable-artifact-repos.md
registries/external-reviewable-artifact-repos.json
```

## Current Site mirror

```text
docs/standards/README.md
docs/standards/external-reviewable-artifact-repos.md
docs/standards/external-reviewable-artifact-repos-status.md
docs/standards/site_standards_handoff.md
```

## Downstream target expectation

A Publisher or wiki mirror should display:

- the standards title;
- the authoritative source repo;
- the authoritative registry path;
- the initial registered artifact repo;
- the Site mirror path;
- the boundary that downstream display does not change registry authority.

## Required Site validation before downstream display

```bash
python tools/standards_mirror_automation.py
```

## Boundary

This readiness note does not create the downstream mirror. It defines the minimum content and boundary for the next Publisher or wiki integration step.
