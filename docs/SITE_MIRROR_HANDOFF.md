# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat and governed transition observability
Phase: ecosystem-chat-transition-identity-installed
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
-> acquire governed transition projection
-> all-local validation
-> commit bounded generated state on main
-> deploy Pages
-> verify transition page, index, and import status
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

Neither state grants execution, admissibility, final-receipt, custody, or reconstruction authority.

## Ecosystem Chat transition identity

Installed:

```text
assets/ecosystem-chat-transition-identity.js
fixtures/ecosystem-chat/transition-identity.example.json
scripts/check_ecosystem_chat_transition_identity.py
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_chat_receipt_envelopes.py
```

Every browser-local chat interaction now creates a preview candidate with:

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

The transition identity is added to the visible response and local preview receipt line. The same identifiers are also added to the SDK manifest preview.

## Current cross-repository path

```text
Ecosystem Chat / SDK / LLM-adapter
-> canonical DECLARED candidate
-> hybrid-collab-bridge
-> Ecosystem-Delegation
-> Standing-Proof-Engine
-> master-records/orchestration
-> final receipt
-> Master-Records custody
-> reconstruction
-> Site projection
```

## Non-negotiable boundary

```text
Site may draft, classify, visualize, filter, and emit preview candidates.
Site must not execute, mutate repositories, access credentials, grant admissibility or delegation, sign receipts, issue final receipts, admit Master-Records records, or claim reconstruction success.
A local hash is not a final receipt.
A Site candidate is not execution authority.
A projection is not source authority.
```

## Validation surface

The existing receipt-envelope validator now invokes the transition-identity validator, so the current Site `validate` and `public-guard` task paths cover this new contract without adding a workflow.

## Remaining files/modules and destinations

```text
StegVerse-Labs/Site:
- current-main validation evidence for transition identity linkage
- verify public transition routes
- display native executor handoff status when exported by orchestration

master-records/orchestration:
- current-main validation evidence for custody/reconstruction and executor handoff declaration
- executor activation receipt and activation-state transition

Downstream after validation:
- StegVerse-Labs/admissibility-wiki
- GCAT-BCAT-Engine/Publisher
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit
```

## Next task

```text
1. Verify Site validation passes with the chat transition identity contract.
2. Verify orchestration validation passes with the executor handoff declaration.
3. Add an executor activation receipt schema and bounded activation operation.
4. Export executor handoff state through the same Site projection contract.
5. Propagate verified status downstream only after current-main evidence exists.
```

## Release posture

No release tag is authorized. Current-main validation, executor activation, and downstream propagation remain pending.

## Archive readiness

This handoff contains the current Site architecture, installed transition identity linkage, boundaries, remaining work, and continuation order. Earlier conversation context is not required; the complete thread is ready for archiving.
