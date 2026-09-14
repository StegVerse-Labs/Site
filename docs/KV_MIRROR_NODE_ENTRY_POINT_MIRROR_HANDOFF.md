# KV_MIRROR_Node entry-point mirror handoff

Updated: 2026-09-14
Repository: `StegVerse-Labs/Site`
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Parent handoff: `docs/MIR_CONNECTION_ROUNDTRIP_TECHNICAL_GUIDE_MIRROR_HANDOFF.md`
Implementation branch: `kv-mirror-node-entrypoint-test-20260914`
Cleanup branch: `cleanup-kv-mirror-node-handoff-20260914`
Preferred-custody integration branch: `kv-mirror-preferred-custody-read-review-20260914`
Status: `CHECKED OUT / KV_MIRROR_Node PREFERRED CUSTODY WIRED INTO MIR RETAINED-RETURN READ_REVIEW / FINAL EXACT-HEAD VALIDATION PENDING`

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

The release-text cleanup was merged through PR #1330 and its documentation-maintenance claim was terminalized through PR #1331.

```text
cleanup_pr = 1330
cleanup_merge_commit = 293a864fce8f3c8fd64bb8f382c4185d6eca2260
cleanup_claim_terminalization_pr = 1331
cleanup_claim_terminalization_merge_commit = f3abde36458ebe0255a8731be12e5f8c6af443a2
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

## Preferred custody READ_REVIEW integration

The existing `assets/mir-accounting-return-v1.js` retained-return adapter now calls `buildPreferredKvCustodyBinding(...)` while preparing the existing `evaluator-read-review` / `SDK:EvaluatorReviewIngress` request.

The integration does not create a new transport route. It hashes the exact evaluator request bytes and the preceding continuation receipt, then asks `KV_MIRROR_Node.bindIntrRequest(...)` to bind those hashes to the deterministic KV entry-point profile when `window.StegVerseKVMirrorNode` is available.

When the deterministic mirror is present, the adapter emits:

```text
schema = stegverse.kv-mirror-node.preferred-custody-anchor/v1
state = KV_MIRROR_PREFERRED_CUSTODY_BOUND
kv_entry_point_required = false
kv_entry_point_preferred = true
event_triggered = true
persistent_receiver = false
always_on_application_receiver_required = false
second_user_device_required = false
credential_authority = TV/TVC
github_runtime_authority = NONE
live_kv_runtime_claimed = false
live_provider_write_claimed = false
master_records_custody_claimed = false
final_egress_claimed = false
authentic_external_mir_endpoint_claimed = false
authority_effect = NONE
```

When the mirror is not loaded, the same adapter returns `KV_MIRROR_PREFERRED_CUSTODY_UNAVAILABLE` and continues the existing evaluator transport. This is intentional: preferred custody is observable but is not a transport prerequisite.

`assets/external-counterpart-return-consumer.js` carries the admitted preferred-custody descriptor into both the retained-return consumption result and the existing SDK processing handoff. This preserves the custody-anchor evidence across the already-defined return chain without creating a new route or granting authority.

`tests/mir_return_consumer_runtime.mjs` now loads the deterministic KV mirror before the existing retained-return adapter and requires `KV_MIRROR_PREFERRED_CUSTODY_BOUND` plus `KV_MIRROR_INTR_REQUEST_BOUND_FOR_VALIDATION` while rechecking every no-live-provider/no-runtime/no-second-device/no-completion-claim boundary.

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

PR #1332 initially exposed that the adapter-produced preferred-custody descriptor was not carried through `assets/external-counterpart-return-consumer.js`. That bounded gap was repaired by carrying the descriptor through the existing return-consumption result and SDK processing handoff. Exact-head checks passed on the repaired pre-reconciliation head; this handoff reconciliation creates the final head that must pass again before merge.

## Workflow coverage

`.github/workflows/mir-intr-sdk-return-profile.yml` already covers the modified MIR adapter, external counterpart return consumer, and retained-return runtime test paths and also includes the KV mirror syntax/runtime checks. No workflow authority or runtime authority is added by this integration.

## Claim mapping and terminalization

The released implementation and documentation-maintenance claims remain terminal. This new integration uses a separate bounded active claim:

```text
claim_id = SITE-KV-MIRROR-PREFERRED-CUSTODY-READ-REVIEW-20260914
task_id = MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001
branch = kv-mirror-preferred-custody-read-review-20260914
role = INTEGRATION
state = CLAIMED_FOR_IMPLEMENTATION
handoff = docs/KV_MIRROR_NODE_ENTRY_POINT_MIRROR_HANDOFF.md
credential_authority = TV/TVC
github_token_runtime_authority = NONE
authority_effect = false
activation_effect = false
```

Its claimed paths are limited to:

```text
assets/mir-accounting-return-v1.js
assets/external-counterpart-return-consumer.js
tests/test_mir_intr_sdk_return_profile.py
tests/mir_return_consumer_runtime.mjs
docs/KV_MIRROR_NODE_ENTRY_POINT_MIRROR_HANDOFF.md
data/session-work-claims.d/site-kv-mirror-preferred-custody-read-review-20260914.json
```

## Current limitation

This work does not claim live KV provider installation, iCloud/Drive writeback, provider readback, live KV runtime activation, ProviderRequest materialization, Master Records custody, final egress, or authentic external MIR endpoint substitution. The new binding is deterministic source/test evidence that the retained-return READ_REVIEW request can carry a preferred KV custody anchor without changing transport admission or authority.

## Next admissible work

1. Validate PR #1332 at its final exact head after this scope reconciliation.
2. Merge only if repository orchestration, bootstrap, heartbeat, MIR InTr SDK Return Profile, and applicable build checks pass.
3. After merge, terminalize only the new integration claim using repository-approved mutable release fields.
4. Keep live KV provider write/readback under a separate predicate requiring authentic provider evidence.
