# Site Ecosystem Management Handoff

## Purpose

This handoff defines how Site work continues without manual chat recovery, prior-thread dependency, or silent guesses about the next action.

The repository now separates two different completion questions:

```text
Repository-local goal gates: ready
Live governed activation: blocked pending external evidence
```

## Current Goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
Repository: StegVerse-Labs/Site
Primary handoff: docs/SITE_MIRROR_HANDOFF.md
Companion handoff: docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
Destination repository: StegVerse-org/LLM-adapter
Operational workflows: .github/workflows/validate.yml and .github/workflows/site-task-runner.yml
Local goal state: ready
Activation state: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
Contract status: PREPARED_NOT_DEPLOYED
Management state: ecosystem-managed continuation ready after this packet and checker pass
```

## Current Evidence

```text
docs/SITE_FINAL_GOAL_STATUS.json
  -> goal_status: ready
  -> TT bundle-fed status ready
  -> Governance Observatory status ready
  -> local completion receipt ready

docs/SITE_EXTERNAL_EVIDENCE_STATE.json
  -> state: external_evidence_present
  -> local_build_state: repository_managed
```

These records complete repository-local continuation gates. They do not prove a deployed same-origin usage endpoint, provider-owned accounting, Master-Records custody, or reconstructability.

## Activation Gates

Live activation remains blocked until all of the following are verified together:

```text
destination current-main tests
same-origin authenticated deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records custody
reconstructability PASS
```

## Done Definition

The Site repository can be treated as ecosystem-managed when:

```text
1. docs/SITE_MIRROR_HANDOFF.md remains the current task source of truth.
2. Exactly two operational workflows remain active.
3. scripts/run_site_task.py contains the declared validation and continuation tasks.
4. scripts/check_site_ecosystem_management_handoff.py verifies the management packet and computed status artifacts.
5. docs/SITE_FINAL_GOAL_STATUS.json reports repository-local readiness without claiming deployment authority.
6. docs/SITE_EXTERNAL_EVIDENCE_STATE.json records checked-in evidence posture.
7. The next action can be selected without prior chat context.
8. Live transport remains disabled until every activation gate is verified.
```

## Source Documents

```text
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_EXTERNAL_EVIDENCE_STATE.json
docs/SITE_FINAL_GOAL_STATUS.json
docs/SITE_FINAL_ACTIVATION_PENDING.md
docs/SITE_SELF_MANAGED_COMPLETION.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
```

## Active Automation

```text
.github/workflows/validate.yml
  -> bootstrap validation

.github/workflows/site-task-runner.yml
  -> all-local validation
  -> mirror and public guards
  -> TT and external evidence updates
  -> local completion receipt
  -> Pages deployment and public-route verification
  -> retained diagnostics and activation evidence
```

No third operational workflow is required.

## Required Checks

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py all-local
python scripts/check_site_ecosystem_management_handoff.py
python scripts/check_site_final_goal_status.py
python scripts/check_site_final_activation_pending.py
python scripts/check_site_workflow_inventory.py
```

## Next-Action Selection Rules

```text
1. Observe the next current-main Site Task Runner result.
2. If it fails, repair only the exact failing validator without removing checks.
3. If it passes, verify the result, receipt, and manifest artifact set belongs to the same run.
4. Bind verified Site evidence into the activation ledger.
5. Observe StegVerse-org/LLM-adapter current-main usage-session validation.
6. Do not run live endpoint conformance before an authorized same-origin deployment exists.
7. Do not enable live transport until all activation prerequisites pass.
8. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS exist.
```

## Authority Boundary

```text
Site-local goal readiness != live deployment.
External evidence present != authenticated custody.
Validation receipt != deployment evidence.
Workflow artifact != Master-Records custody.
Prepared client != deployed endpoint.
Usage retrieval != authority.
Usage display != admissibility.
No release tag is authorized.
```

## Archive Readiness

This file, together with `docs/SITE_MIRROR_HANDOFF.md`, `docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md`, and `scripts/check_site_ecosystem_management_handoff.py`, is sufficient for a future build session to determine the current goal, preserve the activation boundary, select the next safe action, and continue without requiring the prior chat thread.
