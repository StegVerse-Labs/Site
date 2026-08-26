# Site Orchestration Repair

## Scope

This record preserves the structural repair that converts `Site Task Runner` from an independently triggered automation surface into a downstream worker governed by the successful `Site Bootstrap Validate` result.

## Installed repair

```text
Upstream owner: Site Bootstrap Validate
Downstream worker: Site Task Runner
Authorized mutation/deployment trigger: successful workflow_run on main
Authoritative checkout: exact upstream head_sha
Manual dispatch: validation-only
Direct push authority: disabled
Schedule authority: disabled
Pull-request authority: disabled for worker
Superseded run policy: cancel-in-progress
Generated-state commit marker: [skip ci]
```

Relevant commits:

```text
aa3fdce23d4a810f515ffe18fe7285025b096b3c
- removed Site Task Runner push and schedule triggers
- bound worker execution to successful Site Bootstrap Validate completion on main
- checked out the exact validated commit
- made manual dispatch validation-only
- enabled superseded-run cancellation

727363f14e59652d88bb58ccfc5f998ef259b72f
- added scripts/check_site_orchestration_contract.py

1838bdf81adb0413577c60c8b0778e68ce19f0e6
- bound scripts/check_site_orchestration_contract.py into scripts/run_site_task.py validate
```

## Canonical progression

```text
repository change
-> Site Bootstrap Validate
-> validation PASS for exact commit SHA
-> Site Task Runner workflow_run
-> all-local validation
-> generated-state mutation, when changed
-> Pages artifact
-> Pages deployment
-> live-route verification
-> External Chat activation evidence
-> terminal task diagnostic and workflow summary
```

Any failed prerequisite stops the same transition. A manual dispatch may validate but may not mutate generated state or deploy.

## Fail-closed orchestration contract

`scripts/check_site_orchestration_contract.py` rejects:

```text
- worker push trigger
- worker schedule trigger
- worker pull_request trigger
- missing successful-bootstrap dependency
- mutation based only on branch context
- non-authoritative checkout
- cancel-in-progress: false
```

The contract is now the first validator executed by the canonical Site task runner.

## Remaining orchestration work

Destination `StegVerse-Labs/Site`:

```text
- observe the first complete Bootstrap -> Task Runner transition after the repair
- retain the first exact failing validator if the transition remains red
- emit a machine-readable terminal orchestration receipt containing upstream run id, exact SHA, task result, deployment result, live-verification result, supersession status, and authority effect
- verify generated [skip ci] commits do not start a second bootstrap transition
- add a workflow-inventory rule preventing other Site workflows from independently deploying the same Pages environment
- add stale temporary-branch inventory and bounded reclamation receipts
```

Destination `master-records/orchestration`:

```text
- custody the terminal Site orchestration receipt
- validate exact-SHA/run-id continuity
- record supersession and terminal transition state
- return reconstruction PASS or fail closed
```

Downstream destinations after zero-blocker Site activation evidence:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

No downstream destination receives mutation, publication, admissibility, release, or execution authority merely because the Site workflow ran or Pages deployed.

## Authority boundary

```text
workflow completion != activation
validation PASS != deployment authority outside the bound transition
Pages deployment != provider execution
live-route reachability != custody
activation evidence != activation unless all receipt gates pass
manual dispatch != mutation authority
branch existence != active task ownership
superseded run != valid continuation
```

## Continuation

Continue from `docs/SITE_MIRROR_HANDOFF.md` first, then this record for the orchestration-specific repair. No routine manual action is assigned to the user.

## 2026-08-26 bootstrap-name drift and semantic public-observation repair

Live inspection after Site#396 R2 merge found that the canonical worker was not starting after successful bootstrap validation. The workflow declared:

```text
workflow_run.workflows: Site Bootstrap Validate
```

while the actual upstream workflow name is:

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority
```

GitHub workflow_run matching is name-based, so successful main bootstrap runs were not producing the required Site Task Runner transition. This is an orchestration defect, not a semantic-command product failure.

Canonical bounded repair lane:

```text
issue: StegVerse-Labs/Site#501
branch: fix/site-task-runner-semantic-live-501
source trigger repair: exact upstream workflow name
semantic live verifier: scripts/check_semantic_shorthand_live_routes.py
existing worker trigger authority: workflow_run only after successful main bootstrap
push authority: false
schedule authority: false
pull_request authority: false
manual dispatch mutation authority: false
credential requirement for semantic public verification: none
authority effect: none
activation effect: false
```

The new semantic live verifier performs fresh network reads against the public Site and requires exact source-byte equality for the deployed Ecosystem Chat page, VACC page, semantic router, Ecosystem semantic bridge, and VACC runtime. It also requires the semantic scripts to precede the current simple-chat runtime. Deterministic slash-command behavior remains separately proven by the canonical Node/static tests; a fresh source fetch is not misrepresented as browser interaction execution.

Completion for #501 requires exact-head claim/orchestration validation, merge, an observed successful Bootstrap -> Site Task Runner transition, and a durable semantic live-verification receipt. The existing downstream Site orchestration chain remains authoritative; no second deployment or public-observer workflow is created.
