# iosnoperiod

This repository uses some canonical paths that begin with a leading period, especially GitHub workflow paths.

For iPhone and other clients that make leading-period paths difficult to create or move, workflow files may also be represented under `iosnoperiod/`.

The `iosnoperiod/` mirror is not authoritative. It is a convenience mirror for exact-path bootstrap and review.

## Current mirrored workflows

```text
Canonical: .github/workflows/transition-discovery-public-surface.yml
Mirror: iosnoperiod/github/workflows/transition-discovery-public-surface.yml

Canonical: .github/workflows/validate.yml
Mirror: iosnoperiod/github/workflows/validate.yml
```

## Validate mirror purpose

`iosnoperiod/github/workflows/validate.yml` runs the StegVerse AI Entry Point aggregate validator:

```bash
python scripts/check_ecosystem_chat_ai_entry.py
```

This preserves the max-two-workflows standard by preparing one general validate workflow rather than a goal-specific workflow.

Move or copy a mirror file into the canonical path only if the canonical workflow is missing or needs iOS-safe restoration.
