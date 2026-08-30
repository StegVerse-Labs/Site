# StegVerse Source Package Bootstrap v1 Mirror Handoff

Updated: 2026-08-29
Repository: StegVerse-Labs/Site

## Goal

Provide a versioned, distributable, platform-independent device-node receiver for content-addressed StegVerse source packages.

## Canonical flow

```text
any admitted transport
  -> stegverse.source-package/v1
  -> established StegVerse device-node continuity
  -> verify package schema/version
  -> verify every file SHA-256 and complete manifest digest
  -> verify source_identity = sha256:<source_bundle_sha256>
  -> persist bytes in device-local package custody
  -> append materialization receipt to node continuity
  -> remain UNADMITTED until separate governance/admission evidence exists
```

No external platform is required or privileged. GitHub, HTTP, removable storage, local file transfer, node-to-node InTr, or any future transport may carry identical package bytes; transport does not confer authority.

## Sovereignty invariants

```text
github_platform_required: false
specific_external_platform_required: false
network_required_for_local_materialization: false
credential_material_allowed_in_package: false
package_integrity_confers_execution_authority: false
new_node_identity_minted: false
authority_effect: NONE
```

## Version 1 surfaces

- `stegos-node/source-package-v1.schema.json`
- `stegos-node/source-package-bootstrap-v1.html`
- `tests/test_source_package_bootstrap_v1.py`

The earlier `private-source-portable-package-v1` surface is a transitional predecessor and is not the canonical Bootstrap v1 contract.

## Package identity

Canonical source identity:

```text
sha256:<source_bundle_sha256>
```

The manifest digest is calculated over ordered rows of:

```text
path
sha256
size
```

Repository names, Git commit SHAs, PR numbers, URLs, and provider coordinates are optional provenance only.

## Admission boundary

A valid content digest proves byte identity, not authority. Successful local materialization produces:

```text
materialization_state: MATERIALIZED
admission_state: UNADMITTED
execution_authority: NONE
```

A later governance/manifest/receipt lane may admit that exact source identity without retransferring the bytes.

## Runtime truth

```text
generic source-package receiver: IMPLEMENTED_PENDING_VALIDATION
device-local package custody: IMPLEMENTED_PENDING_VALIDATION
source identity: SHA256 CONTENT MANIFEST
GitHub dependency: NONE BY CONTRACT
first distributable package round: NOT YET OBSERVED
Bootstrap v1 release/tag: NOT YET FROZEN
```
