# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: receipted-executor-activation-projection-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: PREVIEW_ONLY
Live backend: not installed
Workflow target: exactly two operational workflows
Result: LOCAL_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING
```

## Canonical workflow progression

```text
Site Bootstrap Validate
-> Site Task Runner
-> acquire governed transition projection and activated executor handoff
-> all-local validation
-> commit bounded generated state on main
-> deploy Pages
-> verify transition page, index, import status, and executor projection
```

Active workflows remain:

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Governed transition observatory

```text
governed-transitions.html
assets/governed-transitions.js
data/governed-transition-index.json
data/governed-transition-index-import-status.json
data/governed-executor-status.json
scripts/acquire_governed_transition_index.py
scripts/import_governed_transition_index.py
scripts/check_governed_transition_observatory.py
scripts/check_governed_transition_index_import.py
scripts/check_governed_transition_live_urls.py
```

Supported import states:

```text
LOCAL_FALLBACK_ACTIVE
RECEIPTED_EXPORT_IMPORTED
```

Neither state grants execution, admissibility, executor activation, final-receipt, custody, or reconstruction authority.

## Receipted executor activation projection

The existing orchestration export artifact now includes:

```text
reports/governed_executor_handoff.active.generated.json
```

Site imports that file into:

```text
data/governed-executor-status.json
```

The projection displays:

```text
from_executor.status = FALLBACK_ONLY
to_executor.status = ACTIVE
activation.state = ACTIVE
activation_receipt_id = executor-activation-receipt:stegverse-ai:example-001
transition_id
run_id
```

The projection is bounded:

```text
projection_grants_execution_authority = false
projection_grants_publication_authority = false
projection_grants_admissibility = false
projection_is_master_records_custody = false
activation_is_per_transition_authority = false
```

Executor activation indicates eligibility to receive governed work. It is not per-transition execution authority and Site cannot activate an executor.

## Ecosystem Chat transition identity

Every browser-local chat interaction creates a preview candidate with:

```text
transition_id
run_id
event_id
origin_manifest_id
origin_class = SITE_INPUT
lifecycle_state = DECLARED
parent_transition_id
previous_receipt_id
```

The candidate targets:

```text
repository:StegVerse-Labs/hybrid-collab-bridge
```

The candidate remains explicitly non-authorizing:

```text
admissibility_result = PENDING
commit_time_validity = PENDING
action_ref = null
final_receipt_id = null
master_record_status = NOT_YET_SUBMITTED
reconstruction_status = NOT_YET_CHECKED
raw_shell_allowed = false
execution_authorized = false
receipt_issued = false
```

## Current cross-repository path

```text
Ecosystem Chat / SDK / LLM-adapter
-> canonical DECLARED candidate
-> hybrid-collab-bridge
-> Ecosystem-Delegation
-> Standing-Proof-Engine
-> master-records/orchestration
-> receipted native executor activation
-> governed transition final receipt
-> Master-Records custody
-> reconstruction
-> Site projection
```

## Non-negotiable boundary

```text
Site may draft, classify, visualize, filter, and emit preview candidates.
Site must not execute, mutate repositories, access credentials, grant admissibility or delegation, sign receipts, issue final receipts, admit Master-Records records, or claim reconstruction success.
Site must not activate executors.
A local hash is not a final receipt.
A Site candidate is not execution authority.
Executor activation is not per-transition execution authority.
A projection is not source authority.
```

## Validation surface

No workflow was added. The existing observatory checker now verifies:

```text
executor projection exists
native executor is ACTIVE
bootstrap executor is FALLBACK_ONLY
activation receipt is present
all projection authority flags remain false
browser renderer loads the executor projection
artifact acquisition requires the activated handoff member
```

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
- current PR validation evidence
- verify deployed executor projection route

Downstream after validation:
- StegVerse-Labs/admissibility-wiki
- GCAT-BCAT-Engine/Publisher
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit
```

## Next task

```text
1. Verify Site validation passes with the executor activation projection.
2. Import the latest successful main-branch orchestration artifact when credentials are available.
3. Verify the deployed governed-transitions page renders the ACTIVE/FALLBACK_ONLY states and activation receipt.
4. Propagate verified status downstream only after current-main and deployed-route evidence exists.
```

## Release posture

No release tag is authorized until current PR validation and deployed-route evidence exist.

## Archive readiness

This handoff contains the current Site architecture, transition identity linkage, receipted executor projection, authority boundaries, remaining work, and continuation order. Earlier conversation context is not required; the complete thread is ready for archiving.
