# Site KV Storage Endpoint v2 Mirror Handoff

Status: SOURCE_IMPLEMENTED / VALIDATION_PENDING / DEPLOYMENT_UNPROVEN / PROVIDER_RUNTIME_UNPROVEN
Repository: `StegVerse-Labs/Site`
Branch: `kv/storage-endpoint-v2`
Updated: 2026-09-15
Goal Task ID: `KV-CONNECTION-REVALIDATION-WORKER-001`
COSV ID: `50000000102000`
Canonical COSV handoff: `StegVerse-Labs/.github/KV_CONNECTION_REVALIDATION_COSV_MIRROR_HANDOFF.md`
Upstream CVK handoff: `StegVerse-Labs/continuity-vault-kit/KV_STORAGE_ENDPOINT_V2_MIRROR_HANDOFF.md`
Authority effect: `NONE`
Activation effect: `false`

## Purpose

Replace the cloud-only KV creation/adoption presentation with a provider-neutral storage-endpoint selector while preserving the exact legacy Google Drive KV #2 request lineage and all existing KV identity, provenance, relationship-tier, and Interlock/InTr semantics.

## Implemented source

`assets/kv-storage-endpoint-manager.js` adds v2 Site request surfaces:

```text
stegverse.site.kv-storage-endpoint-create-request/v2
stegverse.site.kv-storage-endpoint-adoption-request/v2
```

Supported endpoint classes:

- This Device / DEVICE;
- iCloud Drive, Google Drive, OneDrive, Dropbox / CLOUD;
- NAS / Network Storage / NETWORK;
- Removable Storage / REMOVABLE.

Each request retains `NOT_CONNECTED` initial relationship state, `PENDING_INTERLOCK_INTR`, no provider-operation authority, no instance materialization, no relationship mutation, no data movement, no replication, no AI-corpus exposure, `NONE_REQUEST_ONLY`, and `activation_effect=false`.

`normalizeLegacyV1()` accepts only the two existing cloud v1 request schemas and adds a storage-endpoint descriptor as a view-only compatibility projection. It does not change the original request ID, schema, or historical evidence.

## Google Drive KV #2 lineage

The existing owner-observed request remains:

```text
SITE-CLOUD-KV-4347408852127319cbda574f02e03edb
```

The prepared Google Drive action in `cloud-kv-peers.html` still uses `assets/cloud-kv-peer-manager.js` plus the existing resident transport. The new v2 manager is not used to regenerate that request. The page explicitly identifies the preserved lineage and keeps private-content and identity rewrite false.

## UI

The compatibility route `cloud-kv-peers.html` remains in place to avoid breaking links, but its user-facing semantics are now:

```text
My KV | Add KV | KV Instances
```

The creation selector is `Location`, not `Cloud storage`, and exposes device, cloud, NAS/network, and removable targets. The adoption section is `Use an existing KnowledgeVault` rather than cloud-only adoption.

## Validation

Added `tests/kv-storage-endpoint-manager.test.cjs` covering endpoint classes, adapter-specific credential/session posture, existing-KV provenance preservation, v1 normalization, no-secret locator input, and unchanged governance/runtime-effect sentinels.

`.github/workflows/cloud-kv-peer-manager.yml` now validates both the untouched legacy cloud v1 manager and the generic endpoint v2 manager, source syntax, existing Google Drive lineage retention, and absence of positive runtime-effect claims.

Hosted GitHub validation is pending until the PR runs. Local ad-hoc execution was not claimed because the current model container lacked outbound DNS to retrieve branch files.

## README maintenance

The root README must be updated on this PR before merge to list `assets/kv-storage-endpoint-manager.js`, the Add KV storage-endpoint selector, legacy-v1 compatibility, and the provider-runtime-unproven boundary. Do not merge without that README reconciliation.

## Remaining sequence

1. Open the Site PR and obtain hosted validation on the exact head.
2. Reconcile the root README before merge.
3. Preserve the existing Google Drive KV #2 request without re-emission.
4. Do not interpret source, CI, merge, or deployment as provider CONNECT/VERIFY execution or KV #2 materialization.
5. After upstream CVK and Site source merge, continue authentic provider execution only through the already-governed runtime path.

## Manual work

None. Do not re-emit the Google Drive KV #2 request, clear Safari/stegverse.org state, reinstall KV, or authorize Google Drive as part of this source/UI change.
