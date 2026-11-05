# G17 workflow-surface minimization: Site handoff

Goal: G17-WORKFLOW-SURFACE-MINIMIZATION (StegVerse-Labs/.github#167/#168), under
StegVerse-org/.github#166. Rule: at most 2 workflow files per repository, 3 by a
documented exception. Validators fold into `.github/workflows/validation-dispatcher.yml`,
which runs `tools/tasks/task_catalog.json` through `tools/tasks/run_catalog.py`.
Each folded original is kept byte-for-byte under `tools/tasks/folded/` with its sha256
in `control/workflow-surface-registry.json`.

## Batches

Each batch PR folds about 15 `pull_request`/`push` validators that need no credential and
return ALLOW through the catalog runner on main's tree. Every other surface keeps an exception
record (`KEEP_PENDING_LATER_BATCH`, or kept as a writer or credential-bound surface), and
`ceiling_fail_closed.workflow_count` names the exact remaining count.

Each batch branch has one pre-work claim under `data/session-work-claims.d/G17-SITE-*.json`.
The claim names this handoff, and it is released when that batch's PR is merged.

## Remaining work

- Fold the next ~15 credential-free validators per batch until only writers,
  credential-bound, workflow_run and issue-triggered surfaces remain.
- Repair, in their own PRs, validators whose current steps fail on main's tree, and
  validators whose steps re-initialize the checkout. Fold them after that.

## Boundaries

- No secret, token, credential, dependency, cron, dispatch or polling is added or changed.
- The SKAP Vault inside KV is the only PII and credential store for every user, the
  ecosystem's own included.
- No data file is deleted. Stored session-work claims that name folded workflow
  paths are left unedited.

## Round 68 note (P4 a65c67bf)

B12 (StegFin phone observer fold, Site#1653 @ `91eadc66`) released. B13 converts `conectrr-live-verification.yml` job-level `if` to an early NOT_SELECTED select step (pre-image sha256 `e6abdd45bcd07d2fe0c8659752314add641760fbc4c125173e8b206287f59bba` under `tools/tasks/folded/`). Workflow count remains 97 / FAIL_CLOSED on the exception ceiling.
