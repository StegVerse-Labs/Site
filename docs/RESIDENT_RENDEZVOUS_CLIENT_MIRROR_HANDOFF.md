# Site Resident Rendezvous Client Mirror Handoff

Updated: 2026-08-30
Repository: StegVerse-Labs/Site
Issue: #768
Merged PR: #772\nMerge: 9e3ef8878276ffc0d7f92982acf8cced251120d8
State: RELEASED_SOURCE / DISCOVERY_AND_RESIDENT_CONSUMPTION_RECEIPT_BOUND
Authority effect: NONE
Activation effect: false

## Goal

Give the current browser/iPhone a bounded way to place an already-defined resident execution intent onto the StegVerse Service Gateway rendezvous without requiring SSH, systemd access, a second user machine, or an arbitrary remote-command channel.

## Canonical request

The client may submit exactly one v1 request class:

```text
consumer=stegos_kv_intr_chain
resident_request.schema=stegverse.resident-execution-request/v1
resident_request.task_id=SHWP-STEGOS-KV-INTR-CHAIN-001
resident_request.mode=STEGOS_KV_INTR_CHAIN
resident_request.entrypoint=scripts/refresh_and_execute_resident_task.py
```

The exact three admitted steps remain:

```text
SHWP-STEGOS-SOVEREIGN-RELAY-MATERIALIZATION-001
SHWP-STEGOS-RELAY-NODE-KV-CONTINUITY-001
SHWP-DEVICE-KV-INTR-OBSERVATION-001
```

## Authority boundary

The browser request grants no claim, fence, execution authority, credential authority, runtime authority, provider operation, route authority, or canonical KV mutation.

The resident WorkerCoordinator independently decides whether any locally materialized request can progress.

## Configuration

The client consumes an explicit runtime configuration:

```text
gateway_base_url: HTTPS StegVerse Service Gateway origin
target_node_ref: opaque non-secret sovereign node selector
authorization_ref: opaque owner/session authorization reference
```

No credential values or reusable secrets are accepted by the client.

## Fail-closed

- non-HTTPS gateway rejected;
- cross-origin credentials omitted;
- exact request digest computed in WebCrypto;
- lease <= one hour;
- blind retry forbidden after ambiguous POST outcome;
- arbitrary task/command/argv/source path/provider fields impossible through public API;
- response cannot claim execution authority.

## Lifecycle

```text
IMPLEMENTED: IN_PROGRESS
VALIDATED: false
MERGED: false
PUBLIC_GATEWAY_ROUTE_OBSERVED: false
RESIDENT_CONSUMPTION_OBSERVED: false
ACTIVATED: false
COMPLETE: false
```


## Merge evidence

```text
issue: #768 CLOSED_BY_MERGE
PR: #772 MERGED
merge: 9e3ef8878276ffc0d7f92982acf8cced251120d8
validated head: 45e71a16c8a82c4b4802d1995c8d9fa87fb33dbd
Site Handoff Orchestrator: 33351842921 SUCCESS
Site Bootstrap Validate: 33351842932 SUCCESS
Ecosystem Heartbeat Orchestration: 33351842926 SUCCESS
My KV Personal Information: 33351842952 SUCCESS
Site Task Diagnostic Contract: 33351842923 SUCCESS
```

The browser/iPhone request carrier is now merged. Live activation remains gated on a public sovereign Service Gateway rendezvous route and a resident that has refreshed to the merged outbound consumer.


## 2026-08-31 request-003 shared-HB terminal propagation — issue #829

The current browser/iPhone rendezvous producer emits exactly:
```text
RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003
```

The request retains the canonical three-step chain and does not reintroduce endpoint fanout. Request 003 reflects the stronger resident terminal boundary: a DEVICE_KV terminal must retain and independently validate both exact shared HB carrier signals in addition to the underlying exact transport/recovery predicates.

This browser surface remains a request carrier only. It grants no claim, fence, WorkerCoordinator execution authority, heartbeat progression authority, credential, route, transition, receiving, KV mutation, repository, deployment, or release authority. Ambiguous submission still forbids blind retry.


## 2026-09-02 registered-Node discovery recovery — issue #851 R2

Stale PR #854 contained a bounded improvement that had never reached current main: replacing manual resident target/auth inputs with registered-Node Receipt #1 provenance plus same-origin resident discovery.

Recovered current-main sequence:

```text
StegVerseNodeContinuity.status()
-> require REGISTERED
-> require Receipt #1 matches registration
-> provenance = node-receipt-1-sha256:<receipt_sha256>

GET /api/resident-rendezvous/v1/discovery
-> request-003 only
-> consumer stegos_kv_intr_chain
-> state AVAILABLE
-> exactly one SV-NODE-<24 hex> target
-> discovery authority NONE

POST /api/resident-rendezvous/v1/requests
-> discovered target
-> Receipt #1 provenance in existing wire-compatible authorization-ref field
-> request state PENDING only
-> WorkerCoordinator execution authority remains NONE at Gateway
```

My KV Directory exposes **Request resident connection** only to an already-registered browser Node. No manual target selector, credential value, reusable secret, or second user-operated device is required.

Ambiguous POST remains `VERIFY_EXTERNALLY` with blind retry forbidden. Discovery GET is non-mutating and may be repeated.

Branch: `feat/my-kv-resident-rendezvous-discovery-851-r2`
Recovery claim: `SITE-MY-KV-RESIDENT-RENDEZVOUS-DISCOVERY-851-R2-20260902`
State: IMPLEMENTED_SOURCE_PENDING_VALIDATION_MERGE


## 2026-09-02 R2 release reconciliation

Current-main recovery PR #944 merged as `f012af5e9ecad8dc73aff2992314009484a1cac3`.

Validated exact head:

- Site Bootstrap Validate `33713849795` — SUCCESS
- Site Handoff Orchestrator `33713849796` — SUCCESS
- Ecosystem Heartbeat Orchestration `33713849820` — SUCCESS
- My KV Directory Landing `33713849802` — SUCCESS

Stale PR #854 is superseded by #944.

The current-iPhone source path no longer requires manually supplied `target_node_ref` or authorization text. An already-registered Node derives Receipt #1 provenance locally, performs same-origin request-003 discovery, and submits only the discovered canonical target through the bounded existing rendezvous request.

Live Gateway discovery, request storage, resident consumption, and WorkerCoordinator execution remain separate receipt-bound runtime outcomes. They do not retain source ownership and do not create a second-device requirement.
