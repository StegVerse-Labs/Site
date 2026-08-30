# Bootstrap v1 Bundle Materialization Mirror Handoff

Updated: 2026-08-29
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

The browser receiver accepts a local bundle file/object. How the bytes arrived is not part of identity or authority.

No GitHub, hosting provider, package registry, cloud account, credential, URL, or specific transport is required by the materialization contract.

## Runtime truth

```text
single-package receiver: IMPLEMENTED / MERGED
single-package MATERIALIZED_UNADMITTED semantics: IMPLEMENTED / MERGED
canonical distributable bundle capability: IMPLEMENTED / MERGED
bundle-level browser receiver: IMPLEMENTING
first authentic bundle materialization: NOT YET OBSERVED
first four-component continuity replay: NOT YET OBSERVED
Bootstrap v1 release activation: NOT YET AUTHORIZED
```

Newer authentic runtime evidence overrides source/PR/session descriptions.
