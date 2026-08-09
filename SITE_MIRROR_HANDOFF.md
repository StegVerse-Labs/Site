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

## Adjacent active goal — StegGate stable rendezvous hardening

```text
goal_id: STEGGATE-STABLE-RENDEZVOUS-HARDENING
canonical_owner: StegVerse-Labs/Site#24
originating_completed_dependencies:
  - StegVerse-Labs/StegCore#68 — functional StegGate COMPLETE
  - StegVerse-Labs/StegCore#75 — heartbeat/credential integration COMPLETE
state: BLOCKED_CREDENTIAL_VALUES_ABSENT
scheduler_authority: single StegVerse heartbeat
wall_clock_scheduler_authority: false
```

Installed surfaces:

```text
src/steggate-rendezvous-worker.js
wrangler.steggate.jsonc
.github/workflows/steggate-rendezvous-deploy.yml
data/steggate-rendezvous-activation.json
data/tvc-infrastructure-credential-consumer-authority.v1.json
```

Intended stable origin:

```text
https://stegverse.org/api/steggate
```

The Worker contains no StegGate policy engine. It routes only to a verified StegGate micro-node, independently verifies canonical health, proxies the bounded HTTP evaluation contract, and fails closed when no verified node exists.

## Scheduler model

The old hourly cron is removed. `steggate-rendezvous-deploy.yml` now accepts:

```text
repository_dispatch: stegverse-heartbeat   # normative continuity/scheduling carrier
workflow_dispatch                           # diagnostic only
bounded push paths                          # configuration validation only
```

Time does not manufacture heartbeat progress and does not own StegGate lifecycle.

## TV/TVC credential boundary

TV owns credential-reference packaging. TVC owns exact-bound secret-reference read authority. Neither stores or transports raw credential values.

Site imports the pinned no-secret TVC contract:

```text
data/tvc-infrastructure-credential-consumer-authority.v1.json
source: StegVerse-Labs/TVC/contracts/infrastructure-credential-consumer-authority.v1.json
source contract commit: ea6bc05c19001ab9731bc19fb59ff34eebf63e45
validated TVC policy commit: 9105cae48db28780c7fdfd9de7db317bb4595112
TVC validation run: 31305690694
TVC validation artifact: 9035862288
TVC artifact digest: sha256:a6ff49884bd4199f7b6f4ff8999d860d4517b547a4fd495118ccc59c00070562
credentials_recorded: false
credential_values_present: false
```

The Site workflow validates that pinned authority contract before examining execution-environment value presence.

## Strongest current rendezvous evidence

Run `31305845192`, job `93225990737` directly proved:

```text
pinned TVC authority contract validation: PASS
exact Site consumer binding: PASS
TVC reference-read authority: admissible
CLOUDFLARE_API_TOKEN value present in Site Actions: NO
CLOUDFLARE_ACCOUNT_ID value present in Site Actions: NO
Wrangler configuration/deploy: SKIPPED
stable endpoint acceptance: NOT EXECUTED
state: FAIL_CLOSED_CREDENTIAL_ABSENT
artifact: 9035908600
artifact digest: sha256:fe1be4cbdb0cd0a87542fe1ee40b2a1dad561c9355b5647cbfdd187c331c2af8
```

This is the correct fail-closed state. TV/TVC cannot manufacture missing provider credential values.

## Relationship to functional StegGate

Functional StegGate activation is already COMPLETE through the heartbeat-owned ephemeral micro-node topology. Canonical StegCore receipt:

```text
StegVerse-Labs/StegCore/data/steggate-live-activation-receipt.json
state: COMPLETE
deployment_source: heartbeat_ephemeral_micronode
```

The stable `stegverse.org/api/steggate` route is therefore availability/discovery hardening, not a prerequisite for the already-proven StegGate decision/runtime capability.

Canonical heartbeat-to-StegGate proof also exists independently of this stable route:

```text
StegVerse-Labs/.github workflow run 31306010854
heartbeat job 93226408727 SUCCESS
StegGate micro-node job 93226429725 SUCCESS
canonical heartbeat epoch advanced to 4
micro-node artifact 9035963753
micro-node digest sha256:b496a848c0f2561e1eb3b3dcdc33502f3019252995fa83cbe81e1c13c32651ba
```

## Release condition and next executable action

Machine-observable release condition:

```text
CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID both exist in the Site execution environment
AND the pinned TVC authority contract remains valid for the exact Site/workflow/branch binding.
```

When true, the same heartbeat-triggered workflow is authorized to:

1. build the production Wrangler configuration;
2. deploy the non-authorizing rendezvous;
3. verify readiness and canonical health;
4. verify exact ALLOW/DENY/REVIEW/FAIL_CLOSED self-test;
5. persist `LIVE_ACCEPTANCE_PASS` to `data/steggate-rendezvous-activation.json`;
6. retain no-secret deployment evidence.

If the credential values remain absent, the task remains `BLOCKED_CREDENTIAL_VALUES_ABSENT`; no alternate session may pretend the route is deployed.

## Collision and authority boundaries

```text
heartbeat != execution authority
TVC secret-reference ALLOW != secret value presence
credential value presence != StegGate admissibility
rendezvous routing != StegGate policy authority
provider output != authority
SDK validation != execution
local persistence != custody
custody receipt != execution authority
reconstruction PASS != execution authority
workflow artifact != live endpoint evidence
```

Canonical owners:

```text
single heartbeat: StegVerse-Labs/.github#12
StegGate runtime: StegVerse-Labs/StegCore
TV credential-reference packaging: StegVerse-Labs/TV
TVC secret-reference authority: StegVerse-Labs/TVC
stable endpoint publication/discovery: StegVerse-Labs/Site#24
```

## Completion / archive posture

Primary Site application work remains complete. The adjacent stable-rendezvous goal is not complete because actual Cloudflare credential values are absent from the authorized Site execution environment.

No wall-clock retry is normative. The repository is ready to execute on the next admitted heartbeat after the credential-value release condition becomes true.

This handoff fully preserves the blocker and continuation path, but the originating cross-repository StegGate session remains active while the user-directed activation/hardening work is still being pursued.
