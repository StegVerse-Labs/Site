# Site KV Storage Endpoint v2 Mirror Handoff

Status: SOURCE_IMPLEMENTED / README_RECONCILED / HOSTED_VALIDATION_PASS_ON_PRE_HANDOFF_HEAD / PR_OPEN / DEPLOYMENT_UNPROVEN / PROVIDER_RUNTIME_UNPROVEN
Repository: `StegVerse-Labs/Site`
Branch: `kv/storage-endpoint-v2`
Implementation PR: `#1347`
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

The prepared Google Drive action in `cloud-kv-peers.html` still uses `assets/cloud-kv-peer-manager.js` plus the existing resident transport. The new v2 manager is not used to regenerate that request. The page explicitly identifies the preserved lineage, retains the compatibility instruction `No file selection or hash entry required`, and keeps private-content and identity rewrite false.

## UI

The compatibility route `cloud-kv-peers.html` remains in place to avoid breaking links, but its user-facing semantics are now:

```text
My KV | Add KV | KV Instances
```

The creation selector is `Location`, not `Cloud storage`, and exposes device, cloud, NAS/network, and removable targets. The adoption section is `Use an existing KnowledgeVault` rather than cloud-only adoption.

## README maintenance

Root `README.md` is reconciled on PR #1347 with a bounded `MyKV storage endpoint v2 source status` section. It documents endpoint classes, v1 compatibility, exact Google Drive KV #2 request-lineage preservation, storage-endpoint/access-adapter separation, and the explicit provider-runtime-unproven boundary.

## Coordination reconciliation

Site's fail-closed pre-work claim validator exposed a stale September 8 claim for the same root Goal Task ID. The prior evidence-reconciliation work had already merged in PR #1127 at `769cfa4e6c479fef26950889e8a1ea20d0502887` on 2026-09-08 21:36:10 CDT, but its fragment still said `CLAIMED_FOR_IMPLEMENTATION`. PR #1347 reconciles that historical claim to `RELEASED_COMPLETE` with the actual PR/merge evidence and installs one active claim `SITE-KV-STORAGE-ENDPOINT-V2-20260915` with the validator-required expiration/evidence/collision fields. This repairs stale coordination state rather than weakening one-owner-per-task enforcement.

## Validation evidence

`tests/kv-storage-endpoint-manager.test.cjs` covers endpoint classes, adapter-specific credential/session posture, existing-KV provenance preservation, v1 normalization, no-secret locator input, and unchanged governance/runtime-effect sentinels.

`.github/workflows/cloud-kv-peer-manager.yml` validates both the untouched legacy cloud v1 manager and the generic endpoint v2 manager, source syntax, existing Google Drive lineage retention, and absence of positive runtime-effect claims.

Pre-README implementation/coordination head `1ed79f6d9dfa346989ff6675c7a02c16e320b495` produced:

- KV Storage Endpoint Manager run `34941337500`: SUCCESS;
- Site Handoff Orchestrator run `34941337431`: SUCCESS;
- Ecosystem Heartbeat Orchestration run `34941337662`: SUCCESS;
- Site Bootstrap Validate run `34941337780`: SUCCESS;
- Node IndexedDB Schema Migration run `34941337538`: SUCCESS.

An earlier endpoint-manager failure was a compatibility-regression assertion requiring the exact user guidance `No file selection or hash entry required`; the UI was repaired to preserve that existing guidance. Earlier orchestrator failures exposed the missing/incomplete new claim and stale prior active claim; both were reconciled without weakening the validator.

README and handoff commits follow the green implementation head. Exact-head required checks must remain green before PR #1347 is marked ready. Hosted validation proves source/UI/control-plane conformance only; it does not prove deployment, provider access, CONNECT/VERIFY, KV #2 materialization, relationship mutation, data movement, replication, AI-corpus exposure, or runtime activation.

## Remaining sequence

1. Confirm exact-head required checks after README and this handoff reconciliation.
2. Mark PR #1347 ready for review only when required checks are green.
3. Preserve the existing Google Drive KV #2 request without re-emission.
4. Do not interpret source, CI, merge, or deployment as provider CONNECT/VERIFY execution or KV #2 materialization.
5. After upstream CVK and Site source merge, continue authentic provider execution only through the already-governed runtime path.

## Manual work

None. Do not re-emit the Google Drive KV #2 request, clear Safari/stegverse.org state, reinstall KV, or authorize Google Drive as part of this source/UI change.
