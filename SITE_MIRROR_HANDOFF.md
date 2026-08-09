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

The previously tracked Cloudflare Worker deployment remains optional hardening. Its absent credential values are not a blocker to functional StegGate or to the tunnel-native rendezvous path.

```text
optional stable origin: https://stegverse.org/api/steggate
CLOUDFLARE_API_TOKEN value present: NO
CLOUDFLARE_ACCOUNT_ID value present: NO
impact on tunnel-native activation: NONE
```

TV/TVC credential-reference contracts remain valid boundaries for any future provider-specific publication, but they do not manufacture secret values and they do not own StegGate execution.

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
TV credential-reference packaging: StegVerse-Labs/TV
TVC secret-reference authority: StegVerse-Labs/TVC
```

## Completion / archive posture

Primary Site application work remains complete. The StegGate architecture correction is durably installed and now has fresh epoch-5 hosted proof: tunnel-native heartbeat execution is the active path; persistent third-party hosting is optional hardening rather than a prerequisite.

Current-liveness remains lease-sensitive by design. The next admitted heartbeat is the recovery/refresh mechanism when no verified tunnel remains live; no manual user action is assigned.
