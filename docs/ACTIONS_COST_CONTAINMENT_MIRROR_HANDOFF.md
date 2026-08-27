# Actions Cost Containment Mirror Handoff

## Canonical state

```text
goal_id: SITE-ACTIONS-COST-CONTAINMENT-001
repository: StegVerse-Labs/Site
canonical_branch: main
canonical_issue: Site#268
credential_authority: TV/TVC
non_tv_tvc_project_or_provider_secret_allowed: false
github_actions_production_carrier_required: false
preferred_workflow_surface: <=2 stable entry surfaces with evidence-backed exceptions
canonical_claim_registry: data/session-work-claims.json + data/session-work-claims.d/*.json
active_implementation_claim: NONE_ON_SHARED_ACTIONS_HANDOFF
active_validation_claim: NONE
state: ACTIVE_REMEDIATION
thread_archive_ready: false
```

Production/runtime continuity remains StegVerse-owned. GitHub-hosted execution is non-authorizing validation only. No Render path or TV/TVC credential export is permitted.

## 2026-08-26 session-consolidation reconciliation

This section is the current continuation index for the Actions-cost work touched by the 2026-08-22 through 2026-08-26 cost-reduction session. Detailed task-specific handoffs and claim fragments remain authoritative for their individual lanes. Older candidate language below is superseded wherever this section records a later merged/released state.

### Current parent state

Site #268 remains OPEN and the cost/workflow-minimization goal remains ACTIVE. The last documented canonical accounting remains:

```text
audit_start_workflow_surfaces: 131
released_classified_or_remediated: 71/131 = 54.20%
remaining_audit_start_surfaces: 60/131
current_main_workflow_count: 104
workflow_files_eliminated_or_consolidated_historical: 30
live_count_delta_vs_2026-08-23_97_surface_checkpoint: +7
preferred_stable_entry_surfaces: <=2
placeholders: 0
```

Do not infer a newer physical workflow count from individual carrier-only repairs; several repairs reduce schedules, fanout, credential persistence, mutation authority, or artifact custody without deleting a workflow file.

### 2026-08-27 live workflow-count reconciliation

Direct tree inspection of current `main` at `9462c20ff5eb2a0fe8b27f599a266d8d738076c7` finds **104** workflow YAML files. The 97-workflow figure was the exact count at checkpoint `02836ba157a41983dc97259ea2090da93f1dc29b`; it is historical, not current.

Since that 97-surface checkpoint, eight workflow files were added and one was removed:

```text
added:
  check-coinbase-skap-intr-route-consumer.yml
  coinbase-skap-phone-ingress-validation.yml
  generic-login-test-validation.yml
  heartbeat-public-visibility.yml
  stegos-device-root-race-public-observation.yml
  stegos-node-public-observation.yml
  validate-governance-observatory-status.yml
  validate-physical-economics-report-ui.yml

removed:
  hil-cloudflare-deploy.yml

net workflow-count drift: +7
current live count: 104
canonical inventory: data/site-workflow-inventory.json
inventory canonical_workflows: ecosystem-chat-activation-retention.yml; site-task-runner.yml; validate.yml
inventory migration_required_file_count: 101
```

This is a surface-count regression relative to the cost-containment checkpoint, not runtime evidence and not proof that any of the eight added workflows are safe to retire. Each must be reconciled against its active handoff/claim before consolidation or removal.

### VA Claims Guide cost lane — RELEASED

The older VA Claims Guide candidate/branch work is terminally superseded by the released canonical Site repair recorded as Site #428 in this handoff's released accounting. `.github/workflows/va-claims-guide-surface.yml` is no longer an unmutated candidate. Do not recreate the stale #405/#408-era lane.

### VA governed surfaces deployment observer — COMPLETE / RELEASED

Canonical detailed handoff:

`docs/VA_GOVERNED_SURFACES_DEPLOYMENT_ACTIONS_FANOUT_MIRROR_HANDOFF.md`

\`\`\`text
pull_request: 473
validated_head: b06b01cf59b13a120c8a050e2b4ee98debdb8a56
merge_commit: b526c69a647b96cf8ee6e9e44aca0facc1d61241
Site Handoff Orchestrator: 32669715065 SUCCESS
Ecosystem Heartbeat Orchestration: 32669715039 SUCCESS
Site Bootstrap Validate: 32669715040 SUCCESS
task_specific_main_run: 32669754710 SUCCESS
task_specific_main_job: 97268636390 SUCCESS
task_specific_main_head: b526c69a647b96cf8ee6e9e44aca0facc1d61241
verification_marker: VA_GOVERNED_SURFACES_DEPLOYMENT=VERIFIED
state: COMPLETE_RELEASED
\`\`\`

The merged workflow removes its six-hour schedule, `contents: write`, credential-bearing checkout/setup actions, repository observation writeback, and artifact custody. It retains bounded `main` source-change verification and intentional `workflow_dispatch`, anonymous exact-source acquisition, live HTTP/byte-equality deployment checks, and fail-closed VA authority/filing boundaries.

The previously missing push-run evidence is now directly inspectable through the supported GitHub Actions API. Run `32669754710` on exact merge commit `b526c69a647b96cf8ee6e9e44aca0facc1d61241` completed successfully; job `97268636390` emitted `VA_GOVERNED_SURFACES_DEPLOYMENT=VERIFIED`, `VA_GOVERNED_SURFACES_REPOSITORY_WRITEBACK=NONE`, and `VA_GOVERNED_SURFACES_ARTIFACT_CUSTODY=NONE`. The bounded observer claim is released. No user action remains.

### Executive Rhetoric Ledger sync — sovereign replacement source RELEASED, live execution pending

Canonical source/migration owner:

`StegVerse-Labs/StegVerse-Healer/docs/SITE_ERL_SOVEREIGN_SYNC_MIRROR_HANDOFF.md`

Healer #39 / PR #40 installed `executive-rhetoric-ledger-local-sync` on the existing `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` scheduler. Exact head `aca5b7871e2720b0d56757e33fc2a22c10291136` passed Test Readiness run `32670203077`, job `97269769966`, and merged as `ff3d9985b773d91dce0d90351a7a8a04a499c59b`.

```text
source_state: COMPLETE_RELEASED
live_execution_state: MACHINE_OWNED_PENDING_SCHEDULER_RECEIPT
site_legacy_github_workflow_retirement_authorized: false
```

The source handler uses already-materialized Site + Executive_Rhetoric_Ledger roots, validates `publication/compendium.json`, mirrors exact bytes, verifies SHA-256 identity, writes a destination-owned local acknowledgment, refuses GitHub credentials, and grants no remote-checkout/artifact/GitHub-writeback/runtime/provider/publication/activation authority.

Required live scheduler receipt:

`StegVerse-Labs/.github/receipts/healer-sovereign-scheduler/SHWP-HEALER-SOVEREIGN-SCHEDULER-001.json`

Live inspection still reports this receipt absent. Therefore `.github/workflows/sync-executive-rhetoric-ledger.yml` must remain in Site until the sovereign scheduler proves the new target COMPLETE/PASS. Removing it before that proof would create a continuity gap.

### Thought Experiments B27 — WAITING ON SAME SOVEREIGN SCHEDULER

`data/tasks/SITE-ACTIONS-COST-CONTAINMENT-001-B27.json` remains `MACHINE_OWNED_NATIVE_VALIDATION_PENDING`. Healer's released B27 validation carrier is source-complete, but B27 requires an exact `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` live receipt against the then-current Site candidate before the standalone Thought Experiments workflow may be terminally retired. GitHub CI does not substitute for this machine receipt.

### `validate.yml` trigger narrowing — BLOCKED BY ACTIVE STEGFIN PUBLICATION CLAIM

`.github/workflows/validate.yml` remains claimed by `SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817` and must not be modified by this cost lane until that claim releases.

Canonical current receipt:

`receipts/stegfin-ios-local-wallet-transport-388-validation.json`

```text
repository_integration: COMPLETE
publication_observer_state: BOUND_EXECUTION_PENDING_CORRECTED_BOOTSTRAP
classification: SOURCE_AND_SITE_MERGED_CORRECTED_PUBLICATION_PROOF_PENDING
release_blocked: true
```

Release requires a credential-clean main-push Site validation execution proving exact public wallet UI blob `114b3c39052d5b1622407080407259a0040a1369` and corrected bootstrap blob `dc1a86bc564146cdaa645620c8fc698e45029440` as `VERIFIED_PUBLICATION`. After that publication gate, continuation transfers to StegFin #81/current phone for a new MetaMask-browser WebAuthn/PREPARE and injected-provider proof. Only after the Site claim actually releases may this cost lane admit `validate.yml` trigger narrowing.

### Upstream sovereign-runtime dependency — corrected 2026-08-26

Heartbeat activation is terminal and no longer a Site Actions-cost prerequisite. HB32 is protocol-derived at 10 ms / 100 Hz with `OSCILLATOR_ONLY` progression; LIVE-009 is completed.

The Healer scheduler still depends on the separate `SHWP-DURABLE-RUNTIME-ACTIVATION` machine-owned worker/runtime lane. Current canonical blocker is **not** an iPhone receipt: it is the absence of an eligible declared StegVerse-owned/federated sovereign node for native runtime installation/verification.

```text
handoff: StegVerse-Labs/.github/handoffs/SHWP-DURABLE-RUNTIME-ACTIVATION.json
receipt: StegVerse-Labs/.github/receipts/sovereign-runtime-activation/SHWP-DURABLE-RUNTIME-ACTIVATION.json
state: BLOCKED_SOVEREIGN_NODE_REQUIRED_NON_HEARTBEAT
reason: SOVEREIGN_NODE_DECLARATION_NOT_PRESENT
current iPhone HB30 action required: false
```

The historical HB30 inline-capsule handoff is satisfied/superseded and must not be rerun after HB30+. Site ERL/B27 retirement still waits for the real no-token Healer scheduler receipt, but that receipt now depends on sovereign-node runtime availability rather than heartbeat activation.

### Completed projection repair touched by this session

The Ecosystem Node dual-view / VA validator / StegMusic integration repair is terminal and must not be reopened. Final Site PR #425 merged as `d9ce13c8a95d178ad66a93b649b918a7911958c3` after exact-head repository gates passed. It restored Conversation/Governed/Split projection behind the simple user-first Chat surface, aligned stale VA validators to the veteran-first contract, and migrated StegMusic access away from the retired multi-entry launcher. This repair is COMPLETE_RELEASED_BOUNDED_PROJECTION_REPAIR and grants no provider/runtime/activation authority.

## 2026-08-23 endpoint-readiness credential-clean validation — RELEASED

PR #466 / merge `983ba6c4ce69a4932a912042addecf135515c33e` preserved every existing push, pull-request, and manual endpoint-readiness trigger required by open Site #24 while removing credential-persisting `actions/checkout` / `actions/setup-python` dependencies from `.github/workflows/check-stegverse-endpoint-activation-readiness.yml`.

The retained lane now uses `permissions: {}`, refuses credential-bearing environments, anonymously fetches the exact source revision, uses preinstalled Python, and executes the same readiness-boundary validator. Endpoint readiness remains `CONFIGURATION_AND_PERSISTENT_EXECUTION_REQUIRED`; provider, runtime, custody, reconstruction, publication, release, and activation authority remain false and separately owned.

```text
validated head: f1d5574f45d3f4e5c4b30699a1be41c2a9994b3e
Endpoint Activation Readiness: 32647462293 SUCCESS
Site Handoff Orchestrator: 32647462187 SUCCESS
Ecosystem Heartbeat Orchestration: 32647462169 SUCCESS
Site Bootstrap Validate: 32647462188 SUCCESS
release commit: 983ba6c4ce69a4932a912042addecf135515c33e
runtime/publication/custody/reconstruction/release/activation authority: NONE
```

The claim is terminalized in `data/session-work-claims.d/site-endpoint-readiness-credential-clean-20260823.json`.

## 2026-08-23 ST-018 post-merge duplicate validation containment — RELEASED

PR #465 / merge `105ee9dc51782aaabe2317c88a8844210a069f96` removed the redundant `main` push carrier from `.github/workflows/capture-validation-evidence.yml`. ST-018 was already released as credential-clean deterministic validation, so source/schema/validator/workflow changes continue to receive bounded pull-request validation and intentional `workflow_dispatch`, while the duplicate post-merge hosted execution is retired.

The retained lane remains `permissions: {}`, refuses credential-bearing environments, fetches exact source anonymously, uses only local ephemeral receipt enforcement, and has no artifact or issue custody, repository writeback, runtime authority, publication authority, or activation effect.

```text
validated head: d76c8ca09ba210d51d5f845a64768411436d13a4
Capture Validation Evidence: 32647296600 SUCCESS
Site Handoff Orchestrator: 32647296729 SUCCESS
Ecosystem Heartbeat Orchestration: 32647296574 SUCCESS
Site Bootstrap Validate: 32647296479 SUCCESS
release commit: 105ee9dc51782aaabe2317c88a8844210a069f96
runtime/publication/custody/activation authority: NONE
```

The claim is terminalized in `data/session-work-claims.d/site-st018-postmerge-fanout-20260823.json`.

## 2026-08-23 TIDC research PR state-fanout containment — RELEASED

PR #464 / merge `6cf8a259e95a1a2ea6948cc832f5f76edf24fdc4` preserved the complete existing `main` push observation path for TIDC research while narrowing pull-request fanout away from routine machine-produced work-queue, source-expansion, split, and negative-control state. PR validation remains automatic for the public TIDC surface, registry, canonical TIDC handoffs, pilot evidence, blinded-coding schemas/packets/returns, validators, and workflow definition; intentional `workflow_dispatch` remains.

The retained lane is credential-clean with `permissions: {}`, explicit credential refusal, anonymous exact-source acquisition, preinstalled Python, no repository writeback, and no runtime/publication/activation authority. Existing blinded-return processing and its evidence artifact remain intact when a real return is committed. Active TIDC source expansion, aggregate splits, negative controls, blinded evidence, and StegCore observation remain separately owned and incomplete.

The first exact-head attempt exposed a malformed claim fragment and correctly failed the repository-wide pre-work gate. The fragment was repaired into the required registry envelope and hash-bound to this handoff before revalidation. Final exact-head evidence:

```text
validated head: 1bc419f5a80e39c9d275ae4bf8e2c4b6d7bf5d59
TIDC Research Surface: 32647131979 SUCCESS
Site Handoff Orchestrator: 32647132003 SUCCESS
Ecosystem Heartbeat Orchestration: 32647131985 SUCCESS
Site Bootstrap Validate: 32647132019 SUCCESS
release commit: 6cf8a259e95a1a2ea6948cc832f5f76edf24fdc4
runtime/publication/activation authority: NONE
```

The claim is terminalized in `data/session-work-claims.d/site-tidc-research-pr-fanout-20260823.json`.

## 2026-08-23 TVC receipt-import PR task-state fanout containment — RELEASED

PR #463 / merge `22da2b5dc9da8cd42af07aaf18918a5d90e6d884` removed routine `tasks/SITE-TVC-RUNTIME-ASSIST-001.json` persistence from pull-request fanout while preserving its existing `main` push observation path. PR validation remains automatic for the receipt schema, validator, regression tests, and workflow definition; intentional `workflow_dispatch` remains.

The retained lane remains credential-clean with `permissions: {}`, credential refusal, anonymous exact-source acquisition, no repository writeback, no artifact custody, and no runtime or execution-grant authority. TVC runtime/execution-grant/deployment/custody work remains separately owned and incomplete.

```text
validated head: 6b33e2b685b527c9e434558b2d229bc55be81b83
TVC Execution Receipt Import: 32638967647 SUCCESS
Site Handoff Orchestrator: 32638967635 SUCCESS
Ecosystem Heartbeat Orchestration: 32638967657 SUCCESS
Site Bootstrap Validate: 32638967642 SUCCESS
runtime/execution-grant/custody authority: NONE
```

The claim is terminalized in `data/session-work-claims.d/site-tvc-receipt-import-pr-state-fanout-20260823.json`.

## 2026-08-23 GP10 pull-request task-state fanout containment — RELEASED

PR #461 / merge `0cadf1c38a0c391cec2eef31323b471a87032623` preserved the complete existing `main` push path for GP10 workspace validation and non-authorizing deployed-page observation while removing routine `data/operations/gp10_workspace_tasks.json` from pull-request fanout.

Pull-request validation remains automatic for GP10 workspace and examples pages, browser assets, static/deployment validators, the workspace handoff/security baseline, and the workflow definition. Intentional `workflow_dispatch` remains. Existing credential-clean exact-source acquisition, zero repository writeback, zero artifact custody, and zero runtime-control-plane authority remain unchanged.

The claim is terminalized in `data/session-work-claims.d/site-gp10-pr-task-state-fanout-20260823.json`. GP10's authenticated durable service remains blocked until its named StegVerse service/security prerequisites exist, and real field validation/commercial activation remains owned by `StegVerse-Labs/GP10`; neither is inferred complete from this Actions release.

## Other released fanout repairs retained

Released 2026-08-23 integrations include Review Authority #459, HIL semantic continuity #457, HIL semantic replay #455, HIL Site contract #454, TIDC session consolidation #453, HIL live readiness #452, HIL deployed-cycle #451, HIL session consolidation #450, HIL LinkedIn readiness #449, HIL v1 upload #448, HIL v1.1 release #447, HIL end-to-end protocol #446, coherent-transition threshold #445, VA Claims Chat #443, and Thought Experiments #436. Their detailed evidence remains in Git history and terminal claim fragments.

Released 2026-08-22 repairs include VA Claims Guide #428, historical Two Entry Points #410, terminal SV Cost #415, VA privacy preprocessor #426, VA governed-product-goals #429, and VACC Goal 3 contract-suite #432. #413 and #420 remain merged but nonterminal until their task-specific integrated observation conditions are actually satisfied.

## Audit correction: repository-task controller self-fanout is not yet proven

`.github/workflows/observe-and-complete-repository-tasks.yml` still has hourly observation, `contents: write`, task/orchestration-state push paths, state persistence, and artifact custody. No recursive second-generation run caused by that persistence has been observed, so the earlier structural self-fanout hypothesis is not credited as a proven repair and its active observation responsibility remains unchanged.

## Protected and unresolved surfaces

- `.github/workflows/validate.yml` remains claimed by `SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388-20260817`; trigger narrowing waits for actual release.
- `.github/workflows/va-document-evidence.yml` remains owned by open PR #263 / Site #116.
- `.github/workflows/va-pii-realignment-readiness.yml` retains its six-hour PII-RDY-08/09 observer because those readiness gates remain unresolved.
- Heartbeat-response clock retirement remains gated on stronger sovereign scheduler execution evidence.
- HIL runtime/readiness/custody/private-review/publication lanes remain separately owned and incomplete.
- #413 and #420 remain nonterminal pending exact task-specific integrated evidence.
- `SITE-0001-COHERENT-TRANSITION-THRESHOLD-ACTIVATION` remains `RUNNING` / `MACHINE_OWNED`.
- `observe-rtg-formalism-projection.yml` remains active review-only observation infrastructure; its task state still has machine evidence and governed-transition gates pending, so its daily observer/writeback is retained.
- `docs/HIL_SEMANTIC_CONTINUITY_MIRROR_HANDOFF.md` remains `ACTIVE_FOUNDATIONAL_BUILD`; participant-record integration remains active and scientific/release authority remains false.
- RTG–TT issue #122 remains open and its public mirror activation still requires verified `main` integration and exact downstream ingestion; `.github/workflows/rtg-tt-public-mirror.yml` therefore retains its current main observation carrier.
- TVC runtime/execution-grant/custody coordination remains active; Actions repair narrows only fanout/validation mechanics.
- TIDC research source expansion, split generation, negative controls, blinded evidence, and StegCore observation remain active; the released fanout repair narrows only duplicate PR fanout.
- Site #24 endpoint activation remains open; its readiness observer retains required triggers.
- `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` remains `HANDOFF_READY`; the required scheduler receipt is absent.

## Automation and continuation

Credential-clean `.github/workflows/validate.yml` remains the canonical deterministic repository validation lane while its active StegFin claim persists. `data/session-work-claims.json`, append-only `data/session-work-claims.d/*.json`, and the MACHINE_OWNED Site pre-work gate prevent duplicate mutation and require explicit bounded claims before mutable work.

## Next executable actions

1. Reconcile the eight post-checkpoint workflow additions against their current handoffs/claims and reduce or consolidate only collision-free surfaces; do not treat the historical 97 count as current.
2. Consume a real `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` receipt; then finalize B27 and admit the Site ERL GitHub-carrier retirement if the ERL target is COMPLETE/PASS.
3. Release #413 and #420 only if their exact integrated observation conditions become inspectable and pass.
4. After StegFin Site claim #388 actually releases, admit safe `validate.yml` trigger narrowing while preserving source/schema/config validation and manual full validation.
5. Continue the workflow census and admit the next collision-free recurring/writeback/state-carrier fanout whose runtime/product responsibility is complete or separately owned.
6. Retire heartbeat clocks only after stronger sovereign scheduler execution evidence exists.

No source, PR, workflow success, repository receipt, task assignment, or machine ownership grants runtime, provider, publication, custody, financial, signing, broadcast, settlement, filing, or activation authority.
