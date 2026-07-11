# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

Canonical handoff path: `docs/SITE_MIRROR_HANDOFF.md`

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: first-failing-validator-repair-installed
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
Result: BOUNDED_VALIDATOR_REPAIR_INSTALLED_VALIDATION_PENDING
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
scripts/run_site_task.py
```

Expected public route after deployment:

```text
https://stegverse-labs.github.io/Site/governed-transitions.html
```

The page displays the canonical relational fields and projection provenance, including import state, source repository or fallback, source receipt and commit, hash verification, and live-feed status.

## Import contract

`master-records/orchestration` exports `governed-transition-index-export`, containing the generated index and an export receipt. The Site importer verifies the receipt, artifact name, SHA-256, record count, and authority boundary before replacing the local projection.

Supported states remain `LOCAL_FALLBACK_ACTIVE` and `RECEIPTED_EXPORT_IMPORTED`. Neither state grants execution, admissibility, custody, reconstruction, or final-receipt authority.

## Fail-path diagnostic contract

Installed repository-local diagnostics:

```text
scripts/run_site_task.py
reports/site-task-diagnostic.json
.github/workflows/site-task-runner.yml
```

For every declared task, the task runner now writes a machine-readable diagnostic containing:

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

No workflow was added. The diagnostic is evidence of task execution only. It is not a final receipt, admissibility result, custody record, execution authority, deployment authorization, or production issuer verification.

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
Run: 29162235846
Commit: ddae4ec4a122e1ec1a60832ae4556c5dab7765f8
Selected task: all-local
Diagnostic artifact: site-task-diagnostic-29162235846-1
Artifact digest: sha256:74bdc68249c3f5ba03dc5fee15bf5d68575b94e18b5bf4f34bae4a2124aab140
Diagnostic status: FAILED
Failed validator: scripts/check_ecosystem_chat_application.py
Validator index: 1
Exit code: 1
Authority effect: NONE
Site mode: PREVIEW_ONLY
State change authorized: false
```

The diagnostic artifact was generated and uploaded successfully. It identified the first failing validator without inference.

The nested validator output showed that all AI-entry checks, cross-wiki metadata graph checks, and media-pipeline mirror checks passed except one exact handoff declaration:

```text
FAIL docs/SITE_MIRROR_HANDOFF.md missing docs/SITE_MIRROR_HANDOFF.md
```

This was a repository-local documentation contract mismatch. The handoff now contains the canonical path declaration `docs/SITE_MIRROR_HANDOFF.md`. No validator was weakened, and no deployment, receipt, custody, admissibility, execution, or external-repository boundary changed.

## Latest bounded build

```text
Commit: 3d0096f7ca9017df68529625f5604895750f9e18
File: scripts/run_site_task.py
Change: stream validator output while preserving the first failing validator, completed validator sequence, exit code, bounded detail, and no-authority posture in reports/site-task-diagnostic.json.

Commit: 4e924f4f762cbddb061e444b6236aaffd44c53f8
File: .github/workflows/site-task-runner.yml
Change: upload the diagnostic artifact on success or failure and include its key fields in the workflow summary.

Current repair:
File: docs/SITE_MIRROR_HANDOFF.md
Change: restore the exact canonical handoff-path declaration required by the media-pipeline mirror validator and record the diagnostic artifact evidence.
Authority effect: none.
Verification: pending the next validate, public-guard, and all-local runs.
```

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
  - verify the canonical handoff-path repair
  - verify validate and public-guard
  - verify all-local progresses beyond validator 1
  - governed artifact acquisition as a declared task
  - live URL verification for page, index, and import status
  - Ecosystem Chat transition identity linkage

master-records/orchestration:
  - Master-Records custody admission contract
  - reconstruction-result enrichment
  - native StegVerse AI executor handoff

Downstream after validation:
  - StegVerse-Labs/admissibility-wiki
  - GCAT-BCAT-Engine/Publisher
  - StegVerse-002/stegguardian-wiki
  - StegVerse-Labs/Sit
```

## Next task

```text
1. Verify the current Site Task Runner diagnostic no longer fails on the canonical handoff path.
2. Verify validate and public-guard both pass.
3. Inspect any successor diagnostic and repair only the next recorded validator if one fails.
4. Add a declared artifact-acquisition task behind one existing workflow.
5. Add live URL verification for governed-transitions.html, its index, and import status.
6. Add Master-Records custody and reconstruction references only from canonical receipts.
7. Connect Ecosystem Chat interactions to the same transition identities and projection feed.
```

## Archive readiness

This handoff contains the current Site architecture, authority boundaries, diagnostic receipt contract, exact failing validator, bounded repair, remaining work, and next task. Earlier conversation context is not required.
