# Coherent Transition Threshold Actions Fanout Mirror Handoff

Updated: 2026-08-23
Repository: `StegVerse-Labs/Site`
Parent Actions handoff: `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
Implementation task: `SITE-0001-COHERENT-TRANSITION-THRESHOLD`
Activation task: `SITE-0001-COHERENT-TRANSITION-THRESHOLD-ACTIVATION`
Workflow: `.github/workflows/coherent-transition-threshold.yml`
Claim: `SITE-COHERENT-THRESHOLD-PR-FANOUT-CONTAINMENT-20260823`
State: `IMPLEMENTATION_IN_PROGRESS`

## Source of truth and authority boundary

The bounded threshold implementation task is complete, but activation is separately `RUNNING` and machine-owned. The activation task explicitly requires derivation after relevant heartbeat, orchestration, or repository-task state changes and forbids manually setting `THRESHOLD_ESTABLISHED`.

This Actions repair therefore does not retire the main-branch observation path. It only removes avoidable pull-request fanout caused by routine carrier/state files that do not need a PR validation run to keep active main observation functioning.

```text
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
runtime_authority_effect: false
activation_authority_effect: false
Render: prohibited
```

## Pre-repair fanout

The workflow currently triggers both `push` and `pull_request` on the same broad list, including:

- `data/ecosystem-heartbeat-state.json`;
- `data/site-orchestration-state.json`;
- `data/coherent-transition-threshold-state.json`;
- `data/coherent-transition-threshold-observation.json`;
- threshold task and activation task objects;
- `scripts/observe_and_complete_repository_tasks.py`.

Those paths are runtime/orchestration/task/derived-state carriers. Their inclusion in `push` remains relevant to the active activation observer, but duplicating them in `pull_request` creates avoidable hosted validation whenever a PR carries routine state/projection updates.

## Retained automatic PR validation inputs

Pull-request validation must remain automatic for files that define threshold behavior or its validation contract:

- `docs/COHERENT_TRANSITION_THRESHOLD_LAYER.md`;
- `docs/session-consolidation/COHERENT_TRANSITION_THRESHOLD_SESSION_TRANSFER_2026-08-02.md`;
- `data/coherent-transition-threshold.schema.json`;
- `scripts/derive_coherent_transition_threshold.py`;
- `scripts/check_coherent_transition_threshold.py`;
- `scripts/check_coherent_transition_threshold_activation.py`;
- `.github/workflows/coherent-transition-threshold.yml`.

`workflow_dispatch` remains for intentional manual validation.

## Retained main observation responsibility

The `push` trigger remains unchanged in this repair, including heartbeat, orchestration, task, derived-state, schema, documentation, and validator paths. This preserves the active activation task's machine-observable next action without treating workflow success as activation proof.

## Completion gate

This repair is released only when:

1. pull-request triggers are narrowed exactly as described;
2. the main push trigger remains intact;
3. manual dispatch remains;
4. permissions remain `contents: read`;
5. no threshold predicate or activation state is changed;
6. session-claim validation passes;
7. Site handoff orchestration passes;
8. canonical Site Bootstrap validation passes;
9. integration merges;
10. this handoff and the claim record are terminalized with exact evidence.

A workflow PASS proves validation only. It does not establish `THRESHOLD_ESTABLISHED`, runtime continuity, sovereign scheduler execution, or ecosystem activation.
