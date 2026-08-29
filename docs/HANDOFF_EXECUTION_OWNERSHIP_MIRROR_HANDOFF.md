# Site Execution-Ownership Mirror Handoff

## Source of truth and supersession boundary

This file is the canonical execution-ownership and collision-partition record for `StegVerse-Labs/Site` under `StegVerse-Labs/repo-standards#37` and `StegVerse-Labs/Continuity/docs/REPOSITORY_HANDOFF_STANDARD.md`.

It supersedes only execution-ownership interpretation for the current Site `*_MIRROR_HANDOFF.md` set. It does not supersede product semantics, orchestration state, validation evidence, task ownership, claims/fences/leases, deployment state, activation state, release state, or authority records. `docs/SITE_MIRROR_HANDOFF.md` remains the current product/task source of truth identified by `.stegverse/repo-heartbeat.json`.

Current bounded state preserved:

```text
StegGate four-app execution progress: 11/30 verified gates / 37%
fully functional public apps: 0/4
goal complete: false
Site activation: pending authentic provider/persistent endpoint/runtime evidence
current orchestration: repository-native and machine-owned
credential authority: TV/TVC
heartbeat grants execution authority: false
```

## Execution ownership and collision partition

Standard: `stegverse.handoff-execution-ownership/v1`.

### MANUAL / SESSION-STARTABLE

```yaml
- task_id: SITE-HANDOFF-OWNERSHIP-ADOPTION-636
  execution_owner: repo-standards #37 integration lane + Site repository owner
  claim_state: CLAIMED_FOR_INTEGRATION
  worker_registry_ref: StegVerse-Labs/repo-standards#37 + StegVerse-Labs/Site#636 + branch docs/handoff-ownership-adoption-636
  manual_execution_allowed: true
  manual_allowed_role: integration
  collision_scope: this execution-ownership mirror handoff and adoption metadata only; excludes current Site orchestration/product work, four-app goal, HIL upload, heartbeat/browser/endpoint/shorthand lanes, provider/runtime work, deployment, release, credentials, claims/fences/leases, and downstream product mutation
  release_condition: exact-head repository validation is observed, migration PR is merged, issue #636 is reconciled, and repo-standards adoption state is updated
  next_executable_action: validate and merge ownership metadata only
```

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: SITE-ACTIVE-WORK-AGGREGATE
  execution_owner: current per-task worker/machine owner recorded by docs/SITE_MIRROR_HANDOFF.md, data/site-orchestration-state.json, data/ecosystem-heartbeat-state.json, active issues/PRs, task registries, claims/fences/leases, and upstream/downstream handoffs
  claim_state: MACHINE_OWNED
  worker_registry_ref: docs/SITE_MIRROR_HANDOFF.md + data/site-orchestration-state.json + data/ecosystem-heartbeat-state.json + current issues/PRs/scoped handoffs + StegVerse-Labs/.github control-plane records
  manual_execution_allowed: false
  manual_allowed_role: observation
  collision_scope: StegGate four-app execution, HIL upload, heartbeat/orchestration, browser binding, endpoint publication, semantic shorthand, provider/persistence/custody/reconstruction chain, Site activation, deployment observation, and any capability with a current owner
  release_condition: newest valid orchestration/task/issue/claim/fence/lease/handoff explicitly releases or supersedes the exact collision scope
  next_executable_action: preserve current owners and consume authentic machine/runtime evidence without duplicating their work
```

### ESCALATED / AUTHORITY-OWNED

```yaml
- task_id: SITE-AUTHORITY-BOUNDARY-AGGREGATE
  execution_owner: applicable Site/runtime/provider/deployment authority -> TV/TVC where credentials apply -> ecosystem governance
  claim_state: ESCALATED
  worker_registry_ref: docs/SITE_MIRROR_HANDOFF.md + current upstream/downstream authority handoffs + TV/TVC credential records
  manual_execution_allowed: false
  manual_allowed_role: reconciliation
  collision_scope: credential authority, provider authorization, deployment/publication authority, Site activation authority, release authority, custody, admissibility/certification, and cross-repository mutation authority
  release_condition: exact bounded authority is explicitly granted by its canonical mechanism
  next_executable_action: fail closed; deployment, workflow PASS, public reachability, orchestration completion, receipt presence, or migration metadata are not activation/release authority
```

### COMPLETED / SUPERSEDED

- Existing completed Site implementation surfaces remain complete only at their recorded bounded states and are not reopened by this migration.
- Any historical implication that a `RUNNING`, `READY`, `BLOCKED`, queued, or machine-owned Site task is manually startable is superseded by the worker-owned aggregate above.
- Any inference that deployment/publication, orchestration completion, or this migration proves Site activation, release, provider execution, custody, or admissibility is superseded/prohibited.
- This handoff supersedes execution-ownership interpretation only.

## Completion rule

The Site handoff-ownership target is migration-complete when this exact execution-ownership record is validated and merged and repo-standards records Site as `MIGRATED`, while current product/runtime/orchestration owners remain unchanged.
