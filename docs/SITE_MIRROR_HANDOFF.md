# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: receipted-transition-index-import-installed
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
Result: LOCAL_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING
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

## Latest workflow failure

```text
Branch: main
Workflow: Site Task Runner
Job: run-site-task
Run: 29157692302
Commit: 59db1f798dd37e1f9d9620e8e0191e91fd3af613
Result: failed in 12 seconds
Annotations: 2
Selected task: all-local
First failing step: Run declared Site task
Failure class: repository-local declared-task validation failure; exact validator output unavailable from the connector response
```

Verified run context:

- runner provisioning, checkout, Python setup, optional dependency installation, and checked-in TT fallback confirmation succeeded;
- the workflow resolved the push-triggered task to `all-local`;
- canonical TT checkout and TT propagation steps were skipped by declared conditions;
- failure occurred inside `python scripts/run_site_task.py all-local` at `Run declared Site task`;
- commit, Pages configuration, artifact upload, and Pages deployment were skipped;
- no deploy, release, tag, credential access, external-repository mutation, or public authority transition occurred.

The earlier `Site Bootstrap Validate` failure at run `29155796294` remains relevant because `all-local` begins with the same repository-local validation chain. The complete validator output and both annotations remain required before selecting a bounded repair.

## Required evidence before repair

1. both annotation messages from run `29157692302`;
2. complete output from `Run declared Site task`;
3. the first validator invoked by `all-local` that returned nonzero;
4. complete `Validate application` output and annotations from run `29155796294` where available;
5. confirmation that any repair remains preview-only and repository-local.

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
  - all-local validation diagnostic and bounded repair
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
1. Obtain and inspect the complete `Run declared Site task` output and both annotations from run 29157692302.
2. Identify the first failing validator in the `all-local` chain.
3. Repair only that repository-local validator failure.
4. Verify `validate` and `public-guard` both pass.
5. Add a declared artifact-acquisition task behind one existing workflow.
6. Add live URL verification for governed-transitions.html, its index, and import status.
7. Add Master-Records custody and reconstruction references only from canonical receipts.
8. Connect Ecosystem Chat interactions to the same transition identities and projection feed.
```

## Archive readiness

This handoff contains the current Site architecture, authority boundaries, exact latest workflow stage, unresolved evidence, remaining work, and next task. Earlier conversation context is not required.