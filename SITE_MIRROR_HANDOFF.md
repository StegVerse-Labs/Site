# Site Mirror Handoff

## Current source of truth

This file is the authoritative continuation record for `StegVerse-Labs/Site`.

## Primary Site application goal

```text
Goal: governed Ecosystem Chat and AI Entry application with fail-closed live activation, recoverability, release, and downstream evidence boundaries
Repository-local result: COMPLETE
Manual user tasks: NONE
Recursive repository-local goal expansion: DISABLED
```

The completed primary Site application implementation remains governed by its existing validation, custody, reconstruction, release, and downstream evidence boundaries. Absent live evidence never becomes success.

## Adjacent active goal — StegGate tunnel-native rendezvous

```text
goal_id: STEGGATE-TUNNEL-NATIVE-RENDEZVOUS
canonical_owner: StegVerse-Labs/Site#24 + StegVerse-Labs/StegCore heartbeat tunnel runtime
originating_completed_dependencies:
  - StegVerse-Labs/StegCore#68 — functional StegGate COMPLETE
  - StegVerse-Labs/StegCore#75 — heartbeat/credential integration COMPLETE
state: CURRENT_HEARTBEAT_TUNNEL_VERIFIED
scheduler_authority: single StegVerse heartbeat
wall_clock_scheduler_authority: false
persistent_third_party_host_required: false
```

The active path is the heartbeat-owned StegGate micro-node plus its verified ephemeral public tunnel. Render is not authoritative and is not an activation prerequisite. A provider-specific stable-domain route such as `https://stegverse.org/api/steggate` is optional availability/discovery hardening only.

## Installed tunnel/discovery surfaces

```text
StegVerse-Labs/.github/.github/workflows/steggate-heartbeat-integration.yml
StegVerse-Labs/.github/management/STEGGATE_HEARTBEAT_CREDENTIAL_INTEGRATION_001.json
StegVerse-Labs/StegCore/.github/workflows/steggate-heartbeat-worker-reusable.yml
StegVerse-Labs/StegCore/.github/workflows/steggate-fallback-public-runtime.yml
StegVerse-Labs/StegCore/src/stegcore/endpoint_discovery.py
StegVerse-Labs/StegCore/management/steggate-heartbeat-credential-integration.json
StegVerse-Labs/Site/src/steggate-rendezvous-worker.js
StegVerse-Labs/Site/data/steggate-rendezvous-activation.json
```

`src/steggate-rendezvous-worker.js` contains no StegGate policy engine. It resolves only a registry-declared live StegGate micro-node, independently verifies canonical health, proxies the bounded HTTP contract, and fails closed when no verified node exists.

## Canonical tunnel acceptance

A tunnel is usable only after independent verification of:

```text
/health                  state=healthy; canonical_three_layer_bound=true
/v1/self-test            exact ALLOW / DENY / REVIEW / FAIL_CLOSED
/v1/evaluate             deterministic complete-matrix acceptance
```

Historical tunnel success does not assert current liveness. Tunnel endpoints are lease-bound and must be re-resolved and reverified for current use.

## Current heartbeat tunnel proof

Fresh canonical proof:

```text
StegVerse-Labs/.github workflow run: 31325104576
heartbeat job: 93274099310 SUCCESS
StegGate micro-node job: 93274112655 SUCCESS
heartbeat id: HB-31325104576-5
heartbeat epoch: 5
StegCore commit executed: f0d764b2b5b48987d75ea4efd1da1fafde04b406
current observed tunnel origin: https://owners-recipes-catherine-laid.trycloudflare.com
/health: PASS
/v1/self-test: PASS
/v1/evaluate: PASS
heartbeat artifact: 9041292966
heartbeat digest: sha256:bc0c6d498f0f270f2fa1ec2de29444b4d2cd809d726287fb70f36f2decb9e919
micro-node artifact: 9041297862
micro-node digest: sha256:a1222757e3fe0187b58ce2bd26c32600c70087c14c5f9e48f68ee7ffa2473b69
observed_at: 2026-08-09T16:57:13.142713Z
```

The deterministic evaluation returned canonical `ALLOW` with all required matrix predicates PASS, permission/admissibility separation preserved, no external execution, and no continuity receipt minted by the observer.

The older issue-comment registry origin from 09:14 UTC remains historical rotating-endpoint evidence only. Consumers must not equate that declaration with current liveness.

## Stable-domain / provider-specific lane

The Cloudflare Worker stable-domain lane remains optional hardening. It is now an **actually activated StegVerse heartbeat worker task**, not merely a documented blocker.

Canonical worker continuation:

```text
task: STEGGATE-STABLE-RENDEZVOUS-WORKER-001
registry: StegVerse-Labs/.github/control/worker-registry.json
handoff: StegVerse-Labs/.github/handoffs/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
authorization: StegVerse-Labs/.github/authorizations/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
worker: steggate-rendezvous-deployment-worker
adapter: process:steggate-rendezvous-deployment-v1
claim: SHWP-STEGGATE-STABLE-RENDEZVOUS-WORKER-001-G13
worker_instance: steggate-rendezvous-deployment-worker-HB7-G13
heartbeat_epoch: 7
fencing_token: 13
state: BLOCKED
current_transition: CREDENTIAL_VALUES_ABSENT
expected_next_transition: CREDENTIAL_RECHECK
checkpoint: checkpoints/workers/STEGGATE-STABLE-RENDEZVOUS-WORKER-001/HB7-G13.json
worker_receipt: receipts/steggate-rendezvous-worker/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
heartbeat_run: 31325420776
heartbeat_job: 93274879376 SUCCESS
heartbeat_artifact: 9041376225
heartbeat_artifact_digest: sha256:590af345db1d942993345f7d5ecff50998ddc4d6898331d7bcf6d3adabd94756
```

The canonical heartbeat status projection independently classified this unfinished worker as `archive_eligible=true`, with `executor_binding=BOUND`, heartbeat timing established, authority resolved, a live claim/fence, and a canonical checkpoint. This means the remaining provider-specific hardening is now worker-owned in the precise sense required by the session-consolidation rule; it is not merely durably assigned.

The worker performs no wall-clock polling. On admitted heartbeat execution it re-evaluates the bounded provider credential references. Missing values return `BLOCKED` and remain claimed/checkpointed. When values are present, the same worker validates the exact Cloudflare Workers capability, verifies the pinned canonical Site rendezvous source blob, deploys only the non-authorizing `stegverse-steggate-rendezvous` route, and requires readiness/health/four-disposition live acceptance before returning `COMPLETED`.

```text
optional stable origin: https://stegverse.org/api/steggate
CLOUDFLARE_API_TOKEN value present: NO
CLOUDFLARE_ACCOUNT_ID value present: NO
impact on tunnel-native activation: NONE
release condition for worker transition: both values are present in the authorized heartbeat execution environment
```

TV/TVC credential-reference contracts remain valid boundaries for provider-specific publication. They do not manufacture secret values and they do not own StegGate execution.

## Current execution rule

Machine-observable current-use condition:

```text
A heartbeat-owned StegGate tunnel is freshly discoverable
AND it independently passes canonical health
AND it passes exact self-test
AND deterministic /v1/evaluate passes the acceptance contract.
```

This condition is satisfied by heartbeat epoch 5 evidence above. Consumers may use a verified tunnel only within its actual live lease. If no current tunnel is discoverable, the system fails closed and the next admitted heartbeat worker is the canonical recovery path. Do not wait on Render build minutes or provider-specific hosting credentials.

## Collision and authority boundaries

```text
heartbeat != execution authority
tunnel availability != StegGate admissibility
registry declaration != current health
provider transport != policy authority
rendezvous routing != StegGate policy authority
SDK validation != execution
local persistence != custody
custody receipt != execution authority
reconstruction PASS != execution authority
workflow artifact != current endpoint evidence
```

Canonical owners:

```text
single heartbeat: StegVerse-Labs/.github#12
StegGate runtime/tunnel: StegVerse-Labs/StegCore
Site tunnel consumption/rendezvous: StegVerse-Labs/Site#24
stable-domain hardening worker: StegVerse-Labs/.github/control/worker-registry.json#STEGGATE-STABLE-RENDEZVOUS-WORKER-001
TV credential-reference packaging: StegVerse-Labs/TV
TVC secret-reference authority: StegVerse-Labs/TVC
```

## Completion / archive posture

Primary Site application work remains complete. The StegGate architecture correction has hosted proof: tunnel-native heartbeat execution is the active path; persistent third-party hosting is optional hardening rather than a prerequisite.

The optional stable-domain hardening itself is not complete because the Cloudflare credential values are absent, but its continuation is no longer chat-owned or merely documented. It is actively claimed by the single-heartbeat worker registry with a bound executor, heartbeat-relative timing, fencing token, live BLOCKED transition, worker receipt, and canonical checkpoint. Current-liveness remains lease-sensitive by design; the heartbeat remains the recovery/refresh mechanism and no wall-clock scheduler owns the lane.
