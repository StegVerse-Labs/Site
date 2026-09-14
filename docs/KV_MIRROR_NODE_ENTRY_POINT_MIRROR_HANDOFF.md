# KV_MIRROR_Node entry-point mirror handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Parent handoff: `docs/MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md`
Branch: `kv-mirror-node-entrypoint-test-20260914`
Status: `CHECKED OUT / SOURCE-SIDE KV ENTRY-POINT MIRROR TEST ADDED / PR VALIDATION PENDING`

## Purpose

Create a deterministic `KV_MIRROR_Node` analogous to the MIR NODE MIRROR pattern so the Interlock/InTr loop can test the expected shape of an actual KV Entry Point without claiming that a live KV provider was written, read back, or activated.

The mirror node is a validation/custody profile. It must not become a mandatory transport prerequisite for the bounded event-triggered evaluator/InTr round trip.

## Expected KV Entry Point attributes represented

`assets/kv-mirror-node.js` defines a deterministic mirror node with:

```text
schema = stegverse.kv-mirror-node.entry-point/v1
node_kind = KV_MIRROR_Node
profile_id = KV_ENTRY_POINT
counterpart_pattern = MIR NODE MIRROR
provenance = DETERMINISTIC_MIRROR_ONLY
principal_ref = owner-local principal reference
device_ref = owner current-device reference
provider_class = OWNER_CONTROLLED_PERSONAL_CLOUD
adapter_profile = intr-kv-entrypoint-adapter-v1
owner_authorized = true
write_capable = true
read_capable = true
```

It also declares the namespaces expected at a real KV entry point:

```text
principal
device
node
request
receipt
continuity
reconstruction
```

## Authority and lifecycle boundaries

The mirror node enforces:

```text
credential_authority = TV/TVC
execution_authority = NONE
github_runtime_authority = NONE
authority_effect = NONE_CUSTODY_PROFILE_ONLY
kv_entry_point_required = false
kv_entry_point_preferred = true
event_triggered = true
persistent_receiver = false
always_on_application_receiver_required = false
second_user_device_required = false
live_kv_runtime_claimed = false
live_provider_write_claimed = false
```

This preserves the current Universal InTr invariant: KV is preferred for durable custody, continuity, reconstruction, and receipt readback, but this bounded transport proof must still be able to validate without converting KV into an always-on receiver or hard transport dependency.

## InTr binding semantics

`bindIntrRequest(...)` accepts only declared InTr profiles and requires:

```text
profile
manifest_sha256
request_sha256
prior_receipt_hash
```

The binding returns `stegverse.kv-mirror-node.intr-request-binding/v1` with the retained node hash, manifest hash, request hash, prior receipt hash, request namespace, receipt namespace, and `authority_effect=NONE`.

## Tests added

`tests/kv_mirror_node_runtime.mjs` exercises the deterministic mirror and checks:

```text
KV_MIRROR_Node validates
MIR NODE MIRROR pattern is declared
kv_entry_point_required=false
kv_entry_point_preferred=true
event_triggered=true
persistent_receiver=false
always_on_application_receiver_required=false
credential_authority=TV/TVC
github_runtime_authority=NONE
live_kv_runtime_claimed=false
live_provider_write_claimed=false
evaluator-read-review request binds by manifest/request/prior-receipt hashes
making KV mandatory for transport is rejected
claiming live KV runtime is rejected
unaccepted InTr profile is rejected
```

Local deterministic validation completed before PR creation:

```text
node --check assets/kv-mirror-node.js: PASS
node tests/kv_mirror_node_runtime.mjs: PASS
```

## Workflow coverage

`.github/workflows/mir-intr-sdk-return-profile.yml` now includes the KV mirror asset/test paths and executes:

```text
node --check assets/kv-mirror-node.js
node tests/kv_mirror_node_runtime.mjs
```

## Current limitation

This work does not claim live KV provider installation, iCloud/Drive writeback, readback, ProviderRequest materialization, Master Records custody, final egress, or authentic external MIR endpoint substitution. It only creates and tests the expected source-side mirror attributes for a real KV Entry Point.

## Next admissible work

1. Validate the PR at exact head.
2. If green, merge the source-side KV mirror node test.
3. Continue by wiring the `KV_MIRROR_Node` profile into the evaluator READ_REVIEW or MIR retained-return path as a preferred custody anchor while preserving `kv_entry_point_required=false` for bounded event-triggered transport.
4. Add live KV provider write/readback only under a separate predicate with authentic provider evidence.
