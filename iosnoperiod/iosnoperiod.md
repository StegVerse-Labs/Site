# iOS No-Period Path Handling

This directory documents repository paths that normally begin with a leading dot.

On iOS, leading-dot paths can be difficult to create or move through mobile interfaces. For that reason, this directory records no-leading-dot mirror paths and the canonical destination paths they correspond to.

## Current mapped workflow

| No-leading-dot path | Canonical repository path | Purpose |
|---|---|---|
| `iosnoperiod/github/workflows/check-ecosystem-chat.yml` | `.github/workflows/check-ecosystem-chat.yml` | Runs the Ecosystem Chat contract checker on relevant pushes, pull requests, and manual dispatch. |

## Rule

The no-leading-dot mirror is not the active GitHub Actions workflow location.

When manual iOS movement is required, copy the mapped no-leading-dot file content into the canonical path shown above.

The active workflow path starts with a leading dot in the repository. It is displayed here without that leading dot as requested: `github/workflows/check-ecosystem-chat.yml`.
