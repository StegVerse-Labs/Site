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

## Round 69 note (P4 a65c67bf)

B13 (Conectrr NOT_SELECTED, Site#1672 @ `144041e7`) released. B14 converts four read-only public observers' observe-job `if: github.event_name != 'pull_request'` to early NOT_SELECTED select steps. Workflow count remains 97 / FAIL_CLOSED on the exception ceiling.

## Round 70 note (P4 a65c67bf)

B14 (four observers NOT_SELECTED, Site#1673 @ `44d2ee64`) released. B15 fully folds `mykv-public-propagation-proof` into the stable dispatcher (catalog group `mykv-public-propagation-proof.validate`); workflow_count 97→96.

## Round 71 note (P4 a65c67bf)

B15 (fold mykv-public-propagation-proof, Site#1674 @ `cb75d51b`) released. B16 fully folds `site-homepage-chat-public-asset-observation` into the stable dispatcher; workflow_count 96→95.

## Round 72 note (P4 a65c67bf)

B16 (fold homepage-chat public-asset observation, Site#1675 @ `455ccf74`) released. B17 fully folds both remaining converted observers (`sv002-sovereign-intr-profile-proof`, `sv002-status-public-http-proof`) into the stable dispatcher; workflow_count 95→93.

## Round 73 note (P4 a65c67bf)

B17 (fold both sv002 observers, Site#1676 @ `f0087fae`) released. B18 fully folds `evaluator-review-ui-validation` and `check-hil-deployed-controlled-cycle-evidence` into the stable dispatcher (anonymous checkout → dispatcher credential-free checkout); workflow_count 93→91.

## Round 74 note (P4 a65c67bf)

B18 (fold evaluator-ui + HIL deployed-cycle, Site#1677 @ `fc741ae0`) released. B19 fully folds `canonical-generated-intr` and `check-tvc-execution-receipt-import` into the stable dispatcher; workflow_count 91→89.

## Round 75 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B19-20261105 released. G17-SITE-WORKFLOW-SURFACE-B20-20261105 fully folds hil-intr-submission-contract, check-hil-end-to-end-protocol, check-hil-v1-upload-surface, check-hil-v1-1-release into the stable dispatcher; workflow_count 89→85.

## Round 76 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B20-20261105 released. G17-SITE-WORKFLOW-SURFACE-B21-20261105 fully folds validate-review-authority-projection, check-stegverse-endpoint-activation-readiness, hil-site-contract, hil-semantic-replay into the stable dispatcher; workflow_count 85→81.

## Round 77 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B21-20261105 released. G17-SITE-WORKFLOW-SURFACE-B22-20261105 fully folds stegbrowser-sv002-lane-adaptation, stegbrowser-sv002-validated-lane-retest, hil-semantic-continuity-tasks, validate-stegos-persistent-card-ux into the stable dispatcher; workflow_count 81→77.

## Round 78 note (P4 a65c67bf)

B22 released. B23 fully folds `check-tidc-research` (multi-job + matrix) into the stable dispatcher; workflow_count 77→76.

## Round 79 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B23-20261105 released. G17-SITE-WORKFLOW-SURFACE-B24-20261105 fully folds validate-physical-economics-report-ui, check-hil-session-consolidation, no-required-third-party-runtime, check-coinbase-skap-intr-route-consumer, va-filing-integration-contract into the stable dispatcher; workflow_count 76→71.

## Round 80 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B24-20261105 released. G17-SITE-WORKFLOW-SURFACE-B25-20261105 fully folds va-federal-plus-security-baseline, va-pii-detection-evaluation, va-pii-model-leakage-evidence, va-pii-production-detector-evidence, va-pii-redaction-credential-realignment, va-pii-redaction-working-copy-evidence into the stable dispatcher; workflow_count 71→65.

## Round 81 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B25-20261105 released. G17-SITE-WORKFLOW-SURFACE-B26-20261105 fully folds va-private-document-runtime, va-governed-product-goals, two-entry-points-execution-state, vacc-goal3-contract-suite, va-claims-chat-surface into the stable dispatcher; workflow_count 65→60.

## Round 82 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B26-20261105 released. G17-SITE-WORKFLOW-SURFACE-B27-20261105 fully folds check-hil-linkedin-launch-readiness, hil-announcement-contract, check-sv002-authentic-runtime-evidence-harness, conectrr-security-overlay, capture-validation-evidence into the stable dispatcher; workflow_count 60→55.

## Round 82 amendment (P4 a65c67bf)

Dropped hil-announcement-contract and check-sv002-authentic-runtime-evidence-harness from B27 after pre-existing content/syntax failures on the fold PR; kept three folds; workflow_count 60→57.

## Round 83 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B27-20261105 released. G17-SITE-WORKFLOW-SURFACE-B28-20261105 fully folds va-claim-assistant-activation, gp10-workspace-security into the stable dispatcher; workflow_count 57→55.

## Round 84 note (P4 a65c67bf)

G17-SITE-WORKFLOW-SURFACE-B28-20261105 released. G17-SITE-WORKFLOW-SURFACE-B29-20261105 fully folds check-hil-live-readiness into the stable dispatcher; workflow_count 55→54.
