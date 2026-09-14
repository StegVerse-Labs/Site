# KV_MIRROR_Node entry-point mirror handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Parent handoff: `docs/MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md`
Implementation branch: `kv-mirror-node-entrypoint-test-20260914`
Cleanup branch: `cleanup-kv-mirror-node-handoff-20260914`
Status: `RELEASED / MERGED / SOURCE-SIDE KV ENTRY-POINT MIRROR TEST VALIDATED / CLAIM TERMINALIZED`

## Release evidence

The bounded KV_MIRROR_Node entry-point mirror implementation was validated and merged through PR #1325.

```text
implementation_pr = 1325
implementation_head = 5a1c06a0b787ef7e504c441b6d6610acf7159cee
implementation_merge_commit = 8800ec843c9eece278bdb7ba3840cd1c5ffa4d48
implementation_merged_at = 2026-09-14T20:00:17Z
```

The related session-work claim was terminalized through PR #1329.

```text
terminalization_pr = 1329
terminalization_head = 5ce0d67bcf83edc1dde445837e2d5fa09925bd9f
terminalization_merge_commit = fa64e163f420c7808020666a38bc868e2bdc1494
terminalization_merged_at = 2026-09-14T20:09:00Z
claim_state = RELEASED_COMPLETE
```

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

## Tests added and validated

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

Validated before PR #1325 merged:

```text
node --check assets/kv-mirror-node.js: PASS
node tests/kv_mirror_node_runtime.mjs: PASS
MIR InTr SDK Return Profile: PASS
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Handoff Orchestrator: PASS
```

## Workflow coverage

`.github/workflows/mir-intr-sdk-return-profile.yml` includes the KV mirror asset/test paths and executes:

```text
node --check assets/kv-mirror-node.js
node tests/kv_mirror_node_runtime.mjs
```

## Claim mapping and terminalization

PR #1325 exact head initially failed repository orchestration because branch `kv-mirror-node-entrypoint-test-20260914` did not resolve to exactly one active pre-work claim. The bounded repair updated the existing active MIR claim fragment only; it did not create a second active MIR claim.

PR #1329 then performed terminalization-only claim maintenance. Current main readback records:

```text
claim_id = SITE-MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-20260912
task_id = MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001
branch = kv-mirror-node-entrypoint-test-20260914
handoff = docs/KV_MIRROR_NODE_ENTRY_POINT_MIRROR_HANDOFF.md
role = RELEASED_INTEGRATION
state = RELEASED_COMPLETE
pull_request = 1325
release_commit = 8800ec843c9eece278bdb7ba3840cd1c5ffa4d48
claim_released_at = 2026-09-14T20:00:17Z
archive_eligible = true
authority_effect = false
activation_effect = false
credential_authority = TV/TVC
github_token_runtime_authority = NONE
```

The claim scope remained limited to the bounded KV mirror source/test/workflow/index/handoff/claim paths:

```text
assets/kv-mirror-node.js
tests/kv_mirror_node_runtime.mjs
.github/workflows/mir-intr-sdk-return-profile.yml
docs/KV_MIRROR_NODE_ENTRY_POINT_MIRROR_HANDOFF.md
docs/MIR_CONNECTION_DOCUMENTATION_INDEX.md
data/session-work-claims.d/site-mir-connection-roundtrip-technical-guide-20260912.json
```

## Current limitation

This work does not claim live KV provider installation, iCloud/Drive writeback, readback, ProviderRequest materialization, Master Records custody, final egress, or authentic external MIR endpoint substitution. It only creates and tests the expected source-side mirror attributes for a real KV Entry Point.

## Next admissible work

1. Wire the `KV_MIRROR_Node` profile into the evaluator READ_REVIEW or MIR retained-return path as a preferred custody anchor while preserving `kv_entry_point_required=false` for bounded event-triggered transport.
2. Add live KV provider write/readback only under a separate predicate with authentic provider evidence.
