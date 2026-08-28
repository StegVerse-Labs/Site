# My KV Connection Health Projection Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#584`
Branch: `feature/my-kv-connection-health`
State: SOURCE_LANE_OPEN / IMPLEMENTATION_IN_PROGRESS
Authority effect: NONE
Activation effect: false
Updated: 2026-08-28

## Purpose

Project canonical Personal KV connection assembly health into My KV directory cards without moving connection, provider, credential, or reconciliation authority into Site.

## Upstream authority

Canonical connection state remains upstream in `StegVerse-Labs/continuity-vault-kit`:

- `KV_CONNECTION_ASSEMBLY_SOURCE_MIRROR_HANDOFF.md`
- `KV_CONNECTION_REGISTRY_MATERIALIZATION_MIRROR_HANDOFF.md`
- `schemas/kv-connection-health-receipt.schema.json`

Machine reconciliation remains resident WorkerCoordinator-owned in `StegVerse-Labs/.github`.

## Site bridge contract

Site reads bounded health only through:

`window.StegVerseKVConnectionHealthBridge`

Expected read request:

```text
schema: stegverse.site.my-kv.connection-health-request/v1
directory_id: <known My KV domain>
canonical_path: <exact KV path>
access: READ_ONLY
authority_effect: NONE
```

Expected bounded response includes:

- canonical path;
- compatibility state;
- optional last observation time;
- optional reason;
- revalidation-required boolean;
- credential material present: false;
- provider operation authorized: false.

## Allowed states

```text
UNASSEMBLED
ASSEMBLED_UNVERIFIED
VERIFIED
DEGRADED
REVALIDATION_REQUIRED
BLOCKED_SOURCE_CHANGE
BLOCKED_SESSION
BLOCKED_RUNTIME
RETIRED
```

## Invariants

1. Missing health bridge fails closed.
2. Site never fabricates VERIFIED.
3. Canonical path must exactly match the selected My KV domain.
4. Secret-bearing fields are rejected.
5. credential_material_present must be false.
6. provider_operation_authorized must be false.
7. Site stores no private connection health state.
8. Health projection is read-only.
9. Connect/refresh remains delegated to the direct-source SKAP bridge.
10. Revalidation/repair remains upstream machine execution, not a Site action in this lane.

## Planned source

- `docs/MY_KV_CONNECTION_HEALTH_MIRROR_HANDOFF.md`
- `assets/my-kv-directory.js`
- `my-kv.html`
- `tests/my-kv-directory.test.cjs`
- `scripts/check_my_kv_directory.py`
- active Site session-work claim fragment

## Current boundary

Source projection only. No provider session, private KV mutation, SKAP resolution, or connection repair is performed by this branch.
