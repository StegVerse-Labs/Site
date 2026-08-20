# StegOS Device-Continuity Projection Mirror Handoff

Updated: `2026-08-20T11:10:00-05:00`

## Active goal

```text
goal_id: SITE-STEGOS-DEVICE-CONTINUITY-298
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#298
canonical_source_owner: StegVerse-Labs/StegOS#19
source_commit: 9e2c58cc22e6ce339d43383caa70be43c714b370
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
claim_registry_collision: data/session-work-claims.json remains owned by active Site#268 work and is NOT mutated by this lane
```

## Exact current projection

```text
stegos-bootstrap/index.html                         561e21d38df310aee838716ab9f2a4a6175485d5
stegos-bootstrap/stegos-bootstrap.js                15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js              1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0
stegos-bootstrap/device-local-autostart.js           b1bbe4907c29d1ba66fd4ff3321507c6e52dc344
stegos-bootstrap/service-worker.js                  3cba6ca48c8b093d0f0baa48aff000a544e93cc6
stegos-bootstrap/stegverse-reference-model.js        bd8e7553b61425386f6cf65db4766b952c148ed4
stegos-bootstrap/tvc-sovereign-local-model-route.js  3ca841310b904c2e09390512043f30f301976b1d
stegos-bootstrap/manifest.webmanifest                a223ec9454f46d0e9b91d4862f11de701792144a
```

## New continuity semantics

The public StegOS path now distinguishes:

```text
device continuity identity: stegdevice-*
browser/runtime node identity: stegnode-web-*
task identity/fence: per admitted inference task
```

`stegnode-web-*` is not physical-device identity. A persisted StegOS store creates one `stegdevice-*` continuity root and explicitly binds node instances to it through `stegos.web_device_node_binding_receipt.v1` in the existing hash-chain journal.

Different unsynced roots are separate chains:

```text
sync_state: UNSYNCED
parent_continuity_id: null
implicit_cross_root_continuation_allowed: false
governed_transfer_required_for_cross_root_continuation: true
```

No cross-root synchronization is implemented or implied by this projection.

The browser does not claim hardware serial/UDID attestation. The root records `hardware_attestation: UNAVAILABLE_TO_BROWSER` and no serial, Wi-Fi/MAC, Apple account, provider credential, or GitHub token is retained.

## Evidence Bundle additions

`Show Evidence Bundle` now includes:

```text
device_continuity
device_continuity_id
node_instance_id
continuity_semantics
```

For fresh storage, the device-continuity root receipt is the journal origin. For pre-existing StegOS storage, the receipt explicitly records `ROOT_ESTABLISHED_AFTER_EXISTING_LOCAL_HISTORY` and the count of earlier local entries rather than retroactively claiming physical identity for them.

Every later task receipt remains in the same journal after the continuity root/node binding, so claim/fence/terminal/reconstruction evidence is cryptographically downstream of the device continuity binding.

## Validation

Canonical Site validator:

`./scripts/check_stegos_ipod_bootstrap_projection.py`

Current validator requires exact blob identity plus:
- `stegdevice-*` continuity root semantics;
- `stegnode-web-*` remaining a distinct node identity;
- explicit node-binding receipt;
- separate-chain semantics for unsynced roots;
- fail-closed implicit cross-root continuation;
- future governed transfer requirement;
- no browser hardware-attestation claim;
- separate root/node fields in exported evidence;
- existing device-local inference/task/credential boundaries.

Hosted CI is supplemental only and is not activation evidence.

## Release condition

```text
exact projection on Site main
-> validator source installed
-> physical public load creates/reuses device_continuity_id
-> evidence bundle separates device_continuity_id from node_instance_id
-> journal replay PASS
-> same persisted storage reuses the same continuity root
-> deliberately separate unsynced storage/device context produces a different root
```

Do not call cross-device sync complete until an explicit governed root-transfer mechanism exists and is proven.
