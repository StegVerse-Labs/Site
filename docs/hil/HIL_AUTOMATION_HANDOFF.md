# HIL Automation Handoff

The active continuation path is automation-first.

## Trigger

Merging the gateway pull request containing `.github/workflows/hil-automated-deployment-proof.yml` causes the proof workflow to run on future HIL gateway changes and permits an immediate manual-free `workflow_dispatch` or push-triggered proof.

## Evidence produced

The workflow emits a `hil-automated-deployment-proof` artifact containing:

- intake readiness before restart;
- intake readiness after restart;
- publication readiness after restart;
- first-process and restarted-process logs;
- `HIL-LIVE-READINESS-OBSERVATION-v2`.

## Governed promotion boundary

The Site does not infer external production deployment from a GitHub-hosted observation. Promotion is controlled by:

- `data/hil-observation-promotion-policy.json`;
- `scripts/import_hil_live_readiness_observation.py`;
- `.github/workflows/import-hil-live-readiness-observation.yml`.

The importer verifies the observation schema, canonical observation hash, Primary and prompt identities, readiness before and after restart, publication readiness, credential separation, durable-path reuse, scope-specific requirements, and explicit non-authority fields.

A `GITHUB_HOSTED_EPHEMERAL_DEPLOYMENT_PROOF` may establish only bounded process-restart, credential-separation, and readiness-contract observations. It may not establish external production deployment, production durable storage, public acquisition authority, publication authority, or Master Record append authority.

An `AUTHORIZED_EXTERNAL_DEPLOYMENT` observation additionally requires an environment identifier, service identifier, persistent-storage reference, operator or automation identity, and deployment commit SHA. Even that scope grants no acquisition, publication, execution, or Master Record authority.

Promoted observations are append-only under `data/hil-observations/<source-observation-sha256>.json`. The workflow defaults to dry-run and requires an explicit apply selection before committing a promoted record.

## Human action elimination

Credential values are generated, masked, separated, and discarded by the gateway proof workflow. No user secret entry is required for the bounded GitHub-hosted proof. Durable-path reuse and process restart are executed automatically. Validation fails closed.

The remaining transfer step is mechanical: place the emitted observation JSON at the selected repository-relative incoming path or otherwise make it available to the import workflow. Promotion never converts bounded evidence into broader authority.
