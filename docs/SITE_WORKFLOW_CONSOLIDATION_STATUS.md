# Site Workflow Consolidation Status

## State

The repository-owned Site workflow target is two active workflow surfaces:

1. `.github/workflows/validate.yml`
   - Role: bootstrap validation gate.
   - Runs the workflow inventory before application validation.

2. `.github/workflows/site-task-runner.yml`
   - Role: stable declared-task execution surface and GitHub Pages deployment surface.
   - Runs automatically only after successful bootstrap validation on `main`.
   - Manual and scheduled declared-task execution remain available.

The Actions page may continue showing thousands of historical runs and GitHub-managed Pages runs. Historical run count is not the current repository workflow-file count.

## Generated inventory

```text
scripts/write_site_workflow_inventory.py
data/site-workflow-inventory.json
```

The inventory records every `.yml` and `.yaml` file under `.github/workflows`, including:

```text
workflow file and display name
triggers
canonical or migration-required classification
contents/pages/id-token permissions
secret usage
artifact upload
Pages deployment
git push
release or tag capability
```

Installed commits:

```text
0f6b1500b58176d98995cacd6147fe352111bb27
  deterministic workflow inventory writer

da7b3139d2b869ffd647e0fe323586f85dc429c6
  Bootstrap inventory execution before application validation
```

## Disabled placeholder

`.github/workflows/cfp_ingest_standings_polls.yml` may remain as a triggerless comment-only placeholder when connector deletion is blocked. It must declare no `on:` block and no jobs, and the inventory must classify its operational effect as inactive before it can be excluded from active-entry-point counting.

## Authority boundary

The inventory does not disable, delete, rename, dispatch, release, tag, deploy, merge, or authorize any workflow. A noncanonical workflow may be retired only after its triggers, permissions, secrets, artifacts, generated files, receipts, and state changes are mapped into a declared task behind one of the two canonical workflows.

Site remains preview-only. Workflow inventory or migration status does not grant admissibility, execution authority, deployment authority, release authority, receipt standing, or Master-Records custody.

## Completion condition

Consolidation is verified only when the generated inventory and current-main runs establish:

```text
canonical operational workflow count: 2
migration-required operational workflow count: 0
Site Bootstrap Validate: PASS
Site Task Runner all-local: PASS
```

A triggerless, jobless placeholder is not an operational workflow entry point but remains a cleanup item until deleted.

## Current verification boundary

Green is not claimed until the next Bootstrap run prints the generated inventory counts and the resulting Site Task Runner diagnostic is inspected.

## Next actions

1. Inspect `data/site-workflow-inventory.json` from the next Bootstrap execution.
2. Separate historical/GitHub-managed Actions runs from repository-owned operational workflow files.
3. Verify any remaining noncanonical file has no trigger and no jobs or migrate it through the declared task runner.
4. Verify Site Bootstrap Validate and exactly one post-bootstrap `all-local` progression on the current `main` head.
5. Remove the disabled CFP placeholder when deletion is explicitly permitted and technically available.
