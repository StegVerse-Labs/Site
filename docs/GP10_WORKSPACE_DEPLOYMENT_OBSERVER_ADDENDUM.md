# GP10 Workspace Deployment Observer Addendum

Status: INSTALLED — MACHINE-OWNED RETRY
Updated: 2026-08-02
Canonical handoff: `docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`
Canonical task: `data/operations/gp10_workspace_tasks.json#GP10-SITE-DEPLOYMENT-OBSERVATION`

## Gap corrected

The original Site security workflow validated committed repository source but did not prove that GitHub Pages was serving that source. Repository file presence and a static-check PASS therefore could not satisfy deployment observation.

## Installed observer

- Script: `scripts/check_gp10_workspace_deployment.py`
- Workflow: `.github/workflows/gp10-workspace-security.yml`
- Receipt: `validation/gp10-workspace-deployment-receipt.json`
- Artifact: `gp10-workspace-security-<commit>`

The observer fetches both unlisted hosted pages with cache-busting query values and bounded retries. It fails closed unless:

1. each response is HTTP 200;
2. each hosted response exactly equals the checked-out committed file bytes;
3. local and hosted SHA-256 values therefore match;
4. both pages expose the required CSP, no-referrer, security-script, noindex, and no-execution-authority markers.

A pull-request run emits `BLOCKED` rather than comparing an undeployed branch against deployed main.

## Deterministic state

- `PASS`: both deployed pages exactly match committed source and all required markers are present.
- `FAILED`: network failure, deployment lag beyond bounded retries, byte mismatch, or missing marker.
- `BLOCKED`: pull-request source is not eligible to prove main-branch deployment.
- `RETRY`: canonical task state until a workflow receipt is inspected.

## Authority boundary

The receipt proves only correspondence between the named committed files and the observed static deployment. It does not prove evidence truth, user identity, authentication, custody, approval, federal certification, commercial release, or execution authority.

## Continuation

The repository-native workflow owns the next execution. The originating chat session owns no observation claim and is not required for retry, diagnosis, or receipt inspection.
