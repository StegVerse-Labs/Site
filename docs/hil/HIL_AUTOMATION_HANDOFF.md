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

## Import boundary

The Site must not infer external production deployment from the GitHub-hosted observation. A later importer may promote the observed gates only when the receipt scope and authority fields satisfy the target environment policy.

## Human action elimination

Credential values are generated, masked, separated, and discarded by the workflow. No user secret entry is required for the bounded GitHub-hosted proof. Durable-path reuse and process restart are executed automatically. Validation fails closed.
