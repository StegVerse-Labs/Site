# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

Canonical path: `docs/SITE_MIRROR_HANDOFF.md`

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: workflow-consolidation-and-validator-progression
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: PREVIEW_ONLY
Live backend: not installed
Live provider invocation: false
Live solver execution: false
Live signatures: false
Verified receipt issuer: false
Workflow target: exactly two operational repository workflows
Result: BOUNDED_REPAIRS_INSTALLED_LIVE_VALIDATION_PENDING
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
  -> all-local
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

The inventory records every repository workflow file, its triggers, job presence, operational classification, write permissions, secret use, artifact upload, Pages deployment, git push, and release/tag capability.

Installed commits:

```text
0f6b1500b58176d98995cacd6147fe352111bb27
  initial workflow inventory writer

fd8901c9c0e83bc7571072158c44b46bf369d190
  operational workflow inventory guard

cc508ec835e5bf8582f2fca7c76812e0c7ef90c9
  has_jobs and operational classification added

7a804a258a12c576de05dbef0caf1c09dd45c7e5
  Bootstrap now enforces the two-operational-workflow guard
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

## Latest Site Task Runner evidence

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
Artifact digest: sha256:3f9ac587c82b970d5ae9114b163b78889baf5464fcf278ca926a913cea9d9680
```

Exact failure:

```text
docs/ECOSYSTEM_CHAT_UX_STATUS.md missing required text: credential
```

Bounded repair installed:

```text
File: docs/ECOSYSTEM_CHAT_UX_STATUS.md
Commit: eb33a3eb1563fe712ef0aff8a6242fa1dc4b85d9
Change: explicit credential access prohibition added
Authority effect: NONE
Workflow change: none
Live verification: pending
```

No validator was weakened. No deployment, release, tag, merge, credential use, or authority expansion occurred.

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
```

The Site importer verifies the orchestration export receipt, artifact name, SHA-256, record count, and authority boundary before replacing the local projection.

Supported states remain:

```text
LOCAL_FALLBACK_ACTIVE
RECEIPTED_EXPORT_IMPORTED
```

Neither state grants execution, admissibility, custody, reconstruction, or final-receipt authority.

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
- verify commit eb33a3e progresses beyond validator 2
- inspect and repair only the next recorded validator if one fails
- verify workflow inventory guard passes
- register scripts/check_site_workflow_inventory.py in validate and public-guard task surfaces
- verify validate and public-guard both pass
- verify exactly one post-bootstrap all-local run
- run import-governed-transition-index through Site Task Runner
- verify governed-transitions.html, index, and import-status routes
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
1. Verify Site Bootstrap Validate passes on the latest main head.
2. Verify the workflow inventory reports exactly two operational workflows.
3. Verify exactly one post-bootstrap all-local run is created.
4. Inspect its diagnostic and confirm validator 2 passes.
5. Repair only the next recorded validator if one fails.
6. Register the workflow inventory guard in validate and public-guard task surfaces.
7. Verify validate and public-guard both pass.
8. Run import-governed-transition-index.
9. Verify public governed-transition routes.
```

## Release posture

No release tag is authorized. Validation, successful artifact acquisition, public-route verification, custody, reconstruction, and chat linkage remain incomplete.

## Archive readiness

This handoff contains the current Site architecture, authority boundaries, workflow consolidation state, latest diagnostic, installed repair, remaining work, and continuation order. Earlier conversation context is not required; the complete thread is ready for archiving.
