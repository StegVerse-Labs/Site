# Transition Experimental Engine v1

This bundle upgrades the Transition Periodic Table into a static-output experimental engine.

## What it adds

- `tools/transition_experimental_orchestrator.py`
- dependency-aware experiment selection
- parallel-ready sandbox run manifests
- ledger rows
- knowledge deltas
- review queue
- 3D lattice coordinates
- generated transition detail pages

## Workflow path

The bundle preserves this real GitHub Actions path:

```text
.github/workflows/transition-experimental-engine.yml
```

If upload blocks the leading-dot folder, create the workflow manually with GitHub's **Create new file** path field.

## Operating rule

The engine runs one eligible experiment per workflow run, then stops.
