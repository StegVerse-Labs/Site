# My KV DEVICE_KV Query/Return Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#863`
Branch: `feat/my-kv-device-kv-query-863`
State: RELEASED
Updated: 2026-08-31T13:24:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Provide the canonical DEVICE_KV query/return implementation for My KV directory, connection-health, and installation-status reads.

## Upstream

- StegOS #145 / PR #146 / merge `ba1e43dbadaef367c32c7a354fe2857746f6f1cd`
- CVK #164 / PR #165 / merge `f91e465bbf7196557005a8112a6c70c8712f9aaf`
- CVK #166 / PR #167 / merge `70b19663305e63ac6016af9b56848e91aa89b77c`
- .github #676 / PR #677 / merge `677ee5b65f6c8a7d4ced85e66e34850400675282`

## Browser chain

```text
My KV directory/health request
 -> current registered Node state
 -> kv.interlock.request.v1 + selector
 -> generated buildIntent("device-kv", ...)
 -> shared HB buildBinding(...)
 -> generated buildMaterializationRequest(..., {kv_request})
 -> Node outbox
 -> DEVICE_KV sync
 -> admitted resident query
 -> CVK read-only projection
 -> resident HB-derived response signal
 -> /intr/device-kv/result
 -> browser validates exact result/request/node binding
 -> browser recovers exact response bytes from HB-derived carrier
 -> StegVerseKVDirectoryBridge / StegVerseKVConnectionHealthBridge / StegVerseKVInstallationStatusBridge
```

## Runtime target

The fail-closed target gains `result_url`.

- unavailable target: `ingress_url=null`, `result_url=null`
- observed conforming target: exact same origin
  - `/intr/materialization`
  - `/intr/device-kv/result`

Both paths are projected only from authentic HTTPS `/intr/profile` evidence.

## Invariants

- exact current StegOS generated artifact + manifest only;
- query payload hash is canonical `kv_request`;
- authority ref is bound to exact current Node id;
- selector is directory id + exact canonical path only;
- query carries no provider credentials;
- result lookup cannot execute or re-read KV state;
- result response must be recovered from the exact canonical HB-derived carrier signal;
- response/request/materialization/node hashes must match;
- Site stores no private KV directory response as repository or durable public state;
- file bytes are not returned in directory listing;
- missing target/result/bridge fails closed.

## Claimed surfaces

- `assets/generated/site-browser-intr-connectors.js`
- `assets/generated/site-browser-intr-connectors.manifest.json`
- `assets/hb-intr-carrier.js`
- `assets/my-kv-device-kv-query-bridge.js`
- `stegos-node/device-kv-intr-sync.js`
- `stegos-node/device-kv-intr-sync-target.json`
- `scripts/project_device_kv_intr_sync_target.py`
- `my-kv-directory.html`
- `my-kv.html`
- `tests/canonical-generated-intr.test.cjs`
- `tests/test_device_kv_intr_sync.py`
- `tests/test_device_kv_intr_sync_target_projector.py`
- `tests/test_site_hb_intr_carrier_migration.py`
- `tests/my-kv-directory.test.cjs`
- `docs/MY_KV_DEVICE_KV_QUERY_RETURN_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-my-kv-device-kv-query-863-20260831.json`

## Completion boundary

Exact artifact copy, target/result projection, browser query/return bridge, exact HB response recovery, deterministic tests/checkers, exact-head Site validation, merge, claim terminalization. Runtime activation remains separately dependent on an authentically observed public sovereign profiled ingress and a real resident private KV root.


## 2026-08-31 public iPhone bridge-bootstrap correction

User-observed public Safari evidence showed the corrected owner-controlled import UI while the directory card still rendered `BRIDGE_UNAVAILABLE`. That isolates the failure ahead of DEVICE_KV query execution: the page did not have a usable `StegVerseKVDirectoryBridge` global at initialization.

The Site page now treats query-bridge availability as a runtime dependency that must be verified, not as a one-time nullable global capture.

Directory bootstrap:

```text
initial versioned query-bridge script load
-> verify StegVerseKVDirectoryBridge.listDirectory
-> if absent, append cache-busting retry script
-> verify bridge again
-> only then call loadDirectory
-> canonical DEVICE_KV query / local InTr runtime / HB return path
```

Landing connection-health bootstrap follows the same rule for `StegVerseKVConnectionHealthBridge.getDomainHealth`.

The query module itself now tolerates partial initialization. It returns early only when both canonical bridge methods already exist; otherwise it supplies whichever bridge half is missing and emits `StegVerseKVQueryBridgeModuleState` as non-authorizing module evidence.

The public UI may no longer convert a missing script/global into the generic statement that the user should "connect" a KnowledgeVault bridge. A bridge bootstrap failure is reported as the exact missing DEVICE_KV asset/module condition.

This correction changes no KV, HB, Node, credential, provider, or execution authority. It only ensures the already-merged canonical query/return path is actually initialized before the UI evaluates it.


## 2026-08-31 live KnowledgeVault installation-status extension

Merged upstream:

- continuity-vault-kit PR #168 / merge `b62387bb5ddb13dcca6ff5c7c24e5a14a2a10d23`
- StegVerse-Labs/.github PR #725 / merge `0ffe6a5ea61b2a0c24a28b702545ffbd8f6c0ec7`

My KV Step 2 now uses the existing DEVICE_KV query/return lane as its primary installation check:

```text
registered current Node
-> StegVerseKVInstallationStatusBridge.getInstallationStatus()
-> MY_KV_INSTALLATION_STATUS
-> Site / MyKVOnboarding
-> selector _System/installation.receipt.json
-> DEVICE_KV
-> current resident KV root
-> CVK bounded installation projection
-> HB-derived KV -> DEVICE return
-> browser exact-result validation
-> record Step 2 only when KV_INSTALLATION_VERIFIED
```

A verified live result requires resident KV-root observation, canonical receipt presence, validated template parity, bounded source census, and a canonical receipt digest. It explicitly requires `current_cloud_provider_observation=false`; Step 5 remains the cloud-provider revalidation boundary.

If the live query is unavailable, a previously validated local proof may still restore continuity under the existing bounded fallback rules. If the resident KV is reached and explicitly reports `KV_INSTALLATION_NOT_VERIFIED`, that result is not overridden automatically by stale local proof.

The Connect / verify KV button also attempts live DEVICE_KV status first. It opens the owner-selected receipt picker only when the live result cannot verify the installation.


## 2026-09-02 Personal-KV provider-root boundary reconciliation

The current iPhone service worker is local-cache ingress only for `MY_KV_DIRECTORY_PROJECTION` and `MY_KV_CONNECTION_HEALTH`. It is **not** a canonical provider-backed KV receiver for `MY_KV_INSTALLATION_STATUS`, Workspace projection, or Personal Contact Profile operations.

Accordingly, the Site query bridge now permits device-local admission evidence only for directory/health. Installation status requires downstream/canonical KV delivery. This prevents browser-local cache state from being interpreted as Personal-KV runtime observation.

Upstream source state now includes a bounded provider-root resolver:

```text
StegVerse-Labs/continuity-vault-kit/runtime/personal_provider_binding.py
 -> StegVerse-Labs/.github/scripts/materialize_personal_kv_provider_root.py
 -> DEVICE_KV consumer
```

The owner-connected KnowledgeVault and canonical installation receipt exist. The remaining automatic-runtime blocker is an active TVC-owned provider session. Site must not acquire, store, or synthesize that provider credential/session and must continue to fail closed or offer the explicit owner-mediated Files fallback.


## Release reconciliation — 2026-09-02

The canonical claim `SITE-MY-KV-DEVICE-KV-QUERY-863-20260831` is already `RELEASED`.

```text
pull_request: #866
release_commit: 7c426aeddb39769f33c7c243749122724b1f34ea
archive_eligible: true
```

The DEVICE_KV query/return source implementation is released. Current device-local runtime validation remains a separate observation concern and does not keep this handoff in active implementation state.


## 2026-09-21 fresh-Node relationship-state correction

A newly registered Node with no historical KnowledgeVault relationship exposed a semantic defect in the Step 2 installation-status model. The prior device-local projection treated an empty DEVICE_KV store as `KV_INSTALLATION_NOT_VERIFIED` and asserted `resident_kv_root_observed=true`, which incorrectly implied that a KV relationship already existed.

The corrected projection is three-state and non-authorizing:

```text
KV_RELATIONSHIP_NOT_ESTABLISHED
  kv_relationship_established=false
  resident_kv_root_observed=false
  installation_receipt_present=false

KV_INSTALLATION_NOT_VERIFIED
  kv_relationship_established=true
  resident_kv_root_observed=true
  installation_receipt_present=false

KV_INSTALLATION_VERIFIED
  kv_relationship_established=true
  resident_kv_root_observed=true
  installation_receipt_present=true
```

An empty DEVICE_KV relationship surface now returns `KV_RELATIONSHIP_NOT_ESTABLISHED`. My KV Step 2 therefore offers explicit owner choices to create a new device-local KV or deliberately connect an existing KV. The installation-receipt picker remains hidden for the fresh-Node state and is exposed only after the owner selects the existing-KV path or DEVICE_KV has already produced relationship evidence.

Node registration and `MY_KV_ONBOARDING_STEP_1_COMPLETED` remain Node continuity only and cannot establish or imply a KV relationship. TV/TVC credential authority, Interlock/InTr transition authority, fail-closed query/return semantics, existing verified-KV behavior, and Step 5 cloud revalidation remain unchanged.


## 2026-09-21 browser-local KV installation-claim correction

Authentic current-iPhone Safari observation showed the `device-kv-install.html` surface reporting:

```text
State: INSTALLED
Storage: device-local-browser-indexeddb
Persistence: requested; granted=false
Exact readback: true
```

That combination proves browser-origin IndexedDB initialization and exact readback, but not an installed resident KnowledgeVault. The implementation had conflated “rows exist and read back” with “installed”.

The corrected state model is:

```text
BROWSER_KV_NOT_INITIALIZED
  initialized=false
  installed=false

BROWSER_KV_INITIALIZED_BEST_EFFORT
  initialized=true
  installed=false
  installation_claimed=false
  persistent_storage_granted=false

BROWSER_KV_INITIALIZED_PERSISTENCE_GRANTED
  initialized=true
  installed=false
  installation_claimed=false
  persistent_storage_granted=true
```

Even a granted browser persistence request remains browser-origin storage, not proof of native software, an OS service, a filesystem mount, or an independently durable resident runtime. The page now says exactly what it does: create browser-local KV data. Cloud/KV peer setup may consume an initialized exact-readback browser KV as a local data instance without converting that fact into an installation claim.

This repair preserves the separate `KV_RELATIONSHIP_NOT_ESTABLISHED` relationship model and does not advance any authentic Device -> KV -> SKAP -> KV -> Device runtime predicate.
