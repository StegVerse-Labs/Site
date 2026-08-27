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


## 2026-08-26 first restored worker execution and next exact failure

PR #503 merged the workflow-name repair at `92cb42f737fc3357c0f522b771b8a3afee14bba3`. Main Bootstrap run `33023831125` completed SUCCESS and, for the first time after the name-drift repair, started Site Task Runner run `33023865047` through the intended `workflow_run` dependency.

The worker therefore proved:

```text
bootstrap -> exact-SHA task runner trigger: OBSERVED
source bootstrap run: 33023831125
exact source SHA: 92cb42f737fc3357c0f522b771b8a3afee14bba3
task runner run: 33023865047
trigger restoration: PASS
deployment/live semantic verification: NOT REACHED
```

The first exact worker failure occurred before deployment in the existing all-local validation stage:

```text
validator: scripts/check_ecosystem_chat_traversal.py
failure: current ecosystem-chat.html no longer contains the historical public traversal strip
canonical current UX: user-first single primary governed chat
result: VALIDATOR_DRIFT, not semantic runtime failure
```

The current page and `docs/ECOSYSTEM_CHAT_UX_STATUS.md` intentionally use the simplified user-first chat surface. Follow-up on the same #501 lane updates the traversal validator to accept the current canonical projection while still fail-closing if a legacy traversal script is reintroduced without its bounded visible contract.

Follow-up branch: `fix/site-task-runner-semantic-live-501-r2`.


## 2026-08-26 second restored worker execution and gateway-validator drift

PR #504 merged the current user-first traversal validator alignment at `d6e832a365977072dbad8bd3f7ae8d4d83555208`. Main Bootstrap run `33024114647` completed SUCCESS and started Site Task Runner run `33024139176`.

The worker advanced beyond the repaired traversal gate:

```text
check_ecosystem_chat_traversal.py: PASS
legacy_traversal_public_surface=false
semantic_discovery_before_chat_runtime=true
```

The next exact pre-deployment failure was nested under `scripts/check_ecosystem_chat_receipt_envelopes.py`:

```text
nested validator: scripts/check_ecosystem_chat_gateway_activation.py
failure: node discovery binding missing marker: ecosystem-chat-portable-node
classification: VALIDATOR_DRIFT
```

The canonical identity is already bound in `data/ecosystem-chat-gateway.json` as `discovery.required_node_id=ecosystem-chat-portable-node`. The current discovery implementation intentionally compares `advertisement.node_id` to `discovery.required_node_id` rather than duplicating that identity literal in JavaScript. Follow-up #501 repair therefore validates the dynamic config binding in source while retaining the exact identity check in the canonical config.

Follow-up branch: `fix/site-task-runner-semantic-live-501-r3`.


## 2026-08-27 diagnostic-contract drift after validator-chain repairs

The #501 worker chain continued through bounded successor repairs for unrelated stale validation contracts:

```text
HIL v1.1 compatibility validator: repaired via #506 / PR #507 / merge 3538beebbbeab37550ad62fb1e9c2d1e7e9788a1
HPS user-first visualization validator: repaired via #508 / PR #509 / merge 1d3fe52d7035ec729e89f4a65c6fe4b4c367724c
unified governed experience status validator: repaired via #510 / PR #511
unified hero formatting boundary R2: repaired via PR #513 / merge 0eaa4286d8e863ba5dd6b9a9ec17334d30a0a012
```

Main Bootstrap run `33025739352` completed SUCCESS and started Site Task Runner `33025759856`. That worker proved all of the above validators PASS, then failed at `scripts/check_site_task_diagnostic_contract.py`.

Exact failure:

```text
missing dedicated "Upload Site task diagnostic" step
missing run/attempt-bound site-task-diagnostic artifact name
missing if-no-files-found: error for dedicated diagnostic artifact
missing "Failed validator:" summary line
obsolete assertion that only three workflows may exist in the repository
classification: DIAGNOSTIC_CONTRACT_DRIFT
semantic product failure: false
deployment reached: false
```

The diagnostic addendum still requires a run/attempt-bound diagnostic artifact on passing and failing task runs. R4 therefore restores that dedicated artifact and summary while preserving the existing combined live-verification bundle. The validator's obsolete exact-three-workflow inventory assertion is replaced with a required-subset check for the three workflows relevant to this diagnostic contract; the repository's many other active workflows are not invalid merely because they exist.

R4 branch: `fix/site-task-runner-semantic-live-501-r4`.

No push, schedule, pull-request mutation, provider, credential, publication, custody, or activation authority is added.


## 2026-08-27 rejected-bootstrap preemption repair

After R4 merged at `283fd9c03c1c4ccf785882621b1a45fdf6c9b02a`, concurrent repository work produced multiple Bootstrap runs sharing source commit `c106d47a8e7dec4f465b2e41360336a78aa38426` across different branches.

Observed sequence:

```text
Bootstrap 33025998914: main / c106d47... / SUCCESS
Bootstrap 33026013396: integration/governance-observatory-v0.1.0-release-awareness-512 / c106d47... / CANCELLED
Site Task Runner 33026022510: valid same-SHA worker / CANCELLED
Site Task Runner 33026026753: rejected-source completion / SKIPPED
```

The worker workflow correctly rejects non-main or unsuccessful Bootstrap completions at the job-level `if` guard, but GitHub applies workflow-level concurrency before the job guard. Because the concurrency group used only `head_sha`, the rejected/cancelled completion could preempt the already-admitted main worker for the same SHA.

R5 changes only the concurrency key:

```text
before: site-orchestrated-transition-<head_sha>
after:  site-orchestrated-transition-<head_sha>-<upstream_conclusion>
```

Therefore a cancelled/failed upstream completion cannot cancel a valid SUCCESS worker. Multiple SUCCESS transitions for the same SHA still supersede one another. Manual dispatch remains separately keyed by `manual`.

The orchestration contract now enforces the conclusion-partition marker. No trigger, mutation, deployment, credential, execution, custody, publication, or activation authority is expanded.

R5 branch: `fix/site-task-runner-semantic-live-501-r5`.


## 2026-08-27 generated-state concurrent-main regeneration repair

Current main advanced beyond the earlier detached-HEAD repair. Site Task Runner run `33070136632` completed the declared `all-local` task successfully, including Site mirror, homepage, free-tier trust, live URL, StegOS-node, final-goal, local-completion, and ingestion validators. The first failure moved to generated-state persistence.

Observed failure:

```text
source Bootstrap: 33070102114
source SHA: f713324eaf3e1db189f47c8ec3c6caa17c40b869
declared Site task: PASS
failed step: Persist generated Site state
failure mode: git rebase origin/main
classification: CONCURRENT_MAIN_GENERATED_STATE_REBASE_CONFLICT
deployment reached: false
semantic live verification reached: false
```

The generated commit conflicted with concurrent main changes across generated data/status files. Rebasing a stale generated snapshot is unsafe because it can either fail or force an arbitrary choice between two generated projections.

R6 replaces rebase-based persistence with bounded regenerate-on-current-main semantics:

```text
initial generated candidate
-> attempt push
-> if non-fast-forward / main advanced
-> discard stale generated commit
-> fetch + hard reset to current origin/main
-> reacquire governed transition/external framework inputs
-> rerun the declared Site task
-> stage the newly regenerated data/docs projection
-> retry push
-> maximum 3 attempts
-> fail closed if races continue
```

The orchestration validator now requires the regeneration policy and rejects a return to `git rebase origin/main` or `git pull --rebase` for generated-state persistence.

### Machine-readable task vector visibility

The active #501 task now carries the canonical COSV task notation explicitly:

```text
profile: task.v1
notation: L R U I V G O C M T B E A P
width: 14
canonical profile: StegVerse-Labs/.github/management/COSV_PROFILE_V1.json
concrete vector: null until emitted by the canonical COSV projection path
```

The separate semantic state-vector reference remains `stegverse.semantic-state-vector/v1` and is not conflated with the 14-digit COSV task profile.

R6 branch: `fix/site-task-runner-semantic-live-501-r6`.

No push, schedule, pull-request, provider, credential, custody, publication, or activation authority is added.


## 2026-08-27 sustained-main-churn retry-window refinement

R6 merged at `9154363d9a525fea70791fff1136ccf80dc45a91` and its exact-head Site Bootstrap validation passed. Site Task Runner `33070552227` then exercised the new regenerate-on-current-main policy under real concurrent repository activity.

Observed behavior:

```text
declared all-local task: PASS
initial generated-state push: rejected because main advanced
retry 2: regenerated from then-current main, push rejected by another main advance
retry 3: regenerated again from newer main, push rejected by another main advance
conflicting rebase: NONE
stale generated commit replay: NONE
result: FAILED_AFTER_3_BOUNDED_RETRIES
classification: HIGH_CHURN_GENERATED_STATE_WRITEBACK_STARVATION
Pages deployment reached: false
semantic live verification reached: false
```

This proves the R6 safety property: concurrent main changes no longer create merge/rebase conflicts. The remaining failure is liveness under unusually dense main-branch churn.

R7 retains exactly the same regenerate-before-retry semantics and widens only the bounded retry window from 3 attempts to 12. It remains fail-closed after the bounded window. No force push, rebase, conflict auto-resolution, authority expansion, or stale generated-state overwrite is allowed.

Machine-readable COSV task notation remains explicit on the active task:

```text
task.v1 = L R U I V G O C M T B E A P
width = 14
concrete vector = null until canonical COSV projection evidence exists
```

R7 branch: `fix/site-task-runner-semantic-live-501-r7`.
