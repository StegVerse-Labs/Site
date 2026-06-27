# Site Manual Task Elimination

## Assumptions

1. `StegVerse-Labs/Site` should not require manual inspection to know whether the current local continuation gates have passed.
2. Source authority remains outside Site where declared: Publisher for papers, `Admissible-Existence/TT` for TT records, and `StegVerse-Labs/governance-observatory` for Governance Observatory records.
3. Site may automate fetching, rendering, checking, and committing mirror state, but Site does not gain execution authority from those actions.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. The canonical repository paths begin with a leading period.

## Done Definition

This document is done when every remaining local manual task has a repository-managed workflow, script, or generated state file.

## Eliminated Manual Tasks

| Former manual task | Repository-managed replacement |
|---|---|
| Check whether TT bundle exists | `scripts/write_site_external_evidence_state.py` |
| Render TT status after bundle arrival | `scripts/render_tt_code_representation_status.py` |
| Check Governance Observatory mirror status | `scripts/check_site_governance_observatory_status.py` |
| Decide whether final Site goal is ready | `scripts/update_site_final_goal_status.py` |
| Validate final goal state | `scripts/check_site_final_goal_status.py` |
| Confirm final activation remains bounded | `scripts/check_site_final_activation_pending.py` |
| Run local continuation sequence in order | `github/workflows/site-autonomous-continuation.yml` |
| Commit computed Site continuation state | `github/workflows/site-autonomous-continuation.yml` |

## Local Continuation Workflow

The local continuation path is now:

```text
github/workflows/site-autonomous-continuation.yml
```

It performs:

```text
checkout Site
checkout Admissible-Existence/TT
build TT propagation bundle
copy TT bundle into Site
render TT status
check Governance Observatory status
write external evidence state
update final goal status
validate final goal status
validate final activation boundary
commit computed state changes
```

## Remaining Non-Local Dependency

The only remaining blocker is externally produced evidence that Site cannot invent:

```text
Publisher paper mirror closure evidence
first committed TT bundle-fed status
Governance Observatory validation evidence
```

These are now monitored by repository workflows and generated status files rather than manual inspection.

## Non-Claims

```text
Manual task elimination does not make Site proof authority.
Manual task elimination does not make Site source authority for Publisher, TT, or Governance Observatory records.
Manual task elimination does not grant commit-time permission.
Manual task elimination does not replace SPE standing determination.
```

## Current State

```text
local_manual_tasks: eliminated
local_continuation: workflow_managed
activation_state: pending_external_evidence
```
