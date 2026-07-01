# Site Standards Handoff

## Purpose

This handoff tells reviewers how to inspect the site-facing standards mirror and where to verify the authoritative registry.

## Site-facing files

```text
docs/standards/README.md
docs/standards/external-reviewable-artifact-repos.md
docs/standards/external-reviewable-artifact-repos-status.md
```

## Site-local validation

```bash
python tools/standards_mirror_automation.py
```

Expected output:

```text
ALLOW standards_mirror_automation_passed
```

## Authoritative source

The authoritative standard and registry remain in:

```text
StegVerse-Labs/repo-standards
```

Authoritative paths:

```text
standards/external-reviewable-artifact-repos.md
registries/external-reviewable-artifact-repos.json
```

## Initial registered artifact repo

```text
StegVerse-Labs/soil-to-structure-matrix
```

## Reviewer sequence

1. Inspect the Site index files.
2. Run the Site-local validator.
3. Verify the source registry in `repo-standards`.
4. Inspect the registered artifact repo handoff files.

## Boundary

This handoff is for reviewer navigation only. It does not change source registry scope, repo review status, release status, deployment status, or downstream routing.
