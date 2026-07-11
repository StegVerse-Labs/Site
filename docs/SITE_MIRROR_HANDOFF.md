# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

Canonical path: `docs/SITE_MIRROR_HANDOFF.md`

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: governed-transition-acquisition-and-public-verification-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: PREVIEW_ONLY
Live backend: not installed
Live provider invocation: false
Live solver execution: false
Live signatures: false
Verified receipt issuer: false
Workflow target: exactly two operational repository workflows
Result: BOUNDED_IMPLEMENTATION_INSTALLED_LIVE_VALIDATION_PENDING
```

## Non-negotiable boundary

Site may draft, classify, visualize, filter, and link governed transition records.

Site must not execute shell commands from the public surface, access credentials, mutate external repositories, grant admissibility, grant delegation, sign receipts, verify production issuers, issue final receipts, admit Master-Records records, or claim reconstruction success.

A projection is not source authority. A verified export is not a final receipt, execution authority, or Master-Records custody.

## Canonical workflow progression

```text
Pull request:
current conflict-free head
  -> Site Bootstrap Validate / bootstrap-validate

Main:
main push
  -> Site Bootstrap Validate / bootstrap-validate
  -> only after success: Site Task Runner / run-site-task
  -> acquire governed transition projection
  -> all-local
  -> commit generated bounded Site state
  -> deploy Pages
  -> verify governed transition page, index, and import-status URLs
  -> site-task-diagnostic-<run>-<attempt>
```

Only the latest current-head checks count. Historical failures from superseded commits or stale pull requests do not establish current standing.

Canonical workflow files:

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

The task runner retains manual dispatch, schedule, and successful post-bootstrap `workflow_run`. Generated-state commit and Pages deployment remain restricted to `main`.

## Workflow consolidation guard

Installed:

```text
scripts/write_site_workflow_inventory.py
scripts/check_site_workflow_inventory.py
data/site-workflow-inventory.json
```

Completion condition:

```text
operational workflow set = validate.yml + site-task-runner.yml
migration-required operational workflow count = 0
Site Bootstrap Validate = PASS
exactly one post-bootstrap all-local run = PASS
```

A triggerless, jobless placeholder is not operational but remains a cleanup item until explicitly deleted.

## Fail-path diagnostic contract

Installed:

```text
scripts/run_site_task.py
scripts/check_site_task_diagnostic_contract.py
reports/site-task-diagnostic.json
.github/workflows/site-task-runner.yml
```

Every declared task writes:

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

Required invariant:

```text
authority_effect = NONE
site_mode = PREVIEW_ONLY
state_change_authorized = false
```

## Latest recorded Site Task Runner evidence

```text
Workflow: Site Task Runner
Run: 29166812942
Branch: main
Commit: dade2f045e71caa5d9aaf60ac7363ead1e34eca1
Task: all-local
Completed validator 1: scripts/check_ecosystem_chat_application.py
Failed validator 2: scripts/check_ecosystem_chat_boundary.py
Exit code: 1
Failure class: VALIDATION_FAILURE
Authority effect: NONE
Site mode: PREVIEW_ONLY
State change authorized: false
Artifact: site-task-diagnostic-29166812942-1
```

Exact historical failure:

```text
docs/ECOSYSTEM_CHAT_UX_STATUS.md missing required text: credential
```

Bounded repair was installed in commit `eb33a3eb1563fe712ef0aff8a6242fa1dc4b85d9`. Current-head verification remains pending. No validator was weakened.

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
scripts/check_governed_transition_live_urls.py
```

The Site importer verifies the orchestration export receipt, artifact name, SHA-256, record count, and authority boundary before replacing the local projection.

Supported states:

```text
LOCAL_FALLBACK_ACTIVE
RECEIPTED_EXPORT_IMPORTED
```

Neither state grants execution, admissibility, custody, reconstruction, or final-receipt authority.

## Governed artifact acquisition

The existing `Site Task Runner` declares:

```text
import-governed-transition-index
```

Scheduled and post-bootstrap `all-local` runs now acquire before validation. Acquisition behavior:

```text
STEGVERSE_REPO_SYNC_TOKEN available
  -> locate latest successful main Runtime Evidence Validation run
  -> locate non-expired governed-transition-index-export artifact
  -> safely extract only index and export receipt
  -> verify through existing importer
  -> record source run, artifact, receipt, commit, and hash posture

Token or receipted artifact unavailable
  -> preserve LOCAL_FALLBACK_ACTIVE
  -> record explicit acquisition_reason
  -> do not claim receipt, hash verification, live feed, custody, or reconstruction
```

`--require-artifact` is available for strict runs that must fail rather than use fallback.

## Public verification

After Pages deployment, the existing Site workflow retries verification for:

```text
https://stegverse-labs.github.io/Site/governed-transitions.html
https://stegverse-labs.github.io/Site/data/governed-transition-index.json
https://stegverse-labs.github.io/Site/data/governed-transition-index-import-status.json
```

The verifier checks HTTP status, page markers, projection type, records structure, import-state contract, and fallback/receipted-import non-overclaim rules.

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
- verify latest Site Bootstrap Validate
- verify workflow inventory reports exactly two operational workflows
- verify exactly one post-bootstrap all-local run
- verify acquisition state and public URL checks
- register scripts/check_site_workflow_inventory.py in validate and public-guard if not already registered
- connect Ecosystem Chat interactions to preserved transition_id and run_id
- remove triggerless CFP placeholder only when deletion is explicitly authorized

master-records/orchestration:
- consume verified Site import evidence before custody admission
- add Master-Records custody admission contract
- add reconstruction-result enrichment
- register native StegVerse AI executor

Downstream after validation:
- StegVerse-Labs/Site status projection
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
```

## Next task

```text
1. Verify current Site Bootstrap Validate and Site Task Runner results.
2. Confirm acquisition chooses RECEIPTED_EXPORT_IMPORTED when the source artifact and token are available, otherwise explicit fallback.
3. Confirm all three public governed-transition URLs pass after deployment.
4. Add Master-Records custody admission and reconstruction-result enrichment in master-records/orchestration.
5. Connect Ecosystem Chat requests and responses to preserved transition_id and run_id.
```

## Release posture

No release tag is authorized. Validation evidence, successful receipted acquisition, public-route verification, custody, reconstruction, and chat linkage remain incomplete.

## Archive readiness

This handoff contains the current Site architecture, authority boundaries, workflow consolidation state, artifact acquisition, public verification, remaining work, and continuation order. Earlier conversation context is not required; the complete thread is ready for archiving.
