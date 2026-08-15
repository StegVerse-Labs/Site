# Actions Cost Containment Mirror Handoff

## Goal

- Goal ID: `SITE-ACTIONS-COST-CONTAINMENT-001`
- Repository: `StegVerse-Labs/Site`
- Branch: `chore/actions-cost-containment-20260814`
- Coordination: `StegVerse-Labs/.github#164`
- Repository issue: `StegVerse-Labs/Site#265`
- Governing invariant: production/continuity execution must remain `StegVerse -> StegVerse -> StegVerse`; GitHub Actions is not a required production carrier.

## Current repository pressure

- active GitHub workflows: 131
- open issue/PR aggregate reported by repository metadata: 60
- user-observed traffic: high clone volume, but clone traffic is not itself Actions billing

## First containment batch

Recurring GitHub-hosted schedules are removed from these operational surfaces while preserving explicit/manual or repository-event validation:

- `.github/workflows/site-handoff-orchestrator.yml`
- `.github/workflows/advance-tidc-internal-work.yml`
- `.github/workflows/advance-marketplace-coinbase-activation.yml`
- `.github/workflows/heartbeat-response-network.yml`

Classification:

- Site handoff orchestration: repository events remain sufficient on GitHub; recurring orchestration is a StegVerse-worker transfer candidate.
- TIDC advancement: necessary operational work; transfer candidate to StegVerse worker.
- Marketplace/Coinbase advancement: necessary only where current task graph remains active; transfer candidate and requires TV/TVC-native credential review because the GitHub workflow references a repository secret directly.
- Heartbeat response network: recurring continuity behavior belongs to StegVerse runtime; GitHub retained for explicit validation only.

## Remaining workflow audit

Code search shows many additional cron-bearing workflows. Every one must be classified as:

- `KEEP_GITHUB_VALIDATION`: necessary repository/CI behavior with justified trigger.
- `TRANSFER_TO_STEGVERSE_WORKER`: necessary recurring operational work.
- `ELIMINATE`: redundant, completed, superseded, or unnecessary.

Priority candidates include heartbeat response observers, StegGate progress observers, TIDC coordinators/reconcilers, VA evidence/runtime polling, public-deployment polling, generated propagation importers, and any hourly retry loop that only re-observes an unchanged blocker.

## Repository hygiene

Branch/issue/PR cleanup is coordinated by `StegVerse-Labs/.github#165`. Preserve active claims, protected/release branches, evaluation snapshots, current worker-owned branches, and evidence references. Exact duplicates and completed/superseded automation artifacts should be closed or deleted in bounded batches.

## Current state

`ACTIVE_REMEDIATION / FIRST_CONTAINMENT_BATCH_IMPLEMENTED / FULL_CENSUS_PENDING`
