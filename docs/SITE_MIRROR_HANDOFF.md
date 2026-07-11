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

The page displays the canonical relational fields and now also displays projection provenance:

```text
import state
source repository or local fallback
source receipt
source commit
hash verification status
live orchestration feed status
```

## Import contract

`master-records/orchestration` now exports:

```text
Artifact: governed-transition-index-export
governed_transition_index.generated.json
governed_transition_index.export-receipt.json
```

The Site importer verifies the export receipt, artifact name, SHA-256, record count, and authority boundary before replacing the local projection.

Supported states:

```text
LOCAL_FALLBACK_ACTIVE
  -> checked-in projection fixture
  -> hash_verified: false
  -> live_orchestration_feed: false
  -> no source receipt claimed

RECEIPTED_EXPORT_IMPORTED
  -> orchestration export receipt verified
  -> index SHA-256 verified
  -> still not a live feed
  -> still no execution, admissibility, custody, or reconstruction authority
```

The importer does not silently treat unavailable artifacts as current orchestration state.

## Current cross-repository path

```text
StegVerse-SDK / LLM-adapter
  -> emit DECLARED canonical candidates

hybrid-collab-bridge
  -> preserve identity and attach bridge evidence

Ecosystem-Delegation
  -> preserve identity and attach delegation references

master-records/orchestration
  -> verify bounded intake
  -> govern lifecycle and final receipt
  -> generate transition index
  -> issue hash-bound export receipt

StegVerse-Labs/Site
  -> verify and import the export artifact
  -> or remain on explicit local fallback
  -> render the bounded projection only
```

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
Run: 29155088387
Commit: b62d558
Result: failed in 9 seconds
Annotations: 2
Failure class: unresolved task-runner validation failure
```

The notification does not expose the failing step, selected declared task, or annotation text. The task runner can invoke multiple repository-local validation surfaces, so no speculative file repair, artifact acquisition, deployment, release, tag, external-repository mutation, or live-boundary change is authorized from this notification alone.

Required evidence before repair:

1. first failing step;
2. both annotation messages;
3. declared task selected for the run;
4. command output identifying which validator failed;
5. confirmation that the repair remains preview-only and repository-local.

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
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
1. Verify Site validate and public-guard after the failing task and annotations are identified.
2. Add a declared artifact-acquisition task behind one existing workflow.
3. Add live URL verification for governed-transitions.html, its index, and import status.
4. Add Master-Records custody and reconstruction references only from canonical receipts.
5. Connect Ecosystem Chat interactions to the same transition identities and projection feed.
6. Preserve the same contract when the external bootstrap executor hands off to the StegVerse AI entity.
```

## Archive readiness

This handoff contains the current Site architecture, installed files, authority boundaries, latest workflow blocker, remaining work, and next task. Earlier conversation context is not required.
