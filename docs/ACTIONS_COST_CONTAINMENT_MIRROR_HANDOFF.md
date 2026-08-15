# Actions Cost Containment Mirror Handoff

## Goal

- Goal ID: `SITE-ACTIONS-COST-CONTAINMENT-001`
- Repository: `StegVerse-Labs/Site`
- Canonical branch: `main`
- Coordination: `StegVerse-Labs/.github#164`
- Workflow-minimization coordination: `StegVerse-Labs/.github#167`
- Repository issues: `StegVerse-Labs/Site#265`, `StegVerse-Labs/Site#268`
- Governing invariant: production/continuity execution must remain `StegVerse -> StegVerse -> StegVerse`; GitHub Actions is not a required production carrier.
- Credential invariant: no NON-TV/TVC project/provider secret or token may be introduced; credential authority remains TV/TVC.
- Preferred workflow surface: minimum technically necessary; `0/1/2` preferred, `>2` only by evidence-backed standalone exception.

## Current repository pressure

- active GitHub workflows at audit start: 131
- open issue/PR aggregate reported by repository metadata at audit start: 60
- branch inventory exceeds 100 and contains obvious duplicate/superseded branch families that require evidence-safe reconciliation

## Completed containment batch 1

Merged by PR #266 at merge commit `41db95c9df05e4a91b44d466ca1ed1231d46cfef`.

Recurring GitHub-hosted schedules were removed while explicit/manual or repository-event validation was preserved for:

- `.github/workflows/site-handoff-orchestrator.yml`
- `.github/workflows/advance-tidc-internal-work.yml`
- `.github/workflows/advance-marketplace-coinbase-activation.yml`
- `.github/workflows/heartbeat-response-network.yml`

Classification:

- Site handoff orchestration: repository events remain sufficient on GitHub; recurring orchestration is a StegVerse-worker transfer candidate.
- TIDC advancement: necessary operational work; transfer candidate to StegVerse worker.
- Marketplace/Coinbase advancement: necessary only while the current task graph remains active; transfer candidate and TV/TVC-native credential review remains required because the retained GitHub workflow references a repository secret directly when explicitly invoked.
- Heartbeat response network: recurring continuity behavior belongs to StegVerse runtime; GitHub retained for explicit validation only.

## Completed containment batch 2

Merged by PR #267 at merge commit `44f593f7b7075958d6b363ddf8caac1ee3541132`.

The following five additional recurring schedules were removed while preserving source-change/manual validation paths:

- `.github/workflows/steggate-four-app-progress.yml` — hourly handoff synchronization is operational progress reconciliation; `TRANSFER_TO_STEGVERSE_WORKER` for recurring ownership, GitHub retained for event/manual use.
- `.github/workflows/check-hil-live-readiness.yml` — six-hour public readiness polling is observation work; `TRANSFER_TO_STEGVERSE_WORKER` for recurring ownership, GitHub retained for event/manual diagnostics.
- `.github/workflows/tidc-task-coordinator.yml` — hourly queue advancement/task execution is operational work; `TRANSFER_TO_STEGVERSE_WORKER`, GitHub retained for source-change/manual validation.
- `.github/workflows/heartbeat-response-blocker-observer.yml` — six-hour blocker polling is continuity observation; `TRANSFER_TO_STEGVERSE_WORKER`, GitHub retained for event/manual diagnostics.
- `.github/workflows/generated-stegpay-propagation-import.yml` — hourly propagation/task-controller reconciliation is operational work; `TRANSFER_TO_STEGVERSE_WORKER`, GitHub retained for source-change/manual use.

No NON-TV/TVC project/provider secret/token was added by this batch.

## Workflow-surface minimization batch 1 — validated merge candidate

Canonical implementation claim:

```text
issue: Site #268
claim: SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B1-20260815
branch: chore/site-validation-workflow-minimization-batch1-20260815
PR: #270
state: VALIDATED_MERGE_CANDIDATE
```

The first-release HIL validator is consolidated into the existing stable HIL live-readiness dispatcher:

- `.github/workflows/check-hil-first-release-readiness.yml` -> `.github/workflows/check-hil-live-readiness.yml`
- the consolidated dispatcher retains push, pull-request, and manual first-release validation;
- deployed HIL observation remains excluded from pull-request execution;
- `permissions: {}` is used;
- repository acquisition uses anonymous public Git fetch rather than `actions/checkout`;
- preinstalled Python is used rather than `actions/setup-python`;
- the job fails closed if GITHUB/GH/PAT/TVC ephemeral/Cloudflare HIL credential variables are exposed to the validation environment;
- the workflow grants no activation, publication, execution, release, custody, provider, or Master Record authority.

Direct hosted validation evidence on PR #270:

```text
HIL stable dispatcher run: 31869072980 SUCCESS
Site Handoff Orchestrator run: 31869072953 SUCCESS
repository-native branch claim: ADMITTED
```

The earlier PR #269 was closed unmerged and superseded by #270 because Site's repository-native pre-work gate correctly required exactly one branch-bound claim and a branch mapping to declared unfinished handoff work. Its implementation was retained in the replacement branch; the supersession was a collision-control correction, not a capability rollback.

### HIL stale-validator discovery preserved

The initial consolidation attempt proved that two older standalone HIL guards are stale against the current canonical v1.1 HIL manifest:

- `scripts/check_hil_activation_state.py` failed `manifest Primary state mismatch` because `data/hil-activation-state.json` still carries historical v0.5 Primary assumptions while the canonical experiment manifest is v1.1;
- `scripts/check_hil_end_to_end_protocol.py` failed `canonical Primary SHA-256 changed` because it hard-codes the superseded Primary hash instead of the canonical v1.1 hash.

Those two standalone workflows were restored unchanged. They are not counted as successfully consolidated and their semantic reconciliation was transferred to the canonical HIL workstream in Site issue #81. Workflow minimization must not weaken them merely to obtain a passing cleanup run.

## Current quantitative state

Audit denominator remains 131 workflow surfaces.

Before PR #270 merge:

- recurring schedules removed in containment batch 1: 4
- recurring schedules removed in containment batch 2: 5
- total known recurring schedules removed: 9
- workflow files removed by validated minimization candidates: 1
- explicitly classified/remediated audit-start surfaces: 10/131
- remaining surfaces requiring KEEP_STANDALONE_EXCEPTION / CONSOLIDATE / TRANSFER / ELIMINATE classification: 121
- current main workflow-file count: 131 until PR #270 is merged
- expected post-merge workflow-file count: 130, subject to direct post-merge API observation

Schedule removal does not itself reduce workflow-file count. The 121 remaining value is a classification denominator, not a claim that 121 schedules exist.

## Classification states

- `KEEP_GITHUB_VALIDATION`: necessary bounded repository/CI behavior retained while minimization is incomplete.
- `KEEP_STANDALONE_EXCEPTION`: workflow remains standalone only when concrete technical/authority evidence prevents safe consolidation.
- `CONSOLIDATE_INTO_STABLE_DISPATCHER`: useful GitHub-bound behavior retained behind a minimum stable workflow doorway.
- `TRANSFER_TO_STEGVERSE_WORKER`: necessary operational work whose recurring execution belongs to a StegVerse-controlled worker/runtime.
- `ELIMINATE`: redundant, completed, superseded, or unnecessary.
- `REVIEW_REQUIRED`: discovered drift or ownership uncertainty prevents safe consolidation until the canonical owner reconciles it.

## Local runtime / formal model convergence

This Site remediation lane does not duplicate the completed local-model/runtime implementation. Organization source of truth records:

- formal local model: `COMPLETE_RELEASED`;
- local runtime discovery/launch/inference/proof: `COMPLETE_RELEASED`;
- descriptive `select a local model/runtime` step: `SUPERSEDED`;
- local-model credential requirement: `NONE`;
- credential authority: `TV/TVC`;
- GitHub token production authority: `NONE`.

Canonical continuation is `StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md` and `StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`. Remaining live carrier/inference activation is worker-owned and outside this remediation lane's collision scope.

## Repository hygiene

Branch/issue/PR cleanup is coordinated by `StegVerse-Labs/.github#165`. Preserve active claims, protected/release branches, evaluation snapshots, current worker-owned branches, and evidence references. Exact duplicates and completed/superseded automation artifacts should be closed or deleted in bounded batches.

Known completed hygiene in this workstream:

- Site PR #255 Vercel carrier closed as superseded by the StegVerse-only runtime architecture;
- Site PR #269 closed unmerged as superseded by repository-native admitted replacement PR #270;
- branch census confirmed more than 100 branches with duplicate families requiring bounded deletion after claim/evidence checks.

## Active claims / collision boundary

- Site cost containment implementation: Site #265;
- Site workflow minimization: Site #268, current exact claim `SITE-WORKFLOW-SURFACE-MINIMIZATION-268-B1-20260815`;
- Site pre-work admission: machine-owned claim `SITE-PREWORK-CLAIM-GATE-MACHINE-001` — admission only, not product implementation;
- HIL semantic reconciliation: canonical HIL workstream / Site #81; observation only from this minimization lane;
- live sovereign runtime activation and Ecosystem Chat inference: canonical resident StegVerse workers — observation only here;
- local model implementation: complete/released — no competing implementation claim permitted;
- TV/TVC credential/route authority: TV/TVC only.

## Validation / release condition

Containment batches 1 and 2 are merged. Workflow-minimization batch 1 is a validated merge candidate: the target HIL stable dispatcher and Site repository-native handoff admission both pass on PR #270.

Batch 1 becomes complete only after:

1. PR #270 merges;
2. post-merge workflow-file count is directly observed;
3. the exact claim is transitioned/released with merge evidence;
4. this handoff is corrected on `main` from merge-candidate to merged state if needed.

Full goal completion still requires classification of the remaining 121 audit-start workflow surfaces, reduction toward the minimum safe workflow count, evidence-backed exceptions for any standalone workflows above the minimum, and bounded issue/PR/branch reconciliation without deleting active evidence or claims.

## Current state

`ACTIVE_REMEDIATION / CONTAINMENT_BATCHES_1_2_MERGED / WORKFLOW_MINIMIZATION_BATCH_1_VALIDATED_MERGE_CANDIDATE / FULL_CENSUS_PENDING`

## Session consolidation

The local-model/runtime and trade-readiness requirements are durably transferred to the canonical organization/runtime worker chain. This session still retains unique workflow-minimization/cost-containment/hygiene implementation responsibility until the active claim is released or transferred and the remaining cleanup work has durable executable owners.
