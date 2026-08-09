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
state: TUNNEL_NATIVE_ADOPTED / AWAIT_CURRENT_HEARTBEAT_TUNNEL
scheduler_authority: single StegVerse heartbeat
wall_clock_scheduler_authority: false
persistent_third_party_host_required: false
```

The active path is the heartbeat-owned StegGate micro-node plus its verified ephemeral public tunnel. Render is not authoritative and is not an activation prerequisite. A provider-specific stable-domain route such as `https://stegverse.org/api/steggate` is optional availability/discovery hardening only.

## Installed tunnel/discovery surfaces

```text
StegVerse-Labs/StegCore/.github/workflows/steggate-heartbeat-worker-reusable.yml
StegVerse-Labs/StegCore/.github/workflows/steggate-fallback-public-runtime.yml
StegVerse-Labs/StegCore/src/stegcore/endpoint_discovery.py
StegVerse-Labs/Site/src/steggate-rendezvous-worker.js
StegVerse-Labs/Site/data/steggate-rendezvous-activation.json
```

`src/steggate-rendezvous-worker.js` contains no StegGate policy engine. It resolves only a registry-declared live StegGate micro-node, independently verifies canonical health, proxies the bounded HTTP contract, and fails closed when no verified node exists.

## Canonical tunnel acceptance

A tunnel is usable only after independent verification of:

```text
/health                 healthy=true; canonical_three_layer_bound=true
/v1/self-test            exact ALLOW / DENY / REVIEW / FAIL_CLOSED
/v1/evaluate             deterministic complete-matrix acceptance
```

Historical tunnel success does not assert current liveness. Tunnel endpoints are lease-bound and must be re-resolved and reverified for current use.

Strongest completed tunnel evidence:

```text
StegCore workflow run: 31305399735
public tunnel step: PASS
full public acceptance step: PASS
verified runtime registry update: PASS
observed_at: 2026-08-09T09:14:06.578269Z
```

The canonical heartbeat-to-Steggate proof also remains valid independently:

```text
StegVerse-Labs/.github workflow run 31306010854
heartbeat job 93226408727 SUCCESS
StegGate micro-node job 93226429725 SUCCESS
canonical heartbeat epoch advanced to 4
micro-node artifact 9035963753
micro-node digest sha256:b496a848c0f2561e1eb3b3dcdc33502f3019252995fa83cbe81e1c13c32651ba
```

## Stable-domain / provider-specific lane

The previously tracked Cloudflare Worker deployment remains optional hardening. Its absent credential values are no longer a blocker to functional StegGate or to the tunnel-native rendezvous path.

```text
optional stable origin: https://stegverse.org/api/steggate
CLOUDFLARE_API_TOKEN value present: NO
CLOUDFLARE_ACCOUNT_ID value present: NO
impact on tunnel-native activation: NONE
```

TV/TVC credential-reference contracts remain valid boundaries for any future provider-specific publication, but they do not manufacture secret values and they do not own StegGate execution.

## Current execution rule

Machine-observable release condition:

```text
A current heartbeat-owned StegGate tunnel is discoverable
AND it independently passes canonical health
AND it passes exact self-test
AND deterministic /v1/evaluate passes the acceptance contract.
```

When true, consumers may use that verified tunnel for the bounded lease window. If no current tunnel is discoverable, the system remains fail-closed and the next admitted heartbeat worker is the canonical recovery path. Do not wait on Render build minutes or provider-specific hosting credentials.

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

Primary Site application work remains complete. The StegGate architecture correction is durably installed: tunnel-native heartbeat execution is the active path; persistent third-party hosting is optional hardening rather than a prerequisite.

Current-liveness verification remains lease-sensitive and must be performed against the current heartbeat tunnel when one exists. That condition is machine-observable and no manual user action is assigned.
