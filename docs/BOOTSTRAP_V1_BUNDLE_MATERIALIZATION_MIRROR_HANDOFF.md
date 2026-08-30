# Bootstrap v1 Bundle Materialization Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`

## Goal

Materialize one complete `stegverse.bootstrap.bundle/v1` on an already-established StegVerse browser node and emit replayable bundle-level evidence without minting a new node identity or granting package execution authority.

## Canonical input

Exactly one local bundle object:

`stegverse.bootstrap.bundle/v1 @ 1.0.0-rc.1`

The bundle must contain:
- frozen `stegverse.bootstrap.release-candidate/v1 @ 1.0.0-rc.1`;
- frozen `stegverse.bootstrap.source-catalog/v1 @ 1.0.0`;
- exactly four `stegverse.source-package/v1 @ 1.0.0` packages;
- deterministic component order:
  - `stegverse.sdk`
  - `stegverse.stegcore`
  - `stegverse.core-lite`
  - `stegverse.master-records`.

## Established continuity requirement

The receiver must use an existing valid StegVerse web-node continuity chain. It may:
- use live IndexedDB continuity for the current origin; or
- replay a valid exported `stegos.web_bootstrap_evidence_bundle.v1` when browser storage is partitioned.

It MUST NOT create a second node identity merely because current-origin IndexedDB is absent.

## Verification order

```text
verify established node/device continuity
  -> verify bundle schema/version and bundle_identity
  -> verify frozen rc.1 candidate identity
  -> verify candidate -> catalog digest binding
  -> verify catalog component set and source identities
  -> verify exactly four package component IDs/order
  -> verify every package file SHA-256
  -> verify every package complete source manifest digest
  -> verify package source_identity == frozen catalog identity
  -> persist all four packages in local package custody
  -> append four per-package materialization receipts
  -> append one aggregate bundle materialization receipt
  -> replay complete node journal
  -> emit bundle-level evidence
```

## Materialization semantics

Successful materialization produces:

```text
bundle_state: MATERIALIZED_UNADMITTED
component_count: 4
all_components_materialized: true
admission_state: UNADMITTED
execution_authority: NONE
release_activated: false
publication_performed: false
```

Bundle/package integrity proves byte identity only. It does not grant execution, SDK admission, release activation, governance, or publication authority.

## Evidence contract

Schema:

`stegverse.device-node-bootstrap-bundle-evidence/v1`

Required evidence includes:
- established node ID;
- established device continuity ID;
- continuity source (`LIVE_EXISTING_WEB_BOOTSTRAP` or verified imported continuity);
- bundle identity;
- candidate identity;
- source identity-set digest;
- ordered four component identities;
- four per-package materialization journal entries;
- aggregate bundle materialization journal entry;
- final deterministic journal replay PASS + tail digest;
- `new_node_identity_minted=false`;
- `execution_authority=NONE`;
- `github_platform_required=false`;
- `specific_external_platform_required=false`;
- `authority_effect=NONE`.

## Transport neutrality

The browser receiver accepts a local bundle object. How the bytes arrived is not part of bundle identity or execution authority.

The original file picker remains an explicit local/offline transport fallback. It is no longer the only machine path.

The canonical online machine-delivery path is the organization Universal InTr contract owned by:

`StegVerse-Labs/.github:docs/BOOTSTRAP_V1_INTR_BUNDLE_DELIVERY_MIRROR_HANDOFF.md`

The Site side MUST NOT obtain bundle bytes from GitHub, a package registry, or a hosting-provider API. The browser may request the exact already-built bundle from the same-origin logical StegVerse route:

`/intr/bootstrap-v1/bundle`

That path is a route projection only; it is not a bundle identity field.

## Universal InTr delivery integration

Companion projection:

`stegos-node/bootstrap-bundle-intr-delivery-v1.html`

The companion surface does not implement a second bundle verifier. It embeds the canonical `bootstrap-bundle-materialization-v1.html` receiver and injects a delivered bundle into that existing file/object intake after validating the transport envelope.

Required transport response:

```text
schema = stegverse.bootstrap.bundle-delivery-response/v1
state = DELIVERED_UNADMITTED
bundle_version = 1.0.0-rc.1
transport_profile = stegverse.universal-intr.adjacent-hop/v1
universal_intr_policy_id = STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001
canonical_protocol_adopted = true
interlock_required_per_hop = true
receipt_hash_chain_required = true
credential_required = false
execution_authority = NONE
release_activated = false
publication_performed = false
authority_effect = NONE_BUNDLE_DELIVERY_ONLY
```

The companion validates:
- request response IDs and established node/device bindings;
- exact response bundle identity and bundle payload hash;
- request ingress receipt schema/hash/boundaries;
- response egress receipt schema/hash/boundaries;
- response egress `prior_receipt_hash == request ingress receipt_hash`;
- no authority transfer;
- exact DEVICE_SYSTEM ↔ STEGOS_ECOSYSTEM adjacent-hop direction;
- no credential requirement.

Only after transport validation does it construct an in-memory JSON file and dispatch the existing receiver's `bundle-file` change event. The canonical receiver then independently re-verifies every bundle/package byte before materialization.

The companion may automatically press the existing materialize control after that canonical verification succeeds. It does not construct materialization receipts itself.

If `/intr/bootstrap-v1/bundle` is unavailable, the companion remains fail-closed and tells the user the sovereign route is unavailable; the canonical receiver's existing local file fallback remains available separately.

## Authority boundary

```text
credential_authority: TV/TVC
browser_credential_required: false
github_token_runtime_authority: NONE
transport_grants_execution_authority: false
package_execution_authority: false
sdk_admission_authority: false
release_activation_authority: false
publication_authority: false
new_node_identity_minted: false
second_machine_required: false
```

Delivery success is not materialization success. Materialization success is not release authorization.

## Runtime truth

```text
single-package receiver: IMPLEMENTED / MERGED
single-package MATERIALIZED_UNADMITTED semantics: IMPLEMENTED / MERGED
canonical distributable bundle capability: IMPLEMENTED / MERGED
bundle-level browser receiver: IMPLEMENTED / MERGED (Site PR #693)
bundle materialization implementation claim: RELEASED (Site PR #694)
Universal InTr bundle-delivery server/worker: IMPLEMENTING in StegVerse-Labs/.github
Site Universal InTr delivery companion: IMPLEMENTING
first authentic InTr bundle delivery: NOT YET OBSERVED
first authentic bundle materialization: NOT YET OBSERVED
first four-component continuity replay: NOT YET OBSERVED
Bootstrap v1 release activation: NOT YET AUTHORIZED
```

Newer authentic runtime evidence overrides source/PR/session descriptions.
