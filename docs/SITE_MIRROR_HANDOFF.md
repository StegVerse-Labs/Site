# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

Canonical handoff path: `docs/SITE_MIRROR_HANDOFF.md`

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: second-validator-repair-and-artifact-acquisition-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site remains preview-only
Live backend: not installed
Site local mode: true
Live provider invocation: false
Live solver execution: false
Live signatures: false
Verified receipt issuer: false
Workflow standard: exactly two active workflows
Result: BOUNDED_REPAIRS_AND_DECLARED_ACQUISITION_INSTALLED_VALIDATION_PENDING
```

## Governed transition observatory

Installed:

```text
governed-transitions.html
assets/governed-transitions.js
data/governed-transition-index.json
data/governed-transition-index-import-status.json
scripts/check_governed_transition_observatory.py
scripts/import_governed_transition_index.py
scripts/check_governed_transition_index_import.py
scripts/acquire_governed_transition_index.py
scripts/run_site_task.py
```

Expected public route after deployment:

```text
https://stegverse-labs.github.io/Site/governed-transitions.html
```

The page displays canonical relational fields and projection provenance, including import state, source repository or fallback, source receipt and commit, hash verification, and live-feed status.

## Import contract

`master-records/orchestration` exports `governed-transition-index-export`, containing the generated index and an export receipt. The Site importer verifies the receipt, artifact name, SHA-256, record count, and authority boundary before replacing the local projection.

Supported states remain `LOCAL_FALLBACK_ACTIVE` and `RECEIPTED_EXPORT_IMPORTED`. Neither state grants execution, admissibility, custody, reconstruction, or final-receipt authority.

## Declared artifact acquisition

The existing Site Task Runner exposes:

```text
import-governed-transition-index
```

The task runs:

```text
scripts/acquire_governed_transition_index.py
scripts/check_governed_transition_index_import.py
scripts/check_governed_transition_observatory.py
```

The acquisition script resolves a successful main-branch `Runtime Evidence Validation` run in `master-records/orchestration`, requires the `governed-transition-index-export` artifact, extracts only the generated index and export receipt, and delegates all receipt, hash, record-count, artifact-name, and authority-boundary checks to the existing importer.

Installed commits:

```text
673a32d0125ea1b76a9ee000187a088220a0516e
0a565828c470c476de8617346596143569ae246f
91e6414874d61f3bda2a5bc15f65cb9280b00400
```

No workflow was added. `.github/workflows/site-task-runner.yml` remains one of exactly two active workflows.

## Fail-path diagnostic contract

Installed repository-local diagnostics:

```text
scripts/run_site_task.py
reports/site-task-diagnostic.json
.github/workflows/site-task-runner.yml
```

For every declared task, the task runner writes a machine-readable diagnostic containing:

```text
task
status
failed_validator
validator_index
exit_code
completed_validators
failure_class
detail
authority_effect
site_mode
state_change_authorized
```

The diagnostic is written on validator failure, missing required validator, test-readiness failure, unhandled exception, unresolved task exit, and successful completion.

The existing Site Task Runner uploads the diagnostic with `if: always()` as:

```text
site-task-diagnostic-<workflow_run_id>-<workflow_run_attempt>
```

The diagnostic is evidence of task execution only. It is not a final receipt, admissibility result, custody record, execution authority, deployment authorization, or production issuer verification.

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, filter, and link governed transition records.
Site must not execute shell commands, access credentials, mutate repositories, grant admissibility, grant delegation, sign receipts, verify production issuers, issue final receipts, admit Master-Records records, or claim reconstruction success.
A projection is not the source of truth.
A verified export is not a final transition receipt.
A verified export is not Master-Records custody.
Authority ALLOW remains distinct from execution.
Commit-time validity remains distinct from state change.
Site remains preview-only until a governed backend independently validates transitions and issues verified receipts.
```

## Validation surface

```text
python scripts/check_governed_transition_observatory.py
python scripts/check_governed_transition_index_import.py
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
python scripts/run_site_task.py import-governed-transition-index
```

Both transition validators are registered in `validate` and `public-guard` through the existing task runner.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Active workflow 2: .github/workflows/site-task-runner.yml
```

No workflow was added.

## Latest diagnostic verification

```text
Branch: main
Workflow: Site Task Runner
Job: run-site-task
Run: 29162414799
Commit: 145878cbea0b53ce8820e32b39424d1ea35d3e62
Selected task: all-local
Diagnostic artifact: site-task-diagnostic-29162414799-1
Diagnostic status: FAILED
Completed validator: scripts/check_ecosystem_chat_application.py
Failed validator: scripts/check_ecosystem_chat_boundary.py
Validator index: 2
Exit code: 1
Failure class: VALIDATION_FAILURE
Authority effect: NONE
Site mode: PREVIEW_ONLY
State change authorized: false
```

The prior canonical handoff-path repair passed. The diagnostic advanced deterministically to validator 2.

The second validator reported exact repository-local documentation drift:

```text
docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md missing required text:
raw_shell_allowed
authority_required
rate_limit_required
receipt_required_for_execution
Restricted admin
```

The boundary document now preserves those exact fixture-aligned declarations while retaining preview-only, no-backend, no-execution, and no-authority posture. No validator was weakened.

## Latest bounded builds

```text
Commit: 145878cbea0b53ce8820e32b39424d1ea35d3e62
File: docs/SITE_MIRROR_HANDOFF.md
Change: restore the exact canonical handoff-path declaration.
Verification: passed; validator 1 completed in run 29162414799.

Commit: 14bd5e686f3977fd28036e99a39b1562a0f2dad0
File: docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md
Change: restore exact machine-readable boundary declarations.
Verification: pending.

Commit: 673a32d0125ea1b76a9ee000187a088220a0516e
File: scripts/acquire_governed_transition_index.py
Change: add bounded acquisition of the receipted orchestration export artifact.

Commit: 0a565828c470c476de8617346596143569ae246f
File: scripts/run_site_task.py
Change: register import-governed-transition-index as a declared task.

Commit: 91e6414874d61f3bda2a5bc15f65cb9280b00400
File: .github/workflows/site-task-runner.yml
Change: expose the declared import task through the existing workflow and make generated-state publication rebase-safe.
```

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
- verify the ecosystem boundary-document repair
- verify validate and public-guard
- verify all-local progresses beyond validator 2
- verify import-governed-transition-index against the orchestration export
- verify public page, index, and import-status routes
- connect Ecosystem Chat interactions to preserved transition_id and run_id

master-records/orchestration:
- consume verified Site import evidence before custody admission
- add Master-Records custody admission contract
- add reconstruction-result enrichment
- register native StegVerse AI executor

Downstream after validation:
- StegVerse-Labs/admissibility-wiki
- GCAT-BCAT-Engine/Publisher
- StegVerse-002/stegguardian-wiki
```

## Next task

```text
1. Verify the current Site Task Runner diagnostic no longer fails on scripts/check_ecosystem_chat_boundary.py.
2. Verify validate and public-guard both pass.
3. Inspect any successor diagnostic and repair only the next recorded validator if one fails.
4. Run import-governed-transition-index through the existing Site Task Runner.
5. Verify governed-transitions.html, its index, and import status after deployment.
6. Add Master-Records custody and reconstruction references only from canonical receipts.
7. Connect Ecosystem Chat interactions to the same transition identities and projection feed.
```

## Archive readiness

This handoff contains the current Site architecture, authority boundaries, diagnostic progression, bounded validator repairs, declared artifact-acquisition task, remaining work, and continuation order. Earlier conversation context is not required; the complete thread is ready for archiving.
