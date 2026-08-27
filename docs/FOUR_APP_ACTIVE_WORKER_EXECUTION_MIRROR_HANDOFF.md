# Four-App Active Worker Execution Mirror Handoff

## Authority

```text
goal_id: STEGGATE-FOUR-PUBLIC-APPS-001
repository: StegVerse-Labs/Site
branch: main
parent_issue: Site#239
canonical_worker_assignments: data/four-app-active-worker-assignments.json
policy_owner: StegVerse-Labs/.github/docs/BLOCKER_RESOLUTION_MIRROR_HANDOFF.md
state: ACTIVE_WORKER_EXECUTION
passive_blocked_task_state_allowed: false
```

This scoped handoff governs execution-state wording and worker ownership for Ecosystem Chat, VACC, Math Solver, and HIL. It does not change any product gate from false to true and does not manufacture activation evidence.

## Governing rule

An unmet predicate is a **dependency condition**, not permission for a task to sit in `BLOCKED` state. Every incomplete four-app capability must be represented by an active documented worker that is executing a solution, workaround, construction, escalation, or authorized retry path.

`BLOCKED` may remain inside historical receipts or as the result of a single fail-closed execution attempt. It is not the ongoing task state. After a failed attempt, the task returns to `WORKER_ACTIVE_*` with the observed condition, next solution action, and evidence required for completion.

Observer-only loops do not count as progress when they merely rediscover the same condition. The worker must either change the system, select/construct another admitted route, produce new evidence, or persist a machine-observable reason why the next action must occur on another canonical worker.

## Current worker assignments

### Ecosystem Chat

```text
state: WORKER_ACTIVE_SOVEREIGN_ACTIVATION
primary_worker: StegVerse-Labs/.github/workers/ecosystem_chat_sovereign_inference_worker.py
canonical_task: .github#60 / SHWP-ECOSYSTEM-CHAT-INFERENCE-001
support: sovereign_runtime_activation_worker -> TVC route task -> LLM-adapter task 020 -> Master Records
condition: post-HB29 sovereign same-execution evidence not yet emitted
next_action: solve/construct eligible sovereign carrier and execute installed chain
```

### VACC

```text
state: WORKER_ACTIVE_AUTHORIZED_EXECUTION_RESOLUTION
primary_worker: StegVerse-org/LLM-adapter#90 / VACP-ADAPTER-AUTHORIZED-EXECUTION-005
observer/executor: va-claim-assistant-provider-preflight.yml
condition: exact admitted provider execution plus protected Master Records authority/configuration have not converged
next_action: resolve an admitted route/authority, execute one real VA request, obtain custody/reconstruction, activate Site projection
```

The six-hour preflight is not allowed to become an indefinite waiting loop. Repeated unchanged failure must drive route/authority-resolution work under the canonical owner.

### Math Solver

```text
state: WORKER_ACTIVE_HOST_ROUTE_REPAIR
primary_worker: StegVerse-org/LLM-adapter#132 / MATH-SOLVER-STEGGATE-RUNTIME-001
support: observe-math-solver-public-runtime.yml + Site math-solver-public-activation.yml
condition: public readiness 404 plus current Render build failures
next_action: repair or replace the admitted host route, then prove readiness -> governed solve -> receipt -> replay
```

Direct Render inspection on 2026-08-12 found the current service `srv-d9epkh3rjlhs73csc3qg` repeatedly entering `build_failed` for recent auto-deploy commits. This is now repair input for the worker, not a passive blocker.

### HIL

```text
state: WORKER_ACTIVE_PARTICIPANT_CYCLE_ACTIVATION
primary_worker: StegVerse-Labs/hybrid-collab-bridge#11
canonical_packages: HIL-QRL-002..007
support: Site heartbeat/SITE-0002-HIL-LIVE -> GCAT/BCAT admission -> Master Records
condition: hosted replay, admission, custody, and public participant cycle incomplete
next_action: execute replay validation, admission, custody, then public governed cycle
```

## Compatibility with fail-closed governance

Fail-closed execution remains mandatory. `WORKER_ACTIVE` means the orchestration/task owner keeps working on the missing condition; it does **not** authorize a product action whose required gate is absent.

The distinction is:

```text
product gate false -> consequence remains refused
worker task -> ACTIVE and solving the false gate
```

## Credential boundary

```text
GitHub token production authority: NONE
credential/route authority: TV/TVC
GitHub Actions: validation/observation only unless a repository contract explicitly grants a bounded non-production action
```

## Required status reporting

Future four-app status reports must say which worker owns every unmet gate and what that worker is doing next. Do not describe an application as simply blocked or waiting.

Historical `BLOCKED` strings in older receipts/status snapshots are observations of prior attempts, not the current orchestration state.

## Completion

```text
four applications assigned to active workers: 4/4
passive unresolved application tasks: 0
worker assignment manifest: COMPLETE
canonical scoped handoff: COMPLETE
product activation gates changed by this mutation: 0
```

MERGED INTO: Site#239 plus the canonical worker/task owners named in `data/four-app-active-worker-assignments.json`.


## 2026-08-27 Math Solver worker reconciliation

The historical Render-host-repair wording above is superseded for current execution.

Current canonical Math Solver worker:
```text
state: WORKER_ACTIVE_SOVEREIGN_CARRIER_OBSERVATION
primary_worker: StegVerse-org/LLM-adapter#132 / scripts/observe_math_solver_public_runtime.py
canonical_task: StegVerse-org/LLM-adapter/tasks/MATH-SOLVER-STEGGATE-RUNTIME-001.json
shared_carrier_owner: StegVerse-org/LLM-adapter#72 Service Gateway / portable-node runtime
Site consumer: Site#240 / unified Ecosystem Chat
credential_authority: TV/TVC
github_token_runtime_authority: NONE
third_party_runtime_required: false
Render runtime authority: NONE
```

Canonical Math source state is 7/9 implementation gates complete. The missing product gates are:
1. observe an eligible StegVerse sovereign carrier serving the current Math Solver readiness/solve routes with canonical StegGate identity, ALLOW/EXECUTED evidence and deterministic replay;
2. consume that exact COMPLETE runtime receipt through Site#240 and directly verify the unified/public Site binding.

The unified Site Math client is now source-bound to the verified activation receipt rather than the stale static gateway URL. Source commits:
- `1f16a9116b44996d6611fd9a69766cb325d015db` — shared `askMath` consumes the governed solver only after Site activation state is COMPLETE;
- `e9bec934942e09ee8c0e899b65649ec5e0ea3598` — activation receipt consumption requires the complete canonical observer check set and exact authority boundaries;
- `8df5129845c23fa5755299379ac1cea8bd378416` — shared runtime validator locks the governed Math binding;
- `a2f9e4ed9ee0834a7e26f24661386a13ed4bb8b5` — legacy hourly/writeback Math activation workflow converted to validation/evidence transport only;
- `1714524a5db47f0fdaaef079338534a4472aa5df` — workflow inventory reconciled to the validation-only capability set.

The current LLM-adapter runtime observation remains BLOCKED because no eligible live carrier has yet answered. No execution or activation is inferred from the Site source binding.
