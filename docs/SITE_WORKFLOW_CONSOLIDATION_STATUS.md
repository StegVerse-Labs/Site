# Site Workflow Consolidation Status

## State

The Site repository is reduced to two active workflow surfaces:

1. `.github/workflows/validate.yml`
   - Role: bootstrap validation gate.
   - Command: `python scripts/check_ecosystem_chat_application.py`.

2. `.github/workflows/site-task-runner.yml`
   - Role: stable declared-task execution surface and GitHub Pages deployment surface.
   - Runs only after successful bootstrap validation when invoked by `workflow_run`.
   - Manual dispatch remains available for declared task selection.

## Disabled placeholder

`.github/workflows/cfp_ingest_standings_polls.yml` remains as a triggerless comment-only placeholder because connector deletion was blocked. It declares no `on:` block and no jobs.

## Current verification boundary

Connector-visible workflow status was not available for the newest repair commit when this file was written. Green is not claimed until Site Bootstrap Validate and Site Task Runner both pass visibly.

## Next actions

- Verify Site Bootstrap Validate passes.
- Verify Site Task Runner `all-local` passes and deploys Pages.
- Remove the disabled CFP placeholder when a later connector/local Git path permits deletion.
