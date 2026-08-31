# Site Resident Rendezvous Client Mirror Handoff

Updated: 2026-08-30
Repository: StegVerse-Labs/Site
Issue: #768
Branch: feature/resident-rendezvous-client
State: SOURCE_IMPLEMENTATION_IN_PROGRESS
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
